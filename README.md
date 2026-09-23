# Gauss RAG

**Documents as knots.** A Claude Code skill that turns a folder of documents into a knot-native RAG
you can search *and see*: header-to-header sections on a per-document ring, cross-references
("see Section 4.2", "Chapter 5", defined terms) as signed Gauss crossings, and several documents
linked into one composite knot. Search returns a hit plus a **construct plan** — the ordered
reading path (the section, what it references, what cites it, its neighbours) that keeps an answer
coherent across follow-ups instead of dropping the thread.

Drop docs into `Gauss/docs/`, run `Gauss/app.py`, get search + an interactive visualization.
**Low budget by default:** BM25 via embedded Weaviate, no embeddings, no OCR — zero API calls until
you opt in.

## Install (Claude Code)

```
/plugin marketplace add sireggserroneous/gauss-rag
/plugin install gauss-rag@gauss-rag
```

Then in any project: ask Claude to "gauss rag this folder" (or run the skill), which scaffolds
`Gauss/` and walks you through it. Requirements: Python 3.11+, `weaviate-client`
(`pip install weaviate-client` or `uv pip install -r requirements.txt`), and poppler (`pdftotext`).

## What you get

| view | shows |
|---|---|
| **simple** | documents as boxes, cross-document references as weighted arrows (gitdiagram-style) |
| **doc** | one document in reading order with → / ← / ✕ reference badges |
| **knot** | one document as a ring: sections as arcs, crossings as chords, dangling refs as red stubs |
| **tangle** | every document's ring interwoven with all cross-document crossings |

Plus an **analysis** overlay: hubs (what everything depends on), fan-out (branchy requirements),
cycles (contention), dangling references (drafting holes). Adding a view is one render function.

**Code too:** drop an `architecture-map.json` in and typed edges (publishes / handles / owns /
consumes / exposes) become crossings; a search on a job returns its execution trace.

## Endpoints (`Gauss/app.py`, 127.0.0.1:8787)

`/search?q=…&construct=1` · `/knot.json` · `/doc?idx=N` · `/analyze` · `/reingest`

## Honest note on what it is and isn't

Measured against plain semantic+lexical RAG, the knot is **not** a better retriever in general.
Its value is **ordering** and **visibility**: a structured reading order for assembling coherent
answers, and a picture of a document's reference topology. It wins on recall only in the narrow
case where the answer is semantically far from the question but explicitly cross-referenced.

MIT — Pedro Paulino (Sir Eggs Erroneous).
