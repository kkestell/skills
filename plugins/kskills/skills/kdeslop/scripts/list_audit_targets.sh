#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: list_audit_targets.sh [file|dir|glob ...]

Print user-facing documentation files to audit, one per line.
Defaults to repo-root docs like README/CHANGELOG/CONTRIBUTING plus docs/.
EOF
}

repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
declare -A seen=()

is_doc_file() {
  local path="$1"
  local base
  base=$(basename "$path")
  [[ "$base" == README* || "$base" == CHANGELOG* || "$base" == CONTRIBUTING* || "$path" == *.md ]]
}

is_skipped_path() {
  local path="$1"
  [[ "$path" == *"/.git/"* ]] && return 0
  [[ "$path" == *"/.worktrees/"* ]] && return 0
  [[ "$path" == *"/node_modules/"* ]] && return 0
  [[ "$path" == *"/target/"* ]] && return 0
  [[ "$path" == *"/dist/"* ]] && return 0
  [[ "$path" == *"/coverage/"* ]] && return 0
  [[ "$path" == *"/docs/internal/"* ]] && return 0
  return 1
}

emit_file() {
  local candidate="$1"
  local abs

  if [[ "$candidate" != /* ]]; then
    if [[ -e "$candidate" ]]; then
      abs=$(cd "$(dirname "$candidate")" && pwd)/$(basename "$candidate")
    elif [[ -e "$repo_root/$candidate" ]]; then
      abs=$(cd "$(dirname "$repo_root/$candidate")" && pwd)/$(basename "$candidate")
    else
      return 0
    fi
  else
    abs="$candidate"
  fi

  [[ -f "$abs" ]] || return 0
  is_doc_file "$abs" || return 0
  is_skipped_path "$abs" && return 0

  if [[ -z "${seen[$abs]:-}" ]]; then
    seen["$abs"]=1
    printf '%s\n' "$abs"
  fi
}

scan_dir() {
  local dir="$1"
  [[ -d "$dir" ]] || return 0

  while IFS= read -r path; do
    emit_file "$path"
  done < <(
    find "$dir" \
      \( -path '*/.git' -o -path '*/.worktrees' -o -path '*/node_modules' -o -path '*/target' -o -path '*/dist' -o -path '*/coverage' -o -path '*/docs/internal' \) -prune -o \
      -type f \( -name '*.md' -o -name 'README*' -o -name 'CHANGELOG*' -o -name 'CONTRIBUTING*' \) -print
  )
}

resolve_target() {
  local target="$1"

  if [[ -e "$target" ]]; then
    if [[ -d "$target" ]]; then
      scan_dir "$target"
    else
      emit_file "$target"
    fi
    return 0
  fi

  if [[ -e "$repo_root/$target" ]]; then
    if [[ -d "$repo_root/$target" ]]; then
      scan_dir "$repo_root/$target"
    else
      emit_file "$repo_root/$target"
    fi
    return 0
  fi

  while IFS= read -r match; do
    [[ -n "$match" ]] || continue
    if [[ -d "$match" ]]; then
      scan_dir "$match"
    else
      emit_file "$match"
    fi
  done < <(compgen -G "$target" || true)

  while IFS= read -r match; do
    [[ -n "$match" ]] || continue
    if [[ -d "$match" ]]; then
      scan_dir "$match"
    else
      emit_file "$match"
    fi
  done < <(compgen -G "$repo_root/$target" || true)
}

if (($# == 0)); then
  scan_dir "$repo_root/docs"
  for base in README.md README CHANGELOG.md CHANGELOG CONTRIBUTING.md CONTRIBUTING; do
    emit_file "$repo_root/$base"
  done
  exit 0
fi

for target in "$@"; do
  case "$target" in
    -h|--help)
      usage
      exit 0
      ;;
    *)
      resolve_target "$target"
      ;;
  esac
done
