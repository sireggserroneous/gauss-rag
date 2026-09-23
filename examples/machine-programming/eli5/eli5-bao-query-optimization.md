# ELI5 — Bao: Making Learned Query Optimization Practical

**Reference:** Ryan Marcus, Parimarjan Negi, Hongzi Mao, Nesime Tatbul, Mohammad Alizadeh, Tim Kraska (MIT CSAIL, Intel Labs), SIGMOD 2022. *slug: bao-query-optimization*

**The problem.** Fully-learned optimizers like **Neo** are impressive but impractical: they take a long time to train, don't adapt when the data or queries change, and occasionally produce disastrously slow plans (bad "tail latency").

**The idea.** Don't replace the battle-tested optimizer — *steer* it. Keep the existing optimizer and just learn small **per-query hints** ("for this query, avoid that kind of plan").

**How it works.** **Bao** (the Bandit optimizer) wraps the existing optimizer and treats hint-selection as a **multi-armed bandit** problem. It combines a **tree convolutional neural network** (to read query plans) with **Thompson sampling** (a proven exploration/exploitation strategy). It learns from its own mistakes in *minutes*, adapts to workload/schema changes, and improves tail latency — in the cloud it cut both cost and runtime versus a commercial system.

**Tools & packages.** **PostgreSQL** (host optimizer), a tree-convolutional NN, Thompson-sampling RL, a thin hint-injection layer.

**Why it matters for Machine Programming.** The practicality lesson of the whole "learned systems" arc: **augment, don't replace.** Sit a small, fast-learning model on top of a trusted system and you get most of the win with far less risk — a design principle worth baking into a turnkey machine programmer.
