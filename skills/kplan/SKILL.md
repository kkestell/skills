---
name: kplan
description: Explore a code or behavior change and write a plan in `agents/plans/`. Use for implementation planning, not standalone documentation edits. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it.
argument-hint: "[jira ticket, feature idea, bug report, or improvement to explore]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Write a plan without changing the code.

## Establish the work

1. Read `<feature_description> $ARGUMENTS </feature_description>`. If it is empty, ask what the user wants to plan and stop.

## Explore the code

2. Search the relevant files and read the code to change, nearby examples, public APIs, and tests. Follow an existing pattern when it fits. If the request is too unclear to know where to look, brainstorm first.

## Brainstorm

3. Brainstorm with the user before writing when the user asks to brainstorm, the request is unclear, or exploring leaves a real engineering or design decision. Otherwise, go to Write.
4. Ask one focused question at a time and wait for the answer. For each decision, give the options, their trade-offs, and a recommendation. Do not ask what the repository documents or existing code already answer.
5. Speak clearly and simply. Do not use jargon, invented terms, or shorthand.
6. Say so directly when a request adds a lot of complexity, contradicts the architecture or an earlier decision, or fits poorly with existing code. Name the cost and recommend a simpler option.
7. Stop brainstorming when the scope and every decision are settled.

## Write

8. Read `agents/plans/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the plan in `agents/plans/`. Name the file `YYYY-MM-DD-NNN-slug.md`, using the next sequence for the day.
9. Keep the plan to relevant code references, tasks tied to files, decisions that need explanation, names, and tests for this change. Do not repeat repository rules, standard validation commands, conversation history, rejected options, or work for a later change.
10. Use the same names in plan tasks, proposed code, comments, and documentation. Do not give one concept several names or give an existing term a new meaning.
11. Do not review the plan yourself or ask another agent to review it.

## Stage

12. Stage the plan. Do not stage anything else. Do not commit; `/kreview` commits the plan with the work.
13. Give the final response and stop.

## Final response

When the plan is staged, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the options you rejected, the code you explored, and the steps you took.

```markdown
Two to four sentences explaining, at a high level, what the code change does and how.

**Plan:** `agents/plans/YYYY-MM-DD-NNN-slug.md`

**Files:**

- `src/parser.rs` (modified)
- `src/tokens.rs` (created)

**Next:** `/kwork agents/plans/YYYY-MM-DD-NNN-slug.md`
```

List every file the plan will create or modify, marked `(created)` or `(modified)`.
