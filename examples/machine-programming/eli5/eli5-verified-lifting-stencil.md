# ELI5 — Verified Lifting of Stencil Computations

**Reference:** Shoaib Kamil, Alvin Cheung, Shachar Itzhaky, Armando Solar-Lezama (Adobe, U. Washington, MIT), 2016. *slug: verified-lifting-stencil*

**The problem.** Tons of valuable numeric code (image filters, simulations) is trapped in old, low-level **Fortran/C** that's fast on yesterday's machine but can't be re-optimized for new hardware. Rewriting it by hand into a modern high-performance language is expensive and risky.

**The idea.** **Lift** the old code: automatically figure out *what it computes* (a clean, high-level mathematical summary), throw away *how* it did it, and let a modern compiler generate a fresh, fast implementation — with a *proof* the summary is equivalent.

**How it works.** They combine **program synthesis** and **verification**: **counter-example-guided inductive synthesis (CEGIS)** searches for a high-level summary (in a predicate language) of a low-level stencil, and an SMT solver *verifies* it's provably equivalent. It's sound and mostly automatic. The lifted summaries let domain-specific compilers parallelize far better than an off-the-shelf compiler could.

**Tools & packages.** A CEGIS synthesis engine, an **SMT solver (Z3)** for verification, a predicate/summary language, DSL back-ends. Sketch-style synthesis lineage (Solar-Lezama).

**Why it matters for Machine Programming.** A rigorous **Adaptation** result — *machine-port legacy code, with a correctness guarantee.* Paired with Dexter (week 8, lifting to Halide), it shows MP's answer to technical debt: don't just help write new code, safely modernize the mountains of old code.
