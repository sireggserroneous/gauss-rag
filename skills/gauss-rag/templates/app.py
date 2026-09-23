#!/usr/bin/env python3
"""Gauss RAG — local app. Ingests Gauss/docs into the knot + Weaviate embedded, serves search,
construct (the assembly plan), the knot data, and the visualization views.
    python3 app.py [--reingest] [--port 8787]
Low budget by default: no OCR, no embeddings (BM25 + knot + views cost only CPU). See gauss.toml.
"""
import json, os, sys, argparse, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    import tomllib
    from gaussrag import pipeline, knot, analyze
    from gaussrag.store import Store
except ImportError as ex:
    sys.exit("missing dependency (%s). Install:  uv pip install -r requirements.txt   or   pip install weaviate-client" % ex)

CFG = {}
if os.path.exists(os.path.join(HERE, "gauss.toml")):
    with open(os.path.join(HERE, "gauss.toml"), "rb") as f:
        CFG = tomllib.load(f)
S = {}


def load(reingest=False):
    kp, cp = os.path.join(HERE, "knot.json"), os.path.join(HERE, "chunks.json")
    if reingest or not (os.path.exists(kp) and os.path.exists(cp)):
        r = pipeline.run(HERE, embed_cfg=CFG.get("embed"), ocr_cfg=CFG.get("ocr"), min_chars=CFG.get("chunk", {}).get("min_chars", 500))
        print("ingested:", r, flush=True)
    with open(kp) as f: S["kn"] = json.load(f)
    with open(cp) as f: S["chunks"] = json.load(f)
    S["store"] = Store(os.path.join(HERE, "store"))


def qvec(q):
    e = CFG.get("embed", {})
    if not e.get("enabled"):
        return None
    return pipeline.embed([q], e["base_url"], e["model"], e.get("api_key", ""))[0]


def search(q, k=8, construct=False):
    kn, chunks, st = S["kn"], S["chunks"], S["store"]
    v = qvec(q)
    hits = st.hybrid(q, v, k) if v else st.bm25(q, k)
    out = []
    for h in hits:
        i = h["idx"]; c = chunks[i]
        arcs = kn["docs"].get(c["doc"], [])
        row = {"idx": i, "score": h.get("score"), "label": c["label"], "doc": os.path.basename(c["doc"]),
               "pos": c["pos"], "n": len(arcs), "text": c["text"][:600],
               "crossings": knot.describe(kn, i, chunks)}
        if construct:
            row["construct"] = [{"idx": p["idx"], "pos": p["pos"], "via": p["via"], "label": p["label"],
                                 "doc": os.path.basename(chunks[p["idx"]]["doc"]), "text": chunks[p["idx"]]["text"]}
                                for p in knot.construct(i, kn, chunks)]
        out.append(row)
    return {"q": q, "mode": "hybrid" if v else "bm25", "hits": out}


def knot_json():
    kn, chunks = S["kn"], S["chunks"]
    return {"docs": {os.path.basename(d): a for d, a in kn["docs"].items()},
            "labels": [c["label"] for c in chunks], "crossings": kn["crossings"], "dangling": kn["dangling"],
            "gauss": {os.path.basename(d): knot.gauss(kn, d) for d in kn["docs"]}}


class H(BaseHTTPRequestHandler):
    def _send(self, body, ctype="application/json", code=200):
        if isinstance(body, (dict, list)): body = json.dumps(body)
        if isinstance(body, str): body = body.encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query); p = u.path
        try:
            if p == "/":
                with open(os.path.join(HERE, "gaussrag", "ui.html")) as f: self._send(f.read(), "text/html; charset=utf-8")
            elif p == "/knot.json": self._send(knot_json())
            elif p == "/search":
                self._send(search((q.get("q") or [""])[0], int((q.get("k") or ["8"])[0]),
                                  (q.get("construct") or ["0"])[0] not in ("0", "false")))
            elif p == "/doc":
                i = int((q.get("idx") or ["0"])[0]); c = S["chunks"][i]
                self._send({"idx": i, "label": c["label"], "doc": os.path.basename(c["doc"]), "pos": c["pos"], "text": c["text"]})
            elif p == "/analyze":
                self._send(analyze.analyze(S["kn"], S["chunks"]))
            elif p == "/reingest":
                S["store"].close(); load(reingest=True); self._send({"ok": True, "chunks": len(S["chunks"])})
            else: self._send({"error": "not found"}, code=404)
        except BrokenPipeError: pass
        except Exception as ex: self._send({"error": str(ex)}, code=500)

    def log_message(self, *a): pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--reingest", action="store_true"); ap.add_argument("--port", type=int, default=8787)
    a = ap.parse_args()
    load(reingest=a.reingest)
    kn = S["kn"]
    print("Gauss RAG · %d chunks · %d docs · %d crossings · %d dangling · search=%s" % (
        len(S["chunks"]), len(kn["docs"]), len(kn["crossings"]), len(kn["dangling"]),
        "hybrid" if CFG.get("embed", {}).get("enabled") else "bm25 (no embeddings)"))
    print("→ http://127.0.0.1:%d" % a.port, flush=True)
    import signal
    def _bye(*_):
        S["store"].close(); sys.exit(0)
    signal.signal(signal.SIGTERM, _bye); signal.signal(signal.SIGINT, _bye)
    ThreadingHTTPServer(("127.0.0.1", a.port), H).serve_forever()
