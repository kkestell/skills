# AI slop rules

Six families of AI "slop," each with the patterns that belong to it, why each
reads as machine-generated, and avoid/prefer examples.

Read these as a **lens, not a checklist**. The example phrases under "Common
forms" are leads, not the set of things to flag. Judge each candidate on whether
the writing actually has the underlying problem — asserting importance instead
of showing it, saying nothing in many words, hedged vagueness — not merely
whether it contains a listed word. A legitimate use of a flagged word is not
slop.

Several rules have no single-phrase signal (rule-of-three, elegant-variation,
magic-number-lists, staccato runs, heading outline) — catch those by reading and
counting.

## Vocabulary & register

Word-level tells: terms large language models reach for far more often than
human writers do, and the dressed-up synonym used where a plain word is clearer.
One on its own is fine — a cluster across a few paragraphs is the signal. The
underlying problem is almost always a fancier word standing in for a plainer,
clearer one.

Audit for the _problem_, not the word. When a flagged word is genuinely the
right one, leave it.

### ai-vocabulary

High density of "AI vocabulary" — the rarer, more distinctive words LLMs
over-produce. A single use is unremarkable; a cluster gives ordinary prose a
recognizable machine "voice."

**Why it's slop:** LLMs regress toward the most statistically typical word, and
these terms are overrepresented in their training-and-feedback loop, so they
surface at an unnatural rate. They are usually a fancier word standing in for a
plain one.

**Common forms:** delve, tapestry, testament, underscore, boast(s), vibrant,
meticulous(ly), nestled, realm, intricate(ly), intricacy, showcase, pivotal,
garner, multifaceted, indelible, paradigm, synergy, holistic, transformative,
unprecedented.

- Avoid: "Let's delve into the rich tapestry of regional cuisine." / "The
  library boasts a vibrant, multifaceted collection."
- Prefer: "Let's look at the region's cuisine." / "The library has a large,
  varied collection."

### ai-vocabulary-extra

A second tier of AI vocabulary — words LLMs over-produce that are _also_ common,
ordinary English, so each hit is lower-confidence. A high density across a
passage is the signal, not one match. Expect false positives and audit lightly.

**Why it's slop:** These spiked in frequency once LLM chatbots became
widespread. Any one is unremarkable, but a cluster gives prose the same machine
voice as the rarer words.

**Common forms:** additionally, align(s) with, bolster, crucial(ly), emphasize,
enduring, enhance, foster, highlight, interplay, landscape, robust(ness),
valuable, seamless(ly), leverage, comprehensive(ly), nuanced, noteworthy,
straightforward, innovative, dynamic, navigate, resonate, embark, streamline,
spearhead, harness.

- Avoid: "Additionally, the robust pipeline enhances throughput, fostering an
  enduring, seamless landscape."
- Prefer: "The pipeline batches writes, so throughput roughly doubled."

### claude-isms

Engineering idioms and metaphors that newer coding-focused models (Claude
especially) over-produce — real terms of art pushed into heavy rotation, so this
is the highest-false-positive cluster in the skill. The signal is density and
reach: the same metaphor recurring across a document, or the jargon applied
outside its home domain ("a load-bearing paragraph"). Never flag a single, apt
use.

**Why it's slop:** These words are legitimate jargon that a model's training
loop overrepresents, so they show up at an unnatural rate and in contexts where
a plain word fits better. Overuse, not the word itself, is the tell — judge
repetition and context.

**Common forms:** load-bearing, belt-and-suspenders / belt and braces, smoking
gun, blast radius, surface (as a verb for "show" / "report"), substrate, ledger,
seam, scaffolding, gate / gated on (for a plain condition), the shape of (a
problem/change), landed (for merged or shipped), wire up / wiring, spike,
synthesize, production-ready, battle-tested.

- Avoid: "This check is load-bearing: it surfaces config errors early and gates
  the whole pipeline, so the belt-and-suspenders validation is
  production-ready."
- Prefer: "This check runs first, so a bad config fails the pipeline before any
  jobs start. The second validation in `load()` is redundant but cheap."

### honesty-signaling

"Honest," "honestly," "genuine," and "genuinely" used as recurring qualifiers —
"the honest take," "an honest assessment," "genuinely impressive."

