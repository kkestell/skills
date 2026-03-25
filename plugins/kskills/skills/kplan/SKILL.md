---
name: kplan
description: Turn a feature idea, bug report, improvement request, or brainstorm into a concrete repo-specific markdown plan with actionable tasks, related documents, validation steps, and open questions. Use after requirements are clear enough to define implementation work, but before coding or running `/kwork`.
argument-hint: "[feature description, bug report, or improvement idea]"
disable-model-invocation: true
---

# Create a Plan

Transform a feature description, bug report, or improvement idea into a structured markdown plan.

## Workflow Context

This skill is part of a structured workflow: kinit -> kstart -> kbrainstorm -> **kplan** -> kwork -> kverify -> kend.
You are currently in the **kplan** step. You are working in a git worktree, not the original repository.

### Current Task
!`cat .k/current_task.json 2>/dev/null || echo '{"error": "No current task. Run /kstart first."}'`

## Feature Description

<feature_description> $ARGUMENTS </feature_description>

If the feature description is empty, ask the user what they'd like to plan. Do not proceed without one.

## 1. Local Research

Scan the repository to understand conventions, existing patterns, and documented guidance:

- Look for similar features in the codebase
- Check for established patterns and conventions
- Review CLAUDE.md for project-specific guidance

## 2. Research Decision

Based on local findings, decide whether external research is needed.

**Always research:** security, payments, external APIs, data privacy — the cost of missing something is too high.

**Skip research:** strong local patterns exist, CLAUDE.md has guidance, user knows what they want.

**Research when uncertain:** unfamiliar territory, no codebase examples, new technology.

Announce the decision briefly and proceed. The user can redirect if needed.

## 3. External Research (Conditional)

Only if Step 2 indicated it. Search for relevant documentation and best practices.

## 4. Consolidate Research

- Document relevant file paths from repo research
- Capture the strongest repo-relative examples for a `Related code` section in the plan
- Note external documentation and best practices (if researched)
- List related issues or PRs discovered
- Capture CLAUDE.md conventions

Optionally summarize findings and ask the user if anything looks off before proceeding.

## 5. Carry Forward Related Docs

If a brainstorm exists at `<docs_path>/brainstorm.md` (read `docs_path` from `.k/current_task.json`), add a `Related documents` section near the top with the exact repo-relative brainstorm path.

If there is no related brainstorm, omit the section.

## 6. Write the Plan

Use `${CLAUDE_SKILL_DIR}/assets/plan-template.md` as a starting scaffold, not a rigid form. Remove sections that do not apply, add sections when needed, and include a `Related code` section with repo-relative paths and one-line reasons.

**Filename:** Write to the task docs directory from `current_task.json`:

`<docs_path>/plan.md`

Read `docs_path` from `.k/current_task.json`.

Write the plan with actionable checkboxes. After writing, print the path and stop.

NEVER CODE — just research and write the plan.
