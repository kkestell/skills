---
name: kdeslop
description: Audit documentation files (README, guides, public docs) for AI-generated slop — vague filler, corporate superlatives, dead metaphors, and other tells that erode reader trust. Invoke this skill whenever documentation is written, modified, or reviewed, even if the user just says "check the docs" or "clean up the README."
argument-hint: "[file path, directory, or glob pattern for docs to audit]"
disable-model-invocation: true
---

# Audit Documentation for AI Slop

Audit user-facing docs for vague filler, corporate puffery, dead metaphors, and other patterns that make the writing feel AI-generated or untrustworthy.

## Inputs

<audit_target> $ARGUMENTS </audit_target>

Resolve targets with `${CLAUDE_SKILL_DIR}/scripts/list_audit_targets.sh [target...]`.

- If no target is provided, use the script defaults.
- If a target is provided, pass it through so the audit stays focused.
- Skip `docs/internal/`, `.worktrees/`, vendored/generated directories, and other working docs unless the user explicitly asks.

## Phase 1: Read and Catalog

Read `${CLAUDE_SKILL_DIR}/references/slop_tells.md` before scoring.

For each file, note its doc type (README, API docs, tutorial, changelog, guide). Calibrate to the genre: changelogs can be dry, READMEs can have personality.

## Phase 2: Flag Trust-Eroding Tells

Flag only concrete, line-referenced issues. Density matters more than isolated words: one "however" is fine; a paragraph full of filler is not.

Use the categories and examples in `references/slop_tells.md`. For each finding, record:

- file and line number
- offending text
- category
- why it hurts trust
- a concrete rewrite or direction

## Phase 3: Score

Assign one severity per file:

- **Clean** — no significant tells, or only isolated instances that read naturally in context
- **Minor** — a few tells scattered across the file; worth a cleanup pass but not embarrassing
- **Moderate** — multiple paragraphs with clustered tells; reads as partially AI-generated
- **Severe** — pervasive slop throughout; the doc needs a rewrite

## Phase 4: Report

Use `${CLAUDE_SKILL_DIR}/assets/audit-report-template.md` as the default report shape.

Present findings grouped by file, worst first. If everything is clean, say so and stop — do not invent problems.

## Guidelines

- Be specific. "Line 14 uses 'leverage'" is useful. "The doc has corporate language" is not.
- Respect intentional style. Calibrate to the project's voice instead of flattening it.
- Do not flag technical claims as slop when they are precise and defensible in context.
- This skill audits. Suggest fixes inline, but do not rewrite the whole doc unless the user asks.
