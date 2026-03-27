# Concurrency

Go makes concurrency easy to start but requires discipline to get right. The core principle: **share memory by communicating, don't communicate by sharing memory.** Channels are the default coordination mechanism; reach for mutexes only when a channel would be unnecessarily complex (simple reference counting, guarding a single field).

## Goroutine Lifetimes Must Be Obvious

Every goroutine you spawn should have a clear answer to: "when does this exit?" A goroutine blocked on a channel send or receive will never be garbage collected — it leaks, along with everything it references.

Make lifetimes obvious through structure:

- **`context.Context` for cancellation**: Pass a context and select on `ctx.Done()` so the goroutine exits when the caller is done.
- **`sync.WaitGroup` for scoped work**: When goroutines must finish before the parent returns, use a WaitGroup. This prevents goroutines from outliving their parent function.
- **Channel closure for producer/consumer**: A producer goroutine closes the channel when done; consumers range over it and exit naturally.

If the lifetime isn't obvious from reading the code, document when and why the goroutine exits.

## Prefer Channels for Coordination, Mutexes for State

Use channels when goroutines need to pass ownership of data, signal completion, or coordinate a pipeline. Use `sync.Mutex` (or `sync.RWMutex`) when multiple goroutines need to read or write a shared field and the interaction is simple enough that a lock is clearer than a channel.

Signs you should use a channel: the data flows in one direction, there's a producer/consumer relationship, or you need fan-out/fan-in.

Signs you should use a mutex: you're protecting a map or counter, the critical section is a few lines, or the "communication" is just "I'm done modifying this."

## Channel Direction

Specify channel direction in function signatures wherever possible:

```go
func produce(out chan<- int)       // can only send
func consume(in <-chan int)        // can only receive
func transform(in <-chan int, out chan<- int)
```

This prevents accidental misuse (closing a channel from the wrong side) and documents the data flow at the type level.

## Buffered Channels Have Semantics

An unbuffered channel synchronizes sender and receiver — use it when you want a handoff. A buffered channel decouples them — use it when you want a bounded queue, a semaphore, or rate limiting. Don't add a buffer just to "make it faster" without understanding the flow control implications.

A common pattern: use a buffered channel as a semaphore to limit concurrency:

```go
sem := make(chan struct{}, maxWorkers)
for _, item := range work {
    sem <- struct{}{} // acquire
    go func(item Item) {
        defer func() { <-sem }() // release
        process(item)
    }(item)
}
```

## Context.Context for Cancellation and Deadlines

Context carries cancellation signals, deadlines, and request-scoped values down a call chain. Always pass it explicitly as the first parameter — never store it in a struct.

Respect context cancellation in long-running operations:

```go
select {
case result := <-work:
    return result, nil
case <-ctx.Done():
    return zero, ctx.Err()
}
```

When starting background work from a request handler, derive a new context if the work should outlive the request. Don't reuse the request context for fire-and-forget operations — it will be cancelled when the handler returns.

## Worker Pool Pattern

For processing a stream of work items with bounded concurrency:

```go
func processAll(ctx context.Context, items []Item, workers int) error {
    g, ctx := errgroup.WithContext(ctx)
    ch := make(chan Item)

    // Start workers
    for range workers {
        g.Go(func() error {
            for item := range ch {
                if err := process(ctx, item); err != nil {
                    return err
                }
            }
            return nil
        })
    }

    // Feed work
    for _, item := range items {
        select {
        case ch <- item:
        case <-ctx.Done():
            break
        }
    }
    close(ch)

    return g.Wait()
}
```

`errgroup` from `golang.org/x/sync` combines WaitGroup semantics with error propagation and context cancellation. Prefer it over hand-rolling goroutine-plus-error coordination.

## Don't Start Goroutines in Library Constructors

A `New` function that secretly starts a goroutine surprises callers — they didn't ask for concurrency and now they have a lifecycle to manage. Instead, provide a `Run` or `Start` method that the caller invokes explicitly, and a `Stop` or `Close` method (or context cancellation) for cleanup. This keeps the caller in control.

## Race Conditions and sync.Map

If you find yourself reaching for `sync.Map`, pause. It's optimized for two narrow patterns: keys that are written once and read many times, or disjoint key sets per goroutine. For everything else, a regular `map` with a `sync.RWMutex` is simpler and often faster.

When the race detector (`go test -race`) reports a problem, fix the design — don't just add locks around the symptom. Data races often indicate a missing ownership boundary.
