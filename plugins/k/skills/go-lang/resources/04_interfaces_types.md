# Interfaces and Types

## Interfaces

### Don't Define Interfaces Until You Need Them

Go interfaces are satisfied implicitly — a type implements an interface by having the right methods, with no declaration of intent. This means interfaces can be defined *after* concrete types exist, by the code that *consumes* them. Take advantage of this: start with concrete types and introduce interfaces only when you have a real second consumer or a genuine need for abstraction.

Preemptive interfaces ("I might need to mock this later") add indirection without benefit. If you only have one implementation, you don't have an interface — you have a concrete type with extra ceremony.

### Consumer Defines the Interface

The package that *uses* a dependency defines the interface it needs, with only the methods it actually calls. The package that *implements* the dependency returns a concrete type. This is the heart of Go's interface philosophy:

```go
// In the consumer package — defines only what it needs
type UserStore interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

// In the implementation package — returns a concrete type
type PostgresStore struct { db *sql.DB }
func NewPostgresStore(db *sql.DB) *PostgresStore { ... }
func (s *PostgresStore) GetUser(ctx context.Context, id string) (*User, error) { ... }
func (s *PostgresStore) ListUsers(ctx context.Context) ([]*User, error) { ... }
```

The implementation has more methods than the consumer's interface requires. That's correct — the interface is the consumer's view, not the producer's contract.

### Keep Interfaces Small

Small interfaces are easier to implement, compose, and satisfy accidentally (which is a feature, not a bug). The standard library's best interfaces have one or two methods: `io.Reader`, `io.Writer`, `fmt.Stringer`, `sort.Interface` (three methods, but tightly coupled).

If your interface has five or more methods, it's probably describing a concrete type rather than a behavior. Consider whether you can split it into smaller interfaces that compose, or whether you should just use the concrete type directly.

### One-Method Interface Naming

Interfaces with a single method are conventionally named as the method plus `-er`: `Reader`, `Writer`, `Closer`, `Formatter`, `Stringer`. Respect canonical names and signatures — if your method is called `Read` and takes `[]byte`, it should match `io.Reader`'s signature and semantics.

### Compile-Time Interface Checks

When there's no static conversion in your code that would catch a missing method, use a compile-time assertion:

```go
var _ json.Marshaler = (*MyType)(nil)
```

This costs nothing at runtime and catches interface drift early. Use it sparingly — only when the compiler wouldn't catch the problem through normal usage.

## Type Design

### Pointer vs. Value Receivers

Choose one receiver type for all methods on a given type and be consistent.

**Use pointer receivers when:**
- The method mutates the receiver
- The receiver contains a `sync.Mutex` or similar non-copyable field
- The receiver is a large struct or might grow to be one
- Any field is a pointer to mutable state (makes mutation intent clearer)

**Use value receivers when:**
- The receiver is a small, immutable value type (like `time.Time`)
- The receiver is a map, func, or channel (already reference types — don't take a pointer to these)
- The receiver is a slice and the method doesn't reslice or reallocate it

When in doubt, use pointer receivers. Mixing receiver types on one type is a code smell — it confuses readers about whether the type is meant to be copied.

### Embedding for Composition, Not Inheritance

Struct embedding promotes the embedded type's methods. This is composition — the embedded type's methods operate on the inner value, not the outer struct. Don't embed a type just to avoid writing forwarding methods unless you want *all* of its methods promoted.

Be careful with embeddings that expose methods you didn't intend to be part of your API. Embedding `sync.Mutex` exports `Lock()` and `Unlock()` — if that's not what you want, use a named field instead:

```go
// Exposes Lock/Unlock as part of the API
type Cache struct {
    sync.Mutex
    items map[string]Item
}

// Keeps synchronization internal
type Cache struct {
    mu    sync.Mutex
    items map[string]Item
}
```

### Nil Slices Are Fine

Prefer `var s []string` (nil) over `s := []string{}` (empty, non-nil). A nil slice behaves identically to an empty slice for `len`, `cap`, `append`, and `range`. The only difference is JSON encoding: nil marshals to `null`, empty to `[]`. Choose based on your API contract, and never force callers to distinguish between nil and empty.

### Use Strong Types

Use `time.Duration` instead of `int` for durations, `net.IP` instead of `string` for IP addresses, `url.URL` instead of `string` for URLs. Strong types prevent misuse at compile time and make function signatures self-documenting.

Similarly, consider defining named types for domain concepts that are currently stringly-typed:

```go
type UserID string
type OrderID string
```

This prevents accidentally passing a UserID where an OrderID is expected, even though both are strings underneath.

### Copying Safety

Some types must not be copied after first use. The most common: any struct containing a `sync.Mutex` (or `sync.WaitGroup`, `sync.Cond`, etc.). Copying a locked mutex creates a second locked mutex that no one can unlock. The `go vet` `copylocks` checker catches the obvious cases, but it can't follow values through interfaces or reflect.

Also watch for types that alias internal buffers. Copying a `bytes.Buffer` copies the slice header but shares the underlying array — writes to one corrupt the other. When in doubt about whether a type from another package is safe to copy, check whether its methods use pointer receivers (a strong hint it's not).

### Generics: Start Concrete

Start with concrete types. If you find yourself writing the same function for `[]int` and `[]string`, that's when generics earn their place. Don't reach for generics to build frameworks, DSLs, or abstract error-handling machinery. The best uses of generics in Go are utility functions (slices, maps, channels) and container types — the same patterns the standard library uses in `slices`, `maps`, and `cmp`.

If a generic function's type constraint is `any`, ask whether it actually needs to be generic or if an `interface{}` parameter (or just a concrete type) would be clearer.
