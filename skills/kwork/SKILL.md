---
name: kwork
description: Implement a plan from `agents/plans/`, write a work log in `agents/work/`, and stage the changes for review. Use to carry out a written plan, not to plan or review. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it.
argument-hint: "[plan path or slug]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Implement the plan, record what was done, and stage the changes for review.

## Establish the work

1. Read `<plan> $ARGUMENTS </plan>` and select the plan in `agents/plans/`:
   - If a path or slug is supplied, resolve it to a plan. Ask which plan to implement and stop only if it matches no plan or is ambiguous.
   - If no argument is supplied, inspect the plans and repository evidence such as existing code, reviews, and Git history to identify unimplemented plans. If exactly one remains, select it and proceed without asking. Do not require an explicit completion marker to recognize an implemented plan. Ask which plan to implement and stop only if no unimplemented plan can be identified or multiple candidates remain.
2. Read the plan.

## Implement

3. Read the code the plan references before changing it. Carry out the plan's tasks in order and write the tests it names.
4. Use the names the plan gives. Do not add work the plan does not call for.
5. When the code contradicts the plan or a task cannot be done as written, make the smallest departure that still meets the plan's goal, record it in the work log, and report it under Surprises. Do not redesign the change.
6. Validate the change. Fix failures before continuing.

## Write the work log

7. Read `agents/work/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the work log in `agents/work/`. Name the file `YYYY-MM-DD-NNN-slug.md`, using today's date, the next sequence for the day, and the plan's slug.
8. Keep the log concise. Record where the work departed from the plan and why, decisions made during the work, the checks that ran, manual verification with the commands to reproduce it, and follow-up work. Do not repeat the plan, the diff, or the conversation.

## Stage

9. Stage the implementation, the work log, and the plan if it is not already staged. Do not stage unrelated changes. Do not commit; `/kreview` commits the work after the review.
10. Give the final response and stop.

## Final response

When the work is staged, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed and the steps you took.

```markdown
One or two sentences saying what was built and whether the plan's goal is met.

**Surprises:**

- A departure from the plan, a detour, something unexpected in the code, or follow-up work.

**Work log:** `agents/work/YYYY-MM-DD-NNN-slug.md` · **Lines:** +120 / −45 (net +75)

**Files:**

- `src/parser.rs` (modified)
- `src/tokens.rs` (created)
- `agents/plans/YYYY-MM-DD-NNN-slug.md` (created)
- `agents/work/YYYY-MM-DD-NNN-slug.md` (created)

**Next:** `/kreview staged changes for agents/plans/YYYY-MM-DD-NNN-slug.md`
```

Write `None.` under Surprises if the work went as planned. Count lines from the staged changes, excluding `agents/`, with `git diff --cached --shortstat -- . ':(exclude)agents'`. List every staged file, marked `(created)` or `(modified)`.
