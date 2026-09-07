---
name: kwork
description: "Execute a repository plan with focused checks and validate the integrated feature at its completion boundary."
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
   - Preserve unrelated changes. Continue from earlier implementation steps.
   - Ask only when overlapping changes leave ownership or intended behavior
     unclear.

### Implement

3. Read the work document completely, then inspect only the related code and
   nearby patterns needed to execute it.
4. Turn its implementation and test bullets into a short working checklist. Skip
   a separate todo tool when the plan is already small enough to track directly.
5. Implement the plan.
   - Treat the feature or milestone as the completion boundary. Intermediate
     plans may leave integration unfinished; preserve existing supported
     behavior and record what remains.
   - Keep architecture coherent as the feature develops. Add temporary guards
     only when needed to prevent incorrect behavior.
   - Follow the plan and repository guidance.
   - Write focused tests through public boundaries, emphasizing edge cases,
     failures, and semantic boundaries.
   - Ask the user only when the plan and its authoritative sources leave a
     material decision unresolved.
   - Keep tool output targeted. Batch independent reads and checks when useful.

### Validate

6. Run focused checks while implementing.
7. Choose checks in proportion to risk and the completion boundary.
   - Use focused tests and checks for intermediate plans.
   - Run the repository's broad gates when the feature or milestone is
     integrated. Run them earlier when a concrete regression risk warrants it or
     repository instructions explicitly require it.
   - For documentation-only, filename-only, and test-only changes, run focused
     checks and inspect the diff unless repository guidance explicitly requires
     broader validation for that change category.
   - Fix regressions. Report expected failures from unfinished integration
     explicitly; do not claim the feature is complete while they remain.
   - Do not repeat passing broad gates unless later changes could affect them.
8. Do not run a plan review or post-implementation review and do not spawn a
   review agent. Review is performed once across the completed milestone with
   `kreview`.

### Commit and hand off

9. Commit only when authorized by the user and allowed by repository guidance. A
   plan boundary does not require a commit.
10. Report what changed, checks run, and any unfinished integration. Distinguish
    completion of an intermediate plan from completion of the feature.

## Principles

- **Use the plan as an index** — follow its source links and tasks without
  recreating the planning exploration.
- **Validate proportionately** — use focused checks during implementation and
  broad gates at the feature or milestone boundary.
- **Defer review to the milestone** — individual slices stay cheap while the
  cumulative result still receives an independent review.
- **Complete integrated features** — plans organize progress; the feature or
  milestone owns completion.
