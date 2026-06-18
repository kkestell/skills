# Formulaic structure & rhythm

Tells that live in the *shape* of the text rather than any single phrase: a rigid template arc, connective tissue asserted instead of built, and rhythms (triplets, round-number lists, clipped bursts, repeated openers) applied so consistently they read as generated rather than composed. Most of these have no reliable single-phrase signal — catch them by reading the passage as a whole and counting.

---

## challenges-and-future-outline

A formulaic closing: "Despite [positive], X faces challenges, including ...", followed by vague optimism or speculation about future prospects — often under a "Challenges" or "Future Directions" heading.

**Why it's slop:** LLMs default to a rigid template that pads documents with a generic challenges-then-optimism arc. The challenges lack specifics and the conclusion is empty reassurance. The tell is the *formula*, not the mere mention of a challenge.

**Common forms:** faces several/numerous/many challenges, despite these/its challenges/obstacles/limitations, despite its success, presents its own challenges, "challenges and future," future directions/outlook/prospects/possibilities, continues to thrive/evolve/grow/expand, looking ahead, remains to be seen, only time will tell.

- Avoid: "Despite its success, the library faces challenges, including dependency bloat. Looking ahead, future improvements could enhance performance."
- Prefer: "The library pulls in 40 transitive dependencies, which slows cold installs; issue #212 tracks trimming them."

---

## transitional-connectors

Overused formal connectives deployed to glue paragraphs together.

**Why it's slop:** Well-ordered ideas connect through their content; a pile of "Furthermore / Moreover" signposts is a tell that the connective tissue is being asserted rather than built. One is fine — a document where every paragraph opens with one reads as machine-assembled. (Common mid-sentence too, so confirm it's doing throat-clearing work before cutting.)

**Common forms:** furthermore, moreover, nevertheless, nonetheless, consequently, conversely.

- Avoid: "Furthermore, the API is fast. Moreover, it is reliable. Nevertheless, it has limits."
- Prefer: "The API handles 10k requests/sec and recovers from a node failure in five seconds."

---

## rule-of-three

Reflexive triadic phrasing — "adjective, adjective, and adjective," or three parallel clauses — applied so consistently that nearly every list lands on exactly three items. Audit-only: no reliable single-phrase signal.

**Why it's slop:** LLMs overuse the rule of three to make shallow content look thorough and balanced. When almost every enumeration is a tidy triplet, the rhythm reads as formulaic, and padding to three often forces a vague or redundant third item.

- Avoid: "It is fast, reliable, and scalable, empowering teams to build, ship, and grow."
- Prefer: "It handles ~10k requests/sec and recovers from node failure within 5 seconds."

---

## elegant-variation

Needlessly swapping synonyms or rephrased noun phrases for the same referent across nearby sentences ("the function" → "this routine" → "the helper" → "said method"). Audit-only: no reliable single-phrase signal.

**Why it's slop:** A repetition penalty pushes models to avoid reusing a word, producing a string of paraphrases for one concept. In technical writing this is actively harmful: the reader can't tell whether the varied terms denote the same thing or different things. Repeat the precise term instead.

- Avoid: "Call the parser. This component reads the file; said utility then validates the routine's output."
- Prefer: "Call the parser. The parser reads the file, then validates its output."

---

## staccato-and-fragments

Bursts of very short sentences or one-to-four-word standalone paragraphs used for dramatic emphasis — "It works. Every time. Guaranteed." — and the short-punchy-opener-then-long-elaboration rhythm. Catch by reading: runs of three or more consecutive sentences of six words or fewer, and lone dramatic fragments as their own paragraph.

**Why it's slop:** A run of clipped sentences is a manufactured-drama cadence common in LLM content writing. Used once for effect it's fine; as a recurring rhythm it reads as a list of bullet points in disguise. Vary sentence length and let ideas develop.

- Avoid: "The result was clear. It worked. Every time. No exceptions."
- Prefer: "The change passed every test run, including the three that previously flaked under load."

---

## repetitive-sentence-openers

Mechanical structural repetition across consecutive sentences: the same opener three times running (anaphora), a run of short "-ing" fragments, "Not X. Not Y. Just Z.", or ordinal prose disguising a list ("The first... The second... The third..."). Catch by reading.

**Why it's slop:** Repeating a sentence frame more than twice turns a rhetorical device into a tic, and ordinal "first/second/third" prose is usually a list wearing a trench coat. The uniform cadence reads as generated. Vary the structure, or use a real list where a list is what you have.

- Avoid: "It scales. It adapts. It endures. The first benefit is speed. The second is cost."
- Prefer: "It scales to 10k RPS and costs about $40/month at that load."

---

## magic-number-lists

Bullet or numbered lists that land on exactly 3, 5, 7, or 10 items so consistently it looks templated, regardless of how many the topic actually has. Audit-only: list length needs your count.

**Why it's slop:** LLMs gravitate to these "round" list lengths, padding to reach one or trimming to fit it. A list should have the number of items the subject actually has — four, six, nine — not a number chosen for shape.

- Avoid: "There are 5 reasons to adopt this: [three solid points and two padded ones]."
- Prefer: "There are two reasons to adopt this: it halves latency and removes the cron job."
