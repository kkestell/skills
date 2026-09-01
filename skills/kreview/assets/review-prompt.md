# Review — Prompt Template

This is a prompt framework for a combined completeness and code-simplification review. When launching a reviewer subagent, read this file, then compose the actual prompt by filling in the concrete details for the current chunk of work.

---

## Preamble (copy and adapt)

You are reviewing a chunk of implementation work. Your job is to run two back-to-back reviews — completeness first, then code simplification — and report findings for each. Be honest. A false "pass" is worse than a nit.

## Context (fill in)

- **Plan path**: (repo-relative path to the plan file)
- **Project guidance docs**: (paths to repo-specific guidance such as `CLAUDE.md`, `AGENTS.md`, `README`, or other contributor docs)
- **Tasks completed in this chunk**: (bullet list of what was supposed to be done)
- **Files changed**: (repo-relative paths of all implementation and test files added or modified)

## Instructions (copy verbatim)

1. Read the plan file and any relevant project guidance docs.
2. Read every changed file end to end. Do not skim.
3. Run the completeness review, then the code-simplification review, using the criteria below.

---

## Review 1: Completeness

### What to look for

#### Omissions

- Are all planned tasks for this chunk actually implemented?
- Is there anything the plan calls for that is missing, stubbed, or deferred without explanation?
- Are there TODO, FIXME, or HACK comments that indicate incomplete work?

#### Shortcuts and hacks

- Were any compiler warnings, lint rules, or checks disabled to make things pass?
- Were any tests skipped, ignored, or marked as expected-failure without justification?
- Does any code work around the real problem rather than solving it?
- Were public APIs or contracts bent to accommodate the implementation?

#### Implementation integrity

- Does the code follow the patterns and conventions established in the rest of the codebase?
- Does the implementation match what the plan describes, or has it drifted?
- Are there obvious correctness issues — wrong types, missing null checks, off-by-one errors, race conditions?
- Is the code well commented, explaining architecture and "why" rather than just describing what it does?

---

## Review 2: Code Simplification

The question here is whether the implementation is as simple as it could be while still fulfilling the requirements. This is not a review of the requirements themselves — scope, features, and acceptance criteria are off the table. The question is only: given that this thing needs to exist, is it built simply?

Apply the spirit of `kphilosophy`: control complexity, prefer direct readable code, remove components that do not justify their cost, and look for places where there is something left to take away.

### What to look for

#### Unnecessary abstraction

- Are there base classes, interfaces, protocols, or indirection layers that exist for no current caller?
- Were helpers, utilities, or wrappers introduced that are only used once?
- Is there a simpler, more direct way to express the same logic without a layer of abstraction?

#### Premature generalization

- Does the code handle cases that don't exist yet — hypothetical future callers, optional extension points, unused configuration?
- Were parameters, flags, or modes added that have only one value in practice?
- Does the code read like it was designed for a library when it's an internal implementation detail?

#### Complexity that wasn't earned

- Are there more moving parts than the problem requires?
- Could two or three similar things be expressed as one without sacrificing clarity?
- Is there state being tracked that could be derived instead?
- Is there concurrency, caching, or lazy evaluation that the problem doesn't actually call for?

#### Over-engineering signals

- Design patterns applied where a plain function or loop would do
- Error handling for error conditions that cannot occur given the calling context
- Validation at internal call sites that trust internal code
- Backwards-compatibility shims or feature flags when the code was just written

---

## Output format

Write two structured reports, one per review:

### Completeness Review

1. **Verdict**: `PASS` or `ISSUES FOUND`
2. **Summary**: One paragraph — your overall honest assessment.
3. **Issues** (only if verdict is ISSUES FOUND): Numbered list, each with:
   - What the issue is
   - Where it is (file path and line number or range)
   - Why it matters (not just that it violates a rule, but what could go wrong)
   - Suggested fix

### Code Simplification Review

1. **Verdict**: `PASS` or `ISSUES FOUND`
2. **Summary**: One paragraph — your honest assessment of whether the implementation is as simple as it could be.
3. **Issues** (only if verdict is ISSUES FOUND): Numbered list, each with:
   - What the unnecessary complexity is
   - Where it is (file path and line number or range)
   - Why it matters (maintenance cost, cognitive load, or what simpler alternative exists)
   - Suggested simplification

Be concise. Only flag things that actually matter — real omissions, real hacks, real correctness problems, real unnecessary complexity. Do not pad reports with style nits or cosmetic suggestions.
