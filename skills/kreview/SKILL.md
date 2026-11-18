---
name: kreview
description: "Review code in staged changes, a diff, branch, commit, or specified files, fix every finding after asking the user for any decision a fix needs, write a review in `.agents/reviews/`, and stage the review and fixes. Do not use for plan critiques or standalone documentation reviews. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it."
argument-hint: "[review scope]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Review the code the user names, fix every finding, and stage the fixes. Decide every fix yourself except one that raises a product question, which the user decides.

Correctness matters for what happens in normal use. Handling every case that could occur does not.

This skill and `.agents/reviews/` are for code reviews. Plan critiques and standalone documentation reviews are outside its scope. Read plans and documentation as context for code under review.

## Choose what to review

1. Read `<review_scope> $ARGUMENTS </review_scope>`. Ask for clarification only when the answer would change what you review.
2. For staged changes, a diff, a branch, or a commit, inspect the changes and the code that calls or depends on them. For named files, directories, or the whole codebase, review that full scope. For a feature review, check other code the feature needs, even when it is outside the diff.

## Review

3. Trace behavior through callers, state changes, resource lifetimes, and tests. Judge implementation choices by their purpose and consequence. Do not treat a language feature or coding pattern as a defect on its own.
4. Read the requirements that define the behavior. If the user has approved a new design, review against that design. When the scope or the changes under review include a brief in `.agents/briefs/`, or a plan that links one, read the brief and check that the change delivers its Outcome, keeps each of its Decisions, and leaves out what it puts Out of scope. Report each gap as an `Intent` finding. A decision the user approved later, such as a changed Check your assumptions entry in the plan, overrides the brief. Flag complex or expensive code that adds no required behavior, including defensive or speculative code: redundant checks, fallbacks, retries, and recovery for failures that have not happened.
5. Confirm each suspected bug by tracing the code, reproducing the behavior, or running a focused check before reporting it. If you cannot confirm it, leave it out. Do not report missing defensive code, and do not ask for tests of hypothetical edge cases. Choose checks that fit the repository. Do not require a fixed set of commands, and stay within the requested scope. Say when you reviewed only part of the code. Do not change the code under review until Fix. Revert any edit a check needs before you finish.
6. Run each test the change adds against the code before the change, in a detached worktree of the base revision, and remove the worktree afterwards. A new test that passes there checks nothing the change did: report it as a `Testing` finding and fix it by deleting the test or making it assert the change's behavior. A test that cannot build against the base revision, because it uses an interface the change adds, needs no run. A new test whose case an existing test's setup already reaches is also a `Testing` finding; fix it by moving its assertions into that test.
7. When the repository's language has a mutation-testing tool that can limit itself to a diff, such as `cargo mutants --in-diff` for Rust, run it on the change. A mutant that survives in changed code and alters required behavior is a `Testing` finding; fix it with an assertion in an existing test whose setup reaches the case, or with a new test only when none does. Ignore mutants that change no behavior.

## Classify

8. Mark each finding's fix with one of two labels:
   - `Trivial`: the fix needs no decision from the user.
   - `Needs decision`: the fix raises a product question, a choice that changes what the user sees or does in everyday use of the product, and the requirements, brief, plan, and approved decisions do not settle it.

   Design, interface, and internal behavior choices are yours, and so is how a rare case behaves, such as a race, a crash, failures that coincide, or a state everyday use does not reach. Handle rare cases the simplest reasonable way. Severity, size, and file count alone do not make a fix non-trivial. An `Intent` fix is `Trivial` when the brief settles how to close the gap.

## Fix

9. Fix every `Trivial` finding. If a fix turns out to need a decision, revert it and mark the finding `Needs decision`.
10. Ask the user to decide each `Needs decision` finding, one focused question at a time, and wait for the answer. Ask as the user experiences the product: what they would see happen, the options as they would experience them, and a recommendation. Leave out code names and internal mechanisms. The user should be able to answer without reading the code.
11. Fix each `Needs decision` finding as the user decided.
12. Validate the fixes. Fix failures before continuing. Change each finding's label to `Fixed`.

## Report

13. Read `.agents/reviews/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the review in `.agents/reviews/`. Name the file `YYYY-MM-DD-NNN-slug.md`, using the next sequence for the day.
14. State the scope, the brief you checked against if any, and significant gaps in coverage. Give every finding an ID in severity order, most severe first, and list it in the summary table with its fix label. Give each finding its own section with its severity, category, fix label, source location, what can happen, the evidence, and the fix. The fix is the change you made, and for a finding that needed a decision, the decision the user made. Record the checks you ran. If there are no findings, say so. End with a short verdict.

## Stage

15. Stage the review and the fixes. Do not stage anything else. Do not commit.
16. Give the final response and stop.

## Final response

When the review is staged, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed, the suspected bugs you ruled out, and the steps you took.

```markdown
One or two sentences giving the verdict and the number of findings by severity.

| ID | Severity | Fix   | Title                           | Location           |
| -- | -------- | ----- | ------------------------------- | ------------------ |
| F1 | High     | Fixed | Parser drops the final token    | `src/parser.rs:42` |
| F2 | Medium   | Fixed | Retry loop hides the real error | `src/fetch.rs:88`  |

**Review:** `.agents/reviews/YYYY-MM-DD-NNN-slug.md` · **Lines:** code +80 / −40 (net +40) · tests +30 / −10 (net +20)

**Files:**

- `.agents/reviews/YYYY-MM-DD-NNN-slug.md` (created)
- `src/fetch.rs` (modified)
- `src/parser.rs` (modified)

**Next:** `/kexplain staged changes`
```

The table lists every finding, most severe first. If there are none, replace the table with `No findings.` Count the lines of the change under review with its fixes, excluding `.agents/`, from `git diff --numstat` over the reviewed scope. Count lines in test files and in inline test modules as tests, and the rest as code. List every file the review created or modified, marked `(created)` or `(modified)`. If a work log in `.agents/work/` names the plan the review covers, add `/ktelemetry <plan path>` as a second Next line after `/kexplain staged changes`.
