# Hooks

Agent hooks this repository installs into a harness configuration directory.

| Hook                | What it does                                                          |
| ------------------- | --------------------------------------------------------------------- |
| `notify.sh`         | Posts a macOS Notification Center banner titled with the workspace.   |
| `no-attribution.sh` | Blocks commit, PR, and release commands carrying Claude attribution.  |

## Install

```bash
./profiles.py install-hooks --claude --codex
```

The command copies each script into `~/<harness>/hooks/` and registers it on
the events it declares: `notify.sh` on `PermissionRequest` and `Stop` in both
harnesses, and `no-attribution.sh` on `PreToolUse` in Claude Code alone, since
it answers with a Claude Code permission decision. It only adds what is
missing, so hooks you configured yourself are left alone, and re-running it
refreshes the installed scripts in place.

Claude Code reads hooks from `~/.claude/settings.json`; Codex reads them from
`~/.codex/hooks.json`. Codex also requires you to trust a newly added hook
before it runs, so run `/hooks` in Codex once after installing.

## Payload

Both harnesses pass the event as JSON on stdin. `notify.sh` reads `cwd` for the
banner title and `hook_event_name` to choose the body, falling back to
`tool_name` for permission requests. `no-attribution.sh` reads
`tool_input.command`, ignores anything that is not a commit, PR, or release
command, and denies the rest when the message carries a `Co-Authored-By:
Claude` trailer or a "Generated with Claude Code" line.
