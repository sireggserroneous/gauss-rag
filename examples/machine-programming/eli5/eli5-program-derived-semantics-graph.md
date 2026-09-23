# ELI5 — Software Language Comprehension using a Program-Derived Semantics Graph

**Reference:** Roshni G. Iyer, Yizhou Sun, Wei Wang (UCLA), Justin Gottschlich (Intel Labs, UPenn), NeurIPS CAP 2020. arXiv:2004.00768. *slug: program-derived-semantics-graph*

**The problem.** The corpus keeps proposing *different* ways to represent code for machines — ASTs, code2vec's paths, inst2vec's XFG, Aroma's simplified parse tree, Halide's DSL, compiler IRs. Each captures *some* meaning but misses higher-order semantics, and none is a single unifying structure.

**The idea.** Build **one** graph that captures a program's meaning at **multiple levels at once** — the **Program-Derived Semantics Graph (PSG)** — rather than juggling many partial representations.

**How it works.** The PSG is a graphical structure designed to hold program semantics from low-level operations up to higher-order intent in a single object, explicitly drawing on and generalizing prior representations (SPT, XFG, lifted lambda calculi, DSLs). It's positioned as a more complete substrate for machine reasoning about code.

**Tools & packages.** A PSG constructor over source/IR, graph-learning machinery. Research-stage; conceptually unifies the earlier representation tools.

**Why it matters for Machine Programming.** This is the **Invention/representation** thread's synthesis paper: the argument that MP needs a *single, rich, multi-level code representation*. For a turnkey machine programmer, "what internal form do we reason over?" is a foundational design choice, and PSG is the corpus's most ambitious answer.
