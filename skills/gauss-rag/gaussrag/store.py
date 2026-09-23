#!/usr/bin/env python3
"""Weaviate embedded store. Chunks are objects; crossings are Weaviate CROSS-REFERENCES between chunk
objects (Pedro's convention: a knot is literally objects with typed refs). BM25 is native, so the
default install searches with zero embedding calls; vectors are optional and upgrade search to hybrid.
"""
import os
from weaviate.classes.config import Configure, DataType, Property, ReferenceProperty
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.query import MetadataQuery
from weaviate.util import generate_uuid5
import weaviate


def _ports(path):
    """Deterministic per-folder ports so two Gauss/ folders never collide (8100-8899 / grpc +1000)."""
    import hashlib
    h = int(hashlib.sha256(os.path.abspath(path).encode()).hexdigest(), 16) % 800
    return 8100 + h, 9100 + h


class Store:
    def __init__(self, path, quiet=True):
        path = os.path.abspath(path)
        env = {"LOG_LEVEL": "error"} if quiet else None
        port, grpc = _ports(path)
        try:
            # embedded startup can exceed the 10s client default on a cold/light node: give it 90s
            self.client = weaviate.connect_to_embedded(persistence_data_path=path, port=port, grpc_port=grpc,
                                                       environment_variables=env,
                                                       additional_config=AdditionalConfig(timeout=Timeout(init=90, query=60, insert=180)))
        except weaviate.exceptions.WeaviateStartUpError as ex:
            if "already listening" not in str(ex):
                raise
            # a previous run of THIS folder died without stopping its embedded db: reuse it
            self.client = weaviate.connect_to_local(port=port, grpc_port=grpc,
                                                    additional_config=AdditionalConfig(timeout=Timeout(init=90, query=60, insert=180)))
        import atexit
        atexit.register(self.close)
        self._ensure()
        self.chunks = self.client.collections.get("Chunk")
        self.xs = self.client.collections.get("Crossing")

    def _ensure(self):
        c = self.client.collections
        if not c.exists("Chunk"):
            c.create("Chunk", vector_config=Configure.Vectors.self_provided(), properties=[
                Property(name="idx", data_type=DataType.INT), Property(name="doc", data_type=DataType.TEXT),
                Property(name="pos", data_type=DataType.INT), Property(name="label", data_type=DataType.TEXT),
                Property(name="kind", data_type=DataType.TEXT), Property(name="text", data_type=DataType.TEXT),
                Property(name="sha", data_type=DataType.TEXT)])
        if not c.exists("Crossing"):
            c.create("Crossing", vector_config=Configure.Vectors.self_provided(), properties=[
                Property(name="cid", data_type=DataType.INT), Property(name="kind", data_type=DataType.TEXT),
                Property(name="label", data_type=DataType.TEXT)],
                references=[ReferenceProperty(name="over", target_collection="Chunk"),
                            ReferenceProperty(name="under", target_collection="Chunk")])

    def reset(self):
        for n in ("Crossing", "Chunk"):
            if self.client.collections.exists(n):
                self.client.collections.delete(n)
        self._ensure()
        self.chunks = self.client.collections.get("Chunk"); self.xs = self.client.collections.get("Crossing")

    @staticmethod
    def uuid(chunk):
        return generate_uuid5(chunk["sha"] + ":" + str(chunk["idx"]))

    def upsert_chunks(self, chunks, vectors=None):
        """chunks: list with idx/doc/pos/label/kind/text/sha. Idempotent (uuid from sha+idx)."""
        with self.chunks.batch.dynamic() as b:
            for i, c in enumerate(chunks):
                b.add_object(uuid=self.uuid(c), vector=(vectors[i] if vectors else None), properties={
                    "idx": c["idx"], "doc": c["doc"], "pos": c["pos"], "label": c["label"],
                    "kind": c.get("kind", "doc"), "text": c["text"], "sha": c["sha"]})

    def upsert_crossings(self, crossings, chunks):
        """Crossings as objects with over/under cross-references to Chunk objects."""
        by_idx = {c["idx"]: c for c in chunks}
        with self.xs.batch.dynamic() as b:
            for x in crossings:
                o, u = by_idx.get(x["over"]), by_idx.get(x["under"])
                if not (o and u):
                    continue
                b.add_object(uuid=generate_uuid5(f"x:{x['id']}:{o['sha']}:{u['sha']}"),
                             properties={"cid": x["id"], "kind": x["kind"], "label": x["label"]},
                             references={"over": self.uuid(o), "under": self.uuid(u)})

    def all_chunks(self):
        out = [o.properties for o in self.chunks.iterator()]
        out.sort(key=lambda c: c["idx"])
        return out

    def bm25(self, query, k=10):
        r = self.chunks.query.bm25(query=query, limit=k, return_metadata=MetadataQuery(score=True))
        return [dict(o.properties, score=o.metadata.score) for o in r.objects]

    def hybrid(self, query, vector, k=10, alpha=0.6):
        r = self.chunks.query.hybrid(query=query, vector=vector, limit=k, alpha=alpha,
                                     return_metadata=MetadataQuery(score=True))
        return [dict(o.properties, score=o.metadata.score) for o in r.objects]

    def count(self):
        return self.chunks.aggregate.over_all(total_count=True).total_count

    def close(self):
        try:
            self.client.close()          # also stops the embedded db process
        except Exception:
            pass
