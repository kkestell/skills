---
name: kmerge
description: Merge a clean, verified feature worktree branch back into `main` using the standard worktree conventions and no PR workflow. Use only after `/kverify` passes and both the primary checkout and target worktree are clean.
argument-hint: "[worktree path or feature branch name]"
disable-model-invocation: true
---

# Merge Worktree Into Main

Merge completed feature work from a dedicated worktree back into `main`. This workflow does not use pull requests.

## Input Target

<merge_target> $ARGUMENTS </merge_target>

If empty, list active worktrees with `git worktree list` and ask which one to merge.

## Conventions

- Worktree root: `<repo_root>/.worktrees/`
- Feature branch pattern: `feature/<YYYY-MM-DD-HH-MM-SS>-<topic-slug>`
- Worktree path pattern: `<repo_root>/.worktrees/<YYYY-MM-DD-HH-MM-SS>-<topic-slug>`

## Step 1: Resolve Target

Prefer `${CLAUDE_SKILL_DIR}/scripts/resolve_merge_target.sh "$ARGUMENTS"` to resolve the branch/path pair and validate the conventions above.

1. Get repo root: `git rev-parse --show-toplevel`
2. If input is an existing directory, treat as worktree path and get branch from `git -C "$worktree_path" branch --show-current`
3. Otherwise treat as branch name and find its worktree from `git worktree list`
4. Validate both values match the conventions above

## Step 2: Safety Checks

Stop on failure:

- Branch must not be `main`
- Primary checkout must be clean (`git status --porcelain`)
- Target worktree must be clean (`git -C "$worktree_path" status --porcelain`)

If the worktree has uncommitted changes, ask the user to run `/kcommit` first.

## Step 3: Quality Gate

From the worktree, run all applicable quality checks (tests, lint, formatter, type checks). Use commands from CLAUDE.md when present.

Do not merge if checks fail.

## Step 4: Merge

From the repo root:

```bash
pre_merge_main=$(git rev-parse main)
git checkout main
git merge --no-ff "$branch_name"
```

If there are conflicts, resolve them, re-run relevant tests, and complete the merge.

## Step 5: Post-Merge Validation

Run relevant tests and lint on `main`. Capture the merged commits:

```bash
git log --oneline "${pre_merge_main}..main"
```

## Step 6: Cleanup

Ask the user whether to clean up:

```bash
git worktree remove "$worktree_path"
git branch -d "$branch_name"
```

If cleanup fails, pause and ask before forcing.

## Output Summary

Report: merged branch, worktree path, merge result, checks run, cleanup result.
