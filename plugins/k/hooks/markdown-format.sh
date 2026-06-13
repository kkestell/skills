#!/usr/bin/env bash
# PostToolUse hook: reformat markdown files with dprint after Write/Edit.
# Reads the hook payload JSON from stdin and formats the touched file.
# No-ops silently if dprint or jq isn't installed.
set -euo pipefail

# If the tools we need aren't installed, do nothing.
command -v dprint >/dev/null 2>&1 || exit 0
command -v jq >/dev/null 2>&1 || exit 0

# The dprint config ships next to this script.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
config="$script_dir/dprint.json"

file="$(jq -r '.tool_input.file_path // .tool_response.filePath // empty')"

# Only handle markdown files that still exist on disk.
case "$file" in
  *.md | *.markdown) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0

# dprint resolves file patterns relative to its base dir and won't touch files
# outside it, so run from the file's own directory and pass the basename.
( cd "$(dirname "$file")" && dprint fmt --config "$config" "$(basename "$file")" ) >/dev/null 2>&1 || true
