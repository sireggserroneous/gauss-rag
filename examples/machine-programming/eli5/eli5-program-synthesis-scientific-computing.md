# ELI5 — Report of the Workshop on Program Synthesis for Scientific Computing

**Reference:** Hal Finkel (Argonne National Lab), Ignacio Laguna (Lawrence Livermore National Lab), eds. US Department of Energy workshop, Aug 2020 / report Jan 2021. arXiv:2102.01687. *slug: program-synthesis-scientific-computing*

**The problem.** Scientific/HPC software (climate models, physics simulations) must run on constantly-changing supercomputers and stay numerically correct. Hand-porting and hand-optimizing this code is a massive, error-prone burden on scientists.

**The idea.** This isn't a system — it's a **community roadmap**. Leading researchers met to ask: where can **program synthesis** (machines writing/transforming code) actually help scientific computing, and what's missing?

**How it works.** The report surveys the landscape and lays out challenges and directions: synthesizing and *lifting* code to portable high-level forms, guaranteeing numerical correctness, handling parallelism and new accelerators, and building the tools/benchmarks the field needs. It's a consensus document with priorities and open problems.

**Tools & packages.** None to install — it references the surrounding ecosystem (synthesis, verification, DSLs, compilers like LLVM/Halide-style approaches).

**Why it matters for Machine Programming.** It's the **institutional/strategic** view of MP: a US national-lab argument that machine programming is essential infrastructure for science, and a checklist of what a mature MP toolchain must provide (portability, correctness guarantees, performance). Useful context for *why* a condensed, turnkey machine-programming runtime is worth building — and what capabilities it should aim to cover.
