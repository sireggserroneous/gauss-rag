# ELI5 — Aroma: Code Recommendation via Structural Code Search

**Reference:** Sifei Luan, Di Yang, Celeste Barnaby, Koushik Sen, Satish Chandra (Facebook, UC Irvine, UC Berkeley), 2019. arXiv:1812.01158. *slug: aroma-code-recommendation*

**The problem.** You've written a few lines and you're stuck. Somewhere in millions of open-source files, other people have written *the rest* of what you need. How do you find and reuse it — by meaning, not just text match?

**The idea.** Search a huge code corpus for method bodies *structurally similar* to your partial snippet, then show you the common "extensions" — the code others usually add around code like yours.

**How it works.** Aroma parses code into a **simplified parse tree (SPT)**, turns it into a sparse feature vector, and indexes a corpus of thousands of projects. Given a query snippet it does a fast approximate search, then **clusters and intersects** the top matches to produce a few concise, de-duplicated recommendations — not one file, but the *consensus* pattern. It's fast (sub-second) and works across 4 languages, with an IDE plugin.

**Tools & packages.** Language parsers to build the SPT, a feature-index for approximate search, an IDE plugin. No heavyweight neural model — it's structural search, which makes it cheap to run.

**Why it matters for Machine Programming.** A strong **Intention** + **Invention** example: your half-written code *is* the intent, and Aroma invents the completion by mining collective practice. Its "simplified parse tree" is later cited (in the PSG paper, week 9) as one of the higher-order code representations MP is converging on.
