# ELI5 — code2vec: Learning Distributed Representations of Code

**Reference:** Uri Alon, Meital Zilberstein, Omer Levy, Eran Yahav (Technion, Facebook AI Research), 2018. arXiv:1803.09473. *slug: code2vec*

**The problem.** Machine-learning models eat vectors, not source code. How do you turn a chunk of code into a single, fixed-length vector that captures what it *does*, so a model can reason about it?

**The idea.** Represent a method as a *bag of paths through its abstract syntax tree (AST)*. Each path connects two leaves (say, a variable to where it's used). Learn a vector for every path, then use an **attention** mechanism to weigh which paths matter and sum them into one "code vector."

**How it works.** Trained on **14 million methods**, the model predicts a method's *name* from its body — a proxy for "understanding" it. The learned vectors capture semantic analogies (like word2vec for code), and it beat prior methods by ~75%. There's a live demo (code2vec.org) and open weights.

**Tools & packages.** A path-extractor over ASTs (the JavaExtractor / later `astminer`), TensorFlow for the attention network, and the released model at `github.com/tech-srl/code2vec`. Java parser front-end.

**Why it matters for Machine Programming.** It's a foundational **representation** — an **Invention**-pillar building block that many downstream MP systems reuse. The corpus's whole "week 3–4" arc (Neural Code Comprehension, Programs-with-Graphs, PSG) is a debate about *the right way to vectorize code*, and code2vec is the reference point they argue against.
