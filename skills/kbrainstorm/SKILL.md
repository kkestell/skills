---
name: kbrainstorm
description: Explore requirements and approaches through collaborative dialogue before planning implementation
---

## Arguments
[feature idea or problem to explore]

# Brainstorm a Feature or Improvement

**Note:** To get the current date for document timestamps, run `date +"%Y-%m-%d"` or `date +"%Y-%m-%d-%H-%M-%S"` for full timestamps.

Brainstorming helps answer **WHAT** to build through collaborative dialogue. It precedes `/kplan`, which answers **HOW** to build it.


## Feature Description

<feature_description> #$ARGUMENTS </feature_description>

**If the feature description above is empty, ask the user:** "What would you like to explore? Please describe the feature, problem, or improvement you're thinking about."

Do not proceed until you have a feature description from the user.

## Execution Flow

### Phase 0: Assess Requirements Clarity

Evaluate whether brainstorming is needed based on the feature description.

**Clear requirements indicators:**
- Specific acceptance criteria provided
- Referenced existing patterns to follow
- Described exact expected behavior
- Constrained, well-defined scope

**If requirements are already clear:**
Use **AskUserQuestion tool** to suggest: "Your requirements seem detailed enough to proceed directly to planning. Should I run `/kplan` instead, or would you like to explore the idea further?"

### Phase 1: Understand the Idea

#### 1.0 Reframe as "How Might We"

Before any research or dialogue, reframe the feature description as a **"How might we…"** question. State it explicitly. This opens solution space and avoids locking in assumptions too early.

Example: *"How might we help users resume interrupted workflows?"* rather than *"Build a resume-session feature."*

#### 1.1 Repository Research (Lightweight)

Scan the repository to understand existing patterns:

- Look for similar features in the codebase
- Check for established patterns and conventions
- Review CLAUDE.md for project-specific guidance

When a similar feature or pattern exists, run a quick **SCAMPER** check on it:

| Letter | Prompt |
|--------|--------|
| **S**ubstitute | What could be swapped out? |
| **C**ombine | What could be merged with something else? |
| **A**dapt | What from another context could apply here? |
| **M**odify | What could be scaled up, down, or reshaped? |
| **P**ut to other use | Could this solve a different problem too? |
| **E**liminate | What could be removed entirely? |
| **R**everse | What if the flow or responsibility were flipped? |

Note any SCAMPER insights for use in Phase 2.

#### 1.2 Collaborative Dialogue

Use the **AskUserQuestion tool** to ask questions **one at a time**.

**Guidelines:**
- Prefer multiple choice when natural options exist
- Start with **Five Whys**: ask "why do you need this?" up to 3 levels deep before moving to scope or behavior. This surfaces the real problem, which is often different from the stated one.
- Then broaden to purpose and users, then narrow to constraints and edge cases
- Validate assumptions explicitly — maintain a running **Assumptions Log** (see below)
- Ask about success criteria

**Assumptions Log:**
Throughout the dialogue, keep a visible, running list:
```
Assumptions so far:
- [assumption 1]
- [assumption 2]
```
Update it after each exchange. Before moving to Phase 2, show the full list and ask the user to confirm or correct it. Unvalidated assumptions are the #1 cause of plan failures.

**Exit condition:** Continue until the idea is clear OR user says "proceed"

### Phase 1.5: Surface Constraints

Before ideating on approaches, explicitly surface constraints with the **AskUserQuestion tool**:

- Time / deadline pressure?
- Existing dependencies or integrations that must be respected?
- Known tech debt or areas to avoid touching?
- Team familiarity with relevant technologies?

Constraints are not blockers — they are **creative inputs**. The best approach often emerges directly from the tightest constraint.

Summarize the confirmed constraints in a short list before moving to Phase 2.

### Phase 2: Explore Approaches

#### 2.1 Diverge — Generate Options Broadly

Before evaluating anything, generate a wide set of possible approaches **without judgment**. Draw from:

- SCAMPER insights from Phase 1.1
- **Analogous domains**: How does another system (inside or outside the codebase) solve a similar problem? Non-obvious analogies often unlock the best approaches.
- Inversion of the obvious solution
- The simplest possible thing that could work

Aim for at least 4–5 raw options at this stage. List them briefly — no pros/cons yet.

