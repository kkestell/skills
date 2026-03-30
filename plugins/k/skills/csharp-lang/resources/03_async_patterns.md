# Async Patterns

## Async Suffix Convention

All async methods must use the `-Async` suffix (e.g., `ProcessAsync`, `GetDataAsync`). This makes async nature explicit at the call site.

## Prefer async/await over ContinueWith

Use `await` instead of `ContinueWith`. The compiler handles exception handling, synchronization context, and task unwrapping correctly.

## Use ValueTask for Hot Paths

Use `ValueTask<T>` (or `ValueTask`) instead of `Task<T>` when:
- The operation is frequently synchronous (cached or fast-path results)
- The method is called in high-throughput scenarios
- You want to avoid allocations

Do not convert all `Task<T>` to `ValueTask<T>` indiscriminately—`ValueTask` has constraints (can only await once).

## Always Pass CancellationToken

All async methods that perform I/O should accept a `CancellationToken` parameter. Put it at the end of the parameter list. Pass the token through to all downstream async calls. Check `token.IsCancellationRequested` in CPU-bound work.

## Avoid async void

Never use `async void` except for event handlers. `async void` exceptions are unobservable and crash the process. Use `async Task` for all non-event async methods.

## ConfigureAwait

In library code, use `ConfigureAwait(false)` to avoid capturing the synchronization context. This prevents deadlocks when consumers block on async code. In application code (UI apps, ASP.NET Core), `ConfigureAwait(false)` is unnecessary but harmless.

## Async Enumerable (IAsyncEnumerable)

Use `IAsyncEnumerable<T>` for streaming data that arrives asynchronously. Use `await foreach` to consume. Prefer over methods returning `Task<List<T>>` when data can be processed incrementally.

## Avoid Deadlock Patterns

Never call `.Result` or `.Wait()` on a Task in contexts with a synchronization context (UI apps, legacy ASP.NET). This causes deadlocks. Use `await` all the way down.

## Thread Safety in Async Code

Remember: `await` yields control, and resumption may be on a different thread. Locks held across `await` can cause deadlocks. Use `SemaphoreSlim.WaitAsync()` instead of `lock` for async synchronization.