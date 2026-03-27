#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: end-task.sh

Reads .k/current_task.json from the current directory, merges the feature
branch into main, retains any optional worktree for post-merge validation,
and deletes the feature branch only when running in place.

Prints:
original_repo_path=...
branch_name=...
worktree_path=...
merge_result=success|failed
cleanup_result=success|failed|skipped
EOF
}

current_repo_path=$(git rev-parse --show-toplevel)
task_file="${current_repo_path}/.k/current_task.json"

if [[ ! -f "$task_file" ]]; then
  echo "No .k/current_task.json found in the current repo." >&2
  exit 1
fi

# Parse current_task.json
original_repo_path=$(python3 -c "import json,sys; print(json.load(sys.stdin)['original_repo_path'])" < "$task_file")
worktree_path=$(python3 -c "import json,sys; print(json.load(sys.stdin).get('worktree_path', ''))" < "$task_file")

branch_name=$(git -C "$current_repo_path" branch --show-current)

if [[ "$branch_name" == "main" ]]; then
  echo "Cannot merge main into itself." >&2
  exit 1
fi

# Safety: current repo must be clean
if [[ -n "$(git -C "$current_repo_path" status --porcelain)" ]]; then
  echo "Current repo has uncommitted changes. Run /k:commit first." >&2
  exit 1
fi

merge_result="failed"
cleanup_result="skipped"

if [[ -n "$worktree_path" ]]; then
  if [[ -n "$(git -C "$original_repo_path" status --porcelain)" ]]; then
    echo "Original repo has uncommitted changes. Clean it up first." >&2
    exit 1
  fi

  original_branch=$(git -C "$original_repo_path" branch --show-current)
  if [[ "$original_branch" != "main" ]]; then
    echo "Original repo is on branch '$original_branch', not main." >&2
    exit 1
  fi

  pre_merge_main=$(git -C "$original_repo_path" rev-parse main)

  if git -C "$original_repo_path" merge --no-ff "$branch_name"; then
    merge_result="success"
  fi

  if [[ "$merge_result" != "success" ]]; then
    printf 'original_repo_path=%s\n' "$original_repo_path"
    printf 'branch_name=%s\n' "$branch_name"
    printf 'worktree_path=%s\n' "$worktree_path"
    printf 'merge_result=%s\n' "$merge_result"
    printf 'cleanup_result=%s\n' "$cleanup_result"
    exit 1
  fi

  echo "--- Merged commits ---"
  git -C "$original_repo_path" log --oneline "${pre_merge_main}..main"
  echo "---"
  echo "Worktree retained at $worktree_path for post-merge validation." >&2
else
  pre_merge_main=$(git -C "$current_repo_path" rev-parse main)

  if git -C "$current_repo_path" switch main && git -C "$current_repo_path" merge --no-ff "$branch_name"; then
    merge_result="success"
  fi

  if [[ "$merge_result" != "success" ]]; then
    printf 'original_repo_path=%s\n' "$original_repo_path"
    printf 'branch_name=%s\n' "$branch_name"
    printf 'worktree_path=\n'
    printf 'merge_result=%s\n' "$merge_result"
    printf 'cleanup_result=%s\n' "$cleanup_result"
    exit 1
  fi

  echo "--- Merged commits ---"
  git -C "$current_repo_path" log --oneline "${pre_merge_main}..main"
  echo "---"

  cleanup_result="success"
  if ! git -C "$current_repo_path" branch -d "$branch_name" 2>/dev/null; then
    echo "WARNING: Could not delete branch $branch_name" >&2
    cleanup_result="failed"
  fi
  if ! rm -f "$task_file"; then
    echo "WARNING: Could not remove $task_file" >&2
    cleanup_result="failed"
  fi
fi

printf 'original_repo_path=%s\n' "$original_repo_path"
printf 'branch_name=%s\n' "$branch_name"
printf 'worktree_path=%s\n' "$worktree_path"
printf 'merge_result=%s\n' "$merge_result"
printf 'cleanup_result=%s\n' "$cleanup_result"
