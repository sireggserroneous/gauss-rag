# ELI5 — Learning to Represent Programs with Property Signatures

**Reference:** Augustus Odena, Charles Sutton (Google Research), ICLR 2020. arXiv:2002.09030. *slug: property-signatures*

**The problem.** In program synthesis you often only have **input/output examples** ("given this, produce that"). How do you hand a machine-learning model a useful summary of *what function the user wants* from just a handful of examples?

**The idea.** Describe a function by the **properties** it satisfies. A property is a yes/no question about inputs and outputs — e.g., "is the output list the same length as the input list?", "is the output always positive?". Ask many such questions and the pattern of yes/no answers — the **property signature** — becomes a fixed-length fingerprint of the desired program.

**How it works.** You can *guess* a program's property signature from only its I/O examples, then feed that signature to a synthesizer. In their experiments this let a baseline synthesizer emit **twice as many correct programs in one-tenth the time**.

**Tools & packages.** A library of properties, a program synthesizer, and ML to predict signatures. Lightweight, research-grade.

**Why it matters for Machine Programming.** A clean **Intention** pillar contribution: it turns fuzzy "here are some examples" intent into something a machine can compute with. For a turnkey machine programmer that accepts examples as a spec, property signatures are a proven way to make that spec ML-friendly.
