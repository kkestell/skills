# Universal Guidelines

## Names are Free of Weasel Words

Type names should be free of weasel words that do not meaningfully add information. Common offenders: `Service`, `Manager`, `Controller`, `Helper`, `Util`. An item handling many bookings can be called `Bookings`. If it does something more specific, append that quality: `BookingDispatcher`.

## Enable Nullable Reference Types

All new C# projects must enable nullable reference types: `<Nullable>enable</Nullable>`. Reference types become non-nullable by default. Use `ArgumentNullException.ThrowIfNull()` at method entry. When null is valid, make it explicit with `T?`.

## Assume .NET 10 and C# 14 by Default

For new work, assume `net10.0` and the SDK-default language version unless the repository or user specifies different compatibility constraints. When supporting older platforms, prefer multi-targeting over artificially avoiding modern syntax everywhere.

## Use Modern Project Structure

- **File-scoped namespaces**: `namespace MyNamespace;` at the top of the file
- **Global usings** in a dedicated file for commonly used namespaces
- **Implicit usings** enabled in project file
- **Top-level statements** for small entry points; prefer an explicit `Program` type once startup logic grows beyond a thin bootstrap

## Prefer Records for Data-Carrying Types

Use `record` for types that primarily carry data and benefit from value-based equality. Records are not automatically immutable: use `init`, readonly members, and careful API design when immutability matters. Use `record struct` only when value semantics are a good fit and copying costs are acceptable. Do not choose `struct` or `record struct` to try to force stack allocation.

## Use Pattern Matching

Prefer pattern matching over `is` + cast. Use switch expressions over switch statements. Leverage property patterns, positional patterns (with records), and list patterns where applicable.

## Magic Values are Documented

Hardcoded values must be accompanied by documentation explaining why the value was chosen, side effects if changed, and external dependencies. Prefer named constants over inline values.

## Use Structured Logging

Use `Microsoft.Extensions.Logging` with named placeholders in templates, not string interpolation. For high-performance scenarios, use `LoggerMessage.Define` or source generators. Never log passwords, tokens, personal data, or API keys.

## Public Types Should Have XML Documentation

Public APIs in reusable libraries and packages should have XML documentation (`<summary>`, `<param>`, `<returns>`). In applications, document non-obvious public surfaces and externally consumed contracts. Enable documentation file generation for libraries: `<GenerateDocumentationFile>true</GenerateDocumentationFile>`.

## Follow .NET Conventions

- PascalCase for public members
- Prefix interfaces with `I`
- `-Async` suffix for async methods
- Avoid exposing `List<T>` in public APIs; prefer `IReadOnlyList<T>`, `IReadOnlyCollection<T>`, or `IEnumerable<T>` unless callers truly need mutation
- `Exception` suffix for exception types
- Prefer `TryGet` pattern for methods that may fail without throwing

Reference the official [Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/) and [C# Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions).
