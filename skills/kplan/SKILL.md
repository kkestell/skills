---
name: kplan
description: Explore a code or behavior change, given a brief from `.agents/briefs/` or a small, clear request, and write a plan in `.agents/plans/`. Use for implementation planning, not standalone documentation edits; send ambiguous or large requests to `/kbrief` first. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it.
argument-hint: "[brief path, or a small jira ticket, bug report, or improvement]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Write a plan without changing the code.

## Establish the work

1. Read `<feature_description> $ARGUMENTS </feature_description>`. If it is empty, ask what the user wants to plan and stop.
2. If it names a brief in `.agents/briefs/`, read the brief. The brief is the user's settled intent: plan to deliver its Outcome, keep every decision it records, and settle its Left to the plan questions yourself.

## Explore the code

3. Search the relevant files and read the code to change, nearby examples, public APIs, and tests. Look beyond the files to change at the rest of the codebase: whether it already does this, whether an existing abstraction has the wrong shape for the change, and whether the change would extend the architecture naturally or sit bolted on. Follow an existing pattern when it is sound.

## Check the input

4. Without a brief, plan only a request that is small and clear: one you can plan without asking the user what the change should do, its scope, or its priorities. If the request is ambiguous, large, or open-ended, or leaves such a question open, stop and give the final response for a missing brief.
5. With a brief, if the code makes a decision in the brief unworkable, stop and tell the user, in their terms, which decision and why. Do not plan around it.

## Decide

6. Settle every decision yourself except product questions. A product question is a choice that changes what the user sees or does in everyday use of the product. Everything else is yours: internal design, which component owns a rule, data and protocol shapes, removing code that cannot run in real use, and how rare cases behave, such as races, crashes, failures that coincide, and states everyday use does not reach. Handle rare cases the simplest reasonable way. A rare-case decision becomes a product question only when it changes what the user sees in everyday use.
7. Choose the option that leaves the codebase simplest overall, which may rewrite an abstraction or delete code rather than make the smallest change.

## Write

8. Read `.agents/plans/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the plan in `.agents/plans/`. Name the file `YYYY-MM-DD-NNN-slug.md`, using the next sequence for the day.
9. Keep the plan to relevant code references, tasks tied to files, decisions that need explanation, names, and tests for this change. Link the brief under Goal instead of restating it. Do not repeat repository rules, standard validation commands, conversation history, rejected options, or work for a later change.
10. In the Test plan, make each case an assertion in an existing test whose setup already reaches it, and add a new test only when none does. Name the behavior each new test guards and why no existing test can carry it. Each new test fails on the code before the change. A change that replaces behavior replaces the tests of the old behavior.
11. Use the same names in plan tasks, proposed code, comments, and documentation. Do not give one concept several names or give an existing term a new meaning.
12. Under Check your assumptions, list the product questions the brief does not settle, such as a feature that behaves differently, something the user relies on that goes away, a path the user will notice is slower, narrowed scope, a new dependency or migration the user has to deal with, or a reading of an ambiguous request that leads to a different product. Most plans have none, one, or two; write `None.` when nothing qualifies. Record your other decisions under Decisions when they need explaining.
13. Write each entry as the user experiences the product, in the form the template shows: what the plan does that they will notice, and the alternative with what it would cost them. Leave out code names, protocol fields, and internal mechanisms. The user should be able to answer without reading the code.
14. Do not review the plan yourself or ask another agent to review it.

## Check your assumptions

15. If the list is `None.`, go to Stage. Otherwise, present the entries to the user in one message, numbered, most consequential first. Give each entry in the same form as in the plan. The user answers only the entries they want changed; the rest stand. Wait for the answer.
16. Edit the affected lines of the plan for each changed entry; do not rewrite the plan. Mark each entry kept or changed, and to what. If a change reopens a product question, present it the same way.

## Stage

17. Stage the plan. Do not stage anything else. Do not commit.
18. Give the final response and stop.

## Final response

When the plan is staged, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the options you rejected, the code you explored, and the steps you took.

```markdown
Two to four sentences explaining, at a high level, what the code change does and how.

**Plan:** `.agents/plans/YYYY-MM-DD-NNN-slug.md`

**Files:**

- `src/parser.rs` (modified)
- `src/tokens.rs` (created)

**Next:** `/kwork .agents/plans/YYYY-MM-DD-NNN-slug.md`
```

List every file the plan will create or modify, marked `(created)` or `(modified)`.

### Missing brief

When the request needs a brief, reply in the form below and nothing else.

```markdown
One or two sentences on what the request leaves open for the user to decide.

**Next:** `/kbrief <request>`
```
