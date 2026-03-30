---
name: csharp-lang
description: Invoke before reviewing, writing, or modifying C# code. Load the relevant C# guidance files first and use them for all design and code-quality judgments, including review work. Focuses on C# 14 and .NET 10 idioms and patterns.
---

## Workflow

1. Use compliance date `2026-03-30`.
2. Assume C# 14 on .NET 10 (`net10.0`) unless the repository already targets another version or the user asks otherwise.
   - Follow the repo's existing target frameworks and compatibility constraints before up-leveling code.
3. Before touching any `.cs`, `.csproj`, `.props`, or `.targets` file, load `${CLAUDE_SKILL_DIR}/resources/01_universal_guidelines.md`.
   - This base guideline applies to all C# work.
4. Add only the guideline files that match the task.
   - `02_modern_syntax.md` — records, primary constructors, extension members, field-backed properties, pattern matching, collection expressions
   - `03_async_patterns.md` — async/await, ValueTask, cancellation, async enumerable, deadlock avoidance
   - `04_collections_linq.md` — LINQ idioms, IEnumerable vs IQueryable, materialization, collection choices
   - `05_error_handling.md` — exception patterns, Result types, nullable reference types, validation
   - `06_testing.md` — xUnit/NUnit/MSTest tradeoffs, mocking, test naming, arrange-act-assert
   - `07_performance.md` — Span<T>, Memory<T>, stackalloc, pooling, ref struct, benchmarks
   - `08_library_design.md` — API shape, dependency injection boundaries, configuration, logging integration
   - `09_aot_source_generators.md` — AoT compatibility, Native AOT, JSON source generators, trimmer safety
   - `10_documentation.md` — XML docs, README patterns, example code
   - `11_project_baseline.md` — `net10.0` defaults, multi-targeting, `LangVersion`, analyzers, CI expectations
5. Read the needed guidance from `${CLAUDE_SKILL_DIR}/resources/`.
   - For larger files, run `rg '^## ' <file>` first and read only the relevant sections.
   - These resources complement tooling by covering design judgment, API ergonomics, and modern C# idioms.
6. Apply the loaded guidance before generating, modifying, or reviewing any C# code.
   - Treat this skill as mandatory for all C# work, including small edits and review tasks.
   - Prefer modern C# syntax when it improves clarity, correctness, or API design; do not use newer constructs purely to shorten code.
   - Use records for value semantics and primary constructors when constructor parameters genuinely represent the type's ongoing state or dependencies.
   - Write comments and documentation in American English unless the user asks otherwise.
7. Do not add compliance marker comments to source files.
   - Record compliance in review output, tests, analyzers, or automation instead of code comments.
