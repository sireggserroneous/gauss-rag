#!/usr/bin/env python3
"""ingest -> knot -> store. Cheap by default: no OCR, no embeddings unless asked."""
import json, os, urllib.request
from . import ingest, knot, code, ocr
from .store import Store


def embed(texts, base_url, model, api_key="", batch=64):
    out = []
    for i in range(0, len(texts), batch):
        body = json.dumps({"model": model, "input": texts[i:i + batch]}).encode()
        h = {"Content-Type": "application/json", "User-Agent": "gaussrag/0.1"}
        if api_key:
            h["Authorization"] = "Bearer " + api_key
        r = json.load(urllib.request.urlopen(urllib.request.Request(base_url.rstrip("/") + "/v1/embeddings",
                                                                     data=body, headers=h), timeout=300))
        out.extend(row["embedding"] for row in r["data"])
    return out


def build_knot(chunks):
    """chunks -> knot dict; stamps idx + sha."""
    for i, c in enumerate(chunks):
        c["idx"] = i
        c["sha"] = ingest.sha(c["text"])
    return knot.build(chunks)


def run(gauss_dir, embed_cfg=None, ocr_cfg=None, min_chars=500, reset=True, log=print):
    docs = os.path.join(gauss_dir, "docs")
    chunks, needs_ocr = ingest.ingest_dir(docs, min_chars=min_chars)
    if needs_ocr and ocr_cfg and ocr_cfg.get("enabled") and ocr_cfg.get("base_url"):
        for pdf in needs_ocr:                      # opt-in: one vision call per page
            md = ocr.ocr_pdf(pdf, ocr_cfg["base_url"], ocr_cfg.get("model", "qwen2.5-vl"), ocr_cfg.get("api_key", ""), log=log)
            chunks.extend(ingest.chunk_markdown(md, pdf, "doc", min_chars=min_chars))
        needs_ocr = []
    # code-Gauss: any architecture-map.json under docs/ becomes symbols + typed crossings
    code_edges = []
    for dirpath, _, files in os.walk(docs):
        for fn in files:
            if fn == "architecture-map.json":
                cch, edges = code.archmap(os.path.join(dirpath, fn))
                code_edges.append((len(chunks), cch, edges)); chunks.extend(cch)
    kn = build_knot(chunks)
    for base, cch, edges in code_edges:
        code.add_edges(kn, cch, edges, base_idx=base)
    st = Store(os.path.join(gauss_dir, "store"))
    if reset:
        st.reset()
    vecs = None
    if embed_cfg and embed_cfg.get("enabled"):
        vecs = embed([c["text"] for c in chunks], embed_cfg["base_url"], embed_cfg["model"],
                     embed_cfg.get("api_key", ""))
    st.upsert_chunks(chunks, vecs)
    st.upsert_crossings(kn["crossings"], chunks)
    n = st.count()
    st.close()
    with open(os.path.join(gauss_dir, "knot.json"), "w") as f:
        json.dump(kn, f)
    with open(os.path.join(gauss_dir, "chunks.json"), "w") as f:
        json.dump(chunks, f)
    return {"chunks": len(chunks), "stored": n, "crossings": len(kn["crossings"]),
            "dangling": len(kn["dangling"]), "docs": len(kn["docs"]), "needs_ocr": needs_ocr,
            "embedded": bool(vecs)}
