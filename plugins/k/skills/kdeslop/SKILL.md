---
name: kdeslop
description: "Detect and fix AI \"slop\" in prose — overused LLM vocabulary, empty significance/legacy claims, vague attributions, hollow rhetorical constructions, formulaic structure, and machine-formatting tells. Fans out one audit subagent per slop category, then rewrites the confirmed slop in place while preserving meaning and the author's voice."
argument-hint: "[file paths to scan and fix]"
---

## Overview

Slop comes in families, and each family is its own kind of reading. This skill splits the audit across six subagents — one per category — each carrying only the rules for its family. They report; you decide and fix.

The rule files live in this skill's `assets/` directory:

| Category                 | Rule file                | What it covers                                                                                                                                                       |
| ------------------------ | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vocabulary & register    | `assets/vocabulary.md`   | AI vocabulary clusters, elevated register, filler adverbs, metaphor crutches                                                                                         |
| Significance & puffery   | `assets/significance.md` | Asserted importance/legacy, inflated copulas, empty participle clauses, PR language, coined concept labels                                                           |
| Rhetorical constructions | `assets/rhetoric.md`     | "not just X," "not X but Y," formulaic openers, false conclusions, false suspense, pedagogical framing, performative candor, self-answered questions                 |
| Sourcing & honesty       | `assets/sourcing.md`     | Vague attribution, exaggerated breadth, cutoff disclaimers, unfilled placeholders, chatbot residue, hedge stacking                                                   |
| Structure & rhythm       | `assets/cadence.md`      | Challenges-and-future template, connector pile-ups, rule of three, elegant variation, staccato bursts, repeated openers, magic-number lists                          |
| Formatting & typography  | `assets/formatting.md`   | Title-case headings, scattered bold, inline-header lists, em-dash overuse, decorative Unicode, curly quotes, tiny tables, heading-level skips, rules before headings |

## Workflow

### 1. Resolve the targets

Resolve the target files from `<input_document> $ARGUMENTS </input_document>`. Accept one or more file or directory paths. **If no paths are given, ask the user which files to audit and stop.** Note this `SKILL.md`'s directory — the `assets/` files are siblings of it.

### 2. Fan out one audit subagent per category

Launch all six subagents **in parallel** (one Agent call per category, in a single message). They are read-only auditors — they do **not** edit anything. Give each subagent this prompt, filled in:

> You are auditing prose for one category of AI "slop." Read the rule file `<skill-dir>/assets/<file>.md` in full — it defines each pattern, why it reads as slop, and avoid/prefer examples. Then read each of these target files end to end: `<target paths>`.
>
> Audit every target against your category's rules as a **lens, not a checklist**. The example phrases in the rule file are leads, not the set of things to flag. Judge each candidate on whether the writing actually has the underlying problem — asserting importance instead of showing it, saying nothing in many words, hedged vagueness — not merely whether it contains a listed word. A legitimate use of a flagged word is not slop. Several rules have no single-phrase signal (rule of three, elegant variation, magic-number lists, staccato runs, heading outline) — catch those by reading and counting.
>
> Report your findings as a list. For each, give: `file:line`, the rule id it falls under, a one-line quote of the problem text, why it's slop here, and a concrete suggested rewrite (or "cut"). If a fix would need a fact you don't have, say so instead of inventing one. Do not edit any files. If you find nothing in your category, say so.

Map each subagent to its file: vocabulary → `vocabulary.md`, significance → `significance.md`, rhetoric → `rhetoric.md`, sourcing → `sourcing.md`, cadence → `cadence.md`, formatting → `formatting.md`.

### 3. Confirm and fix

Collect the six reports. For each finding, **confirm it against the actual sentence and surrounding context** before acting — the subagents are high-recall and will surface false positives. Then rewrite the confirmed slop in place:

- Fix the **underlying problem**, not the surface signal. Replace puffery with the specific fact it was standing in for, or cut it — removing a trigger word while leaving the empty claim intact just hides the slop.
- Preserve the author's meaning, factual content, and voice. When a flagged word is the right word, leave it.
- Prefer the plain version: concrete over grandiose, specific over generic, shorter over padded.
- When a fix would change meaning or needs a fact you don't have, leave it and flag it for the user instead of inventing content.

### 4. Report

Summarize what you changed, grouped by file: line, the category/rule it fell under, and a brief before → after (or what was cut and why). List anything you left for the user to decide, and why.

## Principles

- **Read, don't match** — the rule files are a lens for judging whether prose has the underlying problem, never a find-and-replace word list.
- **Comprehensive over mechanical** — audit the whole text against every category; the subagents cover the families so nothing is judged in isolation.
- **Fix the problem, not the symptom** — remove the underlying puffery or vagueness, not just the trigger word.
- **Preserve meaning and voice** — edits keep the author's intent and facts intact; a legitimate use of a flagged word stays.
- **Don't invent** — if a fix needs a fact you don't have, flag it rather than fabricate.
