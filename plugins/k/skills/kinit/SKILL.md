---
name: kinit
description: "Explore a codebase and generate an AGENTS.md file that documents the project's components, commands, and conventions."
metadata:
  argument-hint: "[path to repo root, or blank for current directory]"
---

## Workflow

### Phase 1 — Locate the repo

1. Resolve `<repo_root> $ARGUMENTS </repo_root>`. If empty, use the current working directory.
2. Confirm the path is a git repository (check for `.git`). If not, tell the user and stop.
3. If `AGENTS.md` already exists at the repo root, stop and ask the user whether to regenerate it (replacing the file) or abort.

### Phase 2 — Explore

4. Build a picture of the project by reading broadly. Use parallel exploration where possible.
   - Read `README`, `README.md`, or equivalent at the repo root.
   - Read any existing guidance docs: `CLAUDE.md`, `CONTRIBUTING.md`, `Makefile`, `Justfile`, `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `build.gradle`, `pom.xml`, `Gemfile`, `composer.json`, etc.
   - Scan the top-level directory structure to understand how the codebase is organized.
   - Identify the **tech stack**: language(s), framework(s), build system. This is project-level info — list it once unless genuinely separate parts of the project use different stacks.
   - Identify the **major parts of the codebase**: what each directory or module is for. Think in terms of what a new contributor needs to know to orient themselves — not an exhaustive catalog of every folder, but enough to understand the shape of the project.
   - Identify the **essential commands**: build, run, test, lint, format, type-check. Pull these from scripts in `package.json`, `Makefile`, `Justfile`, `Cargo.toml`, `pyproject.toml`, CI configs, or the README. If a command is not discoverable, omit it rather than guessing. Commands belong at the project level unless distinct parts of the project have truly different toolchains.

5. Write a short (2–3 sentence) description of the project. What does it do? What is it for?

### Phase 3 — Write AGENTS.md

6. Write `AGENTS.md` at the repo root using the template from `assets/agents-template.md`. Adapt the template to fit what you found — omit sections that don't apply, but keep the structure recognizable.

7. Present the generated `AGENTS.md` to the user and ask if anything needs adjustment before they commit it.

### Phase 4 — Configure Claude Code settings

8. Ask the user if they want to add `~/.k` to the `additionalDirectories` list in `~/.claude/settings.json` (this grants read/write access to the `~/.k` directory for all sessions).
9. If the user answers **yes**:
   - Read `~/.claude/settings.json`.
   - Add `"~/.k"` to `permissions.additionalDirectories` if it is not already present.
   - Write the updated file.
10. If the user answers **no**, skip this step.

11. Ask the user if they want to add a `PreToolUse` hook to `~/.claude/settings.json` that blocks `sed` in Bash commands (nudging the agent toward the `Edit` tool instead).
12. If the user answers **yes**:
    - Read `~/.claude/settings.json`.
    - Ensure a `hooks.PreToolUse` entry exists with a `Bash` matcher containing this hook command (skip if an equivalent hook is already present):
      ```
      jq -r '.tool_input.command' | grep -qE '(^|[|&;` (])sed($|[ ])' && echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"sed is blocked. Use the Edit tool instead."}}' || true
      ```
    - Write the updated file.
13. If the user answers **no**, skip this step.

## Principles

- **Discover, don't invent** — only document what you can verify from the repo. Never guess at commands.
- **Brief and scannable** — this is a quick-reference doc, not a wiki. One line per codebase entry is ideal.
- **Don't repeat yourself** — if the whole project uses one language and one build system, say it once. Only break things into subsections when genuinely separate tech stacks are involved (e.g., a Go backend + React frontend).
- **Map the shape, not every leaf** — the codebase map should help someone orient. It's not a directory listing. Group logically, skip the obvious (e.g., don't list `src/` in a single-crate Rust project).
- **Leave room for the user** — the "Project Rules" section is intentionally empty. It's theirs to fill in.
