---
name: kgo
description: Invoke before reviewing, writing, or modifying Go code (`.go` files). Enforce idiomatic Go development by loading guidance on design, error handling, concurrency, interfaces, testing, and documentation before making code-quality judgments. Mandatory for all Go development, including trivial changes and review work.
---

# Go Development Skill

Enforces idiomatic, guideline-driven Go development. Before writing or modifying any `.go` file, load the relevant guidelines below.

These guidelines capture the design judgment that static analysis cannot: naming taste, API shape, error strategy, concurrency architecture, and documentation quality. They deliberately exclude anything enforced by `gofmt`, `goimports`, `go vet`, `staticcheck`, or `golangci-lint` — those tools should be run separately.

Sources: [Google Go Style Guide](https://google.github.io/styleguide/go/), [Effective Go](https://go.dev/doc/effective_go), [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments).

## Which Guidelines to Load

Load **only** the files that apply to the current task. Use segmented reading (`offset`/`limit`) for large files.

**Always load:** `${CLAUDE_SKILL_DIR}/resources/01_design_guidelines.md` — applies to all Go tasks.

**Load when relevant:**

| Guideline                    | When it applies                                                          |
| ---------------------------- | ------------------------------------------------------------------------ |
| `02_error_handling.md`       | Error returns, wrapping, sentinel errors, panics, must-functions         |
| `03_concurrency.md`          | Goroutines, channels, sync primitives, context.Context, worker pools     |
| `04_interfaces_types.md`     | Interface design, type definitions, generics, embedding, zero values     |
| `05_testing.md`              | Tests, benchmarks, table-driven tests, test helpers, test doubles        |
| `06_documentation.md`        | Doc comments, package docs, examples, godoc presentation                 |

All guideline files are at `${CLAUDE_SKILL_DIR}/resources/<filename>`.

For large files, list headings first with `rg '^## ' <file>` and load only the relevant sections.

## Coding Rules

1. Load the necessary guideline files before generating or reviewing any Go code.
2. Apply the principles ranked by priority: **clarity > simplicity > concision > maintainability > consistency**.
3. Prefer the simplest tool sufficient for the job: core language constructs first, then standard library, then well-known libraries, then new dependencies.
4. Comments in American English unless the user requests otherwise.
