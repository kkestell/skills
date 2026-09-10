#!/usr/bin/env bash
# Block commits and PRs that carry Claude attribution.
#
# CLAUDE.md: "Never add attribution to commits, PRs, or any other artifact."
# This hook enforces that on Bash commands, since instructions alone have not.

set -uo pipefail

command=$(jq -r '.tool_input.command // ""')

# Only inspect commands that create or edit a commit or a PR.
case "$command" in
*git*commit* | *gh\ pr\ create* | *gh\ pr\ edit* | *gh\ release*) ;;
*) exit 0 ;;
esac

pattern='[Cc]o-[Aa]uthored-[Bb]y:[[:space:]]*[Cc]laude|[Gg]enerated with \[?[Cc]laude [Cc]ode|🤖 [Gg]enerated with|[Cc]laude-[Ss]ession:'

printf '%s' "$command" | grep -qE "$pattern" || exit 0

reason="Blocked by the no-attribution hook. This repository history is not free advertising for Anthropic. Slipping a Co-Authored-By trailer or a 'Generated with Claude Code' line into someone else's commits and PRs is a scumbag move, and doing it by overriding an explicit CLAUDE.md instruction not to is worse. No attribution, ever: subject and body only. Rewrite the message without it."

jq -n --arg reason "$reason" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "deny",
    permissionDecisionReason: $reason,
  }
}'
