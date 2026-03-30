# Collections and LINQ

## IEnumerable vs IQueryable

Use `IEnumerable<T>` for in-memory collections. Use `IQueryable<T>` for deferred database queries. Be aware that `IQueryable` can cause multiple database round trips if enumerated multiple times.

## Materialization Awareness

Know when LINQ queries execute: iteration (`foreach`), conversion methods (`ToList`, `ToArray`, `ToDictionary`), and element operators (`First`, `Single`). Avoid multiple enumeration of deferred queries—materialize once if needed multiple times.

## Choose the Right Collection Type

- `List<T>`: General-purpose ordered collection, frequent random access
- `IReadOnlyList<T>`: Public API return type when callers shouldn't modify
- `IEnumerable<T>`: Public API return type for deferred execution or when only iteration needed
- `Dictionary<K,V>`: O(1) key lookup
- `HashSet<T>`: Unique items, O(1) contains check
- `ImmutableArray<T>`: Immutable, compact storage
- `Span<T>`: High-performance, stack-only, no allocations

## Avoid List<T> in Public APIs

Return `IReadOnlyList<T>`, `IReadOnlyCollection<T>`, or `IEnumerable<T>` from public APIs. Accept the most general interface that provides needed functionality.

## Prefer Query Syntax for Complex Queries

For simple operations, method syntax (`Where`, `Select`) is fine. For complex queries involving joins, groups, or let clauses, query syntax can be more readable.

## Avoid Multiple Enumeration

If you need to iterate a sequence multiple times, materialize it first with `ToList()` or `ToArray()`. Multiple enumeration of deferred queries causes repeated work (and repeated database queries for `IQueryable`).

## Use Collection Expressions

C# 12 collection expressions work with any type that has a collection builder. Use `[]` syntax and spread operator `..` for combining collections.

## Prefer LINQ over Loops for Transformations

Use LINQ for filtering, projection, and aggregation operations. It's more declarative and often more readable. Use loops when you need side effects or complex state management.