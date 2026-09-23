# ELI5 — Learning Fitness Functions for Machine Programming

**Reference:** Shantanu Mandal, Todd Anderson, Javier Turek, Justin Gottschlich, Shengtian Zhou, Abdullah Muzahid (Texas A&M, Intel Labs), MLSys 2021. arXiv:1908.08783. *slug: fitness-functions-for-mp*

**The problem.** Genetic-algorithm program synthesis (like *AI Programmer*, week 1) lives or dies by its **fitness function** — the scorer that says how "good" a candidate program is. Hand-crafting that scorer is hard, and a bad one sends evolution in the wrong direction.

**The idea.** Don't hand-write the fitness function — **learn** it. Train a neural network to predict what an *ideal* fitness score should be, and use that to guide evolution.

**How it works.** A neural network learns to estimate fitness values, replacing the brittle hand-tuned scorer. They also add a **minimally-intrusive search heuristic** that nudges "almost-correct" candidates toward fully-correct ones with negligible extra cost. The result finds **more correct programs in fewer generations** than several state-of-the-art synthesis methods.

**Tools & packages.** A genetic-algorithm engine, a neural fitness-predictor (deep-learning stack), a search-heuristic layer.

**Why it matters for Machine Programming.** It directly repairs the weakest link of the corpus's opening paper (AI Programmer): a pure **Invention**-pillar improvement to program synthesis. The meta-lesson — *when a hand-designed component is the bottleneck, learn it* — echoes the learned-systems papers (indexes, optimizers, GC).
