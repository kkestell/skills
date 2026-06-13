# Vocabulary & register

Word-level tells: terms large language models reach for far more often than human writers do, and the dressed-up synonym used where a plain word is clearer. One on its own is fine — a cluster across a few paragraphs is the signal. The underlying problem is almost always a fancier word standing in for a plainer, clearer one.

Audit for the *problem*, not the word. When a flagged word is genuinely the right one, leave it.

---

## ai-vocabulary

High density of "AI vocabulary" — the rarer, more distinctive words LLMs over-produce. A single use is unremarkable; a cluster gives ordinary prose a recognizable machine "voice."

**Why it's slop:** LLMs regress toward the most statistically typical word, and these terms are overrepresented in their training-and-feedback loop, so they surface at an unnatural rate. They are usually a fancier word standing in for a plain one.

**Common forms:** delve, tapestry, testament, underscore, boast(s), vibrant, meticulous(ly), nestled, realm, intricate(ly), intricacy, showcase, pivotal, garner, multifaceted, indelible, paradigm, synergy, holistic, transformative, unprecedented.

- Avoid: "Let's delve into the rich tapestry of regional cuisine." / "The library boasts a vibrant, multifaceted collection."
- Prefer: "Let's look at the region's cuisine." / "The library has a large, varied collection."

---

## ai-vocabulary-extra

A second tier of AI vocabulary — words LLMs over-produce that are *also* common, ordinary English, so each hit is lower-confidence. A high density across a passage is the signal, not one match. Expect false positives and audit lightly.

**Why it's slop:** These spiked in frequency once LLM chatbots became widespread. Any one is unremarkable, but a cluster gives prose the same machine voice as the rarer words.

**Common forms:** additionally, align(s) with, bolster, crucial(ly), emphasize, enduring, enhance, foster, highlight, interplay, landscape, robust(ness), valuable, seamless(ly), leverage, comprehensive(ly), nuanced, noteworthy, straightforward, innovative, dynamic, navigate, resonate, embark, streamline, spearhead, harness.

- Avoid: "Additionally, the robust pipeline enhances throughput, fostering an enduring, seamless landscape."
- Prefer: "The pipeline batches writes, so throughput roughly doubled."

---

## elevated-register

Reaching for a fancier word where a plain one is clearer: "utilize" for "use," "commence" for "start," "facilitate" for "help."

**Why it's slop:** Elevated register performs intelligence rather than demonstrating it. The dressed-up synonym is longer and stiffer without being more precise. The plain word is almost always the right one.

**Common forms:** utilize / utilization, commence(ment), facilitate, endeavor / endeavour, ascertain, ameliorate, elucidate, cognizant, in regards to, with regards to, pertaining to, at this juncture, in the realm of.

- Avoid: "We will utilize this library to facilitate data ingestion at this juncture."
- Prefer: "We use this library to load the data."

---

## filler-adverbs

Sentence adverbs that announce importance or emphasis without earning it.

**Why it's slop:** These adverbs assert that what follows matters instead of showing why. If the sentence still reads correctly with the adverb deleted, it was empty throat-clearing — and LLMs sprinkle them in reflexively, especially at the start of a sentence.

**Common forms:** importantly, essentially, fundamentally, ultimately, inherently, notably, crucially, tellingly, undeniably, undoubtedly, unsurprisingly, interestingly, markedly, remarkably.

- Avoid: "Importantly, the cache is fundamentally a performance optimization."
- Prefer: "The cache is a performance optimization."

---

## metaphor-crutch

Predictable, off-the-shelf metaphors used as filler.

**Why it's slop:** These images are so worn they carry no concrete picture anymore — they're decoration standing in for a specific point, and LLMs reach for the same dozen reflexively. Either find a precise image from the actual subject or say the thing plainly.

**Common forms:** double-edged sword, tip of the iceberg, north star, game changer, paradigm shift, silver bullet, move the needle, think outside the box, low-hanging fruit, deep dive, boil the ocean, circle back, hit the ground running, the devil is in the details, reinvent the wheel, best of breed, bleeding edge, elephant in the room, perfect storm, secret sauce, moving parts.

- Avoid: "Caching is a double-edged sword, but it's the low-hanging fruit that will move the needle."
- Prefer: "Caching cut p99 latency in half, at the cost of stale reads for up to 60 seconds."
