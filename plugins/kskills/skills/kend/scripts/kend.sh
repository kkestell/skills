#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: kend.sh

Reads .k/current_task.json from the current directory, merges the feature
branch into main in the original repo, removes the worktree, and deletes
the feature branch.

Prints:
original_repo_path=...
branch_name=...
worktree_path=...
merge_result=success|failed
cleanup_result=success|failed
EOF
}

worktree_path=$(pwd)
task_file="${worktree_path}/.k/current_task.json"

if [[ ! -f "$task_file" ]]; then
  echo "No .k/current_task.json found in current directory." >&2
  exit 1
fi

# Parse current_task.json
original_repo_path=$(python3 -c "import json,sys; print(json.load(sys.stdin)['original_repo_path'])" < "$task_file")
task_id=$(python3 -c "import json,sys; print(json.load(sys.stdin)['task_id'])" < "$task_file")

branch_name=$(git branch --show-current)

if [[ "$branch_name" == "main" ]]; then
  echo "Cannot merge main into itself." >&2
  exit 1
fi

# Safety: worktree must be clean
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Worktree has uncommitted changes. Run /kcommit first." >&2
  exit 1
fi

# Safety: original repo must be clean
if [[ -n "$(git -C "$original_repo_path" status --porcelain)" ]]; then
  echo "Original repo has uncommitted changes. Clean it up first." >&2
  exit 1
fi

# Safety: original repo must be on main
original_branch=$(git -C "$original_repo_path" branch --show-current)
if [[ "$original_branch" != "main" ]]; then
  echo "Original repo is on branch '$original_branch', not main." >&2
  exit 1
fi

# Capture pre-merge state
pre_merge_main=$(git -C "$original_repo_path" rev-parse main)

# Merge into main in the original repo
merge_result="failed"
if git -C "$original_repo_path" merge --no-ff "$branch_name"; then
  merge_result="success"
fi

if [[ "$merge_result" != "success" ]]; then
  printf 'original_repo_path=%s\n' "$original_repo_path"
  printf 'branch_name=%s\n' "$branch_name"
  printf 'worktree_path=%s\n' "$worktree_path"
  printf 'merge_result=%s\n' "$merge_result"
  printf 'cleanup_result=skipped\n'
  exit 1
fi

# Show merged commits
echo "--- Merged commits ---"
git -C "$original_repo_path" log --oneline "${pre_merge_main}..main"
echo "---"

# Cleanup: remove worktree and delete branch
cleanup_result="success"
cd "$original_repo_path"
if ! git worktree remove "$worktree_path" 2>/dev/null; then
  echo "WARNING: Could not remove worktree at $worktree_path" >&2
  cleanup_result="failed"
fi
if ! git branch -d "$branch_name" 2>/dev/null; then
  echo "WARNING: Could not delete branch $branch_name" >&2
  cleanup_result="failed"
fi

printf 'original_repo_path=%s\n' "$original_repo_path"
printf 'branch_name=%s\n' "$branch_name"
printf 'worktree_path=%s\n' "$worktree_path"
printf 'merge_result=%s\n' "$merge_result"
printf 'cleanup_result=%s\n' "$cleanup_result"
