# Error Handling

Go's error handling philosophy is explicit: errors are values, returned and checked at every call site. This section covers the design decisions around how to create, propagate, and respond to errors.

## When to Ignore an Error

Linters flag unchecked errors, but deciding *whether* to suppress the lint is a judgment call. The bar is: the operation's failure must be harmless, and the reason must be obvious or documented. Closing a read-only file handle is a common example. In all other cases, handle it, return it, or (truly exceptional cases) panic.

## Error Flow: Happy Path on the Left

Handle errors immediately and return early. The normal code path should flow down the left margin at minimal indentation:

```go
// Good: error handled, then move on
val, err := doThing()
if err != nil {
    return fmt.Errorf("doing thing: %w", err)
}
// continue with val

// Bad: normal logic buried in an else
val, err := doThing()
if err != nil {
    return err
} else {
    // normal path awkwardly indented
}
```

If an `if` block has an init statement that creates a variable needed in both branches, move the declaration to its own line to eliminate the `else`.

## Error String Composition

Static analysis catches capitalized error strings and trailing punctuation. The deeper design question is *what context to add* when wrapping. Each layer should add the operation that failed, building a readable chain:

```
"starting server: reading config: open /etc/app.conf: permission denied"
```

Each piece names the action at that level. Don't repeat information the inner error already provides — `"failed to read config: read error: ..."` says "failed" and "error" redundantly.

## Wrapping: %w vs %v

Use `%w` when callers should be able to inspect the underlying error with `errors.Is` or `errors.As`. Place `%w` at the end of the format string.

Use `%v` (or create a fresh error) at system boundaries — RPC handlers, storage layers, IPC — where you want to decouple the caller from internal error types. Wrapping with `%w` across these boundaries leaks implementation details.

```go
// Internal: preserve the chain for callers
return fmt.Errorf("loading user %d: %w", id, err)

// System boundary: break the chain
return fmt.Errorf("storage error: %v", err)
```

## Structured Error Types

For errors that callers need to handle programmatically, define error types or sentinel errors:

```go
// Sentinel errors for simple conditions
var ErrNotFound = errors.New("not found")
var ErrConflict = errors.New("conflict")

// Structured errors for richer context
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation: %s: %s", e.Field, e.Message)
}
```

Callers use `errors.Is` and `errors.As` — never string matching on error messages. Exported functions should return the `error` interface, not concrete error types, so you can change the underlying type later without breaking callers.

## Don't Log and Return

If you return an error, don't also log it. The caller decides how to handle it — logging at both levels produces duplicate noise that makes debugging harder. Log at the point where the error is finally handled (usually near the top of the call stack).

## Panics Are for Bugs, Not Errors

`panic` means "this program has a bug and cannot continue." It is not a substitute for error returns. Use `panic` for:

- Violated invariants that indicate a programming error (e.g., an "impossible" `default` case in a type switch on an internal enum)
- `init` functions where setup failure makes the program non-functional
- Internal implementation details paired with a `recover` that never lets the panic escape the package boundary

Never panic on bad user input, failed I/O, or any condition that could arise in normal operation. In `package main`, prefer `log.Fatal` for configuration errors where a stack trace won't help.

## Must-Functions

Functions prefixed `Must` (e.g., `template.Must`, `regexp.MustCompile`) panic on error. They exist for program initialization where failure is truly fatal:

```go
var tmpl = template.Must(template.ParseFiles("index.html"))
```

Call `Must` functions only at package-level `var` declarations or during `init`. Never call them on user input or runtime data — that turns recoverable errors into crashes.
