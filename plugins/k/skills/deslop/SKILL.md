---
name: deslop
description: Audit user-facing docs for AI-slop signals like vague filler, puffery, dead metaphors, and trust-eroding prose. Use whenever docs are written, changed, or reviewed.
argument-hint: "[file path, directory, or glob pattern for docs to audit]"
disable-model-invocation: true
---

## Workflow

1. Resolve `<audit_target> $ARGUMENTS </audit_target>`.
   - If a target is provided, audit only that file, directory, or glob so the review stays focused.
   - If no target is provided, audit repo-root docs like `README*`, `CHANGELOG*`, `CONTRIBUTING*`, and markdown under `docs/`.
   - Skip `.k/tasks/`, generated output, vendored content, and other working docs unless the user explicitly asks for them.
2. Read `${CLAUDE_SKILL_DIR}/references/slop_tells.md` before scoring anything.
3. Read and calibrate each document before flagging issues.
   - Note the doc type and judge it in context. Changelogs can be dry; READMEs can have some personality.
   - Respect intentional project voice instead of flattening everything into generic technical prose.
4. Record findings only when they are concrete and trust-relevant.
   - Flag line-referenced issues with quoted text, category, why it hurts trust, and a concrete rewrite or direction.
   - Density matters more than isolated words. One fuzzy phrase can be fine; a paragraph full of vague filler is not.
   - Be specific. "Line 14 uses empty puffery" is useful; "the doc feels AI-ish" is not.
   - Do not flag precise, defensible technical claims as slop just because they sound polished.
5. Score each file.
   - `Clean`: no meaningful tells, or only isolated natural-sounding cases
   - `Minor`: a few scattered tells worth tightening
   - `Moderate`: clustered tells across multiple sections
   - `Severe`: pervasive trust-eroding prose that needs a rewrite
6. Write the report using `${CLAUDE_SKILL_DIR}/assets/audit-report-template.md`.
   - Group findings by file, worst first.
   - If everything is clean, say so and stop.
   - Audit only; do not rewrite the full docs unless the user asks.
