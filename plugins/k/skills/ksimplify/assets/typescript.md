# Review criteria — TypeScript / JavaScript

## Scope hints

- **Source extensions**: `*.ts`, `*.tsx`, `*.js`, `*.jsx`, `*.mts`, `*.cts`.
- **Test detection**: `*.test.*`, `*.spec.*`, files under `__tests__/` / `test/` / `tests/`, and setup files for Jest/Vitest/Mocha/Playwright. Distill these into the behavior contract; never feed their bodies to lens agents.
- **Serialization mechanisms** (tag types as SERIALIZED / WIRE in the map): `JSON.stringify`/`parse` round-trips persisted to disk/DB/localStorage, schema validators that pin shapes (`zod`, `io-ts`, `yup`, JSON Schema), ORM models/migrations, and HTTP/RPC request/response DTOs. Field renames or optionality changes on SERIALIZED types break stored or in-flight data.

## Review dimensions

1. **mutation-sharing** — shared mutable objects/arrays handed to callers that mutate them, defensive copies (`{...x}` / `structuredClone` / `.slice()`) that are unnecessary, and the inverse: missing copies where a mutation leaks across a boundary. Unnecessary deep clones on hot paths. (TS/JS is GC'd — this is about aliasing and mutation, not freeing memory.)
2. **typemodel** — discriminated-union opportunities (a `kind`/`type` tag instead of optional-field soup), `any` and over-broad `unknown`, parallel/duplicated `interface`/`type` declarations, `as` assertions that paper over a modeling gap, optional fields (`?`) that should be a union, make-illegal-states-unrepresentable. State validator/serialization impact per finding.
3. **errors** — `try`/`catch` boundary coherence, `throw` vs returned-result conventions used consistently, non-null assertions (`!`) and unsafe casts on values not provably present, optional chaining (`?.`) that silently swallows a real bug, error-message consistency at recovery boundaries. (Simplification only — not bug-hunting.)
4. **idiom** — array methods (`map`/`filter`/`reduce`/`some`/`every`) ↔ explicit loops (both directions; a `reduce` is not always clearer), avoidable intermediate arrays, destructuring and spread where they read better, `async`/`await` vs `.then` chains, template literals vs string concatenation. Respect explicit loops that carry an explanatory comment.
5. **async** — independent `await`s that should be `Promise.all` / `Promise.allSettled`, `await`-in-a-loop where the iterations are independent, redundant `await` on non-promises, floating promises only where collapsing them simplifies (not as a bug hunt), lifecycle/cleanup simplifications. Conservative — record ordering invariants in `global_concern`. **Drop this lens for purely synchronous codebases.**
6. **boundaries** — god-functions and god-components (cohesive sequence vs extractable unit/hook — extraction must pay for itself), and the map's duplication list (unify only if it reduces *total* complexity; cross-package duplication usually stays).
