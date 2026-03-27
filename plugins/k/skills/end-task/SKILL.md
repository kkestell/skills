---
name: end-task
description: Merge the current task branch into `main`, validate the result, retain any optional worktree for post-merge checks, and delete the feature branch only when safe. Use only after `/verify` passes and the repo is clean.
argument-hint: ""
disable-model-invocation: true
---

## Workflow

1. Read `.k/current_task.json`.
   - If it is missing, stop and tell the user to run `/start-task`.
   - If `worktree_path` is absent, assume the task is running in place in the original repo.
   - Read the task context to understand `original_repo_path`, `branch_name`, and whether this task has a separate worktree.
2. Use this step only when the task is genuinely ready to merge.
   - Run this only after `/verify` passes and the repo is clean.
3. Run `bash "${CLAUDE_SKILL_DIR}/scripts/end-task.sh"`.
   - Treat the script as responsible for safety checks, merging, retaining any separate worktree for post-merge validation, and reporting status fields.
   - Do not bypass script failures or improvise around them; the script is the safety boundary for this step.
   - If it fails, report the error and stop.
4. After success, `cd` to `original_repo_path` and run the relevant post-merge quality checks from `CLAUDE.md` on `main`.
   - Treat post-merge validation on `main` as mandatory, not optional cleanup.
5. Report the merge outcome.
   - Include the merged branch, merge result, cleanup result, checks run, and any follow-up needed.
   - If a separate worktree was used, confirm that it was intentionally retained for post-merge validation.
