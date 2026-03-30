# Performance

## Span<T> and Memory<T>

Use `Span<T>` for contiguous memory regions when you need zero-allocation slicing. `Span<T>` is stack-only and cannot be stored in fields. Use `Memory<T>` when you need to store the reference on the heap or across async boundaries.

## stackalloc

Use `stackalloc` to allocate arrays on the stack for small, short-lived buffers. Avoid for buffers larger than 1KB (risks stack overflow). Combine with `Span<T>` for safe stack allocation.

## ref struct

Types that must be stack-only (like `Span<T>`) are `ref struct`. Use `ref struct` when building low-level primitives that wrap stack data. Cannot be boxed, captured in lambdas, or stored in fields.

## ArrayPool<T>

Use `ArrayPool<T>.Shared` for renting large arrays instead of allocating new ones. Always return arrays to the pool. Critical for high-throughput scenarios with frequent large allocations.

## Object Pooling

Pool expensive-to-create objects. Use `ObjectPool<T>` from `Microsoft.Extensions.ObjectPool`. Useful for StringBuilder, large buffers, or objects with expensive initialization.

## Avoid Allocations in Hot Paths

- Use `Span<T>` instead of `string` for parsing
- Use `stackalloc` instead of `new byte[]` for small buffers
- Use `String.Create` for formatting without intermediate strings
- Avoid closures in hot delegates

## String Interpolation

Use `$""` interpolation for readability. For performance-critical code, use `String.Create` or `MemoryExtensions.TryWrite` to format directly into a buffer.

## Boxing Awareness

Avoid implicit boxing of value types (interface casts, `object` parameters, non-generic collections). Use generic versions of methods and collections.

## Use BenchmarkDotNet

Always measure performance with BenchmarkDotNet. Never trust intuition about performance. The JIT and CPU optimizations make naive predictions unreliable.

## StringBuilder

Use `StringBuilder` when concatenating many strings in a loop. For simple concatenation (few operations), string interpolation or `+` is fine—the compiler optimizes.