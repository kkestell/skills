---
name: kwork
description: "Execute a repository plan end to end, validate it, and commit the completed slice."
argument-hint: "[plan, specification, or todo file path]"
---

## Workflow

### Pre-flight

1. Resolve `<input_document> $ARGUMENTS </input_document>`.
   - Prefer `eng/plans/` for plans and `eng/todo/` for tracked follow-up work.
   - If none is supplied, use repository ordering and current state to identify
     the next clearly unimplemented plan. Ask only when more than one candidate
     remains plausible.
2. Check `git status`.
   - The input document is expected task input and belongs in the final commit.
   - Stop for any other staged, unstaged, or untracked paths unless the user
     explicitly authorizes continuing with them.

### Implement

3. Read the work document completely, then inspect only the related code and
   nearby patterns needed to execute it.
4. Turn its implementation and test bullets into a short working checklist. Skip
   a separate todo tool when the plan is already small enough to track directly.
5. Implement the slice.
   - Follow the plan and repository guidance.
   - Write focused tests through public boundaries, emphasizing edge cases,
     failures, and semantic boundaries.
   - Ask the user only when the plan and its authoritative sources leave a
     material decision unresolved.
   - Keep tool output targeted. Batch independent reads and checks when useful.

### Validate

6. Run focused checks while implementing.
7. When the slice is complete, choose final checks in proportion to what
   changed.
   - Run the repository's broad format, lint, type, test, and example gates when
     production behavior, generated artifacts, interfaces, or build outputs
     could plausibly change.
   - For documentation-only, filename-only, and test-only changes, run focused
     checks and inspect the diff unless repository guidance explicitly requires
     broader validation for that change category.
   - Fix failures before committing.
   - Do not repeat passing broad gates unless later changes could affect them.
8. Do not run a plan review or post-implementation review and do not spawn a
   review agent. Review is performed once across the completed milestone with
   `kreview`.

### Commit and hand off

9. Commit the complete, passing slice with no AI attribution unless the
   repository requires it.
10. Report what shipped, the validation results, commit summary, branch, and any
    unresolved follow-up.

## Principles

- **Use the plan as an index** — follow its source links and tasks without
  recreating the planning exploration.
- **Validate proportionately** — focused checks prove narrow changes; broad
  gates prove changes that can affect production behavior or outputs.
- **Defer review to the milestone** — individual slices stay cheap while the
  cumulative result still receives an independent review.
- **Ship complete slices** — leave the repository passing and committable.
