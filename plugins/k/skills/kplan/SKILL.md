---
name: kplan
description: Brainstorm a feature or change with the user, explore the repo to understand how it fits, then produce a concrete implementation plan. Creates `docs/agents/plans/YYYY-MM-DD-NNN-slug.md`.
argument-hint: "[feature idea, bug report, or improvement to explore]"
disable-model-invocation: true
---

## Compatibility

- Treat all paths in this skill as relative to the skill directory unless the host environment provides its own skill-directory variable.
- In Claude-style environments, `${CLAUDE_SKILL_DIR}` may point at this directory. In Codex-style environments, resolve sibling paths like `assets/plan-template.md` directly from this `SKILL.md`.
- If the host environment has a dedicated question-asking tool, you may use it. Otherwise ask the user directly in a normal message.
- This skill plans only. Do not implement code changes here.

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
   - Understand the existing architecture. Map the layers, modules, and boundaries the change will touch.
5. Evaluate the change through PHAME lenses.
   - **Hierarchy** — Does the change respect the existing layer structure? Do dependencies flow in the right direction?
   - **Abstraction** — Is the feature at the right level of abstraction? Does it mix high-level orchestration with low-level detail?
   - **Modularization** — Where does this responsibility belong? Would adding it to an existing module create a God module or violate single-purpose? Would a new module be a nano-module?
   - **Encapsulation** — Does the change respect existing boundaries? Would it require exposing internals that should stay private?
   - If the cleanest solution requires refactoring existing code, say so. The architecture is a living thing. New features should not be bolted on — they should be integrated thoughtfully. It is better to refactor first and then add the feature cleanly than to wedge it in and create structural debt.
6. Decide whether more research is needed and announce the decision.
   - **Skip research:** strong local patterns already exist, project guidance docs already cover the area, and the user has clear intent.
   - **Research when uncertain:** unfamiliar territory, no codebase examples, new technology or library, ambiguous behavior.

### Phase 3 — Recommend

7. Explore and narrow the solution space.
   - Diverge before converging. Generate a few plausible approaches without judgment first — draw from repo patterns, analogous domains, inversion of the obvious solution, and the simplest thing that could work.
   - Stress-test the strongest options: "Imagine this failed in six months. What went wrong?"
   - Present the 2-3 strongest approaches with: brief description, pros, cons, failure modes, and when it's best suited.
   - Lead with your recommendation and why. Prefer simpler approaches (YAGNI). Highlight any refactoring the recommended approach requires and why it's worthwhile.
   - Ask the user which approach they prefer. Refine until aligned.

### Phase 4 — Write the plan

9. Generate the plan filename: `docs/agents/plans/YYYY-MM-DD-NNN-slug.md` where `YYYY-MM-DD` is today's date, `NNN` is the next available zero-padded sequence for that date, and the slug is a short kebab-case summary (3-5 words). Create the `docs/agents/plans/` directory if it does not exist.
10. Write the plan from `assets/plan-template.md`.
    - Use the template as a scaffold, not a rigid form. Keep only the sections that apply, and add sections when the work needs more structure.
    - Every implementation task gets an actionable checkbox. A reader should be able to execute the plan without re-reading the codebase.
    - If refactoring is part of the plan, list refactoring tasks before feature tasks. Explain what each refactor achieves structurally.
    - Include validation steps: what tests to write, what commands to run, what to verify manually.
    - Include open questions for anything still unresolved. When the user later answers an open question, fold the decision into the relevant plan sections (goal, implementation tasks, structural considerations, etc.) and delete the question. Never rename "Open questions" to "Resolved questions" or leave answered questions in place — a plan should read as a coherent document, not a Q&A transcript.
    - `Related code` must be concrete: repo-relative paths plus one-line reasons each file matters. Vague references like "the auth module" are not useful.
11. After writing, print the plan path and stop.
12. Suggest starting `/kwork` in a fresh session or with cleared context if the host environment supports that. Planning conversations consume significant context, and a fresh implementation session preserves room for the actual coding work.
13. Never code here.
