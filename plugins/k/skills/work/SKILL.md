---
name: work
description: "Execute a repo plan end to end: implement, test continuously, update plan checkboxes, commit logical chunks, and prepare the branch for `/verify` or `/end-task`."
argument-hint: "[plan file, specification, or todo file path]"
disable-model-invocation: true
---

## Workflow

1. Read `.k/current_task.json`; if it is missing, stop and tell the user to run `/start-task`.
2. Resolve `<input_document> $ARGUMENTS </input_document>` or default to `<docs_path>/plan.md`.
3. Read the work doc completely.
   - Read linked references and relevant notes under `<docs_path>/research/`.
   - Start fast, but do not skip understanding the plan. The point is to ship complete work, not just produce movement.
   - Use the plan's `Related code` section and `CLAUDE.md` as the default guide rails before inventing new patterns.
4. Ask clarifying questions only if a true blocker remains after reading the docs and related code.
5. Verify the repo setup and baseline quality commands before major edits.
6. Create a Todo list for implementation, tests, and validation.
7. Execute the plan task by task.
   - Read the related code and nearby patterns.
   - Implement in repo style.
   - Add or update tests.
   - Run the relevant checks.
   - Update Todo state.
   - Mark the matching plan checkbox complete.
   - Keep the implementation aligned with the plan unless the user explicitly redirects or the plan is clearly wrong.
   - Test continuously. Fix failures as they appear instead of saving them for the end.
8. If a new repo, library, dependency, or web question blocks implementation, invoke `/research`, save the answer under `<docs_path>/research/`, and continue with the new note as input.
9. Commit each tested logical chunk using `/commit`.
   - Commit early and often when a tested logical unit is complete.
   - Do not commit half-finished work, failing work, or unrelated edits in the same changeset.
10. Run the full suite before handoff.
   - Run tests, lint, formatter, and type checks as applicable.
11. Commit any remaining tested work.
12. Report what shipped, quality-check results, commit summary, branch name, and any follow-up work.
13. Then offer `/verify` or `/end-task`.
