# ELI5 — Halide: A Language and Compiler for Image Processing Pipelines

**Reference:** Jonathan Ragan-Kelley, Connelly Barnes, Andrew Adams, Sylvain Paris, Frédo Durand, Saman Amarasinghe (MIT CSAIL, Adobe), PLDI 2013. *slug: halide*

**The problem.** Image-processing code (blur, resize, filters) can run **10× faster** if you hand-optimize how it uses parallelism and memory — but doing that by hand tangles the *math* together with the *optimization*, making code unreadable and unportable.

**The idea.** **Separate the algorithm from the schedule.** Write *what* to compute once (the pixel math), and *how* to compute it (tiling, vectorization, parallelism, when to recompute vs. store) as a separate, swappable "schedule." One algorithm, many schedules for many machines.

**How it works.** Halide is a DSL embedded in C++ with an LLVM backend. The same 3-line blur can be scheduled dozens of ways to hit different CPUs/GPUs; later versions auto-search for good schedules ("auto-scheduling").

**Tools & packages.** The Halide compiler (C++ + LLVM), its autoscheduler, GPU/CPU code generators. This is a *real deployable dependency*, not just a paper.

**Why it matters for Machine Programming.** Halide is the poster child for the **Adaptation** pillar: adapt one intent to many hardware targets automatically. It shows up twice more in the corpus — *Verified Lifting* and *Dexter* (week 6, week 8) both aim to **auto-translate legacy code into Halide**, which is MP closing the loop: don't just optimize new code, machine-port the old.
