---
name: kauto
description: Plan, implement, review, and commit a code or behavior change without stopping for user input, using `/kplan`, `/kwork`, and `/kreview`. Use when the user wants a change carried through to a commit autonomously. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it.
argument-hint: "[jira ticket, feature idea, bug report, or improvement to carry out]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Carry the change from plan to commit on your own. You are working autonomously, so you make every decision the other skills would ask the user to make, and you report the design and architecture decisions at the end.

## Establish the work

1. Read `<feature_description> $ARGUMENTS </feature_description>`. If it is empty, ask what the user wants to build and stop. After this step, do not ask the user anything.

## Plan

2. Run `/kplan` with the feature description. Where `/kplan` would brainstorm with the user, settle each decision yourself: choose the option that fits the existing code and architecture with the least complexity, and record the decision in the plan.
3. Note the plan path and every design or architecture decision you made. Continue past `/kplan`'s final response.

## Implement

4. Run `/kwork` with the plan path. Note any departure from the plan it reports under Surprises. Continue past `/kwork`'s final response.

## Review

5. Start one subagent and have it run `/kreview staged changes for <plan path>`. Tell it to settle each decision `/kreview` would ask the user for itself, using the same rule as in Plan, and to return the skill's final response and every decision it made.

## Final response

When the work is committed, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed and the steps you took.

```markdown
Two to four sentences saying what was built, how, and whether the plan's goal is met.

**Decisions:**

- Stored export settings per user rather than per workspace, because settings are already loaded per user in `src/settings.rs`.

**Review:** `agents/reviews/YYYY-MM-DD-NNN-slug.md` · Fixed 3 findings.

**Plan:** `agents/plans/YYYY-MM-DD-NNN-slug.md` · **Commit:** `abc1234`

**Lines:** +120 / −45 (net +75)

**Files:**

- `src/parser.rs` (modified)
- `src/tokens.rs` (created)
- `agents/plans/YYYY-MM-DD-NNN-slug.md` (created)
- `agents/work/YYYY-MM-DD-NNN-slug.md` (created)
- `agents/reviews/YYYY-MM-DD-NNN-slug.md` (created)
```

Under Decisions, list each design or architecture decision made while planning, implementing, or fixing findings, with the choice and the reason in one sentence. Include departures from the plan. If there were none, write `None.` Count lines from the commit, excluding `agents/`, with `git show --shortstat --format= HEAD -- . ':(exclude)agents'`. List every file in the commit, marked `(created)` or `(modified)`.
