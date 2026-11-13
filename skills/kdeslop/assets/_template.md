# Deslop audit

Delete placeholder text and unused sections, including this guidance. Include only independently verified findings. Group them under High, Medium, and Low, with IDs `F1`, `F2`, and so on in severity order. All fixes are `Not fixed`; proposed fixes are recommendations, not work performed.

Severity:

- `High`: wrong behavior, a broken guarantee, or misleading documentation.
- `Medium`: will cause mistakes.
- `Low`: clutter.

Lenses: Dead code, Duplication, Broken guarantees, Over-engineering, Hollow tests, Comments and docs vs. code.

## Scope and coverage

- **Repository:** absolute path.
- **Revision:** HEAD commit, or state that there is no HEAD.
- **Working tree:** local changes reviewed, and any changes during the audit that limit the evidence.

| Area | Owned directories and files | Actual coverage and gaps |
| ---- | --------------------------- | ------------------------ |
| Docs | README.md, docs/            | What was checked         |

State exclusions and material gaps, including incomplete reviewer passes and unverified documentation claims. Do not imply complete coverage when the audit was partial.

## Summary

High: 0 · Medium: 0 · Low: 0. Nothing fixed.

| ID | Severity | Lens              | Fix       | Title                          | Location           |
| -- | -------- | ----------------- | --------- | ------------------------------ | ------------------ |
| F1 | High     | Broken guarantees | Not fixed | Cancellation leaves work alive | `src/writer.rs:42` |

If there are no verified findings, replace the table with `No verified findings.` and omit the severity sections. This is not proof that the repository is defect-free.

## High

### F1. Cancellation leaves work alive

High · Broken guarantees · Not fixed · `src/writer.rs:42`

**What's wrong:** Describe the verified problem plainly.

**Consequence:** State the reachable effect and who or what it affects.

**Evidence:** Quote the relevant source lines with exact file and line references. Explain how the orchestrator verified the claim, including callers, usages, and relevant tests checked. Include both sides of a contradiction or duplication when needed.

**Proposed fix:** One line describing the smallest proportionate change; not applied.

## Medium

Use the same finding format. Omit this section if empty.

## Low

Use the same finding format. Omit this section if empty.

## Checks run

List only checks actually run and their results, distinguishing reviewer checks from the orchestrator's independent verification. State when verification was source-only. Put unavailable checks and their effect on confidence in coverage gaps, not in the findings as speculation.

## Verdict

Summarize the verified result and its material limits. Nothing was fixed. Do not add a follow-up plan or next command.
