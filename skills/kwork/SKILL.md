---
name: kwork
description: "Execute a repo plan end to end: implement, validate with independent review passes, and commit at the end."
argument-hint: "[plan, specification, or todo file path]"
---

## Workflow

### Pre-flight

1. Resolve `<input_document> $ARGUMENTS </input_document>` before checking the
   worktree.
   - Prefer `eng/plans/` for implementation plans and `eng/todo/` for tracked
     follow-up work.
   - If no input is supplied, inspect the preferred plan directory and the
     repository state to find a plan whose work has not been implemented. Use
     project-defined ordering when it exists; otherwise prefer the oldest plan
     that is clearly still outstanding. Read enough of each likely plan and the
     related code or history to distinguish an outstanding plan from one that
     was already completed.
   - When one plan is the unambiguous next choice, state the selected path and
     evidence that it remains unimplemented, then continue without asking for
     confirmation. If the selection remains ambiguous, state the candidates and
     ask the user which document to execute. If no outstanding plan can be
     identified, say so and ask which document to execute.
2. Check the git worktree with `git status` and classify every reported path.
   - Changes to the resolved input document are expected task input, not
     unrelated dirty state. This includes an untracked plan, specification, or
     todo file supplied by the user. Continue without asking for confirmation,
     preserve the document, and include it in the final commit.
   - Never suggest committing separately, ignoring, or stashing the input
     document merely to make the pre-flight check clean.
   - If there are staged changes, unstaged changes, or untracked files other
     than the input document, stop and report those paths to the user.
   - Offer to commit, ignore, or stash only the unrelated changes, as
     appropriate. Do not proceed until those paths are clean or the user
     explicitly authorizes continuing with them.

### Orientation

3. Read the work doc completely.
4. If anything is unclear or ambiguous after reading the plan, references, and
   related code, ask the user now.
   - Better to ask once before starting than to build the wrong thing. Get user
     approval to proceed.
   - Skip this step if the plan is clear and the path forward is obvious.
5. Create a Todo list from the plan's implementation tasks.
   - Include testing tasks alongside implementation tasks.
   - Keep tasks specific and completable — each one should map to a plan item.

### Execution

6. Execute the plan task by task.
   - Read the related code and nearby patterns before implementing each task.
   - Implement in repo style. Match naming conventions, error handling patterns,
     and file organization.
   - Write tests according to the plan's test plan section. Tests can come
     before or after the implementation — use your judgment for what fits the
     language, the task, and the change. What matters is that the plan's test
     plan is fulfilled, not the ordering.
   - Focus test effort on edge cases, error paths, and boundary conditions
     against public interfaces. Do not write happy-path-only tests that merely
     restate the implementation or tests that are tightly coupled to internal
     details.
   - Comment the code well. Comments should explain the architecture and the
     "why", not merely describe what the code does.
   - Keep the implementation aligned with the plan unless the user explicitly
     redirects or the plan is clearly wrong.
   - Never use `sed` or other dangerous hacks when editing files.
7. If you find yourself spinning your wheels or faced with an unexpected
   obstacle, stop and ask the user for guidance.

Repeat steps 6–7 until the plan is complete.

### Validate

After all plan work is complete, validate the full body of work with review
passes.

8. Run the full suite.
   - Run tests, lint, formatter, and type checks as applicable.
   - Use the commands from the project's guidance docs or existing repo scripts,
     not ad hoc substitutes.
   - Fix any failures before proceeding.
9. Run a review pass over the completed work using a read-only subagent (no file
   edits, no shell commands).
   - Pass it the plan document, the list of completed tasks, and the list of
     changed files.
   - The subagent invokes the `kreview` skill, which runs a completeness review
     and a code-simplification review in sequence.
   - This ensures the review is independent — a separate model instance with no
     write access evaluates the work.
10. Act on review findings returned by the subagents.
    - If either review reports issues worth fixing: fix them, then re-run the
      relevant quality checks.
    - If both reviews pass, proceed to handoff.

### Commit & Handoff

11. Commit all work using the 7 rules of great commit messages and with no
    AI-tool attribution unless the project explicitly requires it.
    - All plan work, test fixes, and review fixes go into a single commit.
    - Do not commit if tests are failing or work is incomplete.
12. Report what shipped, quality-check results, commit summary, branch name, and
    any follow-up work.

## Principles

- **Start from a known state** — distinguish the named input document from
  unrelated worktree changes before touching implementation files.
- **The plan is your guide** — follow its references, don't reinvent.
- **Follow the test plan** — write tests that cover edge cases, error paths, and
  boundary conditions against public interfaces. Tests can come before or after
  the implementation; what matters is that the plan's test plan is fulfilled.
- **Commit once at the end** — all validated work in a single commit after
  review, unless the plan explicitly calls for multiple commits.
- **Validate at the end** — independent review passes catch what you miss across
  the full body of work.
- **Ship complete features** — don't leave things 80% done.
