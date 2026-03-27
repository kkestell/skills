#!/usr/bin/env bash

set -euo pipefail

warn_manual_claude_launch() {
  local workspace_path="$1"

  echo "WARNING: Open a terminal manually at: $workspace_path" >&2
  echo "Then run: cd \"$workspace_path\" && claude" >&2
}

detect_terminal_emulator() {
  if [[ -n "${TERM_PROGRAM:-}" ]]; then
    printf '%s\n' "$TERM_PROGRAM"
    return
  fi

  if [[ -n "${LC_TERMINAL:-}" ]]; then
    printf '%s\n' "$LC_TERMINAL"
    return
  fi

  ps -o comm= -p "${PPID:-$$}" 2>/dev/null | tr -d '[:space:]'
}

launch_workspace_terminal() {
  local workspace_path="$1"
  local os_type
  local terminal_emulator
  local launch_cmd

  if ! command -v claude >/dev/null 2>&1; then
    echo "WARNING: 'claude' command not found on PATH." >&2
    warn_manual_claude_launch "$workspace_path"
    return
  fi

  os_type=$(uname -s)
  terminal_emulator=$(detect_terminal_emulator)
  printf -v launch_cmd 'cd %q && exec claude' "$workspace_path"

  case "$os_type" in
    Darwin)
      if [[ "$terminal_emulator" == "iTerm.app" || "$terminal_emulator" == "iTerm2" ]]; then
        echo "Launching Claude in a new iTerm2 split at: $workspace_path" >&2

        if ! osascript - "$workspace_path" <<'APPLESCRIPT'
on run argv
    set workspacePath to item 1 of argv

    tell application "iTerm2"
        activate

        if (count of windows) = 0 then
            create window with default profile
        end if

        tell current session of current window
            set newSession to split vertically with default profile
        end tell

        tell newSession
            write text "cd " & quoted form of workspacePath & " && claude"
        end tell
    end tell
end run
APPLESCRIPT
        then
          echo "WARNING: Failed to open an iTerm2 split automatically." >&2
          warn_manual_claude_launch "$workspace_path"
        fi
      else
        echo "WARNING: macOS auto-launch only supports iTerm2." >&2
        if [[ -n "$terminal_emulator" ]]; then
          echo "Detected terminal emulator: $terminal_emulator" >&2
        fi
        warn_manual_claude_launch "$workspace_path"
      fi
      ;;
    Linux)
      echo "Launching Claude in a new terminal at: $workspace_path" >&2

      if command -v xdg-terminal-exec >/dev/null 2>&1; then
        xdg-terminal-exec bash -lc "$launch_cmd" &
      elif command -v x-terminal-emulator >/dev/null 2>&1; then
        x-terminal-emulator -e bash -lc "$launch_cmd" &
      elif command -v xterm >/dev/null 2>&1; then
        xterm -e bash -lc "$launch_cmd" &
      else
        echo "WARNING: No supported terminal launcher found on Linux." >&2
        warn_manual_claude_launch "$workspace_path"
      fi
      ;;
    *)
      echo "WARNING: Unsupported OS for automatic Claude launch: $os_type" >&2
      warn_manual_claude_launch "$workspace_path"
      ;;
  esac
}

usage() {
  cat <<'EOF'
Usage: start-task.sh <task-slug> [workspace|in-place]

Create a task branch and task context. Prints:
repo_root=...
timestamp=...
task_id=...
branch_name=...
mode=...
task_root=...
workspace_path=...
worktree_path=...
docs_path=...
EOF
}

if (($# < 1 || $# > 2)); then
  usage >&2
  exit 1
fi

task_slug="$1"
mode="${2:-workspace}"

if [[ ! "$task_slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Task slug must be kebab-case: $task_slug" >&2
  exit 1
fi

case "$mode" in
  workspace|in-place)
    ;;
  *)
    echo "Mode must be 'workspace' or 'in-place': $mode" >&2
    exit 1
    ;;
esac

repo_root=$(git rev-parse --show-toplevel)

# Verify .k/ exists
if [[ ! -d "${repo_root}/.k" ]]; then
  echo ".k/ directory not found. Run /k:init first." >&2
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
workspace_path=""
task_root="$repo_root"

if [[ "$mode" == "workspace" ]]; then
  git -C "$repo_root" worktree add -b "$branch_name" "$worktree_path" main
  workspace_path="$worktree_path"
  task_root="$workspace_path"
else
  git -C "$repo_root" switch -c "$branch_name" main
fi

mkdir -p "${task_root}/${docs_path}"

if [[ -n "$workspace_path" ]]; then
  cat > "${task_root}/.k/current_task.json" <<TASKEOF
{
  "task_id": "${task_id}",
  "original_repo_path": "${repo_root}",
  "workspace_path": "${workspace_path}",
  "docs_path": "${docs_path}"
}
TASKEOF
else
  cat > "${task_root}/.k/current_task.json" <<TASKEOF
{
  "task_id": "${task_id}",
  "original_repo_path": "${repo_root}",
  "docs_path": "${docs_path}"
}
TASKEOF
fi

if [[ "$mode" == "workspace" ]]; then
  launch_workspace_terminal "$workspace_path"
fi

printf 'repo_root=%s\n' "$repo_root"
printf 'timestamp=%s\n' "$timestamp"
printf 'task_id=%s\n' "$task_id"
printf 'branch_name=%s\n' "$branch_name"
printf 'mode=%s\n' "$mode"
printf 'task_root=%s\n' "$task_root"
printf 'workspace_path=%s\n' "$workspace_path"
printf 'worktree_path=%s\n' "$workspace_path"
printf 'docs_path=%s\n' "$docs_path"
