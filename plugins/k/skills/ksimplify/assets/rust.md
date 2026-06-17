# Review criteria — Rust

## Scope hints

- **Source extensions**: `*.rs`.
- **Test detection**: `#[cfg(test)]` modules, `#[test]` functions, files under `tests/`, and doctests. Distill these into the behavior contract; never feed their bodies to lens agents.
- **Serialization mechanisms** (tag types as SERIALIZED / WIRE in the map): `serde` derives and attributes (`#[serde(...)]`, `rename`, `tag`, `untagged`, `default`), `bincode`/`postcard`/`prost` encodings, on-disk and DB formats. Changing a SERIALIZED type's shape or field names breaks saved data — the map must call these out.

## Review dimensions

1. **ownership** — `.clone()` / `.to_owned()` / `.to_vec()` where a borrow would do, `Arc`/`Rc`/`Box` that don't earn their keep, deep or defensive copies on the hot conversion path, functions taking `T`/`String`/`Vec<T>` by value when `&T`/`&str`/`&[T]` suffices, `.collect()` then re-iterate. Weigh by execution frequency (hot path vs boot-time).
2. **typemodel** — parallel type-family duplication, single-variant `enum`s (check `serde`/persistence first!), newtype wrappers that don't earn their keep, nested `Option<Option<_>>` / `Result<_, Infallible>`, make-illegal-states-unrepresentable via the type system. State `serde`/serialization impact explicitly per finding.
3. **errors** — error-enum / `Result` boundary coherence (`thiserror` at library edges, `anyhow`/`eyre` internally), audit of `.unwrap()` / `.expect()` / `panic!` / `[]` indexing / `unreachable!` on values that are provably present — do NOT flag the idiomatic cases (e.g. a just-inserted key). Redundant `.context()` / `.map_err` wrapping, error-message consistency at recovery boundaries.
4. **idiom** — explicit loops ↔ iterator combinators (both directions; not everything should be a chain), avoidable intermediate `collect()`s, `String` building (`push_str` / `write!` vs `format!`-in-a-loop), `&str` vs `String` params, `if let` / `let else` / `matches!` opportunities. Respect explicit loops that carry an explanatory comment.
5. **concurrency** — `Mutex`/`RwLock` guards held across an `.await`, independent async ops that could `join!`/`try_join!` or `tokio::spawn`, channel topology, `Send`/`Sync` bounds that could relax, lifecycle simplifications. Conservative — only high-confidence findings with the ordering reasoning recorded in `global_concern`. **Drop this lens for single-threaded codebases.**
6. **boundaries** — god-functions (cohesive sequence vs extractable unit — extraction must pay for itself), and the map's duplication list (unify only if it reduces *total* complexity; cross-crate duplication usually stays).
