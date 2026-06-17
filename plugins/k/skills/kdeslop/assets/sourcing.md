# Sourcing, hedging & chatbot residue

Tells about *honesty* and *provenance*: claims laundered through a vague authority, breadth overstated, epistemic limits narrated instead of resolved, templates left unfilled, hedges stacked to dodge commitment, and leftover chat-session correspondence. Several of these (placeholders, cutoff disclaimers, chatbot talk) are near-unambiguous signs of pasted, unreviewed output.

When a fix needs a fact you don't have, flag it for the user rather than inventing content.

---

## vague-attribution-weasel

Opinions or claims pinned on an unnamed authority.

**Why it's slop:** LLMs launder unsupported claims through a vague collective authority. Without a named source the attribution is unfalsifiable and inflates how widely a view is actually held.

**Common forms:** experts/analysts/observers/critics/scientists/researchers argue/say/note/suggest/believe/claim/contend/point out; many/some/several/most experts; according to experts/analysts/sources/some; studies/research/data/evidence show/suggest/indicate/reveal; it is widely/generally/commonly/often regarded/considered/believed/accepted/known; is widely regarded/seen as; industry reports/analysts/sources/experts; many believe.

- Avoid: "Experts agree this is the most efficient approach available." / "Studies show that developers prefer this pattern."
- Prefer: "A 2024 benchmark by the maintainers measured it as 3x faster than the prior approach."

---

## exaggerated-source-quantity

Phrasing that implies many sources or examples when only one or two are given.

**Why it's slop:** LLMs overstate breadth, presenting one or two instances as an open-ended set or broad consensus. It makes coverage or support look more established than it is.

**Common forms:** tools/libraries/frameworks/platforms/languages/companies/options/features such as; a wide/broad/vast/diverse/growing range/variety/array/number of; a number of; numerous; among/and many others/more; a host/plethora/myriad/multitude of; countless.

- Avoid: "Numerous libraries such as Foo and Bar support this out of the box."
- Prefer: "Two libraries support this out of the box: Foo and Bar."

---

## knowledge-cutoff-disclaimer

Hedges that information may be outdated because of a training cutoff, or speculation that facts are "not well documented" followed by a guess at what they "likely" are.

**Why it's slop:** Documentation should state facts, not narrate a model's epistemic limits. A cutoff disclaimer is a direct LLM giveaway, and "not widely documented" hedges frequently precede fabricated or inferred content. Verify the fact or cut the sentence.

**Common forms:** as of my last/knowledge/most recent..., up to my last..., as an AI (language model), I don't/cannot have specific/real-time information/data/access, while specific details/information about..., in the provided/available/given sources/text/context/search results, in the search results, not widely/extensively/well documented, is likely, it is believed that, knowledge cutoff, my training data.

- Avoid: "While specific details about the rate limit are not widely documented, it is likely around 1000 req/min."
- Prefer: "The rate limit is 1000 requests per minute."

---

## placeholder-text

Fill-in-the-blank templates and bracketed placeholders the author never replaced.

**Why it's slop:** Unfilled placeholders are an unambiguous sign of pasted, unreviewed output: the model produced a Mad-Libs template for a human to complete and nobody did. They must be filled in or removed before publishing.

**Common forms:** [insert ...], [describe ...], [your name], [link to ...], [date], [company name], TBD, to be added/determined/filled in. Also catch underscored ALL-CAPS placeholders like `INSERT_URL_30` by eye.

- Avoid: "Contact the maintainer at [Your Name] for access." / "Default timeout: TBD."
- Prefer: "Contact the maintainer at jdoe@example.com for access."

---

## chatbot-collaborative-talk

Conversational meta-commentary aimed at a human chat partner rather than the reader: offers of further help, sign-offs, pleasantries, sycophantic openers, and explicit narration of producing the document.

**Why it's slop:** This is leftover chat-session correspondence that leaked into the published text. It addresses a "user" who doesn't exist for a document reader, adds no information, and is a clear sign of copy-pasted output. Almost always it should simply be deleted.

**Common forms:** I hope this helps, hope this helps, would you like me to, is there anything else, let me know if, feel free to, you're absolutely right, great/excellent/good question, "in this article/post/guide we will...", "we'll explore/discuss/examine/cover/dive into...", "as we've seen/discussed...", in conclusion.

- Avoid: "The function returns a sorted list. Would you like me to explain the algorithm?"
- Prefer: "The function returns a sorted list."

---

## almost-hedge

Hedging an absolute with "almost."

**Why it's slop:** "Almost always" dodges commitment without adding precision — either say "usually" or commit to "always" and defend it. LLMs hedge this way to avoid being pinned down, and readers notice the evasion.

**Common forms:** almost always/never/certainly/exclusively/entirely/completely/invariably/universally.

- Avoid: "This is almost always the fastest option, and it almost never fails."
- Prefer: "This is usually the fastest option. It has failed twice in three years."

---

## hedge-stacking

Several epistemic hedges piled into one sentence — "perhaps," "arguably," "it could be argued that this might possibly..."

**Why it's slop:** One hedge can be honest calibration; three or four in a sentence communicate nothing and signal a model dodging any falsifiable claim. Keep at most one genuine hedge, or commit to the claim. Catch this by reading: two or more hedges in a single sentence ("should" / "would" don't count).

- Avoid: "It could perhaps be argued that this might, in some sense, be seen as a possibly suboptimal choice."
- Prefer: "This is the wrong choice here: it doubles write latency for a feature few users hit."
