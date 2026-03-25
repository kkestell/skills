---
name: kend
description: Merge the current worktree's feature branch back into `main`, run quality checks, clean up the worktree, and delete the feature branch. Use only after `/kverify` passes and the worktree is clean.
argument-hint: ""
disable-model-invocation: true
---

# End Task and Merge

Merge completed feature work from the current worktree back into `main`, then clean up. This workflow does not use pull requests.

## Workflow Context

This skill is part of a structured workflow: kinit -> kstart -> kbrainstorm -> kplan -> kwork -> kverify -> **kend**.
You are currently in the **kend** step. You are working in a git worktree, not the original repository.

### Current Task
!`cat .k/current_task.json 2>/dev/null || echo '{"error": "No current task. Run /kstart first."}'`

## Step 1: Read Context

Read `.k/current_task.json` to get `original_repo_path` and `task_id`. If the file is missing, stop and tell the user to run `/kstart` first.

## Step 2: Run Merge Script

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/kend.sh"
```

The script handles safety checks, merge, and cleanup. If it fails, report the error and stop.

## Step 3: Post-Merge Validation

After the script succeeds, `cd` to the original repo path and run relevant tests and lint on `main`. Use CLAUDE.md for project-specific commands.

## Step 4: Report

Report: merged branch, merge result, checks run, cleanup result.
