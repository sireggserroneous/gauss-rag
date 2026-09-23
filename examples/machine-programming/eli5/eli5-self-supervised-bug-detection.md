# ELI5 — Self-Supervised Bug Detection and Repair (BugLab)

**Reference:** Miltiadis Allamanis, Henry Jackson-Flux, Marc Brockschmidt (Microsoft Research), NeurIPS 2021. arXiv:2105.12787. *slug: self-supervised-bug-detection*

**The problem.** To train a bug-finder with machine learning you need lots of examples of "buggy code + its fix." Those labeled datasets barely exist — real bugs are rare and messy to collect.

**The idea.** Make the training data yourself. Have one model *insert* plausible bugs and another model *catch* them, and let them push each other to improve — no human labels required.

**How it works.** **BugLab** co-trains two networks in a game: a **selector** learns to introduce subtle, realistic bugs into correct code, and a **detector** learns to find and fix them. As the detector gets better, the selector must invent harder bugs — an adversarial loop. The Python implementation beat baselines by **up to 30%** and found **19 previously-unknown bugs** in real open-source projects.

**Tools & packages.** Python; a graph/GNN-based code model (building on "Programs with Graphs"); a self-supervised training loop. Operates on data-and-control-flow graphs of code.

**Why it matters for Machine Programming.** A flagship **Adaptation** result and the corpus's clearest example of *self-supervision beating the data-scarcity problem* — the same trick MP-CodeCheck uses. "Find and fix bugs with no labeled data" is a core capability for any turnkey machine programmer.
