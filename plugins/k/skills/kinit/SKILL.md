---
name: kinit
description: "Explore a codebase and generate an AGENTS.md file that documents the project's components, commands, and conventions."
metadata:
  argument-hint: "[path to repo root, or blank for current directory]"
---

## Compatibility

- Treat all paths in this skill as relative to the skill directory unless the host environment provides its own skill-directory variable.
- If helper agents are unavailable, disallowed, or unnecessary, do the exploration locally. Do not make delegation mandatory.
- If the host environment has a dedicated question-asking tool, you may use it. Otherwise ask the user directly in a normal message.

## What this skill is for

`kinit` bootstraps a new `AGENTS.md` at the root of a repository. It explores the codebase, identifies its components, and writes a concise reference document that other skills (`kplan`, `kwork`, `ktask`) and AI agents can use for orientation.

If an `AGENTS.md` already exists, stop and tell the user. Offer to regenerate it (replacing the existing file) or abort.

## Workflow

### Phase 1 — Locate the repo

1. Resolve `<repo_root> $ARGUMENTS </repo_root>`. If empty, use the current working directory.
2. Confirm the path is a git repository (check for `.git`). If not, tell the user and stop.

### Phase 2 — Explore

3. Build a picture of the project by reading broadly. Use parallel exploration where possible.
   - Read `README`, `README.md`, or equivalent at the repo root.
   - Read any existing guidance docs: `CLAUDE.md`, `CONTRIBUTING.md`, `Makefile`, `Justfile`, `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `build.gradle`, `pom.xml`, `Gemfile`, `composer.json`, etc.
   - Scan the top-level directory structure to understand how the codebase is organized.
   - Identify the **tech stack**: language(s), framework(s), build system. This is project-level info — list it once unless genuinely separate parts of the project use different stacks.
   - Identify the **major parts of the codebase**: what each directory or module is for. Think in terms of what a new contributor needs to know to orient themselves — not an exhaustive catalog of every folder, but enough to understand the shape of the project.
   - Identify the **essential commands**: build, run, test, lint, format, type-check. Pull these from scripts in `package.json`, `Makefile`, `Justfile`, `Cargo.toml`, `pyproject.toml`, CI configs, or the README. If a command is not discoverable, omit it rather than guessing. Commands belong at the project level unless distinct parts of the project have truly different toolchains.

4. Write a short (2–3 sentence) description of the project. What does it do? What is it for?

### Phase 3 — Write AGENTS.md

5. Write `AGENTS.md` at the repo root using the template from `assets/agents-template.md`. Adapt the template to fit what you found — omit sections that don't apply, but keep the structure recognizable.

6. Present the generated `AGENTS.md` to the user and ask if anything needs adjustment before they commit it.

### Phase 4 — Configure ~/.k access

7. Ask the user if they want to add `~/.k` to the `additionalDirectories` list in `~/.claude/settings.json` (this grants read/write access to the `~/.k` directory for all sessions).
8. If the user answers **yes**:
   - Read `~/.claude/settings.json`.
   - Add `"~/.k"` to `permissions.additionalDirectories` if it is not already present.
   - Write the updated file.
9. If the user answers **no**, skip this step.

## Principles

- **Discover, don't invent** — only document what you can verify from the repo. Never guess at commands.
- **Brief and scannable** — this is a quick-reference doc, not a wiki. One line per codebase entry is ideal.
- **Don't repeat yourself** — if the whole project uses one language and one build system, say it once. Only break things into subsections when genuinely separate tech stacks are involved (e.g., a Go backend + React frontend).
- **Map the shape, not every leaf** — the codebase map should help someone orient. It's not a directory listing. Group logically, skip the obvious (e.g., don't list `src/` in a single-crate Rust project).
- **Leave room for the user** — the "Project Rules" section is intentionally empty. It's theirs to fill in.
