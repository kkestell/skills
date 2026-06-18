# Inflated significance & puffery

Prose that *asserts* importance, value, or impact instead of demonstrating it — telling the reader something matters rather than giving the specific facts that would let them judge for themselves. The phrasing is generic enough to attach to almost any topic, which is exactly why it reads as filler.

Fix the underlying problem: replace the puffery with the specific fact it was standing in for, or cut it. Removing the trigger word while leaving the empty claim intact just makes the slop harder to spot.

---

## undue-emphasis-significance

Canned statements that inflate the importance, legacy, or broader significance of the subject, often bolted onto otherwise mundane facts.

**Why it's slop:** LLMs puff up subjects by asserting significance instead of demonstrating it — "stands as a testament," "plays a vital role" — rather than giving the facts that would let the reader judge.

**Common forms:** stands as a/the, serves as a testament, is/are a testament to, plays a vital/crucial/pivotal/significant/key/central role, pivotal moment, turning point, indelible mark, enduring/lasting legacy, rich cultural heritage/history/tradition, underscores the importance / its significance, highlights the importance, reflects/part of a broader, broader/wider implications, setting the stage for, cementing its, solidifying its role/position/place.

- Avoid: "The bridge stands as a testament to the town's enduring legacy."
- Prefer: "The bridge, built in 1890, is the oldest crossing on the river."

---

## avoidance-of-copulatives

Replacing a plain "is" / "are" / "has" with an inflated linking verb to dress up a simple statement of fact.

**Why it's slop:** LLMs systematically dodge the neutral copula in favor of marketing-flavored verbs, which nudges factual prose toward puffery. The plain verb is almost always clearer and shorter.

**Common forms:** serves as a/the, represents a/the, acts/functions/stands as a/the, features a/an, offers a/an, maintains a/an, is home to, plays host to.

- Avoid: "The module serves as the entry point and features four configuration options."
- Prefer: "The module is the entry point. It has four configuration options."

---

## superficial-participle-analysis

A trailing present-participle ("-ing") clause bolted onto a factual sentence that editorializes about significance, role, or impact instead of stating anything verifiable.

**Why it's slop:** The participle adds no facts — just a generic value judgment that could be pasted onto almost any sentence.

**Common forms:** a trailing ", highlighting / underscoring / emphasizing / showcasing / reflecting / symbolizing / cementing / embodying / encapsulating / demonstrating / illustrating / reinforcing / signaling / representing its/the/their..."; ", contributing to / serving as / further enhancing / helping to / allowing it to / making it..."; ", ensuring..."

- Avoid: "The service caches responses for 60 seconds, ensuring optimal performance and reliability."
- Prefer: "The service caches responses for 60 seconds, which cut median latency from 200ms to 40ms."

---

## manufactured-discourse

Claims that the subject has "sparked debate," "raised questions," or "prompted reflection" about broad abstract themes, with no specific source for the supposed discourse.

**Why it's slop:** The "debate" is unattributed and exists mainly to make the subject sound consequential.

**Common forms:** has generated/sparked/ignited/fueled debate/discussion/controversy about/around/over; raises important/profound/broader questions about; prompted broader/deeper reflection; shaped emerging.

- Avoid: "The feature has sparked debate about privacy, ownership, and the future of the web."
- Prefer: "A 2025 EFF post criticized the feature's default data-sharing setting."

---

## promotional-puffery

Travel-brochure or press-release tone applied to a neutral subject.

**Why it's slop:** Even when asked for neutral prose, LLMs drift into advertisement-like writing, reusing the same promotional adjectives regardless of topic. It signals marketing copy rather than informative documentation.

**Common forms:** in the heart of, a diverse array/range/variety of, rich cultural heritage, breathtaking, gateway to, worth a visit, natural beauty, cutting-edge, state-of-the-art, world-class, seamlessly integrates, picturesque, hidden gem, must-see / must-visit, stunning.

- Avoid: "This cutting-edge, world-class framework offers a diverse array of powerful features."
- Prefer: "The framework includes routing, templating, and an ORM."

---

## press-release-commitment

Prose that frames an organization or project as expressing a "commitment to," "dedication to," or "focus on" virtuous goals like quality, innovation, excellence, or community.

**Why it's slop:** LLMs echo self-congratulatory PR language. Attributing lofty commitments to a project is unverifiable framing, not fact, and reads as ad copy.

**Common forms:** commitment to excellence/quality/innovation/sustainability/diversity/safety/the community, dedication/dedicated to, focuses on delivering, strives to deliver/provide/offer, dedicated to providing, proud to announce/present/offer/introduce, passionate about.

- Avoid: "The team's commitment to excellence and dedication to quality drive every release."
- Prefer: "The team runs the full test suite and a security review before each release."

---

## invented-concept-label

A coined analytical term — a noun plus an abstract suffix used as if it were an established concept.

**Why it's slop:** Branding a phenomenon with a coined label makes shallow observation sound like theory. The label rarely refers to anything established; it's inflation. Describe the phenomenon plainly or use its real name.

**Common forms:** "the [adjective/noun] paradox / trap / vacuum / inversion / chasm / creep / fallacy / illusion / mirage / trifecta" — e.g. "the attention paradox," "the trust vacuum," "the productivity trap."

- Avoid: "This is the classic attention paradox: more features, less focus."
- Prefer: "Adding features kept users in the app longer but lowered task-completion rates."
