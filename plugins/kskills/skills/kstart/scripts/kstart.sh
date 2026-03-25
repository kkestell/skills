#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: kstart.sh <task-slug>

Create a worktree and task context. Prints:
repo_root=...
timestamp=...
task_id=...
branch_name=...
worktree_path=...
docs_path=...
EOF
}

if (($# != 1)); then
  usage >&2
  exit 1
fi

task_slug="$1"

if [[ ! "$task_slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Task slug must be kebab-case: $task_slug" >&2
  exit 1
fi

repo_root=$(git rev-parse --show-toplevel)

# Verify .k/ exists
if [[ ! -d "${repo_root}/.k" ]]; then
  echo ".k/ directory not found. Run /kinit first." >&2
  exit 1
fi

# Verify clean working directory
if [[ -n "$(git -C "$repo_root" status --porcelain)" ]]; then
  echo "Working directory is not clean. Commit or stash changes first." >&2
  exit 1
fi

timestamp=$(date +"%Y%m%d%H%M%S")
task_id="${timestamp}-${task_slug}"
branch_name="feature/${task_id}"
workspace_name=$(basename "$repo_root")
workspace_parent=$(dirname "$repo_root")
worktree_path="${workspace_parent}/${workspace_name}-worktree-${task_slug}"
docs_path=".k/tasks/${task_id}"

# Create worktree as sibling directory
git -C "$repo_root" worktree add -b "$branch_name" "$worktree_path" main

# Create task docs directory in the worktree
mkdir -p "${worktree_path}/${docs_path}"

# Write current_task.json in the worktree
cat > "${worktree_path}/.k/current_task.json" <<TASKEOF
{
  "task_id": "${task_id}",
  "original_repo_path": "${repo_root}",
  "docs_path": "${docs_path}"
}
TASKEOF

# Open VS Code in the worktree
if command -v code &>/dev/null; then
  code "$worktree_path"
else
  echo "WARNING: 'code' command not found. Open VS Code manually at: $worktree_path" >&2
fi

printf 'repo_root=%s\n' "$repo_root"
printf 'timestamp=%s\n' "$timestamp"
printf 'task_id=%s\n' "$task_id"
printf 'branch_name=%s\n' "$branch_name"
printf 'worktree_path=%s\n' "$worktree_path"
printf 'docs_path=%s\n' "$docs_path"
