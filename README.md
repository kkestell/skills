# K

Skills for coding work and prose editing.

The core workflow moves from `kspec` and `kroadmap` through `kplan` and `kwork`.
See [skills/README.md](./skills/README.md) for the full workflow.

## Core workflow

Use these skills to explore an unfamiliar repo, plan and implement a change,
review and commit it, and preserve context between sessions.

| Skill      | What it does                                                                               |
| ---------- | ------------------------------------------------------------------------------------------ |
| `kinit`    | Bootstrap `AGENTS.md` with project orientation and workflow routing.                       |
| `kspec`    | Create or update the authoritative product specification with the user.                    |
| `kroadmap` | Create or update user-directed milestones, ordering, and completion gates.                 |
| `kplan`    | Turn the specification and roadmap into a concrete implementation plan.                    |
| `kwork`    | Execute a plan end to end: implement, validate with independent review passes, and commit. |
| `ktask`    | Execute a bounded one-off task without a persisted plan or commit.                         |
| `kreview`  | Run independent completeness and code-simplification review passes over a body of work.    |

## Everything else

Standalone skills for prose, language-specific review, delegation, and
maintaining this repo.

| Skill         | What it does                                                                    |
| ------------- | ------------------------------------------------------------------------------- |
| `kdeslop`     | Detect and fix AI "slop" in prose while preserving meaning and voice.           |
| `kmarkdown`   | Format Markdown with dprint and hard-wrap prose at 80 columns.                  |
| `krust`       | Apply the Rust API design guidelines when designing or reviewing public APIs.   |
| `kclaude`     | Delegate a task to Claude Code headlessly and report back its result.           |
| `kcodex`      | Delegate a task to Codex headlessly and report back its result.                 |
| `khandoff`    | Write a handoff note so the next session can continue cleanly.                  |
| `kskillissue` | Diagnose a misbehaving skill, fix it in this repo, commit, push, and reinstall. |

## Sync

From inside a checkout, `sync-skills` installs the skill groups you name into
the selected harnesses. Groups may be comma- or space-separated. Skills outside
the selection are removed from those harnesses:

```bash
./profiles.py sync-skills core,ext --claude --codex
```

The groups are `core`, `ext`, and `wip`. The harness flags are `--claude`,
`--codex`, and `--copilot`; each one points at that harness's configuration
directory under your home directory (`~/.claude`, `~/.codex`, `~/.copilot`).
Both a group and at least one harness are required.

Pull the latest repository changes and run the same command again to update
installed skills.

## Hooks

`install-hooks` installs the hooks in [hooks/](./hooks) into the harnesses you
name, copying each script into `~/<harness>/hooks/` and registering it on the
`PermissionRequest` and `Stop` events:

```bash
./profiles.py install-hooks --claude --codex
```

Only `--claude` and `--codex` take hooks. The command adds only what is
missing, so hooks you configured yourself are left alone and re-running it
refreshes the installed scripts in place. Codex skips a hook until you trust
it, so run `/hooks` in Codex once after installing.

## Inspect harnesses

The other `profiles.py` commands are read-only, and report on every harness
unless you narrow them with the same flags:

| Command                          | What it reports                                          |
| -------------------------------- | -------------------------------------------------------- |
| `./profiles.py hooks`            | Configured hooks and the action each hook runs.          |
| `./profiles.py plugins`          | Known marketplaces and installed or configured plugins.  |
| `./profiles.py skills`           | Skills available directly, globally, or through plugins. |
| `./profiles.py mcp`              | Configured MCP server names.                             |
| `./profiles.py skills --copilot` | Any of the above, for one harness.                       |

## Repository layout

```text
hooks/
  notify.sh
skills/
  core/
    kplan/
      SKILL.md
      assets/
    kwork/
      SKILL.md
  ext/
    kmarkdown/
      SKILL.md
  wip/
    kresearch/
      SKILL.md
```

Each group contains standalone skill directories. There are no plugin manifests
or marketplace catalogs.

## Development

Install the repository tooling and run the full validation suite:

```bash
npm install
npm run check
```

Validate one skill:

```bash
npm run validate -- skills/<group>/<skill-name>
```

See [AGENTS.md](./AGENTS.md) for authoring conventions.
