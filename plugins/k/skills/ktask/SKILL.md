---
name: ktask
description: "Execute a quick one-off task: plan lightly (optionally via subagent), implement, validate. No plan file, no commit, no pre-flight checks."
metadata:
  argument-hint: "[task description — a bug fix, small feature, refactor, or improvement]"
---

## Workflow

### Phase 1 — Understand & Plan

1. Read `<task_description> $ARGUMENTS </task_description>`; if it is empty, ask what they want done and stop.
2. Decide whether subagent planning is needed.
   - **Skip planning entirely** if the task is trivially obvious (e.g., fixing a typo, updating a single config value, renaming a method).
   - **Plan locally** if the task is small but benefits from a moment of thought (e.g., a focused bug fix with a clear cause, a small refactor).
   - **Delegate to a subagent** if the task touches multiple files or areas and would benefit from an independent planning pass.
3. If planning (locally or via subagent), use the lightweight template from `assets/task-plan-template.md`.
   - The plan lives **only in conversation context** — do not write it to `!`echo ~/.k/workspaces/${PWD//\//_}`/plans/` or any other file.
   - If using a subagent, pass the task description and the template, then incorporate the returned plan into your context.
   - If the plan reveals the task is larger than a quick one-off, stop and suggest `/kplan` instead.
4. If anything is unclear, ask the user one focused question. Do not spin up a long brainstorming loop — that's what `/kplan` is for.

### Phase 2 — Explore

5. Do a quick exploration of the relevant code.
   - Find the files, functions, and patterns the task will touch.
   - Read enough to understand the local context — not a full architectural survey.
   - Check for nearby patterns to follow: naming conventions, error handling style, test structure.

### Phase 3 — Execute

6. Implement the change.
   - Match repo style and conventions.
   - Comment the code well — explain the "why", not just the "what".
   - Write or update tests for the changed behavior.
   - Keep changes focused and minimal. This is not the time for drive-by refactors unless they directly support the task.
7. If you hit an unexpected obstacle or the scope balloons, stop and tell the user. Suggest `/kplan` if the task needs more structure.

### Phase 4 — Validate

8. Run the relevant quality checks.
   - Run tests, lint, formatter, and type checks as applicable.
   - Use the commands from the project's guidance docs or existing repo scripts.
   - Fix any failures.
9. Do a single review pass over the completed work.
   - Launch a review subagent when it adds value; otherwise review locally.
   - Subagents start with fresh context, so include all necessary context in the review prompt.
   - Build the review prompt by reading `assets/task-review-prompt.md`, then filling in the specifics of the task and all changed files.
   - The reviewer should check for correctness, completeness, and whether the code matches the task description — not a full architectural review.
10. Fix any issues the review found, then re-run quality checks.

### Phase 5 — Report

11. Report what was done, what files changed, and the quality-check results.
    - Do **not** commit. The user commits when they are ready.
    - If there is follow-up work, mention it but do not create follow-up docs.

## Principles

- **Fast and focused** — this is the quick path. If it's not quick, switch to `/kplan` → `/kwork`.
- **Plan in context, not on disk** — no plan file. The plan is a conversation artifact.
- **Minimal ceremony** — no pre-flight git checks, no baseline tests, no commit. Just understand, do the work, validate, and report.
- **Still rigorous** — write tests, run checks, review the code. "Quick" does not mean "sloppy".
