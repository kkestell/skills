---
name: krust
description: Invoke before reviewing, writing, or modifying Rust code (`.rs` files). Enforce guideline-driven Rust development by loading the relevant Microsoft Rust guidance before making design or code-quality judgments. Mandatory for all Rust development, including trivial changes and verification work.
---

**Compliance date: 2026-02-21**

<!-- The Pragmatic Rust Guidelines are copyrighted (c) by Microsoft Corporation and licensed under the MIT license. -->

# Rust Development Skill

Enforces structured, guideline-driven Rust development. Before writing or modifying any `.rs` file, load the relevant guidelines below.

## Which Guidelines to Load

Load **only** the files that apply to the current task. Use segmented reading (`offset`/`limit`) for large files.

**Always load:** `${CLAUDE_SKILL_DIR}/resources/08_universal_guidelines.md` — applies to all Rust tasks.

**Load when relevant:**

| Guideline                                     | When it applies                                                     |
| --------------------------------------------- | ------------------------------------------------------------------- |
| `01_ai_guidelines.md`                         | AI agents, LLM-driven code, APIs designed for AI consumption        |
| `02_application_guidelines.md`                | Application-level error handling (anyhow/eyre), CLI tools, mimalloc |
| `03_documentation.md`                         | Public API docs, doc comments, module-level documentation           |
| `04_ffi_guidelines.md`                        | FFI boundaries, dynamic libraries, cross-DLL data sharing           |
| `06_performance_guidelines.md`                | Hot paths, allocation patterns, async yield points                  |
| `07_safety_guidelines.md`                     | Unsafe code, soundness, undefined behavior, Miri                    |
| `09_libraries_building_guidelines.md`         | Cargo features, native -sys crates, cross-platform builds           |
| `10_libraries_interoperability_guidelines.md` | Public API types, Send/Sync, avoiding third-party type leakage      |
| `11_libraries_resilience_guidelines.md`       | Avoiding statics, mockable I/O, glob re-exports, strong types       |
| `12_libraries_ux_guidelines.md`               | Smart pointers in APIs, dependency injection, error types, builders |

All guideline files are at `${CLAUDE_SKILL_DIR}/resources/<filename>`.

For large files (`08`, `09`, `11`, `12`), list headings first with `rg '^## ' <file>` and load only the relevant sections.

## Coding Rules

1. Load the necessary guideline files before generating any Rust code.
2. Apply the M-CANONICAL-DOCS documentation format: summary sentence < 15 words, then extended docs, Examples, Errors, Panics, Safety, Abort sections as applicable.
3. Comments in American English unless the user requests otherwise.
4. If the file is fully compliant, add: `// Rust guideline compliant 2026-02-21`
