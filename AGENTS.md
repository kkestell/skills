# AGENTS.md

Guidance for working on Kyle Kestell's agent skill library.

## Purpose

This repository is a plain collection of reusable agent skills. Vercel's
`skills` CLI discovers and installs the skill directories directly. Do not add
Claude Code or Codex plugin wrappers, manifests, marketplace catalogs, or
namespaces.

## Structure

Skills are organized by group under `skills/`:

```text
skills/
  core/
    my-skill/
      SKILL.md
      assets/
      references/
      scripts/
  ext/
  wip/
```

Only add supporting directories that the skill actually uses.

Core skills form the standard workflow and must not refer to skills in `ext/`.
Standalone skills live in `ext/`, and unfinished skills live in `wip/`.
`profiles.py` installs only the groups explicitly selected; validation covers
all three. Promote a skill by moving its directory between groups.

## Hooks

Agent hooks live in `hooks/` as standalone shell scripts, outside the skill
groups. `profiles.py install-hooks` copies them into a harness configuration
directory and registers them. A hook must read its event payload as JSON on
stdin, work under both Claude Code and Codex, and exit 0 even when it cannot do
its job, so a cosmetic failure never surfaces as an agent error. `npm run
check` shellchecks everything in `hooks/`.

## Naming rules

- Use kebab-case for directory names.
- Keep the directory name and skill `name` identical.
- Keep one skill per directory.

## Adding a skill

1. Create `skills/<group>/<name>/SKILL.md` and any required supporting
   resources.
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

The repository itself is the install source. Install the core and extension
groups into Claude Code and Codex with:

```bash
./profiles.py sync-skills core,ext --claude --codex
```

Do not add plugin or marketplace validation to the repository.

## Validation

Before committing, confirm every `skills/<group>/<name>/SKILL.md` has valid
frontmatter, skill names are unique across all groups, folder names match skill
names, and examples and assets do not expose secrets.

Run the full check suite:

```bash
npm install
npm run check
```

The check runs typechecking, validator unit tests, skill validation, shellcheck
for shell scripts, Node checks for Node-based skills, and actionlint for GitHub
workflows.
