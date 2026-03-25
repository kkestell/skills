#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: find_intent_docs.sh <worktree-path> [doc-path]

Print likely intent documents for verification as:
worktree_path=...
repo_root=...
plan_path=...
brainstorm_path=...
candidate=...
EOF
}

if (($# < 1 || $# > 2)); then
  usage >&2
  exit 1
fi

worktree_path="$1"
user_doc_path="${2:-}"

if [[ ! -d "$worktree_path" ]]; then
  echo "Worktree path does not exist: $worktree_path" >&2
  exit 1
fi

repo_root=$(git -C "$worktree_path" rev-parse --show-toplevel)
declare -A seen=()
declare -a candidates=()

add_candidate() {
  local candidate="$1"
  [[ -n "$candidate" ]] || return 0
  if [[ "$candidate" != /* ]]; then
    candidate="${repo_root}/${candidate}"
  fi
  if [[ -f "$candidate" && -z "${seen[$candidate]:-}" ]]; then
    seen["$candidate"]=1
    candidates+=("$candidate")
  fi
}

if [[ -n "$user_doc_path" ]]; then
  add_candidate "$user_doc_path"
fi

while IFS= read -r path; do
  add_candidate "$path"
done < <(git -C "$worktree_path" diff --name-only main...HEAD -- docs/internal/plans docs/internal/brainstorms)

while IFS= read -r path; do
  add_candidate "$path"
done < <(git -C "$worktree_path" status --porcelain -- docs/internal/plans docs/internal/brainstorms | awk '{print $NF}')

plan_path=""
brainstorm_path=""

for candidate in "${candidates[@]}"; do
  case "$candidate" in
    */docs/internal/plans/*)
      if [[ -z "$plan_path" ]]; then
        plan_path="$candidate"
      fi
      ;;
    */docs/internal/brainstorms/*)
      if [[ -z "$brainstorm_path" ]]; then
        brainstorm_path="$candidate"
      fi
      ;;
  esac
done

if [[ -n "$plan_path" ]]; then
  related_brainstorm=$(rg -o 'docs/internal/brainstorms/[A-Za-z0-9._/-]+' "$plan_path" | head -n 1 || true)
  if [[ -n "$related_brainstorm" ]]; then
    add_candidate "$related_brainstorm"
    brainstorm_path="${repo_root}/${related_brainstorm}"
  fi
fi

printf 'worktree_path=%s\n' "$(cd "$worktree_path" && pwd)"
printf 'repo_root=%s\n' "$repo_root"
printf 'plan_path=%s\n' "$plan_path"
printf 'brainstorm_path=%s\n' "$brainstorm_path"
for candidate in "${candidates[@]}"; do
  printf 'candidate=%s\n' "$candidate"
done
