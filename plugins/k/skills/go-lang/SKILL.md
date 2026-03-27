---
name: go-lang
description: Invoke before reviewing, writing, or modifying Go code. Load the relevant Go guidance files first and use them for all code-quality judgments, even on small changes.
---

## Workflow

1. Before touching any `.go` file, load `${CLAUDE_SKILL_DIR}/resources/01_design_guidelines.md`.
   - This base guideline applies to all Go work.
2. Add only the guideline files that match the task.
   - `02_error_handling.md`
   - `03_concurrency.md`
   - `04_interfaces_types.md`
   - `05_testing.md`
   - `06_documentation.md`
3. Read the needed guidance from `${CLAUDE_SKILL_DIR}/resources/`.
   - For larger files, run `rg '^## ' <file>` first and read only the relevant sections.
   - These resources capture the design taste that tooling cannot: API shape, naming judgment, error strategy, concurrency architecture, and documentation quality.
4. Apply the loaded guidance before generating, modifying, or reviewing any Go code.
   - Treat this skill as mandatory for all Go development and review work, including small changes.
   - Use these priorities in order: clarity, simplicity, concision, maintainability, consistency.
   - Prefer the simplest tool sufficient for the job: core language features first, then the standard library, then established libraries, then new dependencies.
   - Write comments in American English unless the user asks otherwise.
5. Run normal Go tooling separately.
   - This skill covers the judgment calls that formatters and linters do not.
