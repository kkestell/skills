# k — Agent Skills

Skills for intentional, high-quality coding work, comparative research, and
prose editing.

The skills are designed to work together: `kplan` decides what the right change
is, and `kwork` carries it through to a finished, reviewed result. See
[skills/README.md](./skills/README.md) for the full workflow.

## Skills

| Skill          | What it does                                                                               |
| -------------- | ------------------------------------------------------------------------------------------ |
| `kinit`        | Explore a repo and bootstrap an `AGENTS.md` orientation doc.                               |
| `kplan`        | Brainstorm a change, explore the codebase, and write a concrete implementation plan.       |
| `kwork`        | Execute a plan end to end: implement, validate with independent review passes, and commit. |
| `kreview`      | Run independent completeness and code-simplification review passes over a body of work.    |
| `ktask`        | Execute a bounded one-off task without a persisted plan or commit.                         |
| `krust`        | Apply the Rust API design guidelines when designing or reviewing public APIs.              |
| `kdeslop`      | Detect and fix AI "slop" in prose while preserving meaning and voice.                      |
| `kformat-docs` | Format Markdown with dprint and hard-wrap prose at 80 columns.                             |
| `kclaude`      | Delegate a task to Claude Code headlessly and report back its result.                      |
| `kwiki`        | Read, search, and edit pages on the private Wiki.js site.                                  |
| `kjira`        | Create, update, and sprint-manage Jira issues in the DANG project (Star Tribune).          |

Skills under `wip/` are in progress and deliberately not installed:

| Skill       | What it will do                                                    |
| ----------- | ------------------------------------------------------------------ |
| `khandoff`  | Write a session handoff document for a future agent or session.    |
| `kresearch` | Research a technical topic across comparable open-source projects. |

## Sync

From inside a checkout, `profiles.py` installs every canonical skill under
`skills/` into the personal Claude Code and Codex profiles (`~/.claude` and
`~/.codex`). It also removes globally installed skills this checkout no longer
defines:

```bash
./profiles.py sync-skills personal
```

On a work machine, sync both the personal profiles and the Star Tribune profiles
(`~/.claude-strib` and `~/.codex-strib`):

```bash
./profiles.py sync-skills work
```

Pull the latest repository changes and run the appropriate sync command again to
update installed skills.

The skills are installed directly, without a Claude or Codex plugin namespace.
Use `kwork`, for example, instead of `k:kwork`.

## Inspect profiles

The other `profiles.py` commands are read-only. They inspect the configured
Claude Code, Codex, and GitHub Copilot profiles:

| Command                 | What it reports                                             |
| ----------------------- | ----------------------------------------------------------- |
| `./profiles.py hooks`   | Configured hooks and the action each hook runs.             |
| `./profiles.py plugins` | Known marketplaces and installed or configured plugins.     |
| `./profiles.py skills`  | Skills available directly, globally, or through plugins.    |
| `./profiles.py mcp`     | Configured MCP server names.                                |
| `./profiles.py diff`    | Differences between each provider's personal/work profiles. |

In `diff` output, `-` marks entries found only in the personal profile and `+`
marks entries found only in the work profile. Providers with a single profile
are skipped.

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
