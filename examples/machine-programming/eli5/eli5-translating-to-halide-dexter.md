# ELI5 — Automatically Translating Image Processing Libraries to Halide (Dexter)

**Reference:** Maaz Bin Safeer Ahmad, Jonathan Ragan-Kelley, Alvin Cheung, Shoaib Kamil (U. Washington, UC Berkeley, Adobe), OOPSLA 2019. *slug: translating-to-halide-dexter*

**The problem.** Halide (week 2) makes image code fast and portable — but only if it's *written in Halide*. Companies have decades of hand-written **C++** image code (e.g., in Adobe Photoshop) that can't benefit. Rewriting it by hand is huge and risky.

**The idea.** Automatically translate existing low-level C++ image functions into equivalent **Halide**, *guaranteeing* the translation means the same thing — then let Halide's autoscheduler make it fast on any platform.

**How it works.** **Dexter** parses a C++ function into a DAG of small stages, then uses a **domain-specific program-synthesis algorithm** (plus verification) to infer each stage's meaning in a high-level IR, and finally emits Halide. It scales to real functions with tiling, conditionals, and multi-stage pipelines. On Photoshop code it translated **264 of 353** functions, with median **7.0× (Intel) / 4.5× (ARM)** speedups.

**Tools & packages.** A C++ front-end/DAG parser, a synthesis+verification engine, an intermediate representation, and **Halide** (target + autoscheduler). Same synthesis lineage as Verified Lifting.

**Why it matters for Machine Programming.** The **Adaptation** pillar at industrial scale: *machine-modernize a real product's code, provably.* Together with Verified Lifting it forms the corpus's "lift legacy code into a fast DSL" theme — a concrete, high-value job for a turnkey machine programmer.
