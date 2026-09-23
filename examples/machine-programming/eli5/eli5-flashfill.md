# ELI5 — Automating String Processing in Spreadsheets Using Input-Output Examples (FlashFill)

**Reference:** Sumit Gulwani (Microsoft Research), POPL 2011. *slug: flashfill*

**The problem.** Millions of non-programmers wrangle text in spreadsheets — reformatting names, extracting parts of dates, fixing phone numbers. They can't write code, but they *can* show one or two examples of what they want.

**The idea.** Watch a couple of examples ("John Smith" → "Smith, J.") and **synthesize a small program** that does that transformation, then apply it to the whole column. Programming by example, for everyone.

**How it works.** Gulwani designed a restricted string-manipulation DSL (substrings, regex-ish matches, conditionals, loops) and a synthesis algorithm using **version-space algebra** that finds *all* programs consistent with the examples, ranks them, and picks the most likely one — in a fraction of a second. It detects ambiguous inputs and asks for clarification. It shipped as **Flash Fill in Microsoft Excel 2013**.

**Tools & packages.** The string DSL, a version-space-algebra synthesis engine, and an Excel add-in. Famously, the tool "synthesized part of itself."

**Why it matters for Machine Programming.** The canonical **Intention** success story — real users, real product, intent given purely by example. It's the proof that programming-by-example works at scale, and the semantic-parsing survey (week 10) traces the lineage from this to today's natural-language-to-code systems.
