---
name: kplan
description: Brainstorm a feature or change with the user, explore the repo to understand how it fits, then produce a concrete implementation plan. Creates a plan in `~/.k/workspaces/...`.
metadata:
  argument-hint: "[feature idea, bug report, or improvement to explore]"
  disable-model-invocation: "true"
---

## Workflow

### Phase 1 — Understand

1. Read `<feature_description> $ARGUMENTS </feature_description>`; if it is empty, ask what they want to plan and stop.
2. Decide whether brainstorming is needed.
   - If the request already has concrete scope, clear acceptance criteria, and constrained behavior, skip to Phase 2.
   - If the idea is fuzzy, broad, or has multiple possible interpretations, or if the user requests it, brainstorm first.
3. Brainstorm through collaborative dialogue.
   - Reframe the problem as a "How might we..." question.
   - Start with "why" questions and go a few levels deep. The stated request is often a proxy for the real problem.
   - Ask one question at a time.
   - Move from broad to narrow: purpose and users first, then constraints, edge cases, dependencies, and success criteria.
   - Prefer multiple choice when natural options exist — it's faster for the user and forces you to think about realistic possibilities.
   - Keep a running list of assumptions and validate them explicitly.
   - Ask about success criteria: how will the user know this worked?
   - Treat constraints as creative inputs, not annoyances. They often determine which approaches are actually viable.
   - Continue until the idea is clear or the user says "proceed."

### Phase 2 — Explore the repo

4. Explore the codebase to understand how the feature fits.
   - Find similar features, adjacent code, and prior attempts at the same problem.
   - Read project guidance docs when they exist so the plan matches repo conventions and architectural constraints.
   - Understand the existing architecture. Map the layers, modules, and boundaries the change will touch.
5. Evaluate the change through PHAME lenses.
   - **Hierarchy** — Does the change respect the existing layer structure? Do dependencies flow in the right direction?
   - **Abstraction** — Is the feature at the right level of abstraction? Does it mix high-level orchestration with low-level detail?
   - **Modularization** — Where does this responsibility belong? Would adding it to an existing module bloat its scope or blur its focus? Would a new module be a nano-module?
   - **Encapsulation** — Does the change respect existing boundaries? Would it require exposing internals that should stay private?
   - **Testability** — Can the new behavior be tested in isolation? Are dependencies injectable? Would the design force tests to rely on complex setup, global state, or implementation details? If something is hard to test, that's usually a design signal — reconsider the boundaries.
   - For OOP codebases: also consider whether SOLID principles are upheld where they already matter.
   - If the cleanest solution requires refactoring existing code, say so. The architecture is a living thing. New features should not be bolted on — they should be integrated thoughtfully. It is better to refactor first and then add the feature cleanly than to wedge it in and create structural debt.
6. Enumerate hard constraints the solution must satisfy.
   - Security posture, API compatibility, language/runtime constraints, existing data contracts, performance budgets, deployment constraints.
   - These are eliminators, not trade-offs. Any candidate that violates a hard constraint is disqualified before scoring.
7. Decide whether more research is needed and announce the decision.
   - **Skip research:** strong local patterns already exist, project guidance docs already cover the area, and the user has clear intent.
   - **Research when uncertain:** unfamiliar territory, no codebase examples, new technology or library, ambiguous behavior.

### Phase 3 — Evaluate

8. Generate candidate solutions.
   - Produce 2–3 meaningfully distinct approaches before evaluating any of them. Resist elaborating on the first idea — that's anchoring.
   - Source candidates from: existing repo patterns, analogous domains, inversion of the obvious solution, and the most boring/conventional thing that could work.
9. Eliminate disqualified candidates.
   - Apply the hard constraints from step 6. Remove any candidate that fails a hard constraint. This keeps the scoring step clean.