**Why it's slop:** Claude's training vocabulary leans hard on honesty language,
so these qualifiers recur at a rate no human writer matches. They also assert
candor instead of demonstrating it: a claim isn't more true for being labeled
honest, and "genuinely" adds emphasis without evidence. Cut the qualifier or
replace it with the specific reason the claim holds. (Full staged-sincerity
constructions — "I'll be honest," "the honest answer is" — are covered under
performative-candor below.)

**Common forms:** honest(ly), genuine(ly), an honest assessment/look/answer, a
genuine result/improvement, genuinely impressive/useful/hard.

- Avoid: "Honestly, the migration was genuinely worth it — an honest assessment
  shows real gains."
- Prefer: "The migration was worth it: it cut the hosting bill by 40%."

### elevated-register

Reaching for a fancier word where a plain one is clearer: "utilize" for "use,"
"commence" for "start," "facilitate" for "help."

**Why it's slop:** Elevated register performs intelligence rather than
demonstrating it. The dressed-up synonym is longer and stiffer without being
more precise. The plain word is almost always the right one.

**Common forms:** utilize / utilization, commence(ment), facilitate, endeavor /
endeavour, ascertain, ameliorate, elucidate, cognizant, in regards to, with
regards to, pertaining to, at this juncture, in the realm of.

- Avoid: "We will utilize this library to facilitate data ingestion at this
  juncture."
- Prefer: "We use this library to load the data."

### filler-adverbs

Sentence adverbs that announce importance or emphasis without earning it.

**Why it's slop:** These adverbs assert that what follows matters instead of
showing why. If the sentence still reads correctly with the adverb deleted, it
was empty throat-clearing — and LLMs sprinkle them in reflexively, especially at
the start of a sentence.

**Common forms:** importantly, essentially, fundamentally, ultimately,
inherently, notably, crucially, tellingly, undeniably, undoubtedly,
unsurprisingly, interestingly, markedly, remarkably.

- Avoid: "Importantly, the cache is fundamentally a performance optimization."
- Prefer: "The cache is a performance optimization."

### metaphor-crutch

Predictable, off-the-shelf metaphors used as filler.

**Why it's slop:** These images are so worn they carry no concrete picture
anymore — they're decoration standing in for a specific point, and LLMs reach
for the same dozen reflexively. Either find a precise image from the actual
subject or say the thing plainly.

**Common forms:** double-edged sword, tip of the iceberg, north star, game
changer, paradigm shift, silver bullet, move the needle, think outside the box,
low-hanging fruit, deep dive, boil the ocean, circle back, hit the ground
running, the devil is in the details, reinvent the wheel, best of breed,
bleeding edge, elephant in the room, perfect storm, secret sauce, moving parts.

- Avoid: "Caching is a double-edged sword, but it's the low-hanging fruit that
  will move the needle."
- Prefer: "Caching cut p99 latency in half, at the cost of stale reads for up to
  60 seconds."

## Inflated significance & puffery

Prose that _asserts_ importance, value, or impact instead of demonstrating it —
telling the reader something matters rather than giving the specific facts that
would let them judge for themselves. The phrasing is generic enough to attach to
almost any topic, which is exactly why it reads as filler.

Fix the underlying problem: replace the puffery with the specific fact it was
standing in for, or cut it. Removing the trigger word while leaving the empty
claim intact just makes the slop harder to spot.

### undue-emphasis-significance

Canned statements that inflate the importance, legacy, or broader significance
of the subject, often bolted onto otherwise mundane facts.

**Why it's slop:** LLMs puff up subjects by asserting significance instead of
demonstrating it — "stands as a testament," "plays a vital role" — rather than
giving the facts that would let the reader judge.

**Common forms:** stands as a/the, serves as a testament, is/are a testament to,
plays a vital/crucial/pivotal/significant/key/central role, pivotal moment,
turning point, indelible mark, enduring/lasting legacy, rich cultural
heritage/history/tradition, underscores the importance / its significance,
highlights the importance, reflects/part of a broader, broader/wider
implications, setting the stage for, cementing its, solidifying its
role/position/place.

- Avoid: "The bridge stands as a testament to the town's enduring legacy."
- Prefer: "The bridge, built in 1890, is the oldest crossing on the river."

### avoidance-of-copulatives

Replacing a plain "is" / "are" / "has" with an inflated linking verb to dress up
a simple statement of fact.

**Why it's slop:** LLMs systematically dodge the neutral copula in favor of
marketing-flavored verbs, which nudges factual prose toward puffery. The plain
verb is almost always clearer and shorter.

