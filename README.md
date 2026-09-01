# k — Agent Skills

Skills for intentional, high-quality coding work, comparative research, and prose editing.

The skills are designed to work together — `/kplan` decides what the right change is, and `/kwork` carries it through to a finished, reviewed result. See [plugins/k/skills/README.md](./plugins/k/skills/README.md) for the full workflow writeup.

## Skills

| Skill          | What it does                                                                               |
| -------------- | ------------------------------------------------------------------------------------------ |
| `kinit`        | Explore a repo and bootstrap an `AGENTS.md` orientation doc.                               |
| `kplan`        | Brainstorm a change, explore the codebase, and write a concrete implementation plan.       |
| `kwork`        | Execute a plan end to end: implement, validate with independent review passes, and commit. |
| `kreview`      | Run independent completeness and code-simplification review passes over a body of work.    |
| `ksimplify`    | Global, multi-agent simplification review of a whole codebase, with a human approval gate. |
| `kresearch`    | Comparative technical research across comparable open-source GitHub projects.              |
| `ktask`        | Bounded one-off work — plan lightly, implement, validate. No plan file, no commit.         |
| `kdeslop`      | Detect and fix AI "slop" in prose while preserving meaning and voice.                      |
| `kformat-docs` | Reformat Markdown documents with dprint (hard-wrap at 80 columns).                         |

The plugin also ships the `/khandoff` command (write a session handoff document).

## Install via Plugin Marketplace (Claude Code & Codex)

This repository is a native marketplace source for both Claude Code and Codex. They do not read the same marketplace file:

- Claude Code reads `.claude-plugin/marketplace.json`.
- Codex reads `.agents/plugins/marketplace.json`.

Both marketplace manifests point at the same self-contained plugin bundle: `plugins/k`.

### Claude Code

Add the marketplace once per machine, then install the plugin:

```text
/plugin marketplace add kkestell/skills
/plugin install k@k
```

Plugin skills are namespaced by the plugin name, so `kplan` is invoked as `/k:kplan`.

Refresh when the published marketplace changes:

```bash
claude plugin marketplace update k
claude plugin update k@k
```

A local checkout can be used as the marketplace instead — see [Local Development](#local-development).

To require the marketplace for a particular project, add it to that project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "k": {
      "source": {
        "source": "github",
        "repo": "kkestell/skills"
      }
    }
  }
}
```

### Codex CLI

Codex uses its own marketplace manifest in `.agents/plugins/marketplace.json`:

```bash
codex plugin marketplace add kkestell/skills
codex plugin add k@k
```

Refresh the snapshot when the published marketplace changes:

```bash
codex plugin marketplace upgrade k
```

A local checkout can be used as the marketplace instead — see [Local Development](#local-development).

## Repository Layout

```text
.claude-plugin/
  marketplace.json                         # Claude Code marketplace catalog (one plugin: k)
.agents/
  plugins/
    marketplace.json                       # Codex marketplace catalog (one plugin: k)
plugins/
  k/                                        # the single plugin wrapper
    .claude-plugin/plugin.json              # Claude Code manifest
    .codex-plugin/plugin.json               # Codex manifest (interface metadata)
    commands/                               # khandoff
    skills/                                 # canonical skill content
      README.md
      kplan/
        SKILL.md
        assets/
      ...
skills/
  kplan -> ../plugins/k/skills/kplan        # symlink into canonical skill
  ...
```

Skill content lives once under `plugins/k/skills/<name>/`, inside the plugin so the plugin root is self-contained. Repo-root `skills/<name>` symlinks point into those canonical copies, so there is no content duplication and the conventional `skills/` path still works. The real files stay within `plugins/k/` because Codex copies the plugin directory into its install cache and does not follow symlinks that escape it.

Claude Code intentionally omits `version` from `plugins/k/.claude-plugin/plugin.json`, so git commits drive marketplace updates. The Codex manifest keeps a semver `version`, because Codex plugin ingestion expects one.

## Local Development

Install the repository tooling once:

```bash
npm install
```

See [AGENTS.md](./AGENTS.md) for authoring conventions.

### Installing from a local checkout

Both CLIs accept a local path as a marketplace source, which is how to work on the skills without publishing. If the GitHub marketplace is already installed, remove it first — both are named `k`, so they collide.

Claude Code:

```bash
claude plugin uninstall k@k
claude plugin marketplace remove k
claude plugin marketplace add ~/src/skills
claude plugin install k@k
```

Codex:

```bash
codex plugin remove k@k
codex plugin marketplace remove k
codex plugin marketplace add ~/src/skills
codex plugin add k@k
```

Each CLI records the checkout path in its own config:

| CLI         | Config file               | Entry                                              |
| ----------- | ------------------------- | -------------------------------------------------- |
| Claude Code | `~/.claude/settings.json` | `"source": { "source": "directory", "path": "…" }` |
| Codex       | `~/.codex/config.toml`    | `source_type = "local"` with `source = "…"`        |

### Picking up edits

The two CLIs differ here, and the difference matters day to day:

- **Claude Code reads the checkout directly.** A saved edit takes effect in the next session — no commit, no push, no version bump, no reinstall.
- **Codex copies the plugin into a snapshot** under `~/.codex/plugins/cache/k/k/<version>/` and reads that. Edits are invisible until the snapshot is rebuilt:

  ```bash
  codex plugin remove k@k && codex plugin add k@k
  ```

  `codex plugin marketplace upgrade k` does not do this — it only refreshes Git marketplaces and errors on a local one.

Other things worth knowing:

- Skills are loaded when a session starts, so restart the session to pick up an edit. A session already running keeps the version it started with.
- The recorded path is absolute. Moving or renaming the checkout breaks the install — re-add the marketplace at the new path.
- Claude Code also leaves a version-keyed directory under `~/.claude/plugins/cache/`. It is a leftover from installation and is not what a local marketplace reads, so a stale copy there is expected and harmless.
- To install into an alternate profile, set the config-dir environment variable for the whole command: `CLAUDE_CONFIG_DIR=~/.claude-work claude plugin marketplace add ~/src/skills`, or `CODEX_HOME=~/.codex-work codex plugin marketplace add ~/src/skills`.
- To return to the published version, remove the local marketplace and re-add `kkestell/skills` as shown above.

## Validation

Run all repository checks (typecheck, tests, skill validation, shellcheck, actionlint):

```bash
npm run check
```

Validate a single skill:

```bash
npm run validate -- skills/<skill-name>
```

Validate only the marketplace entrypoints:

```bash
npm run validate:marketplaces
```
