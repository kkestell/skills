---
name: kmerge
description: Merge a completed worktree branch into main using the standard worktree conventions (no PR workflow)
---

## Arguments
[worktree path or feature branch name]

# Merge Worktree Into Main

Merge completed feature work from a dedicated worktree back into `main`.
This workflow does not use pull requests.

## Input Target

<merge_target> #$ARGUMENTS </merge_target>

If `<merge_target>` is empty:
- List active worktrees with `git worktree list`
- Ask the user which worktree path (or branch) should be merged
- Do not continue until a target is selected

## Shared Conventions (must match `/kwork`)

- Base branch: `main`
- Worktree root: `<repo_root>/.worktrees/`
- Timestamp format: `YYYY-MM-DD-HH-MM-SS`
- Work ID: `<timestamp>-<topic-slug>`
- Feature branch: `feature/<work-id>`
- Worktree path: `<repo_root>/.worktrees/<work-id>`

Expected patterns:
- Branch regex: `^feature/[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+$`
- Worktree path regex: `.*/\.worktrees/[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+$`

## Step 1: Resolve Target Branch and Worktree

1. Resolve repo root:
   ```bash
   repo_root=$(git rev-parse --show-toplevel)
   ```
2. Interpret input:
   - If input is an existing directory, treat it as `worktree_path`
   - Otherwise treat input as `branch_name`
3. Resolve missing side:
   - If you have `worktree_path`, get branch:
     ```bash
     branch_name=$(git -C "$worktree_path" branch --show-current)
     ```
   - If you have `branch_name`, find worktree path from `git worktree list`
4. Validate both values were resolved and match the conventions above.

## Step 2: Safety Checks Before Merge

Run these checks and stop on failure:

- `branch_name` must not be `main`
- Primary checkout (`repo_root`) must be clean (`git status --porcelain` empty)
- Target worktree must be clean (`git -C "$worktree_path" status --porcelain` empty)
- If worktree has uncommitted changes, ask the user to run `/kcommit` first

## Step 3: Quality Gate in Worktree

From `worktree_path`, run the quality checks that apply in this repo:

- Tests
- Lint
- Formatter in check mode
- Type checks (if applicable)

Use commands from `CLAUDE.md` when present.

Do not merge if checks fail.

## Step 4: Merge Into Main

From `repo_root`:

```bash
pre_merge_main=$(git rev-parse main)
git checkout main
git merge --no-ff "$branch_name"
```

If there are conflicts:
- Resolve conflicts immediately
- Re-run relevant tests
- Complete the merge only after conflicts are fully resolved

## Step 5: Post-Merge Validation

After merge, run final checks on `main`:

- Full relevant test suite
- Lint (and formatter/type checks if required by repo policy)

Capture merged commit summary:

```bash
git log --oneline "${pre_merge_main}..main"
```

## Step 6: Cleanup Worktree and Branch

Ask the user whether to clean up merged artifacts.

If yes:

```bash
git worktree remove "$worktree_path"
git branch -d "$branch_name"
```

If cleanup fails because files are still present, pause and ask before forcing removal.

## Output Summary

When complete, report:

- Merged branch name
- Worktree path used
- Merge result (success/failure)
- Checks run and outcomes
- Cleanup result (kept or removed worktree/branch)
