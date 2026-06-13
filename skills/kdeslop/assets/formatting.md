# Formatting & typography

Tells that live in the Markdown source and character choices rather than the prose: decorative formatting, mechanical structure, and stray characters that betray pasted chatbot output. Each is weak on its own — Word, macOS, and house styles produce some legitimately — so read them as signals alongside the prose tells, not proof. Several are best caught by scanning the raw source and the heading outline.

---

## title-case-headings

Headings that Capitalize Every Major Word instead of using sentence case.

**Why it's slop:** Blanket title case across every heading is a decorative habit from slide decks and marketing copy. Most documentation house styles use sentence case, so title-casing every heading reads as machine-generated. A high-confidence tell is a capitalized minor word mid-heading ("With," "The," "And"); catch title case without one by reading.

- Avoid: "## Getting Started With The Configuration File"
- Prefer: "## Getting started with the configuration file"

---

## overuse-of-boldface

Mechanical, scattered boldface — multiple bolded phrases per paragraph, or every instance of a term bolded — rather than reserving bold for a term's first definition.

**Why it's slop:** Emphasizing many phrases adds no information and dilutes real emphasis. It mimics listicle and sales-pitch formatting. Catch by reading: prose paragraphs with three or more bold spans, or a term bolded on every occurrence.

- Avoid: "A **leveraged buyout** uses **debt financing** so **firms** can control **cash flows**."
- Prefer: "A leveraged buyout uses debt financing so firms can control a company's cash flows."

---

## inline-header-lists

Vertical lists where every item is a short bold header, a colon, then a sentence ("- **Performance:** It is faster."), repeated down the whole list — or literal "•" bullet characters pasted into Markdown source.

**Why it's slop:** The uniform bold-header-colon-sentence structure repeated for every item is a hallmark of LLM output imitating feature grids, and often replaces prose that would read more naturally. A raw "•" in Markdown source (rather than "-" / "*") is itself a paste-from-chatbot tell.

**Common forms:** a literal `•` bullet character; `**Bold header:**` followed by a sentence, repeated for every list item.

- Avoid: "- **Speed:** It is faster. / - **Cost:** It is cheaper. / - **Size:** It is smaller."
- Prefer: "It is faster, cheaper, and smaller than the previous version."

---

## overuse-of-em-dashes

Em dashes (—) and en dashes (–) used far more often than the genre warrants, especially to punch up parallel clauses where a comma, colon, or parentheses would do.

**Why it's slop:** Strongly associated with LLM output. Repeated em dashes setting off dramatic asides or "not X — but Y" parallelisms read as sales flourish. Best read as a signal alongside other tells, not on its own.

**Common forms:** the characters `—` and `–`, especially several within a short passage.

- Avoid: "The result is clear — and it changes everything — for how we deploy."
- Prefer: "The result is clear, and it changes how we deploy."

---

## unicode-decoration

Decorative non-text Unicode used as shorthand in prose: arrow characters (→ ⇒ ➜) standing in for "leads to" / "produces," and ornamental symbols pasted as bullets or emphasis.

**Why it's slop:** An arrow in running prose is a shorthand the writer didn't expand. It's common in chatbot output but reads as half-finished in published text. Write out the relationship.

**Common forms:** the characters `→ ⇒ ➜ ➔` in running prose.

- Avoid: "Request → validation → handler → response."
- Prefer: "A request is validated, passed to the handler, and turned into a response."

---

## curly-quotes

Curly/typographic quotation marks (" ") and apostrophes (' ') where straight ones (" ') are expected, especially mixed inconsistently.

**Why it's slop:** ChatGPT and some models default to curly marks, often inconsistently. In technical docs, code, and config the distinction matters and straight marks are expected, so stray curly marks suggest pasted LLM output. Not proof on its own — Word, macOS, and Chicago style produce them legitimately. Curly double quotes are the clearer tell; curly apostrophes are too common to flag mechanically, so scan for those by eye.

- Avoid: "Set the "name" field and don't forget the 'id'."
- Prefer: "Set the \"name\" field and don't forget the 'id'."

---

## unusual-tables

Tiny tables holding only a couple of facts (a two-row "Metric / Value" grid) that would read more naturally as a sentence or inline list. Catch by reading: Markdown tables with two or fewer data rows.

**Why it's slop:** LLMs reach for tables to make sparse content look structured. A two- or three-row table adds formatting overhead without helping the reader; prose serves better.

- Avoid: "| Metric | Value | / | --- | --- | / | Latency | ~40ms |"
- Prefer: "Median latency is about 40ms."

---

## skipping-heading-levels

A heading hierarchy that skips a level (e.g. "#" straight to "###"), or a document whose sections start at level 3 with no level-2 headings. Catch by reading the heading outline.

**Why it's slop:** LLMs tend to start sections at the third heading level and skip the second. It breaks the document outline and accessibility conventions, and a hand-formatted page rarely has this quirk.

- Avoid: "# Overview / ### Installation"
- Prefer: "# Overview / ## Installation"

---

## thematic-breaks-before-headings

A horizontal rule (---, ----, ***) inserted before each heading throughout a document, ruling off every section. Catch by reading: a horizontal rule whose next non-blank line is a heading, repeated throughout.

**Why it's slop:** Raw Markdown from chatbots often places a rule before each heading. Headings already separate sections, so the extra rules are redundant machine formatting that human authors rarely add.

- Avoid: "...end of section. / ---- / ## History"
- Prefer: "...end of section. / ## History"