#### 2.2 Pre-Mortem — Stress Test Before Committing

Before narrowing down, run a quick **pre-mortem** on the most promising options:

> *"Imagine it's six months from now and this feature failed. What went wrong?"*

For each candidate approach, name 1–2 realistic failure modes. This surfaces constraints and risks that only become visible once you've committed to a direction — better to find them now.

#### 2.3 Converge — Propose 2–3 Best Approaches

From the diverge list, select the **2–3 strongest approaches** (informed by constraints and the pre-mortem) and present them fully:

For each approach, provide:
- Brief description (2-3 sentences)
- Pros and cons
- Failure modes identified in pre-mortem
- When it's best suited

Lead with your recommendation and explain why. Apply YAGNI—prefer simpler solutions.

**Design Quality Lens** — for each approach, briefly evaluate:

| Principle | Question |
|-----------|----------|
| **SRP** | Does each major component have one reason to change? |
| **OCP / DIP** | Can it be extended without modification? Do high-level parts depend on abstractions, not concretions? |
| **YAGNI / KISS** | Are we building only what's needed now, in the simplest possible way? |
| **Value Objects** | What domain concepts (IDs, money, emails, status) should be wrapped — not left as raw primitives? |
| **Complexity** | Is there accidental complexity we can remove? Prefer solutions with low change amplification. |

Identify the object stereotype for each major component: *Information Holder, Service Provider, Coordinator, Controller, Interfacer, or Structurer*.

Use **AskUserQuestion tool** to ask which approach the user prefers.

### Phase 3: Capture the Design

Write a brainstorm document to `docs/internal/brainstorms/YYYY-MM-DD-HH-MM-SS-<topic>-brainstorm.md`.

**Timestamp is required (no exceptions):**

- Generate a local timestamp once using `date +"%Y-%m-%d-%H-%M-%S"`.
- Always include the full `HH-MM-SS` segment in the filename.
- Never write a brainstorm file with a date-only prefix.

**Filename construction and validation:**

- Build filename as: `docs/internal/brainstorms/<timestamp>-<topic>-brainstorm.md`
- Use kebab-case for `<topic>` (lowercase letters, numbers, dashes only).
- Validate before writing with this pattern:
  - `^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+-brainstorm\.md$`
- If validation fails (especially missing `HH-MM-SS`), regenerate and fix the filename before writing.

**Examples:**

- GOOD: `docs/internal/brainstorms/2026-03-23-14-05-19-user-onboarding-brainstorm.md`
- BAD: `docs/internal/brainstorms/2026-03-23-user-onboarding-brainstorm.md` (missing `HH-MM-SS`)

**Document structure:** Key sections: How Might We, Why This Approach, Assumptions (validated), Constraints, Key Decisions, Failure Modes, Open Questions.

Ensure `docs/internal/brainstorms/` directory exists before writing.

**Planning handoff requirement:** If this brainstorm leads to `/kplan`, the plan should include this brainstorm's exact repo-relative path in a `Related documents` section. `/kwork` relies on that reference to checkpoint both docs on `main` before it creates a worktree.

### Phase 4: Handoff

Use **AskUserQuestion tool** to present next steps:

**Question:** "Brainstorm captured. What would you like to do next?"

**Options:**
1. **Proceed to planning** - Run `/kplan` (will auto-detect this brainstorm)
2. **Refine design further** - Continue exploring
3. **Done for now** - Return later

## Output Summary

When complete, display:

```
Brainstorm complete!

Document: docs/internal/brainstorms/YYYY-MM-DD-HH-MM-SS-<topic>-brainstorm.md
(must include full `HH-MM-SS`; do not show date-only filenames)

Key decisions:
- [Decision 1]
- [Decision 2]

Validated assumptions:
- [Assumption 1]
- [Assumption 2]

Next: Run `/kplan` when ready to implement.
```

## Important Guidelines

- **Stay focused on WHAT, not HOW** - Implementation details belong in the plan
- **Ask one question at a time** - Don't overwhelm
- **Diverge before converging** - Generate broadly, then narrow with intention
- **Apply YAGNI** - Prefer simpler approaches
- **Keep outputs concise** - 200-300 words per section max

NEVER CODE! Just explore and document decisions.
