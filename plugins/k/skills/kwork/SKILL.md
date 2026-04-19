---
name: kwork
description: "Execute a repo plan end to end: implement, validate with independent review passes, and commit at the end."
metadata:
  argument-hint: "[plan, specification, or todo file path]"
  disable-model-invocation: "true"
---

## Workflow

### Pre-flight

1. Check that the git repo is clean.
   - Run `git status`. If there are staged changes, unstaged changes, or untracked files, stop and report them to the user.
   - Offer to commit the changes, add them to `.gitignore`, or stash them — whatever makes sense for what you see.
   - Do not proceed until the repo is clean or the user explicitly says to continue with dirty state.
   - If there are existing lint or test failures, offer to fix them before proceeding. There is no such thing as a "pre-existing" issue. We fix issues as soon as we see them.

### Orientation

2. Resolve `<input_document> $ARGUMENTS </input_document>`.
   - Prefer `!`echo ~/.k/workspaces/${PWD//\//_}`/plans/` for implementation plans and `!`echo ~/.k/workspaces/${PWD//\//_}`/todo/` for tracked follow-up work.
3. Read the work doc completely.
4. If anything is unclear or ambiguous after reading the plan, references, and related code, ask the user now.
   - Better to ask once before starting than to build the wrong thing. Get user approval to proceed.
   - Skip this step if the plan is clear and the path forward is obvious.
5. Verify the repo setup and baseline quality commands before major edits.
   - Delegate baseline verification to a subagent if it will save context.
   - Confirm dependencies are installed, then run tests, lint, formatter, and type checks as applicable.
   - Capture a concise baseline summary: what passed, what failed, and any broken baseline issues.
   - If the baseline is already broken, fix it before proceeding.
6. Create a Todo list from the plan's implementation tasks.
   - Include testing tasks alongside implementation tasks.
   - Keep tasks specific and completable — each one should map to a plan item.

### Execution

7. Execute the plan task by task.
   - Read the related code and nearby patterns before implementing each task.
   - Implement in repo style. Match naming conventions, error handling patterns, and file organization.
   - Write tests according to the plan's test plan section. Tests can come before or after the implementation — use your judgment for what fits the language, the task, and the change. What matters is that the plan's test plan is fulfilled, not the ordering.
   - Focus test effort on edge cases, error paths, and boundary conditions against public interfaces. Do not write happy-path-only tests that merely restate the implementation or tests that are tightly coupled to internal details.
   - Comment the code well. Comments should explain the architecture and the "why", not merely describe what the code does.
   - Keep the implementation aligned with the plan unless the user explicitly redirects or the plan is clearly wrong.
   - Never use `sed` or other dangerous hacks when editing files.
8. If you find yourself spinning your wheels or faced with an unexpected obstacle, stop and ask the user for guidance.

Repeat steps 7–8 until the plan is complete.

### Validate

After all plan work is complete, validate the full body of work with review passes.

9. Run the full suite.
   - Run tests, lint, formatter, and type checks as applicable.
   - Use the commands from the project's guidance docs or existing repo scripts, not ad hoc substitutes.
   - Fix any failures before proceeding.
10. Run review passes over the completed work by delegating to opencode via the review script.
     - Run `!`cat plugins/k/skills/kreview/scripts/review.sh` $PLAN_PATH --files $CHANGED_FILES --tasks $COMPLETED_TASKS` from the repo root, passing the plan path, all tasks completed, and the list of all changed files (implementation and test).
     - The script launches opencode with read-only permissions (no edit or bash) and invokes `/kreview`, which runs a completeness review and a test quality review.
     - This ensures reviews are independent — a separate model instance with no write access evaluates the work.
11. Act on review findings returned by the review script.
     - If either review reports issues worth fixing: fix them, then re-run the relevant quality checks.
     - If both reviews pass, proceed to handoff.

### Commit & Handoff

12. Commit all work using the 7 rules of great commit messages and with no AI-tool attribution unless the project explicitly requires it.
    - All plan work, test fixes, and review fixes go into a single commit.
    - Do not commit if tests are failing or work is incomplete.
13. Report what shipped, quality-check results, commit summary, branch name, and any follow-up work.

## Principles

- **Start clean** — verify the repo state before touching anything.
- **The plan is your guide** — follow its references, don't reinvent.
- **Follow the test plan** — write tests that cover edge cases, error paths, and boundary conditions against public interfaces. Tests can come before or after the implementation; what matters is that the plan's test plan is fulfilled.
- **Commit once at the end** — all validated work in a single commit after review, unless the plan explicitly calls for multiple commits.
- **Validate at the end** — independent review passes catch what you miss across the full body of work.
- **Ship complete features** — don't leave things 80% done.
