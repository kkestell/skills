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
| `kformat-docs` | Reformat Markdown documents with dprint (never wrap text).                                 |

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

For a local checkout, Claude Code expects an explicit local path:

```bash
claude plugin marketplace add ./
claude plugin install k@k
```

Refresh from the marketplace when the repo changes:

```bash
claude plugin marketplace update k
claude plugin update k@k
```

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

Refresh the marketplace snapshot when the repo changes:

```bash
codex plugin marketplace upgrade k
```

Local checkouts work too — point at the repo root:

```bash
codex plugin marketplace add .
codex plugin add k@k
```

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
