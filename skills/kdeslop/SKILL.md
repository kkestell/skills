---
name: kdeslop
description: "Audit the current repository for dead code, duplication, broken guarantees, over-engineering, hollow tests, and misleading comments or docs. Delegate parallel area reviews, independently verify and deduplicate findings, and write and stage a review in `.agents/reviews/` without fixing anything. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it."
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Find consequential defects and unnecessary complexity. Reviewers gather candidates. You decide which concerns share a cause, how much they matter, and what the project should do about them. Audit the current repository, not just a diff. Judge the work by its behavior and evidence, not by guesses about AI authorship. Do not limit the audit to files known to have been written by an agent.

Nothing gets fixed. The only file you create or change is the final review; stage only that file. Do not invoke `/kreview`'s fix workflow, commit, or start follow-up work.

## Carve up the repository

1. Locate the repository in the current directory. Record its absolute path, HEAD commit, and working-tree status. Review the current working tree, including local changes, without modifying or discarding them; distinguish local changes from HEAD in the report. If there is no HEAD commit, record that fact rather than inventing a revision.
2. Read the README, applicable agent instructions such as `AGENTS.md` and `CLAUDE.md`, and the build and test configuration. Read any project defect policy, known-issue register, and relevant previous review. When a later fix is cited as a miss, check whether the defect existed at the reviewed revision and whether the report had already identified it. Use a verified miss to guide the relevant workflow assignment. Inventory the hand-written source, tests, docs, scripts, and configuration. Skip generated files, lockfiles, vendored code, and data.
3. Split the repository into at most 10 areas along real boundaries and keep tests with the code they exercise. Assign docs, scripts and configuration where their claims can be checked. Give every in-scope file an owner. Identify the consequential workflows that cross those areas and name one reviewer to follow each from its normal entry point through to the outcome. Group related workflows into the same assignment where practical.
4. Keep the areas small enough for a single pass. If the repository cannot fit within 10 bounded passes, prioritize consequential areas and explicitly record the files or directories left uncovered. Never imply that a partial audit covered the whole repository.

## Fan out

5. Start one fresh reviewer per area and run them in parallel. Use separate agent sessions when available, otherwise subagents. Use the current checkout read-only, not new worktrees that omit local changes. In Hypercube, pass the repository's absolute path as `dir` and the full brief as the session message. If neither sessions nor subagents are available, tell the user the parallel audit cannot run and stop rather than silently substituting a solo audit.
6. Give each reviewer a self-contained brief. Include the lenses and boundaries below in full; do not assume it inherits this skill or your conversation. Supply:
   - The absolute repository path and HEAD commit (or lack of one), any local changes relevant to its area, a two-sentence project description, and orientation files to read first, including applicable project review and triage rules.
   - Its owned files and workflows, their entry points, and any audit exclusions. The workflow owner can read the implementation and tests on either side of a handoff.
   - All six lenses, plus any specific suspicions worth investigating. Suspicions are leads, not findings to validate at any cost.
   - The reviewer boundaries, time and tool-call budget, and report format below.

### Lenses

Each reviewer covers every lens in its area:

1. **Dead code:** unused functions, exports, branches, files, settings, environment variables, flags, CLI options, build targets, DTO fields, and CSS rules. Check callers and dynamic discovery before calling something unused.
2. **Duplication:** logic implemented twice, near-copies that have drifted, or parallel tools and scripts that do the same job. Similar syntax alone is not a defect; show the needless maintenance or behavioral consequence.
3. **Broken guarantees:** Trace what a caller is entitled to expect through the code that actually delivers the result. At a handoff, follow what each side receives, when the action takes effect, and what the caller sees on success or failure. Choose paths supported by the code, ordinary use or prior failures. Include plain bugs even when the project has no written guarantee.
4. **Over-engineering:** abstractions, options, fallbacks, or configurability with one caller or no real use; defensive handling of impossible cases; indirection that only forwards calls. One caller alone is not proof: explain what can be removed while preserving required behavior.
5. **Hollow tests:** Compare the path the test drives and the outcome it observes with the behavior it claims. A test that supplies a downstream component with an already-correct value can pass while the real caller supplies a different one. Explain which failure could still pass and why it matters.
6. **Comments and docs vs. code:** wrong or stale comments, historical narration ("previously", "we changed"), references to plans, tickets, or phases, and comments that merely restate code. Check operational instructions and promises against the implementation. Explain the consequence of a discrepancy for someone relying on the document. Do not treat intentional historical records such as changelogs, plans, and work logs as current implementation guidance.

