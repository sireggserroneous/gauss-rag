# ELI5 — Neural Code Comprehension: A Learnable Representation of Code Semantics

**Reference:** Tal Ben-Nun, Alice Shoshana Jakobovits, Torsten Hoefler (ETH Zurich), NeurIPS 2018. *slug: neural-code-comprehension*

**The problem.** Most "ML for code" work treated code like English sentences or raw syntax trees. But code has structure English doesn't — function calls, branches, and statements whose order can be swapped without changing meaning. Token/AST models miss this.

**The idea.** Don't learn from the source text — learn from what the code *actually does* at a lower level, using the compiler's own intermediate representation (IR).

**How it works.** They build a **conteXtual Flow Graph (XFG)** from LLVM IR that captures both data flow and control flow, then learn embeddings for IR statements — **inst2vec** — the way word2vec learns word meanings from context. Because it operates on LLVM IR, the representation is *language-agnostic*: C, C++, anything that compiles to LLVM shares one embedding space.

**Tools & packages.** **LLVM** (to compile source → IR), the XFG builder, and the inst2vec embedding model (released open-source). LLVM is the real dependency here.

**Why it matters for Machine Programming.** A key **Invention/representation** result: work at the IR level and you get one model for many languages. That "meet in the middle at the IR" idea recurs across the corpus (it's a theme of the week 7–8 lectures on intermediate representations) and is exactly the kind of shared substrate a single turnkey runtime would want.
