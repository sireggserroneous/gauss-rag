# ELI5 — Neo: A Learned Query Optimizer

**Reference:** Ryan Marcus, Parimarjan Negi, Hongzi Mao, Chi Zhang, Mohammad Alizadeh, Tim Kraska, Olga Papaemmanouil, Nesime Tatbul (Brandeis, MIT, Intel Labs), 2019. *slug: neo-query-optimizer*

**The problem.** When a database runs a query, an "optimizer" decides *how* — which tables to join first, which indexes to use. Good optimizers are decades of hand-tuned heuristics, brittle and workload-specific.

**The idea.** Let the database *learn* to optimize by experience, like a game-playing AI learns moves — get better at planning the more queries it runs.

**How it works.** **Neo** (Neural Optimizer) uses **deep reinforcement learning**: a value network predicts how fast a partial plan will run, guiding a search over join orders and operators. It **bootstraps from an existing optimizer** (even one as simple as PostgreSQL's) so it starts sane, then keeps learning from real query outcomes, adapting to the data. It matched or beat state-of-the-art *commercial* optimizers.

**Tools & packages.** **PostgreSQL** (bootstrap + execution), a deep value network (PyTorch/TensorFlow-era), an RL training loop, query-plan featurization.

**Why it matters for Machine Programming.** Learned Index Structures said "ML can *be* a data structure"; Neo says "ML can *be* the optimizer." It's a strong **Invention/Adaptation** example and sets up **Bao** (week 6), which fixes Neo's practicality problems.
