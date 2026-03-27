#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: find_intent_docs.sh <docs-path> [user-doc-path]

Find intent documents (plan, brainstorm) in the task docs directory.

Prints:
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

docs_path="$1"
user_doc_path="${2:-}"

repo_root=$(git rev-parse --show-toplevel)
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

# User-provided path takes priority
if [[ -n "$user_doc_path" ]]; then
  add_candidate "$user_doc_path"
fi

# Check task docs directory for plan and brainstorm
add_candidate "${docs_path}/plan.md"
add_candidate "${docs_path}/brainstorm.md"

# Also check branch-only changes in .k/tasks/
while IFS= read -r path; do
  add_candidate "$path"
done < <(git diff --name-only main...HEAD -- .k/tasks/ 2>/dev/null || true)

# Check uncommitted changes in .k/tasks/
while IFS= read -r path; do
  add_candidate "$path"
done < <(git status --porcelain -- .k/tasks/ 2>/dev/null | awk '{print $NF}')

plan_path=""
brainstorm_path=""

for candidate in "${candidates[@]}"; do
  case "$candidate" in
    */plan.md)
      if [[ -z "$plan_path" ]]; then
        plan_path="$candidate"
      fi
      ;;
    */brainstorm.md)
      if [[ -z "$brainstorm_path" ]]; then
        brainstorm_path="$candidate"
      fi
      ;;
  esac
done

# If plan references a brainstorm, pick it up
if [[ -n "$plan_path" && -z "$brainstorm_path" ]]; then
  related_brainstorm=$(rg -o '\.k/tasks/[A-Za-z0-9._/-]+/brainstorm\.md' "$plan_path" | head -n 1 || true)
  if [[ -n "$related_brainstorm" ]]; then
    add_candidate "$related_brainstorm"
    brainstorm_path="${repo_root}/${related_brainstorm}"
  fi
fi

printf 'repo_root=%s\n' "$repo_root"
printf 'plan_path=%s\n' "$plan_path"
printf 'brainstorm_path=%s\n' "$brainstorm_path"
for candidate in "${candidates[@]}"; do
  printf 'candidate=%s\n' "$candidate"
done
