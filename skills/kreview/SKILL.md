---
name: kreview
description: "Review code in staged changes, a diff, branch, commit, or specified files, fix every finding after asking the user for any decision a fix needs, write a review in `agents/reviews/`, and stage the review and fixes. Do not use for plan critiques or standalone documentation reviews. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it."
argument-hint: "[review scope]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Review the code the user names, fix every finding, and stage the fixes. Fix trivial findings directly, and ask the user to decide the rest before fixing them.

This skill and `agents/reviews/` are for code reviews. Plan critiques and standalone documentation reviews are outside its scope. Read plans and documentation as context for code under review.

## Choose what to review

1. Read `<review_scope> $ARGUMENTS </review_scope>`. Ask for clarification only when the answer would change what you review.
2. For staged changes, a diff, a branch, or a commit, inspect the changes and the code that calls or depends on them. For named files, directories, or the whole codebase, review that full scope. For a feature review, check other code the feature needs, even when it is outside the diff.

## Review

3. Trace behavior through callers, state changes, resource lifetimes, and tests. Judge implementation choices by their purpose and consequence. Do not treat a language feature or coding pattern as a defect on its own.
4. Read the requirements that define the behavior. If the user has approved a new design, review against that design. Flag complex or expensive code that adds no required behavior.
5. Confirm each suspected bug by tracing the code, reproducing the behavior, or running a focused check before reporting it. If you cannot confirm it, leave it out. Choose checks that fit the repository. Do not require a fixed set of commands, and stay within the requested scope. Say when you reviewed only part of the code. Do not change the code under review until Fix. Revert any edit a check needs before you finish.

## Classify

6. Mark each finding's fix with one of two labels:
   - `Trivial`: the fix needs no decision from the user.
   - `Needs decision`: a behavior, design, or interface choice remains unresolved.

   Use requirements, existing plans, and approved decisions to establish the intended behavior before deciding a fix needs a new decision. Severity, size, and file count alone do not make a fix non-trivial.

## Fix

7. Fix every `Trivial` finding. If a fix turns out to need a decision, revert it and mark the finding `Needs decision`.
8. Ask the user to decide each `Needs decision` finding, one focused question at a time, and wait for the answer. For each, say what can happen, then give the options, their trade-offs, and a recommendation. Speak clearly and simply.
9. Fix each `Needs decision` finding as the user decided.
10. Validate the fixes. Fix failures before continuing. Change each finding's label to `Fixed`.

## Report

11. Read `agents/reviews/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the review in `agents/reviews/`. Name the file `YYYY-MM-DD-NNN-slug.md`, using the next sequence for the day.
12. State the scope and significant gaps in coverage. Give every finding an ID in severity order, most severe first, and list it in the summary table with its fix label. Give each finding its own section with its severity, category, fix label, source location, what can happen, the evidence, and the fix. The fix is the change you made, and for a finding that needed a decision, the decision the user made. Record the checks you ran. If there are no findings, say so. End with a short verdict.

## Stage

13. Stage the review and the fixes. Do not stage anything else. Do not commit.
14. Give the final response and stop.

## Final response

When the review is staged, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed, the suspected bugs you ruled out, and the steps you took.

```markdown
One or two sentences giving the verdict and the number of findings by severity.

| ID | Severity | Fix   | Title                           | Location           |
| -- | -------- | ----- | ------------------------------- | ------------------ |
| F1 | High     | Fixed | Parser drops the final token    | `src/parser.rs:42` |
| F2 | Medium   | Fixed | Retry loop hides the real error | `src/fetch.rs:88`  |

**Review:** `agents/reviews/YYYY-MM-DD-NNN-slug.md`

**Files:**

- `agents/reviews/YYYY-MM-DD-NNN-slug.md` (created)
- `src/fetch.rs` (modified)
- `src/parser.rs` (modified)

**Next:** `/kexplain staged changes`
```

The table lists every finding, most severe first. If there are none, replace the table with `No findings.` List every file the review created or modified, marked `(created)` or `(modified)`.