10. Evaluate surviving candidates.
    - For each candidate:
      - **Attachment map** — Where does this attach to the existing system? What files change? What existing patterns does it follow or deviate from?
      - **Assumptions** — What does this candidate assume about the existing system? (e.g., "assumes module X owns concern Y", "assumes this endpoint is only called from Z"). These become the plan's known failure modes.
      - **Pre-mortem** — Imagine this solution failed or caused problems in six months. What went wrong? Surface non-obvious risks — the "seems fine" option that has a subtle coupling problem.
    - Score each surviving candidate against these criteria, roughly in priority order:
      - **Architectural fit** — Does it follow existing patterns, or introduce a new abstraction class? New abstractions have a cost: surface area, documentation, onboarding debt.
      - **Locality** — How viral is the change? A solution that touches one file beats one that touches ten, all else equal. Coordinated updates across distant parts of the codebase are fragile.
      - **Minimal surface area** — Does the solution introduce new configuration knobs, new abstractions, new failure modes? Prefer the option that adds the least new *stuff* to the system's conceptual footprint.
      - **Testability** — Can the new behavior be tested through clean public interfaces? Does the approach require mocking internals, complex setup, or integration-only tests to verify? Prefer designs where the interesting behavior is reachable from unit tests. If a candidate forces test complexity, that's a design cost.
      - **Maintainability** — Will a stranger understand why this was done this way in six months? Partly about clarity of intent, partly about whether the solution pattern already exists elsewhere in the codebase.
11. Argue against your top pick.
    - Steelman the alternatives one more time, specifically targeting the winner's weaknesses. If it still wins, you have higher confidence.

### Phase 4 — Recommend

12. Present the 2–3 strongest approaches with: brief description, pros, cons, failure modes, and when it's best suited.
    - Lead with your recommendation and why. Prefer simpler approaches (YAGNI). Highlight any refactoring the recommended approach requires and why it's worthwhile.
    - State assumptions explicitly. The plan should document what it assumed about the existing system, because those assumptions are where implementation plans go wrong.
    - Ask the user which approach they prefer. Refine until aligned.

### Phase 5 — Write the plan

13. Generate the plan filename: `!`echo ~/.k/workspaces/${PWD//\//_}`/plans/YYYY-MM-DD-NNN-slug.md` where `YYYY-MM-DD` is today's date, `NNN` is the next available zero-padded sequence for that date, and the slug is a short kebab-case summary (3-5 words). Create the directory if it does not exist.
14. Write the plan from `assets/plan-template.md`.
    - Use the template as a scaffold, not a rigid form. Keep only the sections that apply, and add sections when the work needs more structure.
    - Every implementation task is a concrete, actionable bullet. A reader should be able to execute the plan without re-reading the codebase.
    - If refactoring is part of the plan, list refactoring tasks before feature tasks. Explain what each refactor achieves structurally.
    - Include a test plan section before the implementation tasks. Define what to test, at what level (unit, integration, e2e), and what the key assertions are. Focus on edge cases, error paths, and boundary conditions — not happy-path tests that merely restate the implementation. Tests should target public interfaces so they survive refactors. The implementer uses this test plan during implementation, so it must be specific enough to write meaningful tests.
    - Include validation steps: what tests to write, what commands to run, what to verify manually.
    - Include open questions for anything still unresolved. When the user later answers an open question, fold the decision into the relevant plan sections (goal, implementation tasks, structural considerations, etc.) and delete the question. Never rename "Open questions" to "Resolved questions" or leave answered questions in place — a plan should read as a coherent document, not a Q&A transcript.
    - `Related code` must be concrete: repo-relative paths plus one-line reasons each file matters. Vague references like "the auth module" are not useful.

### Phase 6 — Review the plan architecture

15. Run an architectural review pass on the written plan before handing it off for implementation.
    - Launch a dedicated architecture-review subagent when it adds value; otherwise perform the review locally.
    - Subagents start with fresh context, so include all necessary context in the review prompt.
    - Read `assets/architecture-review-prompt.md`, then compose the actual review prompt with the concrete plan path, repo guidance docs, and the most relevant files or modules from `Related code`.
    - The reviewer should evaluate whether the plan fits the current architecture cleanly and should look specifically for hierarchy, abstraction, modularization, encapsulation, and SOLID problems before code is written.
    - Instruct the reviewer to focus on architectural drift and structural oversights, not cosmetic style feedback.
16. Act on the review findings.
    - If the review reports issues worth fixing, update the plan to address them. Fold the fixes into the relevant sections instead of appending a transcript of the review.
    - If the fixes materially change the architecture, sequencing, or scope, run the architectural review again on the updated plan.
    - Repeat until the plan is structurally sound or the remaining concerns are explicit open questions for the user.
17. After the review loop is complete, print the final plan path and stop.
18. Suggest starting `/kwork` in a fresh session or with cleared context. Planning conversations consume significant context, and a fresh implementation session preserves room for the actual coding work.
19. Never code here.
