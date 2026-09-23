# ELI5 — Evaluating Large Language Models Trained on Code (Codex)

**Reference:** Mark Chen, Jerry Tworek, Heewoo Jun, et al. (OpenAI), 2021. arXiv:2107.03374. *slug: codex-evaluating-llms-on-code*

**The problem.** Can a general language model, if you feed it enough code, actually *write working programs* from a plain-English description?

**The idea.** Take a GPT language model, fine-tune it on a huge pile of public GitHub code, and measure whether it can turn a docstring ("return the list sorted, ignoring case") into correct, runnable code.

**How it works.** They built **Codex** and a benchmark called **HumanEval** — 164 hand-written programming problems scored by *actually running unit tests* (functional correctness, not text similarity). Codex solved **28.8%** of problems in one try (GPT-3: 0%); with **100 samples per problem** and picking the ones that pass tests, **70.2%**. A production Codex powers **GitHub Copilot**. The paper is honest about limits (long chains of reasoning, security, alignment).

**Tools & packages.** A GPT/transformer model, the HumanEval benchmark (released), a sandboxed code-execution harness for scoring, large-scale sampling.

**Why it matters for Machine Programming.** This is the **Intention** pillar's modern face: natural language in, code out, at scale. Two ideas here are directly reusable for us — **execute-and-test to judge generated code**, and **sample-many-then-filter** — both of which a turnkey machine programmer would lean on heavily.
