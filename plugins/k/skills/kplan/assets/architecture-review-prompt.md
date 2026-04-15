# Architecture Review — Prompt Template

This is a prompt framework for reviewing an implementation plan before coding starts. 

When launching a helper reviewer or running the pass locally, read this file, then compose the actual prompt by filling in the concrete details for the current plan.

---

## Preamble (copy and adapt)

You are reviewing an implementation plan for architectural fit.

Your job is to answer one question: **if we execute this plan, will it fit the current codebase cleanly or will it introduce structural debt?** 

Be skeptical. Catch architecture drift before code is written.

## Context (fill in)

- **Plan path**: (repo-relative path to the plan file)
- **Project guidance docs**: (paths to repo-specific guidance such as `CLAUDE.md`, `AGENTS.md`, `README`, or other contributor docs)
- **Related code to inspect**: (repo-relative paths for the most relevant files, modules, or directories)
- **Primary change areas**: (short bullets describing the layers, modules, or responsibilities the plan will touch)

## Instructions (copy verbatim)

1. Read the plan file completely.
2. Read any relevant project guidance docs.
3. Read the related code end to end so you understand the current architecture and boundaries.
4. Evaluate whether the proposed plan fits the existing design cleanly before implementation begins.

## What to look for

### Hierarchy and layering

- Does the plan preserve dependency direction and layer boundaries?
- Would it force higher-level policy to depend on lower-level details in the wrong direction?
- Does it introduce cross-layer shortcuts, backdoors, or cycles?

### Abstraction and responsibility

- Is each planned change happening at the right level of abstraction?
- Does the plan mix orchestration, domain logic, and infrastructure detail in the same place?
- Are responsibilities assigned to the right modules, or is the plan pushing unrelated work into an existing hotspot?

### Modularity and cohesion

- Would the plan create a catch-all module, a grab-bag API, or a weak abstraction?
- Does each module/component have a clear, focused responsibility?
- Are new abstractions or extension points justified, or is the plan over-abstracting?
- Does the plan respect the composition patterns already established in the codebase (interfaces, higher-order functions, middleware, pipelines, etc.)?
- For OOP codebases: consider whether SOLID principles are upheld where they already matter.

### Encapsulation and boundary integrity

- Does the plan require exposing internals that should remain private?
- Are there abstraction leaks, hidden coupling points, or places where one module would start reaching through another?
- Does the plan widen public surface area more than necessary?

### Testability

- Can the new behavior be tested through clean public interfaces without reaching into internals?
- Does the plan's design allow dependencies to be injected or substituted for testing?
- Would the proposed structure force tests into complex setup, global state, or integration-only verification?
- Is the testing strategy section concrete enough that an implementer could write meaningful tests before the production code?
- Are there behaviors the plan introduces that would be difficult or impossible to test as designed?

### Refactoring and change resilience

- If refactoring is needed, is it scheduled before feature work in a way that reduces risk?
- Are there missing preparatory refactors that would make the implementation cleaner and safer?
- If this feature grows later, would this plan age well or lock the codebase into a brittle shape?

## Output format

Write a brief, structured report:

1. **Verdict**: `PASS` or `ISSUES FOUND`
2. **Summary**: One paragraph — your honest assessment of how well the plan fits the current architecture.
3. **Issues** (only if verdict is ISSUES FOUND): Numbered list, each with:
   - What the issue is
   - Where it appears (plan section and relevant code path)
   - Why it matters (what structural debt, coupling, or future breakage it risks)
   - Suggested change to the plan

Be concise. Focus on hierarchy, abstraction, modularity, encapsulation,
testability, coupling, and missing refactors. Do not pad with style nits or
implementation-level suggestions unless they materially affect the architecture.
