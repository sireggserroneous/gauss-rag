# Example: a Machine Programming curriculum, as a knot

This is the corpus Gauss RAG was first run on for real: **Stanford's CS 329M, Machine Programming**
— programs that write, understand, and repair programs — taught by Dr. Justin Gottschlich and
**offered freely**: the lecture recordings are available to anyone at no cost. The reading list below
is that course's, organised week by week, with a set of plain-language **ELI5** explainers written
alongside it while working through it. It is here for two reasons: it shows what Gauss does on a real
folder, and the curriculum itself is worth having.

- Course page: <https://sites.google.com/view/gottschlich/mp-stanford-cs-329m>
- Guest lecturers and materials: <https://sites.google.com/stanford.edu/329m>
- Catalog entry: <https://bulletin.stanford.edu/courses/2242401>

The result on this folder, with no embeddings and no OCR (BM25 only, zero API calls):

| | |
|---|---|
| documents | 62 (28 papers, 7 lectures, 26 ELI5 notes, 1 readme) |
| sections | 1,299 |
| crossings | 290 |
| dangling references | 156 |

The knots-of-knots effect appeared on its own: the ELI5 notes became the most-cited hubs (the note on
Aroma cited 29 times, code2vec 17) because the papers mention those systems by name, so the notes
link into their sources — the "one real reference plus your notes" study model, live.

## What's in this folder

- `eli5/` — the 26 ELI5 explainers, one per paper or system. **Included in full.** Start here if you
  want the course without the math.
- The papers and lecture slides are **not** included: they are published work under their own
  copyrights. Every one is linked below. Download them into `Gauss/docs/Ref/` and `Gauss/docs/Lectures/`
  and you reproduce the knot exactly.

## Reproduce it

```
python3 <skill-dir>/scaffold.py            # creates ./Gauss
mkdir -p Gauss/docs/Ref Gauss/docs/Lectures
cp examples/machine-programming/eli5/*.md Gauss/docs/eli5/   # your notes
# drop the papers below into Gauss/docs/Ref/, slides into Gauss/docs/Lectures/
Gauss/.venv/bin/python Gauss/app.py
```

## The reading list

Titles are given where certain; otherwise the arXiv identifier is the link and the ELI5 note names
the paper. `→ eli5` points at the explainer for it.

**Foundation**
- arXiv:2603.16021 — <https://arxiv.org/abs/2603.16021>

**Week 1 — what machine programming is**
- The Three Pillars of Machine Programming — <https://arxiv.org/abs/1803.07244> → `eli5-three-pillars-of-machine-programming.md`
- AI Programmer: Autonomously Creating Software Programs Using Genetic Algorithms — <https://arxiv.org/abs/1709.05703> → `eli5-ai-programmer.md`
- The Case for Learned Index Structures — <https://arxiv.org/abs/1712.01208> → `eli5-learned-index-structures.md`
- arXiv:1812.01158 — <https://arxiv.org/abs/1812.01158>

**Week 2 — representing code**
- code2vec: Learning Distributed Representations of Code — <https://arxiv.org/abs/1803.09473> → `eli5-code2vec.md`
- Halide: A Language and Compiler for Image Processing Pipelines (PLDI 2013) → `eli5-halide.md`
- arXiv:1812.01158 (revisited) — <https://arxiv.org/abs/1812.01158>

**Week 3 — code semantics and similarity**
- MISIM: A Neural Code Semantics Similarity System — <https://arxiv.org/abs/2006.05265> → `eli5-misim.md`
- arXiv:2204.07225 — <https://arxiv.org/abs/2204.07225>
- Neural Code Comprehension: A Learnable Representation of Code Semantics (NeurIPS 2018) → `eli5-neural-code-comprehension.md`

**Week 4 — programs as graphs, synthesis by example**
- Learning to Represent Programs with Graphs — <https://arxiv.org/abs/1711.00740> → `eli5-programs-with-graphs.md`
- Learning to Represent Programs with Property Signatures — <https://arxiv.org/abs/2002.09030> → `eli5-property-signatures.md`
- Automating String Processing in Spreadsheets Using Input-Output Examples (FlashFill, POPL 2011) → `eli5-flashfill.md`

**Week 5 — finding and fixing bugs, learned systems**
- Self-Supervised Bug Detection and Repair (BugLab) — <https://arxiv.org/abs/2105.12787> → `eli5-self-supervised-bug-detection.md`
- A Zero-Positive Learning Approach for Diagnosing Software Performance Regressions (NeurIPS 2019) → `eli5-zero-positive-perf-regressions.md`
- Neo: A Learned Query Optimizer (VLDB 2019) → `eli5-neo-query-optimizer.md`

**Week 6 — large models on code, verified lifting**
- Evaluating Large Language Models Trained on Code (Codex) — <https://arxiv.org/abs/2107.03374> → `eli5-codex-evaluating-llms-on-code.md`
- Verified Lifting of Stencil Computations (PLDI 2016) → `eli5-verified-lifting-stencil.md`
- Bao: Making Learned Query Optimization Practical (SIGMOD Record 2022) → `eli5-bao-query-optimization.md`

**Week 7 — synthesis for science, learned systems components**
- arXiv:2004.13301 — <https://arxiv.org/abs/2004.13301> → `eli5-learned-garbage-collection.md`
- arXiv:2404.04621 — <https://arxiv.org/abs/2404.04621>
- Report of the Workshop on Program Synthesis for Scientific Computing → `eli5-program-synthesis-scientific-computing.md`

**Week 8 — code search and graph-transformation repair**
- Aroma: Code Recommendation via Structural Code Search — <https://doi.org/10.1145/3355089.3356549> → `eli5-aroma-code-recommendation.md`
- Hoppity: Learning Graph Transformations to Detect and Fix Bugs in Programs (ICLR 2020) → `eli5-hoppity.md`

**Week 9 — fitness functions and program-derived semantics**
- arXiv:1908.08783 — <https://arxiv.org/abs/1908.08783> → `eli5-fitness-functions-for-mp.md`
- Software Language Comprehension using a Program-Derived Semantics Graph — <https://arxiv.org/abs/2004.00768> → `eli5-program-derived-semantics-graph.md`

**Week 10 — semantic parsing**
- A Survey on Semantic Parsing → `eli5-survey-semantic-parsing.md`

**Also explained in `eli5/`** (systems that recur across the course): MP-CodeCheck, IsoPredict,
Dexter (translating image-processing libraries to Halide), Learned Garbage Collection.

**Lectures** — weeks 1, 2, 3, 4, 6, 7 and 8 of the 2024 offering of CS 329M. The slides and the
free lecture recordings are the instructor's material; get them from the course pages above rather
than from here.

## What to look at in the knot

Open the **tangle** view and hover the ELI5 segment: the chords fan out to the papers each note
explains. Search *"program synthesis from input-output examples"* and the construct plan starts at
the FlashFill note and steps into the POPL paper. Tick **analysis** and the fan-out list is the
course's spine — the sections that reference the most other material.
