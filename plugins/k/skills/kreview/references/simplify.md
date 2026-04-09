# Simplify

## The Zen

Simplification is the discipline of removing incidental complexity so the code
does the necessary work, and no more. The goal is not clever terseness. The
goal is a design with fewer moving parts, fewer concepts to hold in your head,
and fewer places for behavior to drift out of sync.

Good simplification usually comes from elimination rather than invention:
delete duplicate paths, collapse unnecessary indirection, remove state that can
be derived, and use existing abstractions instead of rebuilding them nearby.
The result should be easier to read, easier to change, and harder to misuse.

## What Good Simplification Looks Like

- **One clear path for one job.** Similar behavior is implemented once, then
  reused.
- **State exists only when it must.** Derived values are computed from source
  data rather than stored and synchronized manually.
- **Control flow is direct.** The happy path is readable without tracing
  through layers of bookkeeping.
- **Parameters are purposeful.** Functions take the inputs they truly need,
  not bags of loosely related toggles.
- **Comments carry weight.** Comments explain intent or constraints, not what
  the code already says plainly.

## What to Look For in a Review

### Duplication and near-duplication

- Two or more code paths that perform the same sequence with minor variation.
- Hand-rolled logic that redoes what an existing local helper, utility, or
  abstraction already provides.
- Parallel constants, mappings, or condition trees that must be updated
  together.

### Incidental complexity

- Extra wrapper layers that add little beyond forwarding parameters.
- State that mirrors another value and must be kept in sync manually.
- Branches that exist only to support edge cases caused by the current design.

### Parameter and API clutter

- Functions with too many boolean flags, nullable options, or loosely related
  parameters.
- Call sites that construct bulky argument objects for a narrow operation.
- APIs that force the caller to perform setup work the callee could own.

### Redundant work

- Recomputing the same value multiple times in the same flow.
- Broad scans, repeated parsing, or repeated allocation where a narrower path
  would do.
- Updating state or triggering work when nothing materially changed.

### Comment and structure noise

- Comments that narrate obvious code rather than explaining why it exists.
- Deep nesting that hides a simple underlying rule.
- Small helper functions or components whose names add no clarity and whose
  bodies are used only once.

## Anti-Patterns

| Anti-Pattern | What Happens | Why It Hurts |
|---|---|---|
| **Copy-paste variation** | Similar logic forks into multiple local versions | Fixes and behavior changes drift apart |
| **Parameter soup** | Function signature grows flags, nulls, and optional knobs | Call sites become hard to read and easy to misuse |
| **Incidental state** | Derived data is stored and synchronized manually | State goes stale; bugs hide in update order |
| **Needless indirection** | Wrapper layers forward work without adding meaning | More files and symbols to read, little value gained |
| **Ceremonial comments** | Comments restate the code | Noise crowds out the few comments that matter |
| **Redundant work** | The same computation or update happens repeatedly | Wasted time, extra complexity, and harder profiling |
| **Speculative cleanup hook** | Extra extension points or toggles exist for imagined futures | Present-day complexity grows without current benefit |

## Severity Guide

- **Critical:** Complexity or redundancy that creates correctness bugs, such as
  duplicated logic that already diverged or mirrored state that can become
  inconsistent.
- **High:** Repeated patterns or parameter clutter in a core path that make
  normal changes risky or error-prone.
- **Medium:** Noticeable indirection, redundant work, or comment noise that
  materially slows comprehension or routine maintenance.
- **Low:** Local cleanup opportunities that would improve readability but are
  unlikely to cause bugs on their own.
