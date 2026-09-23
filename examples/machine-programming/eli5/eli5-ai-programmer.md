# ELI5 — AI Programmer: Autonomously Creating Software Programs Using Genetic Algorithms

**Reference:** Kory Becker, Justin Gottschlich (Bloomberg LP, Intel Labs), 2017. arXiv:1709.05703. *slug: ai-programmer*

**The problem.** Can a machine write a whole working program *by itself*, with almost no human help — not autocomplete, but "here's the goal, go build it"?

**The idea.** Treat program-writing like evolution. Start with random programs, keep the ones that score better against a goal (the *fitness function*), breed and mutate them, repeat. Over many generations, working programs emerge.

**How it works.** The trick that makes it tractable: generate programs in a *tiny* instruction set (a Brainfuck-style language with ~8 instructions) so the search space is small enough for a genetic algorithm to explore. A fitness function measures how close each candidate's output is to the desired output; selection + crossover + mutation drive the population toward correct programs. It generated real programs ("Hello World", reversing a string, simple math) from scratch.

**Tools & packages.** A genetic-algorithm engine, a minimal-language interpreter (Brainfuck-style VM), and a fitness/scoring loop. Lightweight — no neural nets, no GPU.

**Why it matters for Machine Programming.** It's the clearest early example of the **Invention** pillar (and **Intention** via the fitness spec). It also seeds a thread the corpus returns to — *Learning Fitness Functions for Machine Programming* (week 9) fixes this paper's hardest part: hand-writing the fitness function.
