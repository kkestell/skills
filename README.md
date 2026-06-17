# k — Agent Skills

Skills for intentional, high-quality coding work, comparative research, and prose editing.

The skills are designed to work together — `/kplan` decides what the right change is, and `/kwork` carries it through to a finished, reviewed result. See [plugins/k/skills/README.md](./plugins/k/skills/README.md) for the full workflow writeup.

## Skills

| Skill       | What it does                                                                               |
| ----------- | ------------------------------------------------------------------------------------------ |
| `kinit`     | Explore a repo and bootstrap an `AGENTS.md` orientation doc.                               |
| `kplan`     | Brainstorm a change, explore the codebase, and write a concrete implementation plan.       |
| `kwork`     | Execute a plan end to end: implement, validate with independent review passes, and commit. |
| `kreview`   | Run independent completeness and code-simplification review passes over a body of work.    |
| `ksimplify` | Global, multi-agent simplification review of a whole codebase, with a human approval gate. |
| `kresearch` | Comparative technical research across comparable open-source GitHub projects.              |
| `ktask`     | Bounded one-off work — plan lightly, implement, validate. No plan file, no commit.         |
| `kdeslop`   | Detect and fix AI "slop" in prose while preserving meaning and voice.                      |

The plugin also ships the `/khandoff` command (write a session handoff document).

## Install via Plugin Marketplace (Claude Code & Codex)

The repo-root `.claude-plugin/marketplace.json` manifest is consumed natively by both [Claude Code](https://code.claude.com/docs/en/plugin-marketplaces) and the [Codex CLI](https://github.com/openai/codex) — no separate configuration is needed.

### Claude Code

Add the marketplace once per machine, then install the plugin:

```text
/plugin marketplace add kkestell/skills
/plugin install k@k
```

Plugin skills are namespaced by the plugin name, so `kplan` is invoked as `/k:kplan`.

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

The same marketplace works with `codex plugin marketplace`:

```bash
codex plugin marketplace add kkestell/skills
codex plugin marketplace upgrade k
```

Local checkouts work too — point at the repo root:

```bash
codex plugin marketplace add .
```

## Repository Layout

```text
.claude-plugin/
  marketplace.json                         # marketplace catalog (one plugin: k)
skills/                                     # canonical skill content
  kplan/
    SKILL.md
    assets/
  ...
plugins/
  k/                                        # the single plugin wrapper
    .claude-plugin/plugin.json              # Claude Code manifest
    .codex-plugin/plugin.json               # Codex manifest (interface metadata)
    commands/                               # khandoff
    hooks/                                  # dprint markdown-format PostToolUse hook
    skills/
      README.md
      kplan -> ../../../skills/kplan        # directory symlink into canonical skill
      ...
```

Skill content lives once under `skills/<name>/`. The `k` plugin exposes every skill by symlinking each canonical skill into `plugins/k/skills/<name>`, so there is no content duplication. Marketplace plugins dereference within-marketplace symlinks at install time, so end users get real files in their plugin cache.

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