**Common forms:** serves as a/the, represents a/the, acts/functions/stands as
a/the, features a/an, offers a/an, maintains a/an, is home to, plays host to.

- Avoid: "The module serves as the entry point and features four configuration
  options."
- Prefer: "The module is the entry point. It has four configuration options."

### superficial-participle-analysis

A trailing present-participle ("-ing") clause bolted onto a factual sentence
that editorializes about significance, role, or impact instead of stating
anything verifiable.

**Why it's slop:** The participle adds no facts — just a generic value judgment
that could be pasted onto almost any sentence.

**Common forms:** a trailing ", highlighting / underscoring / emphasizing /
showcasing / reflecting / symbolizing / cementing / embodying / encapsulating /
demonstrating / illustrating / reinforcing / signaling / representing
its/the/their..."; ", contributing to / serving as / further enhancing / helping
to / allowing it to / making it..."; ", ensuring..."

- Avoid: "The service caches responses for 60 seconds, ensuring optimal
  performance and reliability."
- Prefer: "The service caches responses for 60 seconds, which cut median latency
  from 200ms to 40ms."

### manufactured-discourse

Claims that the subject has "sparked debate," "raised questions," or "prompted
reflection" about broad abstract themes, with no specific source for the
supposed discourse.

**Why it's slop:** The "debate" is unattributed and exists mainly to make the
subject sound consequential.

**Common forms:** has generated/sparked/ignited/fueled
debate/discussion/controversy about/around/over; raises important/profound/
broader questions about; prompted broader/deeper reflection; shaped emerging.

- Avoid: "The feature has sparked debate about privacy, ownership, and the
  future of the web."
- Prefer: "A 2025 EFF post criticized the feature's default data-sharing
  setting."

### promotional-puffery

Travel-brochure or press-release tone applied to a neutral subject.

**Why it's slop:** Even when asked for neutral prose, LLMs drift into
advertisement-like writing, reusing the same promotional adjectives regardless
of topic. It signals marketing copy rather than informative documentation.

**Common forms:** in the heart of, a diverse array/range/variety of, rich
cultural heritage, breathtaking, gateway to, worth a visit, natural beauty,
cutting-edge, state-of-the-art, world-class, seamlessly integrates, picturesque,
hidden gem, must-see / must-visit, stunning.

- Avoid: "This cutting-edge, world-class framework offers a diverse array of
  powerful features."
- Prefer: "The framework includes routing, templating, and an ORM."

### press-release-commitment

Prose that frames an organization or project as expressing a "commitment to,"
"dedication to," or "focus on" virtuous goals like quality, innovation,
excellence, or community.

**Why it's slop:** LLMs echo self-congratulatory PR language. Attributing lofty
commitments to a project is unverifiable framing, not fact, and reads as ad
copy.

**Common forms:** commitment to
excellence/quality/innovation/sustainability/diversity/safety/the community,
dedication/dedicated to, focuses on delivering, strives to
deliver/provide/offer, dedicated to providing, proud to
announce/present/offer/introduce, passionate about.

- Avoid: "The team's commitment to excellence and dedication to quality drive
  every release."
- Prefer: "The team runs the full test suite and a security review before each
  release."

### invented-concept-label

A coined analytical term — a noun plus an abstract suffix used as if it were an
established concept.

**Why it's slop:** Branding a phenomenon with a coined label makes shallow
observation sound like theory. The label rarely refers to anything established;
it's inflation. Describe the phenomenon plainly or use its real name.

**Common forms:** "the [adjective/noun] paradox / trap / vacuum / inversion /
chasm / creep / fallacy / illusion / mirage / trifecta" — e.g. "the attention
paradox," "the trust vacuum," "the productivity trap."

- Avoid: "This is the classic attention paradox: more features, less focus."
- Prefer: "Adding features kept users in the app longer but lowered
  task-completion rates."

## Hollow rhetorical constructions

Sentence-shape tells: constructions that manufacture profundity, drama, or
engagement without adding information. Used once, most are fine; LLMs reach for
them reflexively, especially in openers, taglines, and conclusions. Delete the
construction and state the point.

### not-just-but

