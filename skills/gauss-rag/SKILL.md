---
name: gauss-rag
description: Knot-native RAG for a folder of documents. Use when the user wants to "gauss rag", "knot", "graphify", or "visualize the cross-references of" their documents or project; when they want RAG over a folder that preserves reading order and follows "see Section N" references across documents; or when they drop files into a Gauss/ folder. Scaffolds Gauss/ in the working directory, ingests docs into embedded Weaviate (crossings as cross-references), and serves search + an interactive knot visualization from Gauss/app.py. Low budget by default (no OCR, no embeddings).
---

# Gauss RAG

Documents as knots: header-to-header sections on a per-document ring, cross-references as signed
Gauss crossings, several documents linked into one composite knot. Search returns a hit plus a
**construct plan** — the ordered reading path (the section, what it references, what cites it, its
neighbours) that keeps an answer coherent across follow-ups. Retrieval is BM25 by default (zero
API calls); semantic vectors and VL-OCR are opt-in in `gauss.toml`.

## Steps

1. **Scaffold** — from the user's project root:
   ```
   python3 <skill-dir>/scaffold.py            # creates ./Gauss/{docs,store,app.py,gauss.toml}
   ```
2. **Deps** (once) — Weaviate embedded needs `weaviate-client`:
   ```
   uv venv Gauss/.venv && uv pip install --python Gauss/.venv/bin/python -r <skill-dir>/requirements.txt
   ```
   (`pip install weaviate-client` also works.) Needs `pdftotext` (poppler) for PDFs.
3. **Drop documents** into `Gauss/docs/` — .md, .txt, .pdf (text layer), code. Scanned PDFs are
   listed as `needs_ocr`; enable `[ocr]` in `gauss.toml` to OCR them (costs a vision-model call per page).
   **Code-Gauss:** drop a project's `architecture-map.json` in too — its typed edges (publishes /
   handles / owns / consumes / exposes) become crossings, and a search on a job returns its execution
   trace (job → notification → handling module) as the construct plan.
4. **Run** — `Gauss/.venv/bin/python Gauss/app.py` → http://127.0.0.1:8787
   Ingests on first start (re-run with `--reingest` after adding files). The page has search with
   construct plans and the visualization views (doc, knotted-doc, tangle, simple).
5. **Optional upgrades** in `gauss.toml`: `[embed] enabled = true` turns search hybrid (needs an
   OpenAI-compatible embedder URL); `[ocr] enabled = true` parses scanned PDFs.

## What the user gets
- `/search?q=…&construct=1` — hits with `ring`, `crossings`, and an ordered `construct` plan.
- `/knot.json` — the whole knot: docs (rings), crossings, dangling refs, Gauss codes.
- Dangling references are surfaced, not hidden: a reference to nothing is a drafting hole worth seeing.

## Notes
- Weaviate runs embedded on a **per-folder port** (derived from the store path) so two `Gauss/`
  folders never collide; the app stops it cleanly on SIGTERM/Ctrl-C, and reuses a stale instance of
  the same folder if a previous run died. Startup can take ~10-60s on a light node.
- `analysis` checkbox in the UI: hubs (what everything depends on), fan-out (branchy requirements),
  cycles (contention), dangling (drafting holes) — `/analyze` returns the same as JSON.
- Chunking is header-to-header with runt packing (`[chunk] min_chars`); labels are the TOC path.
- Cross-document references resolve into linked documents when exactly one has the target
  (knots-of-knots); ambiguous ones stay dangling on purpose — never guess a link.
