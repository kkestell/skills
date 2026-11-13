---
name: kdeslop
description: "Audit the current repository for dead code, duplication, broken guarantees, over-engineering, hollow tests, and misleading comments or docs. Delegate parallel area reviews, independently verify and deduplicate findings, and write and stage a review in `agents/reviews/` without fixing anything. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it."
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Find the code and documentation that nobody questioned. You orchestrate: reviewers find; you verify, deduplicate, and report. Audit the current repository, not just a diff. Judge the work by its behavior and evidence, not by guesses about AI authorship. Do not limit the audit to files known to have been written by an agent.

Nothing gets fixed. The only file you create or change is the final review; stage only that file. Do not invoke `/kreview`'s fix workflow, commit, or start follow-up work.

## Carve up the repository

1. Locate the repository in the current directory. Record its absolute path, HEAD commit, and working-tree status. Review the current working tree, including local changes, without modifying or discarding them; distinguish local changes from HEAD in the report. If there is no HEAD commit, record that fact rather than inventing a revision.
2. Read the README, applicable agent instructions such as `AGENTS.md` and `CLAUDE.md`, and the build and test configuration. Inventory the hand-written source, tests, docs, scripts, and configuration. Skip generated files, lockfiles, vendored code, and data.
3. Split the repository into at most 10 areas along real boundaries: a service, frontend, pipeline, infrastructure and CI, or test harness. Aim for roughly 5–15k lines of hand-written code per reviewer, not a quota. Keep each area's tests with it. Make docs their own area, including READMEs, `docs/`, agent instructions, and the build and deploy files they describe. Give every in-scope file one owner; other reviewers may read it for context. In a docs-only repository, one docs area may suffice.
4. Keep the areas small enough for a single pass. If the repository cannot fit within 10 bounded passes, prioritize consequential areas and explicitly record the files or directories left uncovered. Never imply that a partial audit covered the whole repository.

## Fan out

5. Start one fresh reviewer per area and run them in parallel. Use separate agent sessions when available, otherwise subagents. Use the current checkout read-only, not new worktrees that omit local changes. In Hypercube, pass the repository's absolute path as `dir` and the full brief as the session message. If neither sessions nor subagents are available, tell the user the parallel audit cannot run and stop rather than silently substituting a solo audit.
6. Give each reviewer a self-contained brief. Include the lenses and boundaries below in full; do not assume it inherits this skill or your conversation. Supply:
   - The absolute repository path and HEAD commit (or lack of one), any local changes relevant to its area, a two-sentence project description, and orientation files to read first.
   - Its exact area as directories and files, any exclusions, and the files outside it that it may read only for context, such as API contracts used by a frontend.
   - All six lenses, plus any specific suspicions worth investigating. Suspicions are leads, not findings to validate at any cost.
   - The reviewer boundaries, time and tool-call budget, and report format below.

### Lenses

Each reviewer covers every lens in its area:

1. **Dead code:** unused functions, exports, branches, files, settings, environment variables, flags, CLI options, build targets, DTO fields, and CSS rules. Check callers and dynamic discovery before calling something unused.
2. **Duplication:** logic implemented twice, near-copies that have drifted, or parallel tools and scripts that do the same job. Similar syntax alone is not a defect; show the needless maintenance or behavioral consequence.
3. **Broken guarantees:** invariants stated in names, comments, docs, or tests that the code does not enforce; timeouts, retries, budgets, limits, cancellation, or error handling that do not hold; plain bugs found along the way.
4. **Over-engineering:** abstractions, options, fallbacks, or configurability with one caller or no real use; defensive handling of impossible cases; indirection that only forwards calls. One caller alone is not proof: explain what can be removed while preserving required behavior.
5. **Hollow tests:** tests that cannot fail, assert only on mocks, test the implementation instead of the behavior they claim, or cover nothing consequential while real paths go untested.
6. **Comments and docs vs. code:** wrong or stale comments, historical narration ("previously", "we changed"), references to plans, tickets, or phases, and comments that merely restate code. In the docs area, check every concrete claim—command, environment variable, default, path, endpoint, number, or behavior—against the implementation. Flag conflicting repetitions and filler prose. Do not treat intentional historical records such as changelogs, plans, and work logs as current implementation guidance.

### Reviewer boundaries

