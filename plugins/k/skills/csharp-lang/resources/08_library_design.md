# Library Design

## Dependency Injection

When the application already uses a DI container, prefer constructor injection and register services with appropriate lifetimes. Avoid service locator pattern. Reusable libraries should not require a specific container; provide plain constructors and optional `IServiceCollection` integration where it helps.

## Options Pattern

Use `IOptions<T>`, `IOptionsMonitor<T>`, or `IOptionsSnapshot<T>` for configuration. Create strongly-typed options classes. Bind from configuration in startup.

## Logging Integration

Inject `ILogger<T>` where `T` is the consuming type. Use structured logging with named placeholders. Use logger source generators for high-performance logging.

## Interface Segregation

Define small, focused interfaces. Prefer `IReadOnlyList<T>` over `IList<T>` when mutation isn't needed. Split large interfaces into role-specific ones.

## Factory Pattern

Use `Func<T>` or factory interfaces for runtime dependency creation. Avoid passing `IServiceProvider` to construct objects manually.

## Avoid Global State

No static mutable state. If you need global access, wrap in a service and inject it. Makes testing and parallel execution possible.

## Versioning

- Add new overloads rather than changing signatures
- Mark obsolete members with `[Obsolete]` with migration guidance
- Avoid adding optional parameters to existing public members; prefer new overloads for binary compatibility
- Consider `required` properties for new required configuration

## Package Design

Keep packages focused. Avoid taking dependencies when you can avoid them. Use `Nullable` and `Generics` to reduce overloads. For libraries, target the lowest .NET version your consumers genuinely need; for new applications and services, the default baseline remains `net10.0`.

## Public API Surface

Minimize public API surface. Internal is the default; export only what consumers need. Every public type is a commitment.
