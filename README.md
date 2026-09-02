# K

Skills for intentional, high-quality coding work and prose editing.

The skills are designed to work together: `kplan` decides what the right change
is, and `kwork` carries it through to a finished, reviewed result. See
[skills/README.md](./skills/README.md) for the full workflow.

## Core workflow

The skills that carry a change from an unfamiliar repo to a reviewed commit,
across as many sessions as it takes.

| Skill      | What it does                                                                               |
| ---------- | ------------------------------------------------------------------------------------------ |
| `kinit`    | Explore a repo and bootstrap an `AGENTS.md` orientation doc.                               |
| `kplan`    | Brainstorm a change, explore the codebase, and write a concrete implementation plan.       |
| `kwork`    | Execute a plan end to end: implement, validate with independent review passes, and commit. |
| `ktask`    | Execute a bounded one-off task without a persisted plan or commit.                         |
| `kreview`  | Run independent completeness and code-simplification review passes over a body of work.    |
| `khandoff` | Write a handoff note summarizing a session so the next one can continue cleanly.           |

## Everything else

Standalone skills for prose, language-specific review, delegation, and
maintaining this repo.

| Skill         | What it does                                                                    |
| ------------- | ------------------------------------------------------------------------------- |
| `kdeslop`     | Detect and fix AI "slop" in prose while preserving meaning and voice.           |
| `kmarkdown`   | Format Markdown with dprint and hard-wrap prose at 80 columns.                  |
| `krust`       | Apply the Rust API design guidelines when designing or reviewing public APIs.   |
| `kclaude`     | Delegate a task to Claude Code headlessly and report back its result.           |
| `kskillissue` | Diagnose a misbehaving skill, fix it in this repo, commit, push, and reinstall. |

## Sync

From inside a checkout, `sync-skills` installs every skill under `skills/` into
the harnesses you name. It also removes globally installed skills this checkout
no longer defines:

```bash
./profiles.py sync-skills --claude --codex
```

The harness flags are `--claude`, `--codex`, and `--copilot`; each one points at
that harness's configuration directory under your home directory (`~/.claude`,
`~/.codex`, `~/.copilot`). `sync-skills` installs nothing until at least one is
given, so a bare run is an error rather than a surprise.

Pull the latest repository changes and run the same command again to update
installed skills.

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
skills/
  kplan/
    SKILL.md
    assets/
  kwork/
    SKILL.md
  ...
```

Each directory under `skills/` is a standalone skill. There are no plugin
manifests or marketplace catalogs.

## Development

Install the repository tooling and run the full validation suite:

```bash
npm install
npm run check
```

Validate one skill:

```bash
npm run validate -- skills/<skill-name>
```

See [AGENTS.md](./AGENTS.md) for authoring conventions.
