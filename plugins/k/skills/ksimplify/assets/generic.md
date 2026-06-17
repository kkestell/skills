# Review criteria — generic (language-agnostic fallback)

Use this when no language-specific file matches the codebase's primary language. Replace the placeholder terms with the closest equivalent in the actual language.

## Scope hints

- **Source extensions**: derive from the dominant language(s) in the repo.
- **Test detection**: files under `test/`, `tests/`, `spec/`, or named `*_test.*` / `*.test.*` / `*.spec.*` — distill these into the behavior contract; never feed their bodies to lens agents.
- **Serialization mechanisms** (tag types as SERIALIZED / WIRE in the map): on-disk file formats, database schemas/migrations, any explicit (de)serialization annotations or hand-written encode/decode functions, and external API request/response shapes.

## Review dimensions

1. **sharing** — data copied when it could be shared or passed by reference; redundant defensive/deep copies, especially on hot paths. Weigh by execution frequency (per-call vs boot-time).
2. **typemodel** — parallel/duplicated type families, types that don't earn their keep, make-illegal-states-unrepresentable opportunities, single-variant sum types kept for forward-compat (check persistence first). State serialization impact per finding.
3. **errors** — error-handling boundary coherence, audit of unchecked access that can fail at runtime (don't flag the idiomatic, provably-safe cases), redundant error-context wrapping, error-message consistency at recovery boundaries.
4. **idiom** — explicit loops ↔ higher-order constructs (both directions), avoidable intermediate collections, string building (concatenation in a loop vs a builder/buffer). Respect explicit loops that carry an explanatory comment.
5. **concurrency** — locks/guards held across suspension or blocking points, independent operations that could run concurrently (check ordering invariants first), channel/queue topology, lifecycle simplifications. Conservative — only high-confidence findings, ordering reasoning recorded in `global_concern`. **Drop this lens entirely for single-threaded codebases.**
6. **boundaries** — god-functions (cohesive sequence vs extractable unit — extraction must pay for itself), and the map's duplication list (unify only if it reduces *total* complexity; cross-module duplication usually stays).
