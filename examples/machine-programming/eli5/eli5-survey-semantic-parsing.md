# ELI5 — A Survey on Semantic Parsing

**Reference:** Aishwarya Kamath (Oracle Labs), Rajarshi Das (UMass Amherst), AKBC 2019. *slug: survey-semantic-parsing*

**The problem.** Lots of the world's information sits in databases and knowledge bases you can only query with formal languages (like SQL). Ordinary people can't write those. How do we turn "how many customers did we lose last quarter?" into an executable query automatically?

**The idea.** **Semantic parsing** = translate a natural-language sentence into a **logical form** (a formal, executable meaning representation). This survey maps the whole field, from old rule-based systems to modern neural and program-synthesis approaches.

**How it works.** As a survey it breaks a semantic parser into its components (how meaning is represented, how the model is trained, how much supervision is needed) and walks the evolution: hand-written grammars → statistical methods → neural sequence models → treating it as program synthesis. It highlights the key challenge — learning good parsers **without** tons of labeled logical forms.

**Tools & packages.** None to install — it's a map of methods and datasets, useful as a reference index.

**Why it matters for Machine Programming.** It closes the course on the **Intention** pillar: turning human language into executable formal code is *the* interface problem for a machine programmer. This survey is the bridge from classic FlashFill-style programming-by-example to today's natural-language-to-code — exactly the front door a turnkey machine programmer presents to its users.
