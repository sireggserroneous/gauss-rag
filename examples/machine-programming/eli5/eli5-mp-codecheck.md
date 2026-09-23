# ELI5 — MP-CodeCheck: Evolving Logical Expression Code Anomaly Learning

**Reference:** Urs C. Muff, Celine Lee, Paul Gottschlich, Justin Gottschlich (Merly.ai, Cornell, UPenn), 2022. arXiv:2204.07225. *slug: mp-codecheck*

**The problem.** Engineers spend **>50% of their time debugging**. Many bugs hide in *logical expressions* — the conditions in `if`/`while` statements — where a subtle mistake (`<=` vs `<`, a flipped boolean) is easy to write and hard to spot.

**The idea.** Learn what *normal* logical expressions look like, then flag the *anomalies* — expressions that don't fit the patterns learned from billions of lines of real code. No labeled bug dataset needed.

**How it works.** MP-CodeCheck (MPCC) uses **iterative self-supervision**: it teaches itself from unlabeled code, refining its notion of "anomalous" over rounds. Its key ingredient is two **new programming-language representations** built to process billions of lines efficiently. It surfaces suspicious logical expressions for review.

**Tools & packages.** Custom PL representations, a self-supervised training pipeline over massive code corpora, deep-learning stack. A Merly.ai product line.

**Why it matters for Machine Programming.** Pure **Adaptation** pillar — automatically making existing software more correct. It also demonstrates the corpus's recurring recipe: *self-supervision* (learn from code without labels), which shows up again in BugLab (week 5). For a turnkey machine programmer, "catch the bug before the human ships it" is a headline feature.
