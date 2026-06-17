---
name: ksimplify
description: Global, multi-agent simplification review of a whole codebase — map phase, parallel lens passes into a shared ledger, then reconciliation into ranked findings with a human approval gate before any edit. Use when the user wants a deep code-quality review (simpler, more idiomatic, better ownership, less copying) where decisions must be global rather than per-file, behavior must not change, and findings should be presented for approval rather than auto-applied. Not for bug-hunting (use /code-review) or quick single-file cleanup (use /simplify).
---

# Deep simplify — map → lenses → reconcile

A three-phase orchestrated review producing `.k/reviews/<slug>.md` (a dated, numbered findings document — see Phase 0) for human approval. **No edits before the user approves a subset of findings.**

## Core principles (do not skip these)

1. **The global model lives in a written artifact, not the context window.** Reading the whole codebase at once produces shallow-everywhere output (context capacity ≠ attention quality); isolated subagents produce local conclusions. Resolution: deep reading happens in focused bounded passes that write into a shared artifact; the global decision is made by reconciling the distilled artifact, never raw source.
2. **A locally-attractive refactor can be globally wrong.** What makes a change global: serialization boundaries (on-disk formats, wire formats), cache/fingerprint stability, shared ownership, public API. The map must label these explicitly; every finding must tag what it touches.
3. **Tests are distilled, never read by lens agents.** Lens agents get production code plus a one-line-per-test _behavior contract_ (the invariants a `behavior_change: none` refactor must preserve). Handing an agent raw test bodies splits its attention or tempts it to "simplify" the tests, weakening the contract.
4. **Behavior unchanged is the bar.** Every finding carries `behavior_change: none`. A proposal must be clearer OR measurably leaner, not merely different. Respect existing rationale comments — they are load-bearing; never propose deleting them.
5. **Approval gate.** The skill's output is the `<run>.md` findings document presented to the user. Stop there.

## Phase 0 — Scout and set up

1. Identify the codebase's primary language and load its **review criteria** from `assets/`: `typescript.md`, `rust.md`, or `generic.md` as the fallback when no language-specific file matches. The file supplies the source extensions, test-detection patterns, serialization mechanisms, and the per-language review dimensions (the lenses for Phase 2). (A polyglot repo — e.g. a Rust backend + TS frontend — may draw on more than one file; scope each lens pass to the slice its criteria cover.) Read the chosen file now.
2. Scope: `find <src dirs> -name '*.<ext>' | xargs wc -l | sort -n` using the criteria file's extensions. Identify production vs test code, the largest files, and the likely type spine / hot paths.
3. Pick a run slug `<slug>` = `<date>-<NNN>`, where `<date>` is today and `<NNN>` is the next zero-padded sequence number for the day: `slug=$(date +%Y-%m-%d)-$(printf '%03d' $(( $(ls .k/reviews/$(date +%Y-%m-%d)-*.md 2>/dev/null | wc -l) + 1 )))`. Working artifacts (maps, ledgers) go in the **run dir** `.k/reviews/<slug>/`; the final findings document is `.k/reviews/<slug>.md` (referred to below as `<run>/…` and `<run>.md`). `mkdir -p .k/reviews/<slug>`. Exclude `.k/` via `.git/info/exclude` (not the tracked `.gitignore`): `grep -qxF '.k/' .git/info/exclude || echo '.k/' >> .git/info/exclude` — kinit already adds this in repos it set up.
4. If the codebase is large (>~15k production LOC), narrow the review to a subsystem with the user before proceeding — the map must be genuinely complete for reconciliation to work.

## Phase 1 — Map (two cartographer agents, in parallel)

Launch two `general-purpose` agents in one message. Both produce **distilled maps, not file dumps** — descriptive only, no findings, file:line refs everywhere.

**Cartographer A → `<run>/map-structure.md`** (reads the type/data spine; skips all test modules). Sections:

- _Core type graph_: every key type tagged **SERIALIZED** (on-disk format — changing it breaks saved data), **WIRE** (external API shape only), or **INTERNAL**; the (de)serialization attributes/annotations that pin formats; key conversion functions between families.
- _Ownership & sharing graph_: every shared or reference-counted value, shared mutable state, and significant deep copy — what is shared, why (quote rationale comments), what crosses concurrency/thread boundaries.
- _Allocation hotspots_: deep-copy / string-allocation / intermediate-collection clusters, classified by execution frequency (e.g. per-call / per-request / boot-time — frequency determines leverage).
- _Cross-cutting patterns_: error-handling style and boundaries, string-building idioms, constructor conventions, single-variant enums/tagged unions kept for forward-compat, and **every load-bearing rationale comment** (these are constraints, not noise).

**Cartographer B → `<run>/map-modules.md`** (reads orchestration code + distills tests):

