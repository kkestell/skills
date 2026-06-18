# Hollow rhetorical constructions

Sentence-shape tells: constructions that manufacture profundity, drama, or engagement without adding information. Used once, most are fine; LLMs reach for them reflexively, especially in openers, taglines, and conclusions. Delete the construction and state the point.

---

## not-just-but

The "not just X — it's Y" antithesis construction, and its cousins ("not merely," "isn't just," "more than just," "not only ... but also").

**Why it's slop:** This negation-then-elevation pattern manufactures profundity by denying a modest framing and substituting a grander one, usually without adding information.

**Common forms:** not just a/an/the/about, is/it's not just/merely, isn't just/merely, more than just/merely/simply, not only.

- Avoid: "The Miata isn't just a car — it's a canvas for self-expression."
- Prefer: "The Miata is a lightweight, affordable sports car popular with tuners."

---

## not-x-but-y

The negative-parallelism reversal "not X, but (rather) Y" — denying the first framing outright and substituting a grander or "corrected" one. Distinct from not-just-but, which *adds* to X rather than negating it.

**Why it's slop:** LLMs reach for this reversal to sound insightful or to "correct" an assumed misconception, usually without adding information.

**Common forms:** but rather; rather, it is/represents/reflects; it is/isn't/it's not about; ", not just/merely/simply a/an/the/for/with/to/about..."

- Avoid: "The repository is not a database, but rather a single source of truth."
- Prefer: "The repository stores configuration as the single source of truth."

---

## hollow-from-construction

Empty "from X to Y" range framing where X and Y aren't on a real spectrum, and the clichéd idiom "doesn't come / emerge from nowhere."

**Why it's slop:** "From X to Y" implies a meaningful scale; LLMs use it to dress up a list of two loosely related things. "Doesn't emerge from nowhere" gestures at causation without naming a cause. The general "from X to Y" misuse needs your judgment — say what you mean directly.

**Common forms:** doesn't/didn't/does not/did not emerge/come/appear/spring/arise/materialize/happen from nowhere; emerged/came/appeared/sprang/arose from nowhere; "from X to Y" where X and Y aren't really a spectrum.

- Avoid: "This bug didn't emerge from nowhere — it came from a race condition."
- Prefer: "This bug comes from a race condition between the writer and the reaper thread."

---

## formulaic-openers

Stock essay openers that stall before reaching the point.

**Why it's slop:** These framing clauses set a grand, generic scene that could precede almost any topic and add no information. The real sentence starts after the comma. Delete the clause and begin at the point.

**Common forms:** "In an era of/where/when...", "In a world where/of/increasingly...", "In today's / our fast-paced / modern / digital / ever-changing...", "Imagine a world/future/scenario where...", "Imagine if you / what would / being able to..."

- Avoid: "In an era of rapid change, companies must adapt to survive." / "Imagine a world where every API just worked."
- Prefer: "Companies that batch their deploys ship 30% fewer regressions."

---

## false-conclusion

High-school-essay conclusion signposts that announce a wrap-up instead of delivering one.

**Why it's slop:** A conclusion should land through its content, not be flagged with a signpost. If you need to write "to sum up," the summary that follows usually adds nothing the body didn't already establish.

**Common forms:** at the end of the day, all in all, to sum up, in summary, to summarize, all things considered, when all is said and done, in the final analysis, the bottom line is.

- Avoid: "At the end of the day, all things considered, the migration was worth it."
- Prefer: "The migration cut our hosting bill by 40% and took three weeks."

---

## false-suspense-transition

Manufactured-suspense transitions that promise a payoff.

**Why it's slop:** These tee up a reveal to create false drama, padding the prose with a beat of suspense instead of just stating the point. It's a content-marketing tic. Delete the transition and make the statement.

**Common forms:** here's the kicker/thing/catch/twist/secret/deal/problem/rub, here's where it gets interesting/tricky/good/complicated, here's what most people miss / nobody tells you, but here's the..., plot twist.

- Avoid: "The benchmark looked great. But here's the kicker: it ran on cached data."
- Prefer: "The benchmark ran on cached data, so the 10x speedup doesn't reflect production."

---

## pedagogical-framing

Teacher-mode preambles that announce an explanation instead of giving it.

**Why it's slop:** The reader doesn't need to be managed into the explanation — these preambles delay the content and adopt a chatbot's instructional tone. Skip the preamble and explain the thing directly.

**Common forms:** let's break this/it down, let's unpack, let's dive/dig in, let's explore/examine, think of it/this as/like, at its core, the beauty of this/it is, this begs the question.

- Avoid: "Let's unpack this. Think of it as a pipeline, and at its core it's just a queue."
- Prefer: "The system is a queue: producers append jobs, workers pull them in order."

---

## performative-candor

Staged sincerity that performs honesty or emotion rather than being it.

**Why it's slop:** Genuine candor is specific and a little uncomfortable; the polished, risk-free version is a verbal flourish that signals authenticity without carrying any. Generic empathy applicable to any situation is indistinguishable from none.

**Common forms:** I'll be honest, let's be real/honest, to be honest/real/frank/fair (with you/here), I'm not gonna lie, I understand this/that/how/your..., your feelings are valid, I'm sorry to hear.

- Avoid: "I'll be honest, this is a tough problem, and I understand how frustrating it can be."
- Prefer: "This is a tough problem because the deadlock only appears under load above 5k RPS."

---

## question-then-answer

A rhetorical question immediately answered by its own next sentence.

**Why it's slop:** The self-answered question manufactures engagement and pads the prose with a beat that adds nothing — just state the point. LLMs lean on it as an explanatory tic, especially to open sections. Catch this by reading: a question followed by a short answering sentence in the same paragraph.

- Avoid: "So what does this actually do? It deduplicates the queue."
- Prefer: "This deduplicates the queue."
