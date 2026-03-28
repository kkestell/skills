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
   - Read the plan end to end, including every linked reference and every research note under `<docs_path>/research/`.
   - Read the files listed in the plan's `Related code` section. Read them — do not skim.
   - Read `CLAUDE.md` for project-specific quality commands, conventions, and patterns.
   - The point is to ship complete work, not just produce movement. Understand the plan before touching code.
4. If anything is unclear or ambiguous after reading the plan, references, and related code, ask the user now.
   - Better to ask once before starting than to build the wrong thing. Get user approval to proceed.
   - Skip this step if the plan is clear and the path forward is obvious.
5. Verify the repo setup and baseline quality commands before major edits.
   - Confirm dependencies are installed. Run tests, lint, formatter, and type checks to establish a green baseline.
   - If the baseline is already broken, tell the user before proceeding.
6. Create a Todo list from the plan's implementation tasks.
   - Include testing tasks alongside implementation tasks.
   - Keep tasks specific and completable — each one should map to a checkable plan item.
7. Execute the plan task by task.
   - Read the related code and nearby patterns before implementing each task.
   - Implement in repo style. Match naming conventions, error handling patterns, and file organization.
   - Write or update tests for each piece of new functionality.
   - Run the relevant checks after each change.
   - Update Todo state and mark the matching plan checkbox complete (`[ ]` → `[x]`).
   - Keep the implementation aligned with the plan unless the user explicitly redirects or the plan is clearly wrong.
   - Test continuously. Fix failures as they appear instead of saving them for the end.
8. If a new repo, library, dependency, or web question blocks implementation, invoke `/research`, save the answer under `<docs_path>/research/`, and continue with the new note as input.
9. Commit each tested logical chunk using `/commit`.
   - **Commit when:** a logical unit is complete, its tests pass, and it can be described in one sentence.
   - **Do not commit when:** work is half-finished, tests are failing, or unrelated changes are mixed in.
   - Do not wait until the end to commit. Small, meaningful commits build momentum and make review easier.
10. Run the full suite before handoff.
    - Run tests, lint, formatter, and type checks as applicable.
    - Use the commands from `CLAUDE.md`, not ad hoc substitutes.
11. Commit any remaining tested work.
12. Report what shipped, quality-check results, commit summary, branch name, and any follow-up work.
13. Then offer `/verify` or `/end-task`.

## Principles

- **Start fast** — clarify once, then execute.
- **The plan is your guide** — follow its references, don't reinvent.
- **Test as you go** — continuous testing prevents big surprises.
- **Commit frequently** — small, tested, logical chunks.
- **Ship complete features** — don't leave things 80% done.
