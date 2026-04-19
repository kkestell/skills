---
name: kreview
description: "Run independent completeness and test-quality review passes over a body of work."
metadata:
  argument-hint: "[plan path] --files [changed files] --tasks [completed tasks]"
  disable-model-invocation: "true"
---

## Workflow

### Input

1. Resolve the review inputs from `<input_document> $ARGUMENTS </input_document>`:
   - **Plan path**: repo-relative path to the implementation plan.
   - **Tasks completed**: bullet list of what was implemented.
   - **Files changed**: repo-relative paths of all implementation and test files added or modified.
   - If any of these are missing, ask the user to provide them before proceeding.

### Completeness Review

2. Run a completeness review over the full body of work.
   - Prefer running in a parallel subagent; otherwise perform locally.
   - Subagents start with fresh context, so include all necessary context in the review prompt.
   - Build the review prompt by reading `assets/completeness-review-prompt.md`, then filling in the specifics of the full plan.
   - The reviewer reads the plan and all changed files, then evaluates whether the work is genuinely complete with no omissions, hacks, disabled warnings, or workarounds. The reviewer should assume that the code builds and the tests pass and should not verify this itself.

### Test Quality Review

3. Run a test quality review over the tests.
   - Prefer running in a parallel subagent; otherwise perform locally.
   - Subagents start with fresh context, so include all necessary context in the review prompt.
   - Build the review prompt by reading `assets/test-quality-review-prompt.md`, then filling in the specifics.
   - The reviewer reads the implementation and tests, then evaluates whether the tests verify real behavior, cover edge cases, and would actually catch bugs.
   - Steps 2 and 3 can run in parallel when subagents are available.

### Act on Findings

4. Evaluate review results.
   - If either reviewer reports issues worth fixing: report them to the caller so they can be fixed.
   - If both reviewers pass, report success.
5. Return a structured summary:
   - Verdict from each review (PASS or ISSUES FOUND).
   - Combined list of issues (if any), with file paths, line numbers, and suggested fixes.

## Principles

- **Independent** — reviews must be free from the biases of the implementer. Subagents start fresh.
- **Honest** — a false "pass" is worse than a nit. Flag real problems, don't rubber-stamp.
- **Concise** — only flag things that actually matter: real omissions, real hacks, real correctness problems. Do not pad with style nits or cosmetic suggestions.
