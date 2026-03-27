#!/usr/bin/env bash

set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
k_dir="${repo_root}/.k"

already_existed=true

if [[ ! -d "$k_dir" ]]; then
  already_existed=false
fi

mkdir -p "${k_dir}/tasks"

if [[ ! -f "${k_dir}/.gitignore" ]]; then
  printf 'current_task.json\n' > "${k_dir}/.gitignore"
  already_existed=false
fi

# Ensure tasks dir has a .gitkeep so it's committed
if [[ ! -f "${k_dir}/tasks/.gitkeep" ]]; then
  touch "${k_dir}/tasks/.gitkeep"
  already_existed=false
fi

printf 'repo_root=%s\n' "$repo_root"
printf 'k_dir=%s\n' "$k_dir"
printf 'already_existed=%s\n' "$already_existed"