The "not just X — it's Y" antithesis construction, and its cousins ("not
merely," "isn't just," "more than just," "not only ... but also").

**Why it's slop:** This negation-then-elevation pattern manufactures profundity
by denying a modest framing and substituting a grander one, usually without
adding information.

**Common forms:** not just a/an/the/about, is/it's not just/merely, isn't
just/merely, more than just/merely/simply, not only.

- Avoid: "The Miata isn't just a car — it's a canvas for self-expression."
- Prefer: "The Miata is a lightweight, affordable sports car popular with
  tuners."

### not-x-but-y

The negative-parallelism reversal "not X, but (rather) Y" — denying the first
framing outright and substituting a grander or "corrected" one. Distinct from
not-just-but, which _adds_ to X rather than negating it.

**Why it's slop:** LLMs reach for this reversal to sound insightful or to
"correct" an assumed misconception, usually without adding information.

**Common forms:** but rather; rather, it is/represents/reflects; it
is/isn't/it's not about; ", not just/merely/simply
a/an/the/for/with/to/about..."

- Avoid: "The repository is not a database, but rather a single source of
  truth."
- Prefer: "The repository stores configuration as the single source of truth."

### hollow-from-construction

Empty "from X to Y" range framing where X and Y aren't on a real spectrum, and
the clichéd idiom "doesn't come / emerge from nowhere."

**Why it's slop:** "From X to Y" implies a meaningful scale; LLMs use it to
dress up a list of two loosely related things. "Doesn't emerge from nowhere"
gestures at causation without naming a cause. The general "from X to Y" misuse
needs your judgment — say what you mean directly.

**Common forms:** doesn't/didn't/does not/did not
emerge/come/appear/spring/arise/materialize/happen from nowhere;
emerged/came/appeared/sprang/arose from nowhere; "from X to Y" where X and Y
aren't really a spectrum.

- Avoid: "This bug didn't emerge from nowhere — it came from a race condition."
- Prefer: "This bug comes from a race condition between the writer and the
  reaper thread."

### formulaic-openers

Stock essay openers that stall before reaching the point.

**Why it's slop:** These framing clauses set a grand, generic scene that could
precede almost any topic and add no information. The real sentence starts after
the comma. Delete the clause and begin at the point.

**Common forms:** "In an era of/where/when...", "In a world
where/of/increasingly...", "In today's / our fast-paced / modern / digital /
ever-changing...", "Imagine a world/future/scenario where...", "Imagine if you /
what would / being able to..."

- Avoid: "In an era of rapid change, companies must adapt to survive." /
  "Imagine a world where every API just worked."
- Prefer: "Companies that batch their deploys ship 30% fewer regressions."

### false-conclusion

High-school-essay conclusion signposts that announce a wrap-up instead of
delivering one.

**Why it's slop:** A conclusion should land through its content, not be flagged
with a signpost. If you need to write "to sum up," the summary that follows
usually adds nothing the body didn't already establish.

**Common forms:** at the end of the day, all in all, to sum up, in summary, to
summarize, all things considered, when all is said and done, in the final
analysis, the bottom line is.

- Avoid: "At the end of the day, all things considered, the migration was worth
  it."
- Prefer: "The migration cut our hosting bill by 40% and took three weeks."

### false-suspense-transition

Manufactured-suspense transitions that promise a payoff.

**Why it's slop:** These tee up a reveal to create false drama, padding the
prose with a beat of suspense instead of just stating the point. It's a
content-marketing tic. Delete the transition and make the statement.

**Common forms:** here's the kicker/thing/catch/twist/secret/deal/problem/rub,
here's where it gets interesting/tricky/good/complicated, here's what most
people miss / nobody tells you, but here's the..., plot twist.

- Avoid: "The benchmark looked great. But here's the kicker: it ran on cached
  data."
- Prefer: "The benchmark ran on cached data, so the 10x speedup doesn't reflect
  production."

### pedagogical-framing

Teacher-mode preambles that announce an explanation instead of giving it.

**Why it's slop:** The reader doesn't need to be managed into the explanation —
these preambles delay the content and adopt a chatbot's instructional tone. Skip
the preamble and explain the thing directly.

**Common forms:** let's break this/it down, let's unpack, let's dive/dig in,
let's explore/examine, think of it/this as/like, at its core, the beauty of
this/it is, this begs the question.

- Avoid: "Let's unpack this. Think of it as a pipeline, and at its core it's
  just a queue."
- Prefer: "The system is a queue: producers append jobs, workers pull them in
  order."

### performative-candor

Staged sincerity that performs honesty or emotion rather than being it.

**Why it's slop:** Genuine candor is specific and a little uncomfortable; the
polished, risk-free version is a verbal flourish that signals authenticity
without carrying any. Generic empathy applicable to any situation is
indistinguishable from none. The "honest caveat/answer/take" framing is a strong
Claude-specific tell, as is the staged mea culpa ("The honest take: I was
wrong").

**Common forms:** I'll be honest, let's be real/honest, to be
honest/real/frank/fair (with you/here), I'm not gonna lie, the honest
answer/take/caveat/assessment is, one honest caveat, the honest answer starts
with, I understand this/that/how/your..., your feelings are valid, I'm sorry to
hear.

- Avoid: "I'll be honest, this is a tough problem, and I understand how
  frustrating it can be."
- Prefer: "This is a tough problem because the deadlock only appears under load
  above 5k RPS."

### question-then-answer

A rhetorical question immediately answered by its own next sentence.

**Why it's slop:** The self-answered question manufactures engagement and pads
the prose with a beat that adds nothing — just state the point. LLMs lean on it
as an explanatory tic, especially to open sections. Catch this by reading: a
question followed by a short answering sentence in the same paragraph.

- Avoid: "So what does this actually do? It deduplicates the queue."
- Prefer: "This deduplicates the queue."

## Sourcing, hedging & chatbot residue

Tells about _honesty_ and _provenance_: claims laundered through a vague
authority, breadth overstated, epistemic limits narrated instead of resolved,
templates left unfilled, hedges stacked to dodge commitment, and leftover chat-
session correspondence. Several of these (placeholders, cutoff disclaimers,
chatbot talk) are near-unambiguous signs of pasted, unreviewed output.

When a fix needs a fact you don't have, flag it for the user rather than
inventing content.

### vague-attribution-weasel

Opinions or claims pinned on an unnamed authority.

**Why it's slop:** LLMs launder unsupported claims through a vague collective
authority. Without a named source the attribution is unfalsifiable and inflates
how widely a view is actually held.

**Common forms:** experts/analysts/observers/critics/scientists/researchers
argue/say/note/suggest/believe/claim/contend/point out; many/some/several/most
experts; according to experts/analysts/sources/some;
studies/research/data/evidence show/suggest/indicate/reveal; it is
widely/generally/commonly/often regarded/considered/believed/accepted/known; is
widely regarded/seen as; industry reports/analysts/sources/experts; many
believe.

- Avoid: "Experts agree this is the most efficient approach available." /
  "Studies show that developers prefer this pattern."
- Prefer: "A 2024 benchmark by the maintainers measured it as 3x faster than the
  prior approach."

### exaggerated-source-quantity

Phrasing that implies many sources or examples when only one or two are given.

**Why it's slop:** LLMs overstate breadth, presenting one or two instances as an
open-ended set or broad consensus. It makes coverage or support look more
established than it is.

**Common forms:**
tools/libraries/frameworks/platforms/languages/companies/options/features such
as; a wide/broad/vast/diverse/growing range/variety/array/number of; a number
of; numerous; among/and many others/more; a host/plethora/myriad/multitude of;
countless.

- Avoid: "Numerous libraries such as Foo and Bar support this out of the box."
- Prefer: "Two libraries support this out of the box: Foo and Bar."

### knowledge-cutoff-disclaimer

Hedges that information may be outdated because of a training cutoff, or
speculation that facts are "not well documented" followed by a guess at what
they "likely" are.

**Why it's slop:** Documentation should state facts, not narrate a model's
epistemic limits. A cutoff disclaimer is a direct LLM giveaway, and "not widely
documented" hedges frequently precede fabricated or inferred content. Verify the
fact or cut the sentence.

**Common forms:** as of my last/knowledge/most recent..., up to my last..., as
an AI (language model), I don't/cannot have specific/real-time
information/data/access, while specific details/information about..., in the
provided/available/given sources/text/context/search results, in the search
results, not widely/extensively/well documented, is likely, it is believed that,
knowledge cutoff, my training data.

- Avoid: "While specific details about the rate limit are not widely documented,
  it is likely around 1000 req/min."
- Prefer: "The rate limit is 1000 requests per minute."

### placeholder-text

Fill-in-the-blank templates and bracketed placeholders the author never
replaced.

**Why it's slop:** Unfilled placeholders are an unambiguous sign of pasted,
unreviewed output: the model produced a Mad-Libs template for a human to
complete and nobody did. They must be filled in or removed before publishing.

**Common forms:** [insert ...], [describe ...], [your name], [link to ...],
[date], [company name], TBD, to be added/determined/filled in. Also catch
underscored ALL-CAPS placeholders like `INSERT_URL_30` by eye.

- Avoid: "Contact the maintainer at [Your Name] for access." / "Default timeout:
  TBD."
- Prefer: "Contact the maintainer at jdoe@example.com for access."

### chatbot-collaborative-talk

Conversational meta-commentary aimed at a human chat partner rather than the
reader: offers of further help, sign-offs, pleasantries, sycophantic openers,
and explicit narration of producing the document.

**Why it's slop:** This is leftover chat-session correspondence that leaked into
the published text. It addresses a "user" who doesn't exist for a document
reader, adds no information, and is a clear sign of copy-pasted output. Almost
always it should simply be deleted.

**Common forms:** I hope this helps, hope this helps, would you like me to, is
there anything else, let me know if, feel free to, you're absolutely right,
great/excellent/good question, "in this article/post/guide we will...", "we'll
explore/discuss/examine/cover/dive into...", "as we've seen/discussed...", in
conclusion.

- Avoid: "The function returns a sorted list. Would you like me to explain the
  algorithm?"
- Prefer: "The function returns a sorted list."

### almost-hedge

Hedging an absolute with "almost."

**Why it's slop:** "Almost always" dodges commitment without adding precision —
either say "usually" or commit to "always" and defend it. LLMs hedge this way to
avoid being pinned down, and readers notice the evasion.

**Common forms:** almost
always/never/certainly/exclusively/entirely/completely/invariably/universally.

- Avoid: "This is almost always the fastest option, and it almost never fails."
- Prefer: "This is usually the fastest option. It has failed twice in three
  years."

### hedge-stacking

Several epistemic hedges piled into one sentence — "perhaps," "arguably," "it
could be argued that this might possibly..."

**Why it's slop:** One hedge can be honest calibration; three or four in a
sentence communicate nothing and signal a model dodging any falsifiable claim.
Keep at most one genuine hedge, or commit to the claim. Catch this by reading:
two or more hedges in a single sentence ("should" / "would" don't count).

- Avoid: "It could perhaps be argued that this might, in some sense, be seen as
  a possibly suboptimal choice."
- Prefer: "This is the wrong choice here: it doubles write latency for a feature
  few users hit."

## Formulaic structure & rhythm

Tells that live in the _shape_ of the text rather than any single phrase: a
rigid template arc, connective tissue asserted instead of built, and rhythms
(triplets, round-number lists, clipped bursts, repeated openers) applied so
consistently they read as generated rather than composed. Most of these have no
reliable single-phrase signal — catch them by reading the passage as a whole and
counting.

### challenges-and-future-outline

A formulaic closing: "Despite [positive], X faces challenges, including ...",
followed by vague optimism or speculation about future prospects — often under a
"Challenges" or "Future Directions" heading.

**Why it's slop:** LLMs default to a rigid template that pads documents with a
generic challenges-then-optimism arc. The challenges lack specifics and the
conclusion is empty reassurance. The tell is the _formula_, not the mere mention
of a challenge.

**Common forms:** faces several/numerous/many challenges, despite these/its
challenges/obstacles/limitations, despite its success, presents its own
challenges, "challenges and future," future
directions/outlook/prospects/possibilities, continues to
thrive/evolve/grow/expand, looking ahead, remains to be seen, only time will
tell.

- Avoid: "Despite its success, the library faces challenges, including
  dependency bloat. Looking ahead, future improvements could enhance
  performance."
- Prefer: "The library pulls in 40 transitive dependencies, which slows cold
  installs; issue #212 tracks trimming them."

### transitional-connectors

Overused formal connectives deployed to glue paragraphs together.

**Why it's slop:** Well-ordered ideas connect through their content; a pile of
"Furthermore / Moreover" signposts is a tell that the connective tissue is being
asserted rather than built. One is fine — a document where every paragraph opens
with one reads as machine-assembled. (Common mid-sentence too, so confirm it's
doing throat-clearing work before cutting.)

**Common forms:** furthermore, moreover, nevertheless, nonetheless,
consequently, conversely.

- Avoid: "Furthermore, the API is fast. Moreover, it is reliable. Nevertheless,
  it has limits."
- Prefer: "The API handles 10k requests/sec and recovers from a node failure in
  five seconds."

### rule-of-three

Reflexive triadic phrasing — "adjective, adjective, and adjective," or three
parallel clauses — applied so consistently that nearly every list lands on
exactly three items. Audit-only: no reliable single-phrase signal.

**Why it's slop:** LLMs overuse the rule of three to make shallow content look
thorough and balanced. When almost every enumeration is a tidy triplet, the
rhythm reads as formulaic, and padding to three often forces a vague or
redundant third item.

- Avoid: "It is fast, reliable, and scalable, empowering teams to build, ship,
  and grow."
- Prefer: "It handles ~10k requests/sec and recovers from node failure within 5
  seconds."

### elegant-variation

Needlessly swapping synonyms or rephrased noun phrases for the same referent
across nearby sentences ("the function" → "this routine" → "the helper" → "said
method"). Audit-only: no reliable single-phrase signal.

**Why it's slop:** A repetition penalty pushes models to avoid reusing a word,
producing a string of paraphrases for one concept. In technical writing this is
actively harmful: the reader can't tell whether the varied terms denote the same
thing or different things. Repeat the precise term instead.

- Avoid: "Call the parser. This component reads the file; said utility then
  validates the routine's output."
- Prefer: "Call the parser. The parser reads the file, then validates its
  output."

### staccato-and-fragments

Bursts of very short sentences or one-to-four-word standalone paragraphs used
for dramatic emphasis — "It works. Every time. Guaranteed." — and the
short-punchy-opener-then-long-elaboration rhythm. Catch by reading: runs of
three or more consecutive sentences of six words or fewer, and lone dramatic
fragments as their own paragraph.

**Why it's slop:** A run of clipped sentences is a manufactured-drama cadence
common in LLM content writing. Used once for effect it's fine; as a recurring
rhythm it reads as a list of bullet points in disguise. Vary sentence length and
let ideas develop.

- Avoid: "The result was clear. It worked. Every time. No exceptions."
- Prefer: "The change passed every test run, including the three that previously
  flaked under load."

### repetitive-sentence-openers

Mechanical structural repetition across consecutive sentences: the same opener
three times running (anaphora), a run of short "-ing" fragments, "Not X. Not Y.
Just Z.", or ordinal prose disguising a list ("The first... The second... The
third..."). Catch by reading.

**Why it's slop:** Repeating a sentence frame more than twice turns a rhetorical
device into a tic, and ordinal "first/second/third" prose is usually a list
wearing a trench coat. The uniform cadence reads as generated. Vary the
structure, or use a real list where a list is what you have.

- Avoid: "It scales. It adapts. It endures. The first benefit is speed. The
  second is cost."
- Prefer: "It scales to 10k RPS and costs about $40/month at that load."

### magic-number-lists

Bullet or numbered lists that land on exactly 3, 5, 7, or 10 items so
consistently it looks templated, regardless of how many the topic actually has.
Audit-only: list length needs your count.

**Why it's slop:** LLMs gravitate to these "round" list lengths, padding to
reach one or trimming to fit it. A list should have the number of items the
subject actually has — four, six, nine — not a number chosen for shape.

- Avoid: "There are 5 reasons to adopt this: [three solid points and two padded
  ones]."
- Prefer: "There are two reasons to adopt this: it halves latency and removes
  the cron job."

## Formatting & typography

Tells that live in the Markdown source and character choices rather than the
prose: decorative formatting, mechanical structure, and stray characters that
betray pasted chatbot output. Each is weak on its own — Word, macOS, and house
styles produce some legitimately — so read them as signals alongside the prose
tells, not proof. Several are best caught by scanning the raw source and the
heading outline.

### title-case-headings

Headings that Capitalize Every Major Word instead of using sentence case.

**Why it's slop:** Blanket title case across every heading is a decorative habit
from slide decks and marketing copy. Most documentation house styles use
sentence case, so title-casing every heading reads as machine-generated. A
high-confidence tell is a capitalized minor word mid-heading ("With," "The,"
"And"); catch title case without one by reading.

- Avoid: "## Getting Started With The Configuration File"
- Prefer: "## Getting started with the configuration file"

### overuse-of-boldface

Mechanical, scattered boldface — multiple bolded phrases per paragraph, or every
instance of a term bolded — rather than reserving bold for a term's first
definition.

**Why it's slop:** Emphasizing many phrases adds no information and dilutes real
emphasis. It mimics listicle and sales-pitch formatting. Catch by reading: prose
paragraphs with three or more bold spans, or a term bolded on every occurrence.

- Avoid: "A **leveraged buyout** uses **debt financing** so **firms** can
  control **cash flows**."
- Prefer: "A leveraged buyout uses debt financing so firms can control a
  company's cash flows."

### inline-header-lists

Vertical lists where every item is a short bold header, a colon, then a sentence
("- **Performance:** It is faster."), repeated down the whole list — or literal
"•" bullet characters pasted into Markdown source.

**Why it's slop:** The uniform bold-header-colon-sentence structure repeated for
every item is a hallmark of LLM output imitating feature grids, and often
replaces prose that would read more naturally. A raw "•" in Markdown source
(rather than "-" / "*") is itself a paste-from-chatbot tell.

**Common forms:** a literal `•` bullet character; `**Bold header:**` followed by
a sentence, repeated for every list item.

- Avoid: "- **Speed:** It is faster. / - **Cost:** It is cheaper. / - **Size:**
  It is smaller."
- Prefer: "It is faster, cheaper, and smaller than the previous version."

### overuse-of-em-dashes

Em dashes (—) and en dashes (–) used far more often than the genre warrants,
especially to punch up parallel clauses where a comma, colon, or parentheses
would do.

**Why it's slop:** Strongly associated with LLM output. Repeated em dashes
setting off dramatic asides or "not X — but Y" parallelisms read as sales
flourish. Best read as a signal alongside other tells, not on its own.

**Common forms:** the characters `—` and `–`, especially several within a short
passage.

- Avoid: "The result is clear — and it changes everything — for how we deploy."
- Prefer: "The result is clear, and it changes how we deploy."

### unicode-decoration

Decorative non-text Unicode used as shorthand in prose: arrow characters (→ ⇒ ➜)
standing in for "leads to" / "produces," and ornamental symbols pasted as
bullets or emphasis.

**Why it's slop:** An arrow in running prose is a shorthand the writer didn't
expand. It's common in chatbot output but reads as half-finished in published
text. Write out the relationship.

**Common forms:** the characters `→ ⇒ ➜ ➔` in running prose.

- Avoid: "Request → validation → handler → response."
- Prefer: "A request is validated, passed to the handler, and turned into a
  response."

### curly-quotes

Curly/typographic quotation marks (“ ”) and apostrophes (‘ ’) where straight
ones (" ') are expected, especially mixed inconsistently.

**Why it's slop:** ChatGPT and some models default to curly marks, often
inconsistently. In technical docs, code, and config the distinction matters and
straight marks are expected, so stray curly marks suggest pasted LLM output. Not
proof on its own — Word, macOS, and Chicago style produce them legitimately.
Curly double quotes are the clearer tell; curly apostrophes are too common to
flag mechanically, so scan for those by eye.

- Avoid: Set the “name” field and don’t forget the ‘id’.
- Prefer: Set the "name" field and don't forget the 'id'.

### unusual-tables

Tiny tables holding only a couple of facts (a two-row "Metric / Value" grid)
that would read more naturally as a sentence or inline list. Catch by reading:
Markdown tables with two or fewer data rows.

**Why it's slop:** LLMs reach for tables to make sparse content look structured.
A two- or three-row table adds formatting overhead without helping the reader;
prose serves better.

- Avoid: "| Metric | Value | / | --- | --- | / | Latency | ~40ms |"
- Prefer: "Median latency is about 40ms."

### skipping-heading-levels

A heading hierarchy that skips a level (e.g. "#" straight to "###"), or a
document whose sections start at level 3 with no level-2 headings. Catch by
reading the heading outline.

**Why it's slop:** LLMs tend to start sections at the third heading level and
skip the second. It breaks the document outline and accessibility conventions,
and a hand-formatted page rarely has this quirk.

- Avoid: "# Overview / ### Installation"
- Prefer: "# Overview / ## Installation"

### thematic-breaks-before-headings

A horizontal rule (---, ----, ***) inserted before each heading throughout a
document, ruling off every section. Catch by reading: a horizontal rule whose
next non-blank line is a heading, repeated throughout.

**Why it's slop:** Raw Markdown from chatbots often places a rule before each
heading. Headings already separate sections, so the extra rules are redundant
machine formatting that human authors rarely add.

- Avoid: "...end of section. / ---- / ## History"
- Prefer: "...end of section. / ## History"