### Reviewer boundaries

- Read-only: no edits, report files, git writes, or other agents. Do not fix anything, including a trivial issue.
- No paid calls, purchases, deployments, or shared environments. The delegated review itself is authorized. When a consequential conclusion turns on runtime behavior, use the smallest permitted local check that reaches it. An existing integration test or a disposable local probe can qualify. Respect project instructions and keep test state and generated output out of the checkout. Where the check cannot run, state exactly what remains unverified.
- Ignore formatting, naming preferences, generated files, and vendored code. Follow assigned workflows across file boundaries. Send unrelated leads to their owner through the orchestrator.
- Make one pass, then report and stop after about 40 minutes or 60 tool calls, whichever comes first. Report coverage gaps if the budget prevents completion.

### Reviewer report

Return candidates in the final message. For each, name its lens, quote exact source locations, and identify the callers or tests checked. For behavior, give the reachable trigger, the owner of the relevant state, the outcome and the requirement it breaks. For maintainability, show what a reader has to reason about or keep in sync and what could be removed. Distinguish live observation, reproduction, and source tracing. Keep unresolved leads separate. Close with cross-area notes, actual coverage, gaps and checks. A pass may have no findings.

## Verify and weigh findings

7. Collect every report. Retain the actual coverage of incomplete passes and end finished sessions.
8. Recheck candidates against the current source, callers and tests, including guards and recovery. Account for each assigned workflow from its entry point to its observable outcome. If both area reports stop at the same interface, follow the handoff yourself or identify the gap. Classify confirmed defects under the project's fix policy after establishing their consequences. Respect existing dispositions unless the evidence changes their rationale.
9. Count independent problems. Group symptoms when the same ownership decision or correction explains them, even across files or review areas. Keep separate failures distinct when they need independent decisions. When a fix moved a responsibility, check who owns it before, during and after the transition.
   - **Severity** reflects credible impact and circumstances. High covers serious consequences such as loss of user work, unintended authority or substantial disruption. Medium covers material but bounded failures, misleading verification or recurring maintenance costs. Low covers minor defects and local cleanup with a concrete benefit. A broken assertion or inaccurate sentence alone does not determine severity.
   - **Origin** is relative to a named baseline, usually the last reviewed revision. Check the earlier behavior before calling something introduced, worsened or pre-existing. A previously unreported problem can be old. Say when origin is unknown or a group contains both old and new symptoms.
   - **Disposition** follows the repository's threshold and the cost of the remedy. Promote a candidate to a finding when you can recommend a proportionate change on its own merits. Include incidental cleanup with a finding only when it materially informs the same correction. Omit observations whose only rationale is that someone may touch the file later. Respect the audit's read-only boundary for all dispositions.

10. Check whether the reviewed files changed during the audit. Recheck affected evidence or disclose the resulting coverage limit. Do not overwrite anyone's changes or report stale line references as current.

## Report

11. Read `.agents/reviews/_template.md`, or this skill's `assets/_template.md` if the workspace has none. Adapt it to the audit. Write one review in `.agents/reviews/YYYY-MM-DD-NNN-deslop.md` using the next sequence for the day. Include the revision, working tree, comparison baseline, actual area coverage, exclusions, gaps and checks.
12. Count and rank only the findings that warrant a change. When the project requires tracking other confirmed defects, give them a concise, separate, uncounted record within the authorized scope. Give each group an ID in severity order, its lens, origin, evidence, consequence and disposition. Quote exact source locations. Describe a proportionate correction where one is called for. Group evidence under the decision it supports. State that nothing was fixed. If there are no verified findings, say so.
13. Stage only the review file. Preserve existing staged work. Do not commit, fix anything, or initiate follow-up work.

## Final response

Give the counts by severity and the main disposition. Use one line for each High group, link the review, and mention any material coverage limit. Attribute regressions only to the comparison actually checked. When all counts are zero, say `No findings warrant a change. Nothing fixed.`
