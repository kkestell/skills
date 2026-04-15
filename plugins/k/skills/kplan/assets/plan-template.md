# <Plan Title>

Use this template as a scaffold, not a cage. Drop sections that do not apply, expand the ones that matter, and add sections when the work needs more structure.

## Goal

## Desired outcome

## How we got here

Brief summary of the brainstorming process: the problem framing, key assumptions validated with the user, and why this approach was chosen over alternatives.

## Summary of approach

A high level summary of the implementation approach, including the major components of the change and how they interact. This should be a concise overview that gives a clear picture of the plan without needing to read the details below.

## Related code

- `path/to/file` — Why this file or pattern matters

## Current state

- Relevant existing behavior:
- Existing patterns to follow:
- Constraints from the current implementation:

## Structural considerations

How the change fits the existing architecture. Note any PHAME concerns (hierarchy, abstraction, modularization, encapsulation) and how the plan addresses them.

## Refactoring

Refactoring needed before or during the feature work, and what each refactor achieves structurally. Omit if none needed.

## Research

Summarize findings that matter for this plan.

### Repo findings

- Finding:

### External research

- Source:
- Why it matters:

## Test plan

Define what to test and at what level before listing implementation tasks. Focus on tests that earn their keep: edge cases, error paths, and boundary conditions — not happy-path tests that merely restate the implementation. Tests should target public interfaces so they stay useful through refactors.

- **Key behaviors to verify**: (what the feature should do, expressed as testable assertions against public interfaces)
- **Test levels**: (unit, integration, e2e — which level covers what, and why that level is the right one)
- **Edge cases and failure modes**: (boundary conditions, error paths, concurrency concerns, malformed input — this is the most important part)
- **What NOT to test**: (happy paths that just mirror implementation, framework guarantees, internal details that would break on refactor)

## Implementation plan

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Impact assessment

- Code paths affected:
- Data or schema impact:
- Dependency or API impact:

## Validation

- Tests:
- Lint/format/typecheck:
- Manual verification:

## Gaps and follow-up

Features or functionality this plan depends on but cannot deliver. Stub follow-up docs for these live in `!`echo ~/.k/workspaces/${PWD//\//_}`/todo/YYYY-MM-DD-NNN-slug.md` if created.

- Gap:
- Follow-up:

## Open questions

Questions that need user input before implementation can proceed. When the user answers a question, fold the decision into the relevant section of the plan and delete the question. This section should shrink over time and be removed entirely once all questions are resolved.

- Question:
