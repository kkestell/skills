---
name: ktask
description: Carry a code or behavior change through `/kbrief` when it needs one, then `/kplan`, `/kwork`, and `/kreview`, each run by its own Opus 5.5 agent at high effort in the shared checkout, then sanity-check the result and commit it as one commit. Use in Hypercube or another agent orchestration tool when the user wants a change delegated stage by stage. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it.
argument-hint: "[brief path, jira ticket, feature idea, bug report, or improvement to carry out]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Delegate each stage to its own agent and commit the result. You do not plan, implement, or review, and you do not read the plan, the code, or the review. You do not write the brief. You start the agents, pass each one what the previous one reported, check that the stages produced their files, and commit.

## Agents

Start each stage as a new agent with fresh context, running Opus 5.5 at high effort in this checkout. All the agents share the checkout; none gets its own worktree. In Hypercube, use `create_session` with harness `claude`, model `opus`, effort `high`, and `dir` `"."`. If the host cannot start an agent with that model and effort, tell the user and stop.

Each agent asks the user directly for any decision its skill would ask the user for. After you start an agent, wait for its final response without writing to the user. When an agent reports that it could not finish its stage, tell the user what it reported and stop. End each agent once its stage is done.

## Start

1. Read `<feature_description> $ARGUMENTS </feature_description>`. If it is empty, ask what the user wants to build and stop.
2. Run `git diff --cached --name-only`. If anything is staged other than a brief named in the feature description, tell the user it would land in the commit and stop.

## Plan

3. Start the planning agent with this message:

   > Run `/kplan <feature description>`. Ask the user directly for any decision `/kplan` needs. When the plan is staged, reply with `/kplan`'s final response.

4. If its response is `/kplan`'s missing-brief response, end the planning agent and go to Brief. Otherwise, take the plan path from its response and go to Implement.

## Brief

5. Start the brief agent with this message:

   > Run `/kbrief <feature description>`. Work out the change with the user directly. When the brief is staged, reply with `/kbrief`'s final response.

6. Take the brief path from its response. Start a new planning agent with the message in step 3, using the brief path as the feature description, and take the plan path from its response. If it again reports a missing brief, tell the user what it reported and stop.

## Implement

7. Start the work agent with this message:

   > Run `/kwork <plan path>`. Ask the user directly for any decision `/kwork` needs. When the work is staged, reply with `/kwork`'s final response.

8. Take the review scope from the Next line of its response, including any commits it made.

## Review

9. Start the review agent with this message:

   > Run `/kreview <review scope>`. Ask the user directly for any decision a fix needs. When the review is staged, reply with `/kreview`'s final response.

## Commit

10. Check that the stages produced their results. If any check fails, tell the user what is missing and stop without committing.
    - `git diff --cached --name-only -- . ':(exclude).agents'` lists code changes, or the work agent reported commits.
    - The plan, a work log in `.agents/work/`, and a review in `.agents/reviews/` exist and are staged, or are in a commit the work agent reported.
    - A brief named in the feature description or written by the brief agent is staged or already committed.
11. Commit everything staged in one commit. The subject is the plan's title, its first line. The body is two or three sentences on what changed, taken from the agents' responses. If the work agent committed for a plan task, this commit holds the rest.

## Final response

When the work is committed, reply in the form below and nothing else. Build it from the agents' responses and the commit. Lead with the main point, write plainly, and leave out the steps you took.

```markdown
Two to four sentences saying what was built, how, and whether the plan's goal is met.

**Surprises:**

- A departure from the plan or follow-up work the work agent reported.

| ID | Severity | Fix   | Title                           | Location           |
| -- | -------- | ----- | ------------------------------- | ------------------ |
| F1 | High     | Fixed | Parser drops the final token    | `src/parser.rs:42` |
| F2 | Low      | Fixed | Stale comment on the token loop | `src/parser.rs:57` |

**Brief:** `.agents/briefs/YYYY-MM-DD-NNN-slug.md` · **Plan:** `.agents/plans/YYYY-MM-DD-NNN-slug.md` · **Work log:** `.agents/work/YYYY-MM-DD-NNN-slug.md` · **Review:** `.agents/reviews/YYYY-MM-DD-NNN-slug.md`

**Commit:** `abc1234` · **Lines:** +120 / −45 (net +75)

**Files:**

- `src/parser.rs` (modified)
- `src/tokens.rs` (created)
```

Drop the Brief link when there was no brief. Write `None.` under Surprises if the work agent reported none. The table is the review agent's findings table; if it had no findings, replace the table with `No findings.` Count lines from the commit, excluding `.agents/`, with `git show --shortstat --format= HEAD -- . ':(exclude).agents'`, and add the lines of any commits the work agent made. List every code file in the commit, marked `(created)` or `(modified)`.
