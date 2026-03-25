---
name: kbrainstorm
description: Explore fuzzy feature ideas, product problems, requirements, constraints, and tradeoffs through collaborative dialogue before writing a concrete implementation plan. Use when the request is ambiguous, scope is still moving, or you need to compare approaches before `/kplan`.
argument-hint: "[feature idea or problem to explore]"
disable-model-invocation: true
---

# Brainstorm a Feature or Improvement

Brainstorming answers **WHAT** to build through collaborative dialogue. It precedes `/kplan`, which answers **HOW** to build it.

**Current timestamp:** !`date +"%Y-%m-%d-%H-%M-%S"`

## Feature Description

<feature_description> $ARGUMENTS </feature_description>

If the feature description is empty, ask the user what they'd like to explore. Do not proceed without one.

## Execution Flow

### Phase 0: Assess Requirements Clarity

If the user's description already has specific acceptance criteria, exact expected behavior, and constrained scope, suggest proceeding directly to `/kplan` instead.

### Phase 1: Understand the Idea

1. **Reframe as "How Might We"** — before any research, restate the feature as a "How might we…" question. This opens the solution space and prevents locking in assumptions early.

2. **Lightweight repo research** — scan for similar features, established patterns, and CLAUDE.md guidance. Note anything relevant for Phase 2.

3. **Collaborative dialogue** — use AskUserQuestion to ask questions **one at a time**:
   - Start with "why" questions (up to 3 levels deep) to surface the real problem behind the stated one
   - Then broaden to purpose and users, then narrow to constraints and edge cases
   - Prefer multiple choice when natural options exist
   - Ask about success criteria
   - Validate assumptions explicitly — keep a running list and confirm it before moving on

   Continue until the idea is clear or the user says "proceed."

4. **Surface constraints** — before ideating, ask about deadlines, dependencies, tech debt to avoid, and team familiarity. Constraints are creative inputs, not blockers.

### Phase 2: Explore Approaches

1. **Diverge** — generate 4–5 possible approaches without judgment. Draw from repo patterns, analogous domains, inversion of the obvious solution, and the simplest thing that could work.

2. **Stress test** — for the most promising options, ask: "Imagine this failed in six months. What went wrong?" Name 1–2 realistic failure modes per candidate.

3. **Converge** — present the 2–3 strongest approaches with:
   - Brief description (2–3 sentences)
   - Pros, cons, and failure modes
   - When it's best suited

   Lead with your recommendation and why. Prefer simpler solutions (YAGNI).

   Ask the user which approach they prefer.

### Phase 3: Capture the Design

Use `${CLAUDE_SKILL_DIR}/assets/brainstorm-template.md` as the default shape. Keep the headings, drop sections that do not apply, and fill in validated assumptions rather than guesses.

Write to `docs/internal/brainstorms/` using the timestamp from the top of this document:

`docs/internal/brainstorms/<timestamp>-<topic-slug>-brainstorm.md`

Use kebab-case for the topic slug. Ensure the directory exists before writing.

Key sections: How Might We, Why This Approach, Assumptions (validated), Constraints, Key Decisions, Failure Modes, Open Questions.

If this brainstorm leads to `/kplan`, the plan should reference this document's exact repo-relative path in a `Related documents` section so `/kwork` can checkpoint both.

### Phase 4: Handoff

Ask the user:

1. **Proceed to planning** — run `/kplan`
2. **Refine further** — continue exploring
3. **Done for now** — return later

## Guidelines

- Stay focused on WHAT, not HOW — implementation details belong in the plan
- Ask one question at a time
- Diverge before converging
- Prefer simpler approaches
- Keep outputs concise — 200–300 words per section max
- NEVER CODE — just explore and document decisions
