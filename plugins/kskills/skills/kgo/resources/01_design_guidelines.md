# Design Guidelines

These guidelines cover the naming taste, package design, and API shape decisions that require human judgment. Mechanical formatting and import ordering are handled by tooling and excluded here.

## Naming is a Design Decision

Go names carry meaning through context. The package name, receiver type, function signature, and call site all contribute — a good name accounts for all of them.

### Package Names

A package name is a single lowercase word that frames everything exported from it. Callers write `json.Marshal`, not `json.JSONMarshal` — the package name already provides context. Choose names that tell the reader what the package *provides*, not how it's implemented.

Avoid generic names like `util`, `common`, `helpers`, `misc`, `types`, `interfaces`, or `api`. These names say nothing about what's inside and become dumping grounds. If you can't find a specific name, it's a sign the package is doing too much or too little. `httputil` from the standard library is borderline acceptable because it's scoped to HTTP — but `util` alone never is.

When a package exports a single primary type, the constructor should be `New` (e.g., `ring.New`). When a package exports multiple types, constructors include the type name: `http.NewRequest`, `http.NewServeMux`.

### Exported Names

Exported names are always read with their package qualifier. `widget.New` reads well; `widget.NewWidget` stutters. Similarly, `http.Server` is clear; `http.HTTPServer` repeats itself. Let the package name carry its weight.

Methods on a type shouldn't repeat the type name either. On a `Config` receiver, `WriteTo` is better than `WriteConfigTo` — the receiver already tells you what's being written.

### Getters Have No Get Prefix

A field called `owner` has getter `Owner()` and setter `SetOwner()`. The `Get` prefix adds nothing and is not idiomatic. Reserve verb prefixes like `Fetch` or `Compute` for operations that are expensive or involve I/O, so the caller knows the cost.

### Variable Name Length Tracks Scope Distance

A variable's name should be proportional to the distance between its declaration and its last use. Loop indices and short-lived locals earn single letters (`i`, `r`, `w`, `b`). Package-level variables and struct fields used across many lines need more descriptive names.

Standard abbreviations are expected: `r` for `io.Reader`, `w` for `io.Writer`, `b` for `bytes.Buffer` or `[]byte`, `ctx` for `context.Context`, `err` for `error`. Don't fight these — they are idiomatic.

Don't encode the type in the name. `userCount` is better than `numUsers` or `usersInt` — the type system already tells you it's an integer.

### Receiver Names

Receivers are one or two letters abbreviating the type: `s` for `Server`, `cl` for `Client`. Use the same name consistently across every method on that type. Never use `self`, `this`, or `me`.

If a method doesn't use its receiver, omit the name entirely rather than assigning it to `_`.

### Initialisms in Compound Names

Linters catch basic initialism casing (`Url` → `URL`). The judgment call is in compound names: each initialism keeps its own casing independently. `ServeHTTP`, `xmlHTTPRequest`, `newURLParser` — not `ServeHttp` or `NewUrlParser`.

### Avoid Weasel-Word Types

Type names like `Manager`, `Service`, `Controller`, `Handler`, `Processor`, and `Helper` are often symptoms of unclear responsibility. If the type manages bookings, call it `Bookings` or `BookingDispatcher` — whatever describes what it actually does.

The exception is when the word has specific meaning in your domain (e.g., `http.Handler` implements the `Handler` interface). Context matters.

## Package Design

### One Package, One Idea

A package should have a clear, focused responsibility. The standard library is a good model: `bytes` does byte manipulation, `net/http` does HTTP, `encoding/json` does JSON. If you can't describe what a package does in one sentence without "and", consider splitting it.

Group types that are tightly coupled in implementation. Separate types that evolve independently. Think about what a user sees on the godoc page — everything on that page should feel like it belongs together.

### Don't Export Prematurely

Start unexported. Export when there's a real consumer. An unexported function can be freely changed; an exported one is a commitment. This is especially true for types — once a struct is exported, every field addition is visible to every consumer.

### Avoid Package-Level State

Package-level variables are effectively globals. They make testing hard, create hidden coupling between packages, and prevent concurrent use. Prefer passing dependencies explicitly. When package-level state is unavoidable (e.g., a default logger), provide an API that lets callers substitute their own.

## Function and API Design

### Accept Interfaces, Return Structs

Functions should accept interface parameters (asking only for what they need) and return concrete types (giving callers everything they have). This lets consumers define narrow interfaces matching their usage, while producers can add methods freely without breaking anyone.

Return an interface type only when you need to hide implementation details (e.g., the `error` interface) or when the concrete type is truly an internal concern.

### Option Structs for Many Parameters

When a function needs four or more optional parameters, collect them in an option struct passed as the final argument. This is self-documenting, extensible (new fields get zero-value defaults), and reads well at the call site:

```go
client := NewClient(addr, ClientOptions{
    Timeout:    30 * time.Second,
    MaxRetries: 3,
})
```

For APIs where most callers pass no options, consider the variadic option pattern: `func New(addr string, opts ...Option)`. But don't reach for this by default — option structs are simpler and more discoverable via godoc.

### Context is Always the First Parameter

`context.Context` is always the first parameter: `func Do(ctx context.Context, ...)`. Never store a Context in a struct. Never create custom Context types. The only exceptions are when matching an existing interface signature (like `http.Handler`) or at entrypoints where you create `context.Background()`.

### Don't Return Sentinel Values for Errors

Never return `-1`, `""`, or `nil` as a signal that something went wrong. Use Go's multiple return values: `(value, error)` or `(value, bool)`. This prevents callers from accidentally using invalid results — `Parse(Lookup(key))` won't compile if `Lookup` returns `(string, error)`.

### Design for the Zero Value

When possible, design types so that the zero value is immediately useful without a constructor. `sync.Mutex{}` is an unlocked mutex, `bytes.Buffer{}` is an empty buffer ready for writes. This reduces API surface and makes composition easier — a struct embedding your type just works without initialization.

When a zero value can't be useful (the type needs configuration or external resources), make this clear with a constructor and document what happens if someone uses the zero value.

### Prefer Synchronous APIs

Synchronous functions are easier to reason about, test, and compose. The caller can always wrap a synchronous call in `go f()` to add concurrency, but removing concurrency from an async API is hard or impossible. Only provide async APIs when the operation is inherently concurrent (e.g., a server's accept loop).

### Defer for Cleanup

`defer` ties cleanup to the function that acquired the resource. Put the `defer` immediately after acquisition — this keeps open/close together and guarantees cleanup on all exit paths:

```go
f, err := os.Open(path)
if err != nil {
    return err
}
defer f.Close()
```

Remember that deferred calls see the final values of named return parameters. This is useful for modifying error returns in a deferred function, but surprising if you don't expect it.

### Use init Sparingly

`init` functions run at import time with no way for the caller to control ordering, pass arguments, or handle errors. They're appropriate for registering drivers or codecs (`database/sql` drivers, `image` formats) and for compile-time validation. They're inappropriate for anything that does I/O, requires configuration, or could meaningfully fail — use explicit initialization for those.

Blank imports (`import _ "pkg"`) trigger a package's `init` for side effects. Restrict them to `package main` and test files — library packages that require blank imports force hidden coupling on their consumers.
