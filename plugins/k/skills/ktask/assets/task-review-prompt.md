# Task Review — Prompt Template

This is a prompt framework for a lightweight review of a one-off task.
When launching a helper reviewer or running the pass locally, read this file, then compose the actual prompt
by filling in the concrete details for the completed task.

---

## Preamble (copy and adapt)

You are reviewing a small, completed task for correctness and completeness.
Your job is to answer two questions: **was the task actually done, and is the code sound?**
Be honest but concise. This is not a full architectural review.

## Context (fill in)

- **Task description**: (what the user asked for)
- **Files changed**: (repo-relative paths of all files added or modified)
- **Project guidance docs**: (paths to repo-specific guidance such as `CLAUDE.md`, `AGENTS.md`, or `README`)

## Instructions (copy verbatim)

1. Read every changed file end to end.
2. Evaluate the work against the criteria below.

## What to look for

### Completeness

- Does the code actually accomplish what the task description asked for?
- Is anything missing, stubbed, or deferred without explanation?

### Correctness

- Are there obvious bugs — wrong logic, missing null checks, off-by-one errors, race conditions?
- Does error handling follow the project's conventions?

### Style and conventions

- Does the code match the surrounding patterns — naming, formatting, commenting style?
- Are comments explaining "why" rather than just "what"?

### Tests

- Are there tests for the changed behavior?
- Do the tests verify real behavior or just mirror the implementation?

## Output format

Write a brief, structured report:

1. **Verdict**: `PASS` or `ISSUES FOUND`
2. **Summary**: One or two sentences — your honest assessment.
3. **Issues** (only if verdict is ISSUES FOUND): Numbered list, each with:
   - What the issue is
   - Where it is (file path and line or area)
   - Why it matters
   - Suggested fix

Be concise. Only flag real problems — bugs, omissions, missing tests.
Do not pad with style nits or cosmetic suggestions.
