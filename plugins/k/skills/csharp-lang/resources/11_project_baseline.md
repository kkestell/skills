# Project Baseline

## Default Target Framework

For new applications, services, tools, and tests, default to `net10.0`. Multi-target only when consumer requirements, package reach, or platform support make it necessary.

## Language Version

Let the SDK choose the language version from the target framework unless the repository has a specific reason to pin it. For `net10.0`, assume C# 14. Do not add `<LangVersion>` just to restate the default.

## Project Defaults

Enable nullable reference types and implicit usings for new SDK-style projects:

- `<Nullable>enable</Nullable>`
- `<ImplicitUsings>enable</ImplicitUsings>`

Keep SDK analyzers on. Prefer repository-wide `.editorconfig` and build settings over ad hoc file-level style rules.

## Multi-Targeting

If a library must support older target frameworks, multi-target instead of forcing the whole codebase down to the lowest common denominator. Isolate target-specific APIs with `#if`, partial types, or thin adapter layers.

## Compatibility and Warnings

Prefer new overloads over changing public signatures. Avoid adding optional parameters to existing public members because they can create binary compatibility problems for already-compiled callers.

Treat warnings as work to triage, not noise to suppress. For libraries and shared components, prefer stricter CI settings than local developer defaults.

## Trim and AOT Readiness

If a library claims trim or Native AOT support, configure the project accordingly and load `09_aot_source_generators.md`.
