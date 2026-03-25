#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: resolve_merge_target.sh <worktree-path-or-branch>

Resolve the merge target and print:
repo_root=...
worktree_path=...
branch_name=...
branch_convention_ok=true|false
path_convention_ok=true|false
EOF
}

if (($# != 1)); then
  usage >&2
  exit 1
fi

target="$1"
repo_root=$(git rev-parse --show-toplevel)
worktree_path=""
branch_name=""

if [[ -d "$target" ]]; then
  worktree_path=$(cd "$target" && pwd)
  branch_name=$(git -C "$worktree_path" branch --show-current)
else
  branch_name="$target"
  current_path=""
  current_branch=""
  while IFS= read -r line; do
    if [[ -z "$line" ]]; then
      if [[ "$current_branch" == "refs/heads/${branch_name}" ]]; then
        worktree_path="$current_path"
        break
      fi
      current_path=""
      current_branch=""
      continue
    fi
    case "$line" in
      worktree\ *) current_path="${line#worktree }" ;;
      branch\ *) current_branch="${line#branch }" ;;
    esac
  done < <(git -C "$repo_root" worktree list --porcelain; printf '\n')
fi

if [[ -z "$worktree_path" || -z "$branch_name" ]]; then
  echo "Could not resolve target: $target" >&2
  exit 1
fi

branch_convention_ok=false
path_convention_ok=false

if [[ "$branch_name" =~ ^feature/[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+$ ]]; then
  branch_convention_ok=true
fi

if [[ "$worktree_path" == "${repo_root}/.worktrees/"* ]]; then
  path_convention_ok=true
fi

printf 'repo_root=%s\n' "$repo_root"
printf 'worktree_path=%s\n' "$worktree_path"
printf 'branch_name=%s\n' "$branch_name"
printf 'branch_convention_ok=%s\n' "$branch_convention_ok"
printf 'path_convention_ok=%s\n' "$path_convention_ok"
