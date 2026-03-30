# Modern Syntax Guidelines

## Use Records for Data Types

Use `record` for types that primarily carry data and benefit from value-based equality. Records are not automatically immutable; use `init`, readonly members, and careful API design when immutability matters. Use `record struct` when value semantics are a good fit and copying costs are acceptable. Do not choose `record struct` to try to force stack allocation.

## Use Primary Constructors Judiciously

Classes and structs can have primary constructors. Use them when constructor parameters truly represent the type's ongoing state or dependencies and the shortened form stays readable. Prefer explicit fields, properties, or regular constructors when validation, multiple overloads, or hidden state would be clearer. Do not use primary constructors solely to shave off a few lines.

## Use Extension Members (C# 14)

Use extension members when they make an API more discoverable and cohesive around the receiver type. They work best for library-style affordances that naturally belong near the extended type. Avoid turning them into a grab bag of unrelated helpers.

## Use Collection Expressions (C# 12)

Use collection expressions `[]` for initializing lists, arrays, sets, and dictionaries. Use the spread operator `..` to inline elements from other collections. Works with any type that has a collection builder pattern.

## Use Null-Conditional Assignment (C# 14)

When you need to assign through an optional receiver, prefer null-conditional assignment over verbose guard code. It keeps intent obvious while preserving null safety.

## Use Field-Backed Properties (C# 14) Carefully

Use the `field` keyword inside property accessors when you need simple validation, normalization, or side effects without introducing a separate backing field name. If property logic becomes non-trivial, use an explicit field for readability.

## Use Pattern Matching Extensively

Prefer switch expressions over switch statements. Use property patterns to match on object properties. Use positional patterns with records (automatic deconstruction). Use list patterns to match array/list structure.

## Use File-Scoped Namespaces

Put namespace declaration on a single line at the top of the file: `namespace MyNamespace;`. Reduces indentation levels throughout the file.

## Use Global Usings

Create a `GlobalUsings.cs` file for commonly used namespaces. Enable `<ImplicitUsings>enable</ImplicitUsings>` in the project file for SDK-provided implicit usings.

## Prefer Span-Friendly APIs

Modern C# and .NET make `Span<T>` and `ReadOnlySpan<T>` easier to use with fewer explicit conversions. Prefer span-friendly overloads for parsing, formatting, and hot-path text or buffer work when they improve performance without harming readability.

## Know the Smaller C# 14 Features

Keep the remaining C# 14 features in mind when they simplify real code:

- `nameof(List<>)` works for unbound generic types
- Partial constructors and partial events improve source-generator and metaprogramming scenarios
- User-defined compound assignment operators can make numeric or domain-specific types more natural to use

## Use Required and Init Properties

Use `required` keyword for properties that must be set during initialization. Use `init` accessors for properties that can only be set during object construction. Combine with object initializers for immutable types without full record semantics.

## Use Target-Typed New

When type is inferable from context, use `new()` without repeating the type name. Exception: when type isn't clear from immediate context, spell it out for readability.

## Prefer Expression Bodies

Use expression-bodied members (`=>`) for single-expression properties and methods. Use block syntax for complex logic.
