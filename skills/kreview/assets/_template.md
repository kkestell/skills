# Review title

Delete placeholder text and unused sections, including this guidance. Give every finding an ID in severity order, most severe first: `F1`, `F2`, and so on. Each finding gets its own section. Do not put findings in bullets, and do not nest them under severity or category headings.

Every finding is fixed during the review, so its fix label is `Fixed`.

Severity describes the cost of leaving the finding unfixed. The levels, most severe first:

- `High`: wrong results, lost or corrupted data, a crash, or a security hole that normal use can trigger.
- `Medium`: wrong behavior that only an uncommon but realistic case triggers, or code that makes future changes materially riskier or more expensive.
- `Low`: an unlikely edge case, fixed with a comment naming it, or no effect on behavior and little effect on future changes, such as unclear naming, stale comments, or minor duplication.

Categories:

- `Correctness`: required behavior and reachable state changes.
- `Error handling`: failures, useful errors, cancellation, and partial effects.
- `Resources`: resource ownership, lifetime, and cleanup.
- `Concurrency`: shared state, task lifetime, and cancellation.
- `Security`: trust boundaries, permissions, and secrets.
- `Performance`: material costs for realistic inputs.
- `API design`: caller contracts and shared interfaces.
- `Architecture`: responsibilities, dependencies, and needless complexity.
- `Dependencies`: library choices and integration costs.
- `Simplicity`: less code and fewer concepts with behavior preserved.
- `Readability`: clear control flow and local reasoning.
- `Naming`: clear and consistent vocabulary.
- `Comments`: useful explanations of intent, constraints, and consequences in the code.
- `Documentation`: caller guidance and design documents associated with the code under review.
- `Testing`: behavior coverage and reliable assertions.

## Scope and coverage

State what you reviewed in a short paragraph.

Gaps:

- List each material gap in coverage.

## Summary

| ID | Severity | Category    | Fix   | Title                                |
| -- | -------- | ----------- | ----- | ------------------------------------ |
| F1 | High     | Correctness | Fixed | Parser drops the final token         |
| F2 | Low      | Resources   | Fixed | Unclosed file handle on early return |

If there are no findings, replace the table with `No findings.` and omit the finding sections.

## F1. Parser drops the final token

High · Correctness · Fixed · `src/parser.rs:42`

What happens, when, and what it affects, in short paragraphs. Use a list only for a real enumeration, such as several locations.

### Evidence

How you confirmed it: the trace, reproduction, test, or output. Omit this section when there is nothing beyond the description.

### Fix

The change you made. If the fix needed a decision, the decision the user made.

## Checks run

- List the checks you actually ran and their results.

## Verdict

Summarize the review result, referring to findings by ID.
