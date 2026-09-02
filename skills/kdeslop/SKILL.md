---
name: kdeslop
description: "Detect and fix AI \"slop\" in prose — overused LLM vocabulary, empty significance/legacy claims, vague attributions, hollow rhetorical constructions, formulaic structure, and machine-formatting tells. Audits the text category by category, then rewrites the confirmed slop in place while preserving meaning and the author's voice."
argument-hint: "[file paths to scan and fix]"
---

## Overview

Slop comes in families, and each family is its own kind of reading. `assets/slop-rules.md` holds all six families — vocabulary and register, inflated significance, hollow rhetoric, sourcing and hedging, formulaic structure, formatting and typography — with the patterns in each, why each reads as machine-generated, and avoid/prefer examples.

Do this work yourself. Do not delegate the audit or the rewriting to subagents: judging whether a sentence has the underlying problem takes the whole document in view, and the fixes need the same reader who found them.

## Workflow

### 1. Resolve the targets

Resolve the target files from `<input_document> $ARGUMENTS </input_document>`. Accept one or more file or directory paths. **If no paths are given, ask the user which files to audit and stop.** Note this `SKILL.md`'s directory — `assets/slop-rules.md` is a sibling of it.

### 2. Read the rules and the targets

Read `assets/slop-rules.md` in full, then read each target file end to end. Both readings are required before you flag anything: the rules define the underlying problems, and several of them can only be judged against the whole document.

### 3. Audit category by category

Work through the targets once per category — vocabulary, significance, rhetoric, sourcing, cadence, formatting — rather than trying to hold all six lenses at once. One pass per family keeps each reading focused and stops one loud category from crowding out the others.

Treat the rules as a **lens, not a checklist**. The example phrases are leads, not the set of things to flag. Judge each candidate on whether the writing actually has the underlying problem — asserting importance instead of showing it, saying nothing in many words, hedged vagueness — not merely whether it contains a listed word. A legitimate use of a flagged word is not slop.

Several rules have no single-phrase signal: rule-of-three, elegant-variation, magic-number-lists, staccato-and-fragments, repetitive-sentence-openers, question-then-answer, hedge-stacking, unusual-tables, skipping-heading-levels. Catch those by reading and counting. Grep is useful for the character-level tells (em dashes, arrows, curly quotes, `•`) but nothing else.

Note each finding as you go: `file:line`, the rule id, the problem text, and the fix you intend.

### 4. Fix

Rewrite the confirmed slop in place. Re-read the actual sentence and its surrounding context before each edit — a candidate that looked like slop in the pass often turns out to be the right wording in situ.

- Fix the **underlying problem**, not the surface signal. Replace puffery with the specific fact it was standing in for, or cut it — removing a trigger word while leaving the empty claim intact just hides the slop.
- Preserve the author's meaning, factual content, and voice. When a flagged word is the right word, leave it.
- Prefer the plain version: concrete over grandiose, specific over generic, shorter over padded.
- When a fix would change meaning or needs a fact you don't have, leave it and flag it for the user instead of inventing content.

### 5. Report

Summarize what you changed, grouped by file: line, the category/rule it fell under, and a brief before → after (or what was cut and why). List anything you left for the user to decide, and why.

## Principles

- **Do it yourself** — no subagents; the audit and the rewrite are one reading.
- **Read, don't match** — the rules are a lens for judging whether prose has the underlying problem, never a find-and-replace word list.
- **One category at a time** — a focused pass per family so nothing is judged in isolation and nothing gets skipped.
- **Fix the problem, not the symptom** — remove the underlying puffery or vagueness, not just the trigger word.
- **Preserve meaning and voice** — edits keep the author's intent and facts intact; a legitimate use of a flagged word stays.
- **Don't invent** — if a fix needs a fact you don't have, flag it rather than fabricate.
