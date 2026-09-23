# ELI5 — Learned Garbage Collection

**Reference:** Lujing Cen, Ryan Marcus, Hongzi Mao, Justin Gottschlich, Mohammad Alizadeh, Tim Kraska (MIT CSAIL, Intel Labs), MAPL 2020. arXiv:2004.13301. *slug: learned-garbage-collection*

**The problem.** Garbage collection (GC) automatically frees memory a program no longer needs. GC has knobs that dramatically affect performance (like tail latency), but most developers don't know the GC exists, let alone how to tune it for their app.

**The idea.** Let the GC *tune itself* to your specific program, by learning from how the program actually behaves — no human tuning.

**How it works.** They frame GC policy as a **reinforcement-learning** problem: the agent decides GC behavior (like when to collect which generation) to maximize a **custom reward** you care about — request latency for a web server, smoothness for a video app. It targets **long-running programs with a repeating core loop** (servers, databases), so the agent gets lots of feedback to learn from. It's a prototype/sketch, but shows automatic, application-specific GC is feasible.

**Tools & packages.** An RL agent, hooks into a language runtime's garbage collector, a reward-measurement harness. Runtime-level integration is the real dependency.

**Why it matters for Machine Programming.** Another "learn a core system component" result in the **Adaptation/Invention** line (alongside Learned Index Structures, Neo, Bao). The pattern — *optimize a system knob against a real-world reward, automatically* — is exactly what a turnkey machine programmer should do to make deployed software faster without human babysitting.
