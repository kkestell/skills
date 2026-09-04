#!/bin/sh
# Agent hook: pop a Notification Center banner for this workspace.
#
# Installed by `profiles.py install-hooks` on the PermissionRequest and Stop
# events. Claude Code and Codex name those events identically and both deliver
# the event payload as JSON on stdin, so one script serves both harnesses.
#
# Notifications are cosmetic, so every failure path exits 0: a non-zero hook
# exit would surface as an error in the agent for no useful reason.

command -v jq >/dev/null 2>&1 || exit 0
command -v osascript >/dev/null 2>&1 || exit 0

payload=$(cat)
title=$(printf '%s' "$payload" | jq -r '.cwd // "?" | split("/") | last')
case $(printf '%s' "$payload" | jq -r '.hook_event_name // ""') in
  Stop) body="Assistant responded" ;;
  *)    body="Approve $(printf '%s' "$payload" | jq -r '.tool_name // "tool"')" ;;
esac

osascript -e 'on run argv
tell application "System Events" to display notification (item 1 of argv) with title (item 2 of argv)
end run' "$body" "$title" || exit 0
