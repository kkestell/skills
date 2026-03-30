# AoT and Source Generators

## Native AOT

Native AOT compiles .NET to native code at build time, eliminating JIT and enabling smaller, faster-starting applications. Enable with `<PublishAot>true</PublishAot>`.

## AoT Compatibility

To make code AoT-compatible:
- Avoid reflection-based serialization; use source generators
- Avoid dynamic code generation (`System.Reflection.Emit`)
- Use source generators for code that would otherwise use runtime reflection
- Mark roots with `[DynamicDependency]`, `[DynamicallyAccessedMembers]`, `[RequiresUnreferencedCode]`, or `[RequiresDynamicCode]` when necessary
- For libraries that claim AoT support, set `<IsAotCompatible>true</IsAotCompatible>` and fix the resulting analyzer warnings instead of suppressing them by default

## JSON Source Generators

Use `System.Text.Json` source generators instead of reflection-based serialization. Create a `JsonSerializerContext` derived class:

- Create partial class deriving from `JsonSerializerContext`
- Annotate with `[JsonSerializable(typeof(T))]` for types to serialize
- Use `JsonSerializer.Serialize(value, MyContext.Default.T)` instead of `JsonSerializer.Serialize(value)`
- For ASP.NET Core, register the generated context with the app's `JsonSerializerOptions`

## Trimmer Safety

The IL trimmer removes unused code. To stay trimmer-safe:
- Avoid `DynamicDependency` where possible
- Use `[DynamicallyAccessedMembers]` to preserve members accessed via reflection
- Test with `<PublishTrimmed>true</PublishTrimmed>` during development
- Use the SDK analyzers (`<EnableTrimAnalyzer>true</EnableTrimAnalyzer>` and, when relevant, `<EnableAotAnalyzer>true</EnableAotAnalyzer>`) or `<IsAotCompatible>true</IsAotCompatible>` for libraries
- On .NET 10 libraries, enable `<VerifyReferenceAotCompatibility>true</VerifyReferenceAotCompatibility>` when you need stronger guarantees about downstream AoT compatibility

## Regex Source Generators

Use `[GeneratedRegex]` attribute for compile-time regex generation. This is faster and trimmer-safe compared to `new Regex()` at runtime.

## Logging Source Generators

Use `[LoggerMessage]` attribute for high-performance logging. This avoids boxing and string formatting overhead. Creates compile-time logging methods.

## Marshal Source Generators (P/Invoke)

Use `[LibraryImport]` instead of `DllImport` for AoT-compatible P/Invoke. Source generator handles marshalling at compile time.

## Configuration Binder Source Generator

Do not assume `ConfigurationBinder` source generation is always on. Enable it explicitly with `<EnableConfigurationBindingGenerator>true</EnableConfigurationBindingGenerator>` when you want it, and remember that `<PublishTrimmed>true</PublishTrimmed>` also enables it in supported applications. Ensure options types have supported bindable shapes and avoid overly clever constructors or abstractions.

## When to Use Source Generators

Use source generators when:
- You need compile-time code generation
- You want to eliminate reflection
- You need AoT compatibility
- You want better performance by moving work to compile time

Do NOT use source generators for simple cases where runtime code is sufficient and performance is not critical.