- _Module responsibilities_: 1–2 lines each.
- _Control flow_ of the main loop: who calls whom, where state lives, where persistence happens.
- _God-function candidates_: name, file:line, line count (threshold ~80 lines).
- _Suspected duplications_ across modules.
- _Behavior contract_: **one line per test** — `file::test_name — invariant it pins` — exhaustive, grouped by file, with a total count. This is the only form test content enters the review.

**Then validate before Phase 2** (non-negotiable): read both maps in full in the main loop, spot-check the load-bearing claims (serialization boundaries, the central conversion path, lock/ownership rationales) against actual source. Fix anything wrong. Assemble: `{ echo '# review map (Phase 1 — validated <date>)'; echo; cat <run>/map-structure.md; echo; cat <run>/map-modules.md; } > <run>/map.md`

## Phase 2 — Lens passes (Workflow, 6 parallel agents)

Run as a `Workflow` (the user invoking this skill is the multi-agent opt-in). Each lens agent reads `<run>/map.md` in full, then deeply reads a bounded slice of **production code only**, writes findings to `<run>/ledger-<lens>.jsonl` (one JSON object per line — per-lens files avoid interleaved writes), and returns them via structured output.

Finding schema (every field required): `lens, location (file:line), observation, proposed_change, modules_touched (list),
scope (local|cross-cutting), risk (low|medium|high), behavior_change (enum: ["none"]),
confidence (low|medium|high), global_concern (the serialization/cache/sharing constraint
that could block this, or "")`

**Lenses come from the review criteria loaded in Phase 0** (`assets/<lang>.md`). Each review dimension there is one lens, with the language-specific shape of what it should find. Adapt each lens's slice from the map, and drop any dimension the criteria mark as inapplicable (e.g. the concurrency/async lens for a single-threaded or synchronous codebase). Do not invent lenses beyond those criteria; if the codebase has a concern they don't cover, note it for reconciliation rather than spawning an unguided pass.

Common prompt preamble for every lens (include verbatim, adapted):

> Read `<run>/map.md` IN FULL first — it contains the serialization boundaries, cache constraints, ownership rationale, and the behavior contract your proposals must preserve. Production code only; SKIP every test module. The codebase may be carefully written — findings will be subtle; do NOT manufacture findings to fill a quota. Five sharp findings beat fifteen padded ones; zero is acceptable. Cite exact file:line. Tag modules_touched honestly. If a change collides with a global constraint, you may still report it but state the collision in global_concern. Never propose removing rationale comments or weakening documented invariants.

Workflow skeleton (fill LENSES with the prompts + slices; FINDINGS_SCHEMA per above):

```js
export const meta = {
  name: 'lens-passes',
  description: 'Phase 2: parallel lens reviews into a shared ledger',
  phases: [{ title: 'Lens passes' }],
}
phase('Lens passes')
const results = await parallel(LENSES.map(l => () =>
  agent(COMMON.replace(/LENSKEY/g, l.key) + l.prompt,
        { label: `lens:${l.key}`, phase: 'Lens passes', schema: FINDINGS_SCHEMA })))
return { counts: LENSES.map((l, i) => `${l.key}: ${results[i]?.findings.length ?? 'FAILED'}`) }
```

After completion: `cat <run>/ledger-*.jsonl > <run>/ledger.jsonl` (disk files are the source of truth — the workflow return value may be truncated).

## Phase 3 — Reconcile (main loop, on the distilled artifacts ONLY)

Read only `<run>/map.md` + `<run>/ledger.jsonl` — never raw source (spot-verify individual suspicious claims with targeted greps if needed). Produce the findings document at `<run>.md`:

1. **Dedup**: merge findings where lenses converged (note the convergence — it's a confidence signal).
2. **Cluster** related findings into one decision each (if two lenses touch the same function, that's one refactor, not three).
3. **Kill** locally-attractive/globally-wrong items, **with the reason recorded** in a "Killed" section (e.g. "blocked: persisted format / forward-compat"). Also record plausible refactors nobody proposed, so they aren't re-litigated later.
4. **Rank** by leverage vs risk; group into apply-batches (each batch = one fmt → lint → test → commit cycle). Pull low-value or convention-changing items into an "Optional" section with trade-offs stated.

## Approval gate and apply

Present `<run>.md`: lead with a batch summary table, flag anything that changes a documented convention (all-or-nothing items), and ask which batches to apply. **Stop.**

On approval: apply batch-by-batch per the project's conventions — format → lint (zero warnings) → test (green) → single-line commit, no attribution. Discover the exact commands from AGENTS.md or the project's toolchain. After all batches, run /code-review + /simplify over the full diff and smoke-test against a real runtime if the project has one.
