#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: create_worktree.sh [--dry-run] [--base-branch <branch>] <topic-slug>

Create a dedicated feature worktree under <repo_root>/.worktrees/ and print:
repo_root=...
timestamp=...
work_id=...
branch_name=...
worktree_path=...
EOF
}

dry_run=0
base_branch="main"
topic_slug=""

while (($# > 0)); do
  case "$1" in
    --dry-run)
      dry_run=1
      shift
      ;;
    --base-branch)
      shift
      if (($# == 0)); then
        echo "Missing value for --base-branch" >&2
        exit 1
      fi
      base_branch="$1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [[ -n "$topic_slug" ]]; then
        echo "Topic slug already set to '$topic_slug'" >&2
        exit 1
      fi
      topic_slug="$1"
      shift
      ;;
  esac
done

if [[ -z "$topic_slug" ]]; then
  usage >&2
  exit 1
fi

if [[ ! "$topic_slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Topic slug must be kebab-case: $topic_slug" >&2
  exit 1
fi

repo_root=$(git rev-parse --show-toplevel)
timestamp=$(date +"%Y-%m-%d-%H-%M-%S")
work_id="${timestamp}-${topic_slug}"
branch_name="feature/${work_id}"
worktree_path="${repo_root}/.worktrees/${work_id}"

mkdir -p "${repo_root}/.worktrees"

if (( dry_run == 0 )); then
  git -C "$repo_root" worktree add -b "$branch_name" "$worktree_path" "$base_branch"
fi

printf 'repo_root=%s\n' "$repo_root"
printf 'timestamp=%s\n' "$timestamp"
printf 'work_id=%s\n' "$work_id"
printf 'branch_name=%s\n' "$branch_name"
printf 'worktree_path=%s\n' "$worktree_path"
