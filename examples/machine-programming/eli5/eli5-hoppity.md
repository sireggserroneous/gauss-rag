# ELI5 — Hoppity: Learning Graph Transformations to Detect and Fix Bugs in Programs

**Reference:** Elizabeth Dinella, Hanjun Dai, Ziyang Li, Mayur Naik, Le Song, Ke Wang (UPenn, Google Brain, Georgia Tech, Visa Research), ICLR 2020. *slug: hoppity*

**The problem.** Most learned bug-fixers only handle one narrow bug type (like a wrong variable) or a fixed template. Real bugs are diverse — a missing null check, a wrong operator, an extra argument — and fixing them can require several coordinated edits.

**The idea.** Treat "fix the bug" as **editing a graph**. Model the program as a graph, then learn to output a *sequence of graph edits* — delete this node, add that one, replace this value — that transforms the buggy program into a correct one.

**How it works.** Given a buggy JavaScript program as a graph, **Hoppity** predicts, step by step: *where* the bug is (which node) and *what edit* to make (add/delete/replace), chaining edits together to produce the fix. Because edits are general graph operations, it handles a **broad range** of bug types, not a fixed catalog — a real advance over prior template-based repair.

**Tools & packages.** A graph neural network, a graph-edit/decoder model, a JavaScript parser to build program graphs, deep-learning stack. Builds on "Programs with Graphs" (week 4).

**Why it matters for Machine Programming.** The **Adaptation** pillar's most general learned repair in the corpus: *general edits, not templates.* "Find any bug and emit the concrete fix" is a headline capability for a turnkey machine programmer, and the graph-edit framing is a reusable design.
