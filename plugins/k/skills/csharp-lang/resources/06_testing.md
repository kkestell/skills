# Testing

## Test Framework Choice

xUnit is a good default for many modern .NET codebases. NUnit and MSTest are also acceptable when they match the existing repository, tooling, or team expertise. Prefer consistency over framework churn.

## Arrange-Act-Assert Pattern

Structure tests clearly with three sections: Arrange (set up), Act (execute), Assert (verify). Separate sections with blank lines. Keep tests focused on a single behavior.

## Test Naming Convention

Name tests to describe the scenario and expected outcome: `MethodName_Scenario_ExpectedResult`. Use `Fact` for single test cases, `Theory` with `InlineData` for parameterized tests.

## Use Theory for Parameterized Tests

Use `[Theory]` with `[InlineData]` to test multiple inputs with the same logic. Reduces duplication and makes it easy to add new test cases.

## Test Doubles

- **Stub**: Returns canned answers
- **Mock**: Verifies interactions
- **Fake**: Working but simplified implementation

Use interfaces for testability. Avoid mocking concrete classes.

## Mock Libraries

Moq is widely used but has quirks. NSubstitute has cleaner syntax. Use the library your team prefers, but be consistent.

## Avoid Test Interdependence

Tests must be independent. No shared mutable state between tests. Use fixture classes for shared setup. Use `IDisposable`, `IAsyncDisposable`, or framework-native lifetime hooks for cleanup.

## Test What Matters

Test behavior, not implementation details. Don't test private methods directly—if they need testing, refactor. Focus on observable outcomes.

## Integration Tests

Use `WebApplicationFactory` for ASP.NET Core integration tests. Use `TestServer` for in-memory testing. Use test containers for database integration tests.

## BenchmarkDotNet for Performance

Use BenchmarkDotNet for microbenchmarks. Never use `Stopwatch` for performance comparisons—the JIT and runtime optimizations make naive timing misleading.
