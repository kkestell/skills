---
name: kinit
description: "Explore a codebase and generate an AGENTS.md file that documents the project and routes future work to the repository workflow."
argument-hint: "[path to repo root, or blank for current directory]"
---

## Workflow

### Locate the repository

1. Resolve `<repo_root> $ARGUMENTS </repo_root>`. If empty, use the current
   working directory.
2. Confirm that the path is a Git repository by checking for `.git`. If not,
   tell the user and stop.
3. If `AGENTS.md` already exists at the repository root, ask whether to
   regenerate it or leave it unchanged. Never overwrite it without confirmation.

### Explore

4. Build a picture of the project from repository evidence.
   - Read the root README and existing guidance such as `CLAUDE.md` and
     `CONTRIBUTING.md`.
   - Read build manifests, task files, and CI configuration, such as `Makefile`,
     `Justfile`, `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`,
     `build.gradle`, `pom.xml`, `Gemfile`, and `composer.json`.
   - Scan the top-level structure and the main source and test entry points.
   - Identify the tech stack, major codebase parts, and verified commands for
     building, running, testing, linting, formatting, and type-checking. Omit a
     command that cannot be discovered instead of guessing it.

### Write AGENTS.md

5. Write `AGENTS.md` from `assets/agents-template.md`.
   - Fill project-specific sections only with verified facts.
   - Omit a project description, tech-stack item, codebase-map entry, command,
     or entire section when the repository does not establish it. Do not leave
     template prompts in the generated file.
   - Keep the standard document-routing and Project Rules sections. Adapt a
     standard rule only when the repository has an explicit conflicting
     convention.
   - An empty repository still receives the standard sections. Do not ask the
     user to invent its specification, architecture, or roadmap during
     initialization.
6. Write `CLAUDE.md` at the repository root containing only `@AGENTS.md` so
   Claude Code uses the same guidance. If it already contains anything else,
   leave it untouched and tell the user.
7. Present the generated `AGENTS.md` and ask whether it needs adjustment.

## Principles

- **Initialize the workflow, not the product.** `kinit` does not create or infer
  the specification, architecture, roadmap, or implementation plans.
- **Discover, don't invent.** Only document what the repository establishes.
- **Map the shape, not every leaf.** Orient a contributor without reproducing a
  directory listing.
- **Keep the durable rules.** An empty repository still needs document ownership
  and skill-routing guidance.
- **Preserve unrelated work.** Do not modify files other than `AGENTS.md` and
  the `CLAUDE.md` alias.
