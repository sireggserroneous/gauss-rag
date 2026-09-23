# ELI5 — The Three Pillars of Machine Programming

**Reference:** Gottschlich, Solar-Lezama, Tatbul, Carbin, Rinard, Barzilay, Amarasinghe, Tenenbaum, Mattson (Intel Labs + MIT), 2018/2021. arXiv:1803.07244. *slug: three-pillars-of-machine-programming*

**The problem.** "Machine Programming" (MP) — getting machines to help write software — was a scattered field: program synthesis people, ML-for-code people, and systems people were all solving pieces without a shared map. This paper draws the map.

**The idea.** All of MP fits into **three pillars**:
- **Intention** — figure out *what the human wants*. The human can say it in English, draw it, give input/output examples, or point at existing code. Better human↔machine interfaces live here.
- **Invention** — *create or discover* the algorithms and data structures that satisfy the intent (e.g., inventing a new index, composing existing pieces into something new).
- **Adaptation** — *evolve* working software to run better on a given machine/ecosystem: faster, safer, more correct, ported to new hardware.

**How it works.** It's a position/vision paper, not a system. It classifies dozens of research efforts into the three pillars and argues the future is combining them end-to-end.

**Tools & packages.** None directly — but it's the lens for reading every other reference: each paper is really working one or two pillars.

**Why it matters for Machine Programming.** This is the project's north star. Our "turnkey machine programmer" is exactly a system that spans all three pillars: take intent, invent/assemble a solution, and adapt it to the target runtime. When we condense the corpus into one runtime, this is the taxonomy we're condensing *toward*.
