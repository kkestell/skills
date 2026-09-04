# Hooks

Agent hooks this repository installs into a harness configuration directory.

| Hook        | What it does                                                        |
| ----------- | ------------------------------------------------------------------- |
| `notify.sh` | Posts a macOS Notification Center banner titled with the workspace. |

## Install

```bash
./profiles.py install-hooks --claude --codex
```

The command copies each script into `~/<harness>/hooks/` and registers it on
the `PermissionRequest` and `Stop` events. It only adds what is missing, so
hooks you configured yourself are left alone, and re-running it refreshes the
installed scripts in place.

Claude Code reads hooks from `~/.claude/settings.json`; Codex reads them from
`~/.codex/hooks.json`. Codex also requires you to trust a newly added hook
before it runs, so run `/hooks` in Codex once after installing.

## Payload

Both harnesses pass the event as JSON on stdin. `notify.sh` reads `cwd` for the
banner title and `hook_event_name` to choose the body, falling back to
`tool_name` for permission requests.
