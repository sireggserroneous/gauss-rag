# ELI5 — IsoPredict: Detecting Unserializable Behaviors in Weakly Isolated Data Store Applications

**Reference:** Chujun Geng, Spyros Blanas, Michael D. Bond, Yang Wang (Ohio State University), PLDI 2024. arXiv:2404.04621. *slug: isopredict*

**The problem.** Distributed databases run fast by using **weak isolation** — they don't fully pretend transactions happen one-at-a-time. That speed can silently let programs do wrong things ("unserializable" behaviors) that cause data corruption. These bugs are brutal: they may not appear in the run you're watching, only in *some other possible run*.

**The idea.** Don't wait to observe the bug. From *one* correct-looking run, mathematically **predict** whether a *different, still-valid* run exists that would break serializability — and if so, produce it.

**How it works.** IsoPredict is a **dynamic predictive analysis**. It observes an execution, encodes the rules of the data store and the application as **SMT (satisfiability) constraints**, and asks a solver to find a feasible *unserializable* execution. Novel techniques handle branches that diverge, mutually-recursive constraints, and the coverage/precision/speed trade-off. On four benchmarks it predicted real unserializable behaviors, **99% of them genuinely feasible.**

**Tools & packages.** An **SMT solver (e.g., Z3)**, a dynamic execution tracer/instrumentation, constraint-encoding logic. This is formal methods, not ML.

**Why it matters for Machine Programming.** It's the corpus's reminder that MP isn't only neural nets — **Adaptation** (correctness) also comes from *reasoning*. Predictive, solver-based analysis is a complementary tool a serious machine programmer needs alongside learned models, especially for concurrency and distributed-systems bugs that testing misses.
