# AGENTS.md

Guidance for working on this repository — Kyle Kestell's personal agent skill library.

## Purpose

This repo holds general-purpose, reusable agent skills, published as a single Claude Code / Codex plugin named `k`.

## Structure

Skill content lives once under `plugins/k/skills/<name>/`, inside the plugin directory so the plugin root is fully self-contained. Repo-root `skills/<name>` symlinks point into those canonical copies, giving tooling and editors the conventional `skills/` path without duplicating content.

```text
plugins/
  k/
    .claude-plugin/plugin.json             # Claude Code manifest
    .codex-plugin/plugin.json              # Codex manifest (interface metadata + "skills": "./skills/")
    commands/                              # slash commands (khandoff)
    skills/
      README.md                            # workflow overview
      my-skill/                            # canonical skill content
        SKILL.md
        assets/
skills/
  my-skill -> ../plugins/k/skills/my-skill # symlink into the canonical skill
```

- `plugins/k/skills/<name>/SKILL.md` is the canonical content, packaged directly under the plugin root (`<plugin-root>/skills/<name>/SKILL.md`, the [default plugin layout](https://code.claude.com/docs/en/plugins-reference#skills)).
- `skills/<name> -> ../plugins/k/skills/<name>` re-exposes each skill at the repo-root `skills/` path that the validator reads and the docs reference.
- The real files must live inside `plugins/k/`: Codex copies the plugin directory into its install cache and does not follow symlinks pointing outside that directory, so a symlink that escapes the plugin root is dropped and the skill goes missing in Codex.
- The repo-root `.claude-plugin/marketplace.json` catalogs the `k` plugin and is read natively by Claude Code (`/plugin marketplace add ...`) and Codex (`codex plugin marketplace add ...`).

## Naming Rules

- Use kebab-case for directory names.
- Keep the directory name and skill `name` identical (the validator enforces this).
- One skill per directory.

## Adding a Skill

1. Create `plugins/k/skills/<name>/SKILL.md` with valid frontmatter (see below).
2. Re-expose it at the repo root:

   ```bash
   ln -s ../plugins/k/skills/<name> skills/<name>
   ```

3. Run `npm run check`.

### `SKILL.md` frontmatter

Required:

```md
---
name: my-skill
description: Explain what the skill does and when an agent should use it.
---
```

Allowed fields (the validator rejects anything else): `name`, `description`, `metadata`, `license`, `compatibility`, `allowed-tools`, `argument-hint`, `disable-model-invocation`.

`argument-hint` and `disable-model-invocation` are useful for skills that double as explicit slash commands:

```md
---
name: my-skill
description: ...
argument-hint: "[what to pass]"
disable-model-invocation: true
---
```

## Authoring Guidance

- Keep `SKILL.md` concise and activation-oriented; the body has a 500-line limit.
- Put detailed background material and prompts in the skill's `assets/` directory.
- Prefer agent-agnostic instructions unless the skill truly depends on one agent.
- Describe when the skill should be used, not just what it contains.
- Keep examples practical and short.

## Versioning

The `k` plugin declares an explicit `version` in `plugins/k/.claude-plugin/plugin.json` (and the matching `.codex-plugin/plugin.json`). Bump it when shipping a meaningful change. Keep the two manifests in sync.

## Validation

Before committing:

- Confirm each `skills/<name>/SKILL.md` exists with valid frontmatter (`name` + `description`).
- Confirm skill names are unique and match their directory names.
- Confirm examples and assets do not expose secrets.
- Run the full check suite:

  ```bash
  npm install
  npm run check
  ```

`npm run check` runs typecheck, the validator unit tests, skill validation, shellcheck (over `scripts/` and `skills/*/scripts/`), Node typechecks for any Node-based skills, and actionlint over the GitHub workflows.