- Read-only: no edits, report files, git writes, or other agents. Do not fix anything, including a trivial issue.
- No paid API or model calls, purchases, deployments, or access to shared environments. The delegated review itself is authorized; do not launch additional model calls from it. Do not install dependencies or run setup, builds, integration tests, or end-to-end tests.
- Run existing unit tests or linters only when a finding depends on them, and only after checking that the command is local, safe, and does not rewrite files, snapshots, or fixtures. Otherwise use source tracing and state the limitation.
- Ignore formatting, naming preferences, generated files, and vendored code. Stay in the assigned area. Note anything outside it in one line for the orchestrator, including apparent cross-area duplication; do not audit that area yourself.
- Make one pass, then report and stop after about 40 minutes or 60 tool calls, whichever comes first. Report coverage gaps if the budget prevents completion.

### Reviewer report

Return the report as the final message, not a file. Rank findings most consequential first. For each, give:

- **Severity:** `High` for wrong behavior, a broken guarantee, or misleading documentation; `Medium` for something that will cause mistakes; `Low` for clutter.
- **Lens:** one of the six above.
- **Evidence:** exact `file:line` references with the relevant source lines quoted, plus the callers, usages, or tests checked.
- **Consequence:** the concrete effect, not a general preference.
- **Confidence:** `Established` (callers or usages checked) or `Suspected`.
- **Proposed fix:** one line; do not apply it.

List established defects separately from suspected findings and untested opinions. End with cross-area notes, coverage and gaps, and any checks actually run with their results. Say explicitly when there are no findings.

## Verify and deduplicate

7. Collect every report. If a reviewer fails or stops early, retain its actual coverage and record the gap; do not present that area as complete. End finished sessions when their reports have been collected.
8. Check every candidate finding against the current source yourself: open the cited lines, search for callers and usages, and read relevant tests. Apply the same safety limits as the reviewers to any focused checks. A reviewer's confidence label is a claim, not evidence. A suspected finding may survive only if you establish it yourself; drop unconfirmed claims, false positives, speculative concerns, and disproportionate suggestions.
9. Check every cross-area note yourself. Merge reports of the same underlying problem, including a doc claim and the code it contradicts, or both halves of a duplication. Preserve the locations needed to explain the combined finding. Assign severity by the verified consequence using the definitions above, not by the reviewer's ranking.
10. Check whether the reviewed files changed during the audit. Recheck affected evidence or disclose the resulting coverage limit. Do not overwrite anyone's changes or report stale line references as current.

## Report

11. Read `agents/reviews/_template.md`, or this skill's `assets/_template.md` if the workspace has none. Adapt a workspace template to this audit: group findings by severity, use the six lenses, mark every fix `Not fixed`, and omit fix-execution or follow-up sections. Never claim a proposed fix was applied.
12. Write a single Markdown review in `agents/reviews/YYYY-MM-DD-NNN-deslop.md`, using the next sequence for the day across that directory, as `/kreview` does. Include the repository path and revision, local-change context, area ownership and actual coverage, exclusions and material gaps, severity counts, verified findings, and checks actually run. Give findings IDs `F1`, `F2`, and so on in severity order, grouped under High, Medium, and Low. Each finding needs exact `file:line` evidence with quoted source, what is wrong, its concrete consequence, and a one-line proposed fix. Include only findings you independently established, not rejected suspicions or untested opinions. If there are no verified findings, say so without implying proof that the repository is defect-free.
13. Stage only the review file. Do not stage source changes or any pre-existing staged work. Do not commit. Give the final response and stop; do not fix anything or initiate follow-up work.

## Final response

Give the counts by severity, then one line for each High finding, and link the review. Mention any material coverage limit in one short sentence. Do not list every Medium or Low finding in chat, propose a next command, or offer to start fixes.

```markdown
Deslop audit: 2 High, 3 Medium, 1 Low. Nothing fixed.

- **F1:** Cancellation returns success while the background write continues (`src/writer.rs:42`).
- **F2:** The documented dry-run command still deploys (`docs/deploy.md:18`).

**Review:** [agents/reviews/YYYY-MM-DD-NNN-deslop.md](agents/reviews/YYYY-MM-DD-NNN-deslop.md)
```

Omit the High list when there are no High findings. If there are no verified findings, keep the zero counts, say `No verified findings. Nothing fixed.`, and link the review, retaining any coverage limitation.
