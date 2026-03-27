# Testing

## Table-Driven Tests

Table-driven tests are Go's dominant pattern for testing multiple cases. They reduce boilerplate, make it easy to add cases, and produce clear failure output:

```go
func TestParseSize(t *testing.T) {
    tests := []struct {
        name  string
        input string
        want  int64
        err   bool
    }{
        {name: "bytes", input: "100B", want: 100},
        {name: "kilobytes", input: "2KB", want: 2048},
        {name: "empty", input: "", err: true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseSize(tt.input)
            if tt.err {
                if err == nil {
                    t.Fatal("expected error, got nil")
                }
                return
            }
            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }
            if got != tt.want {
                t.Errorf("ParseSize(%q) = %d, want %d", tt.input, got, tt.want)
            }
        })
    }
}
```

Give each case a `name` field and use `t.Run` — this makes test output identify which case failed and lets you run individual cases with `go test -run`.

## Failure Messages Should Identify the Problem

A failure message should tell you: what function was called, with what input, what it returned, and what you expected. The standard pattern:

```
Func(input) = got, want expected
```

For complex structures, use `cmp.Diff`:

```go
if diff := cmp.Diff(want, got); diff != "" {
    t.Errorf("Transform() mismatch (-want +got):\n%s", diff)
}
```

For protocol buffers, add `protocmp.Transform()`:

```go
if diff := cmp.Diff(want, got, protocmp.Transform()); diff != "" {
    t.Errorf("mismatch (-want +got):\n%s", diff)
}
```

## t.Error vs. t.Fatal

`t.Error` records a failure and continues — use it when later checks might reveal additional useful information. `t.Fatal` stops the test immediately — use it when a failure makes subsequent checks meaningless (e.g., a nil pointer that would panic).

In subtests (`t.Run`), `t.Fatal` only stops that subtest, not the parent. This makes it safe to use `t.Fatal` in table-driven subtests.

Never call `t.Fatal` (or `t.FailNow`) from a goroutine other than the test function itself. The `testing` package doesn't support this and it can cause unpredictable behavior.

## Test Helpers

Functions that set up fixtures or perform common assertions should call `t.Helper()` as their first line. This makes failure messages report the caller's line number instead of the helper's:

```go
func assertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}
```

Use `t.Cleanup` for teardown — it runs when the test (or subtest) completes, in LIFO order, and works correctly with parallel tests:

```go
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db, err := sql.Open("postgres", testDSN)
    if err != nil {
        t.Fatalf("opening test db: %v", err)
    }
    t.Cleanup(func() { db.Close() })
    return db
}
```

## Don't Use Assertion Libraries

Go's standard `testing` package plus `cmp.Diff` from `github.com/google/go-cmp` cover nearly all needs. Assertion libraries like testify fragment the developer experience — every library has slightly different naming, failure output, and behavior. They also make test failures harder to read because the assertion framework sits between you and the actual comparison.

If you find yourself writing the same comparison logic repeatedly, extract a helper function that returns `error` (for flexible use) or calls `t.Helper()` and `t.Errorf` (for direct test use). Keep the comparison logic visible.

## Test Doubles

When a test needs to replace a dependency, the consumer defines a minimal interface (see the interfaces guide) and the test provides a fake implementation. Name fakes after their behavior, not their mechanism: `AlwaysSucceeds`, `FailsOnSecondCall`, `RecordsAllCalls`.

Place reusable test helpers and fakes in a `packagetest` or `testutil` sub-package (e.g., `authtest`). This keeps test infrastructure out of production imports.

Prefer real implementations when feasible — a test against a real HTTP server (using `httptest.NewServer`) is more trustworthy than one against a hand-crafted mock. Use the real thing for integration tests and narrow fakes for unit tests.

## TestMain for Global Setup

Use `TestMain` when the entire test suite needs shared setup (starting a database, loading fixtures):

```go
func TestMain(m *testing.M) {
    // setup
    code := m.Run()
    // teardown
    os.Exit(code)
}
```

This runs once per package test binary, before any tests. Keep it minimal — prefer per-test setup with `t.Cleanup` when possible.

## Parallel Tests

Call `t.Parallel()` at the start of tests (and subtests) that are safe to run concurrently. This speeds up test suites, especially for I/O-bound tests. But parallel tests must not share mutable state — if they write to a shared map or file, they'll race.

```go
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        t.Parallel()
        got := Transform(tt.input)
        if got != tt.want {
            t.Errorf("Transform(%q) = %q, want %q", tt.input, got, tt.want)
        }
    })
}
```

Since Go 1.22, loop variables are per-iteration, so no manual capture is needed.
