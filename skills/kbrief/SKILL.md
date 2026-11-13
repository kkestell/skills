---
name: kbrief
description: Work out with the user what a change should do and why, and write a brief in `agents/briefs/` that records their intent and decisions for `/kplan` to plan against. Use for ambiguous, large, or open-ended requests before planning, not for implementation planning. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it.
argument-hint: "[feature idea, problem, or change to think through]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Settle with the user what the change should do and why, and write it down as a brief. The brief records the user's intent so the plan can be checked against it. It does not plan the implementation, and you do not change the code.

## Establish the work

1. Read `<request> $ARGUMENTS </request>`. If it is empty, ask what the user wants to work out and stop.

## Explore the code

2. Read enough of the codebase to understand the current behavior, the constraints that shape the options, and anything the code already settles. Explore to ask informed questions, not to design the implementation.

## Brainstorm

3. Ask one focused question at a time and wait for the answer. For each decision, give the options, their trade-offs, and a recommendation. Do not ask what the repository documents or existing code already answer.
4. Settle the questions the user owns: what the change should do, for whom, its scope, its priorities, and any technical constraint the user cares about, such as a dependency, a data store, or compatibility. Leave every other implementation choice to the plan.
5. Speak clearly and simply. Do not use jargon, invented terms, or shorthand.
6. Say so directly when a request adds a lot of complexity, contradicts the architecture or an earlier decision, or fits poorly with existing code. Name the cost and recommend the option that leaves the codebase simplest overall, which may rewrite an abstraction or delete code rather than make the smallest change.
7. Stop brainstorming when every question the user owns is settled or the user has left it to the planner.

## Write

8. Read `agents/briefs/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the brief in `agents/briefs/`. Name the file `YYYY-MM-DD-NNN-slug.md`, using the next sequence for the day.
9. Write in the user's terms, from the outside of the system. Record only what the user said or approved, with their reasons. Do not name files, functions, or tasks, and do not propose code.
10. Keep the brief short. Leave out the conversation itself; keep the decisions, the reasons behind them, and the options the user turned down.

## Confirm

11. Show the user the brief in full and ask whether it says what they meant. Wait for the answer.
12. Edit the brief for each correction and show the changed parts again until the user confirms it.

## Stage

13. Stage the brief. Do not stage anything else. Do not commit.
14. Give the final response and stop.

## Final response

When the brief is staged, reply in the form below and nothing else. Lead with the main point and write plainly.

```markdown
Two to four sentences stating what the change should do and the decisions that shape it most.

**Brief:** `agents/briefs/YYYY-MM-DD-NNN-slug.md`

**Next:** `/kplan agents/briefs/YYYY-MM-DD-NNN-slug.md`
```
