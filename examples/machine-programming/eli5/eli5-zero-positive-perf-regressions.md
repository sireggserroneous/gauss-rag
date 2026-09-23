# ELI5 — A Zero-Positive Learning Approach for Diagnosing Software Performance Regressions

**Reference:** Mejbah Alam, Justin Gottschlich, Nesime Tatbul, Javier Turek, Timothy Mattson, Abdullah Muzahid (Intel Labs, MIT, Texas A&M), NeurIPS 2019. *slug: zero-positive-perf-regressions*

**The problem.** Software sometimes gets mysteriously slower after a change (a "performance regression"). You rarely have labeled examples of *what a regression looks like* — you mostly have recordings of the program running *normally*.

**The idea.** Learn only from "normal," then flag anything that doesn't fit as a possible regression. They call this **zero-positive learning**: train with zero positive (buggy) examples — it's anomaly detection applied to performance.

**How it works.** The system (**AutoPerf**) records low-level **hardware performance counters** while the program runs, trains **autoencoder** neural networks to reconstruct normal behavior, and raises a flag when reconstruction error spikes — meaning the runtime behavior drifted from normal. It caught real regressions across parallel programs.

**Tools & packages.** Hardware performance counters (e.g., via `perf`/PMU), autoencoder neural nets (deep-learning stack), profiling instrumentation.

**Why it matters for Machine Programming.** An **Adaptation**-pillar result about keeping software *fast*, not just correct. It's also a methodological template — "learn normal, detect the anomaly" — that pairs with BugLab and MP-CodeCheck as MP's toolkit for finding problems without labeled bug data.
