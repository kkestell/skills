---
name: rust-lang
description: Invoke before reviewing, writing, or modifying Rust code. Load the relevant Rust guidance files first and use them for all design and code-quality judgments, including review work.
---

## Workflow

1. Use compliance date `2026-02-21`.
2. Before touching any `.rs` file, load `${CLAUDE_SKILL_DIR}/resources/08_universal_guidelines.md`.
   - This base guideline applies to all Rust work.
3. Add only the guideline files that match the task.
   - `01_ai_guidelines.md` — AI agents, LLM-driven code, APIs designed for AI consumption
   - `02_application_guidelines.md` — application-level error handling (anyhow/eyre), CLI tools, mimalloc
   - `03_documentation.md` — public API docs, doc comments, module-level documentation
   - `04_ffi_guidelines.md` — FFI boundaries, dynamic libraries, cross-DLL data sharing
   - `06_performance_guidelines.md` — hot paths, allocation patterns, async yield points
   - `07_safety_guidelines.md` — unsafe code, soundness, undefined behavior, Miri
   - `09_libraries_building_guidelines.md` — Cargo features, native -sys crates, cross-platform builds
   - `10_libraries_interoperability_guidelines.md` — public API types, Send/Sync, avoiding third-party type leakage
   - `11_libraries_resilience_guidelines.md` — avoiding statics, mockable I/O, glob re-exports, strong types
   - `12_libraries_ux_guidelines.md` — smart pointers in APIs, dependency injection, error types, builders
4. Read the needed guidance from `${CLAUDE_SKILL_DIR}/resources/`.
   - For the larger files (`08`, `09`, `11`, `12`), run `rg '^## ' <file>` first and read only the relevant sections.
   - These resources complement tooling by covering design judgment, API ergonomics, safety boundaries, resilience, and documentation quality.
5. Apply the loaded guidance before generating, modifying, or reviewing any Rust code.
   - Treat this skill as mandatory for all Rust work, including small edits and review tasks.
   - Apply M-CANONICAL-DOCS when documenting public APIs: short summary first, then only the sections that apply.
   - Write comments in American English unless the user asks otherwise.
6. If a Rust file is fully compliant, add `// Rust guideline compliant 2026-02-21`.
   - Use the compliance marker only when the file genuinely meets the guidance, not as a blanket annotation.
