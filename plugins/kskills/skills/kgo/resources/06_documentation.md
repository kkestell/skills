# Documentation

Go documentation lives in the source code and is rendered by godoc. Good doc comments make a package usable without reading the implementation.

## Doc Comment Format

Every exported name — function, type, method, constant, variable — gets a doc comment. The comment is a complete sentence that begins with the name of the thing it describes:

```go
// A Client manages communication with the API.
type Client struct { ... }

// NewClient returns a Client configured with the given options.
// It returns an error if the address is invalid.
func NewClient(addr string, opts ...Option) (*Client, error) { ... }

// Close releases resources associated with the Client.
// It is safe to call Close multiple times.
func (c *Client) Close() error { ... }
```

Starting with the name makes godoc's search and index useful — users scanning a list of declarations immediately see what each thing is.

## Package Comments

Every package needs a package comment. It appears immediately above the `package` clause with no blank line between:

```go
// Package auth provides JWT-based authentication for HTTP services.
package auth
```

For multi-file packages, the package comment needs to appear in only one file. Conventionally, this is `doc.go` for larger packages.

For `package main`, describe the binary:

```go
// Command migrate applies database schema migrations.
package main
```

## What to Document

Focus doc comments on what's not obvious from the signature. Don't restate the types — the reader can see them. Instead, document:

- **Behavior contracts**: What the function promises ("returns results sorted by name")
- **Error conditions**: When and why the function returns errors
- **Lifecycle requirements**: "Call Close when done" or "Safe for concurrent use"
- **Nil/zero behavior**: What happens with nil arguments or zero-value receivers
- **Panics**: When and why the function panics (if it does)

Don't over-document obvious parameters. `Len() int` doesn't need `// Len returns the length` — the name says it. But `Len() int` on a type where "length" could mean different things (bytes? runes? elements?) does benefit from clarification.

## Concurrency Documentation

A read-only operation is assumed safe for concurrent use — no need to document it. Document concurrency when:

- It's unclear whether an operation mutates internal state (e.g., a cache lookup that may insert)
- The type provides synchronization guarantees ("Safe for concurrent use by multiple goroutines")
- A consumer type has concurrency requirements ("Must not be used from multiple goroutines")

## Godoc Formatting

Blank lines separate paragraphs. Indent lines by a tab or two spaces to format them as code blocks. Headings in doc comments start with `#` followed by a space (Go 1.19+):

```go
// # Connection Pooling
//
// The client maintains an internal pool of connections.
// Pool size defaults to 10 and can be configured via Options.
```

URLs are automatically linked. References to other symbols use brackets: `[Client]`, `[Client.Close]`, `[io.Reader]`.

## Examples

Runnable example functions in `_test.go` files are the best documentation — they show real usage and the test runner verifies they still work:

```go
func ExampleNewClient() {
    client, err := auth.NewClient("https://api.example.com")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    // ...
}
```

Example functions appear in godoc next to the symbol they demonstrate. Name them `Example` (package-level), `ExampleFoo` (function), `ExampleFoo_Bar` (method), or `ExampleFoo_suffix` (multiple examples for the same symbol).

## Comment Quality Over Quantity

A comment that restates the code adds noise. A comment that explains *why* the code exists adds signal. Before writing a comment, ask: "Would renaming the function or restructuring the code make this comment unnecessary?" If yes, do that instead.

Comments that explain "why" age well. Comments that explain "what" go stale because they drift from the code they describe. Comments that explain "how" are almost always better expressed as clearer code.
