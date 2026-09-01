# AGENTS.md

Guidance for working on Kyle Kestell's agent skill library.

## Purpose

This repository is a plain collection of reusable agent skills. Vercel's
`skills` CLI discovers and installs the skill directories directly. Do not add
Claude Code or Codex plugin wrappers, manifests, marketplace catalogs, or
namespaces.

## Structure

Each canonical skill lives directly under `skills/`:

```text
skills/
  my-skill/
    SKILL.md
    assets/
    references/
    scripts/
```

Only add supporting directories that the skill actually uses.

Unfinished skills live under `wip/` with the same layout. The Makefile installs
only `skills/`, so nothing in `wip/` reaches an agent profile; validation covers
both. Promote a skill by moving its directory into `skills/`.

## Naming rules

- Use kebab-case for directory names.
- Keep the directory name and skill `name` identical.
- Keep one skill per directory.

## Adding a skill

1. Create `skills/<name>/SKILL.md` and any required supporting resources, or
   `wip/<name>/SKILL.md` if it is not ready to install.
2. Run `npm run check`.

### `SKILL.md` frontmatter

Required:

```md
---
name: my-skill
description: Explain what the skill does and when an agent should use it.
---
```

Allowed fields are `name`, `description`, `metadata`, `license`,
`compatibility`, `allowed-tools`, `argument-hint`, and
`disable-model-invocation`.

## Authoring guidance

- Keep `SKILL.md` concise and activation-oriented; its body has a 500-line
  limit.
- Put detailed background material and prompts in `assets/` or `references/`.
- Prefer agent-agnostic instructions unless the skill depends on one agent.
- Describe when the skill should be used, not only what it contains.
- Keep examples practical and short.

## Distribution

The repository itself is the install source. Install all skills into Claude Code
and Codex with:

```bash
npx skills add kkestell/skills --skill '*' --agent claude-code codex --global --yes
```

Do not add plugin or marketplace validation to the repository.

## Validation

Before committing, confirm every `skills/<name>/SKILL.md` and
`wip/<name>/SKILL.md` has valid frontmatter, skill names are unique across both
directories, folder names match skill names, and examples and assets do not
expose secrets.

Run the full check suite:

```bash
npm install
npm run check
```

The check runs typechecking, validator unit tests, skill validation, shellcheck
for shell scripts, Node checks for Node-based skills, and actionlint for GitHub
workflows.
