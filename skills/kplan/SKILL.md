---
name: kplan
description: Brainstorm a code change with the user, explore the repo to understand how it fits, then produce a concrete implementation plan. Creates a plan in `eng/plans/`, splitting work too large for one implementation session into a sequence of plans. Use this when the user wants to plan new code work or requests a significant change to existing behavior. Do not use it to write or update documentation — a roadmap, spec, design note, or README is edited directly, even when it describes future work.
argument-hint: "[feature idea, bug report, or improvement to explore]"
---

## Workflow

This skill plans code changes and produces a plan file. Documentation — a
roadmap, spec, design note, or README — is edited directly, even when it
describes work that has not been done yet.

### Phase 1 — Understand

1. Resolve `<feature_description> $ARGUMENTS </feature_description>`.
   - If it is present, use it as the proposed work.
   - If it is empty, inspect the repository's planning sources and current
     state to infer the next task. Start with project guidance that owns work
     ordering or a backlog, then consult existing plans, repository history,
     and the implementation only as needed. Choose the strongest single
     candidate rather than asking the user to supply what the repository can
     reveal.
   - State the inferred task and the evidence that makes it next, ask the user
     to confirm that it should be planned, and stop until they answer. If the
     repository does not support a credible inference, ask what they want to
     plan instead.
2. Decide whether brainstorming is needed.
   - If the request already has concrete scope, clear acceptance criteria, and
     constrained behavior, skip to Phase 2.
   - If the idea is fuzzy, broad, or has multiple possible interpretations, or
     if the user requests it, brainstorm first.
3. Brainstorm through collaborative dialogue.
   - Reframe the problem as a "How might we..." question.
   - Start with "why" questions and go a few levels deep. The stated request is
     often a proxy for the real problem.
   - Ask one question at a time.
   - Move from broad to narrow: purpose and users first, then constraints, edge
     cases, dependencies, and success criteria.
   - Prefer multiple choice when natural options exist — it's faster for the
     user and forces you to think about realistic possibilities.
   - Keep a running list of assumptions and validate them explicitly.
   - Ask about success criteria: how will the user know this worked?
   - Treat constraints as creative inputs, not annoyances. They often determine
     which approaches are actually viable.
   - Continue until the idea is clear or the user says "proceed."

### Phase 2 — Explore the repo

4. Explore the codebase to understand how the feature fits.
   - Find similar features, adjacent code, and prior attempts at the same
     problem.
   - Read project guidance docs when they exist so the plan matches repo
     conventions and architectural constraints.
   - Understand the existing architecture. Map the layers, modules, and
     boundaries the change will touch.
5. Evaluate the change through PHAME lenses.
   - **Hierarchy** — Does the change respect the existing layer structure? Do
     dependencies flow in the right direction?
   - **Abstraction** — Is the feature at the right level of abstraction? Does it
     mix high-level orchestration with low-level detail?
   - **Modularization** — Where does this responsibility belong? Would adding it
     to an existing module bloat its scope or blur its focus? Would a new module
     be a nano-module?
   - **Encapsulation** — Does the change respect existing boundaries? Would it
     require exposing internals that should stay private?
   - **Testability** — Can the new behavior be tested in isolation? Are
     dependencies injectable? Would the design force tests to rely on complex
     setup, global state, or implementation details? If something is hard to
     test, that's usually a design signal — reconsider the boundaries.
   - For OOP codebases: also consider whether SOLID principles are upheld where
     they already matter.
   - If the cleanest solution requires refactoring existing code, say so. The
     architecture is a living thing. New features should not be bolted on — they
     should be integrated thoughtfully. It is better to refactor first and then
     add the feature cleanly than to wedge it in and create structural debt.
6. Enumerate hard constraints the solution must satisfy.
   - Security posture, API compatibility, language/runtime constraints, existing
     data contracts, performance budgets, deployment constraints.
   - These are eliminators, not trade-offs. Any candidate that violates a hard
     constraint is disqualified before scoring.
7. Decide whether more research is needed and announce the decision.
   - **Skip research:** strong local patterns already exist, project guidance
     docs already cover the area, and the user has clear intent.
   - **Research when uncertain:** unfamiliar territory, no codebase examples,
     new technology or library, ambiguous behavior.

### Phase 3 — Evaluate

8. Generate candidate solutions.
   - Produce 2–3 meaningfully distinct approaches before evaluating any of them.
     Resist elaborating on the first idea — that's anchoring.
   - Source candidates from: existing repo patterns, analogous domains,
     inversion of the obvious solution, and the most boring/conventional thing
     that could work.
9. Eliminate disqualified candidates.
   - Apply the hard constraints from step 6. Remove any candidate that fails a
     hard constraint. This keeps the scoring step clean.
10. Evaluate surviving candidates.
    - For each candidate:
      - **Attachment map** — Where does this attach to the existing system? What
        files change? What existing patterns does it follow or deviate from?
      - **Assumptions** — What does this candidate assume about the existing
        system? (e.g., "assumes module X owns concern Y", "assumes this endpoint
        is only called from Z"). These become the plan's known failure modes.
      - **Pre-mortem** — Imagine this solution failed or caused problems in six
        months. What went wrong? Surface non-obvious risks — the "seems fine"
        option that has a subtle coupling problem.
    - Score each surviving candidate against these criteria, roughly in priority
      order:
      - **Architectural fit** — Does it follow existing patterns, or introduce a
        new abstraction class? New abstractions have a cost: surface area,
        documentation, onboarding debt.
      - **Locality** — How viral is the change? A solution that touches one file
        beats one that touches ten, all else equal. Coordinated updates across
        distant parts of the codebase are fragile.
      - **Minimal surface area** — Does the solution introduce new configuration
        knobs, new abstractions, new failure modes? Prefer the option that adds
        the least new _stuff_ to the system's conceptual footprint.
      - **Testability** — Can the new behavior be tested through clean public
        interfaces? Does the approach require mocking internals, complex setup,
        or integration-only tests to verify? Prefer designs where the
        interesting behavior is reachable from unit tests. If a candidate forces
        test complexity, that's a design cost.
      - **Maintainability** — Will a stranger understand why this was done this
        way in six months? Partly about clarity of intent, partly about whether
        the solution pattern already exists elsewhere in the codebase.
11. Argue against your top pick.
    - Steelman the alternatives one more time, specifically targeting the
      winner's weaknesses. If it still wins, you have higher confidence.

### Phase 4 — Recommend

12. Present the 2–3 strongest approaches with: brief description, pros, cons,
    failure modes, and when it's best suited.
    - Lead with your recommendation and why. Prefer simpler approaches (YAGNI).
      Highlight any refactoring the recommended approach requires and why it's
      worthwhile.
    - State assumptions explicitly. The plan should document what it assumed
      about the existing system, because those assumptions are where
      implementation plans go wrong.
    - Ask the user which approach they prefer. Refine until aligned.
    - Settle every open decision before moving on. A plan is a decided thing:
      no open questions, no "TBD", no alternatives left for the implementer,
      no choices deferred to implementation time. Ask about everything the repo
      does not settle and wait for the answers.
13. Size the chosen approach against a single implementation session.
    - Sketch the implementation tasks first. Sizing an approach you have not
      decomposed is guesswork.
    - The unit of work is one `kwork` session: one agent implementing, testing,
      reviewing, and committing within the context it starts with. Ask whether
      that session can finish the whole change and still have room for the
      review passes at the end.
    - Signals the work is too large: it spans several subsystems that each have
      to be understood in depth; it requires holding more of the codebase in
      view than one session can; it introduces a new abstraction and then
      migrates existing callers onto it; it has a long mechanical tail after the
      interesting part (many call sites, many fixtures, a wide rename); or the
      task list runs past roughly a dozen substantial items.
    - Signals it fits: one subsystem, a bounded set of files, and tasks that
      mostly share the same context.
    - Announce the verdict and the reasoning. If the work fits, continue to
      Phase 5 and write one plan.
14. Split work that does not fit into a sequence of plans.
    - Cut where the repository is left coherent. Each plan must end with the
      build green, the tests passing, and a commit that stands on its own. Never
      cut mid-refactor or leave callers half migrated.
    - Cut along structural seams, not by task count. A preparatory refactor, the
      new module, and the migration of callers onto it are three plans; the same
      feature sliced arbitrarily in half is not.
    - Order the sequence so each plan depends only on plans before it. If two
      plans need each other, the cut is in the wrong place — move it.
    - Prefer the fewest plans that satisfy those rules. Two or three is common.
      A long chain usually means the approach is too ambitious and the scope
      should be narrowed with the user instead.
    - Present the proposed split: each plan, what it delivers, and why the
      boundaries fall where they do. Get the user's agreement before writing,
      and move the cuts if they want them elsewhere.

### Phase 5 — Write the plans

15. Generate the plan filename: `eng/plans/YYYY-MM-DD-NNN-slug.md` where
    `YYYY-MM-DD` is today's date, `NNN` is the next available zero-padded
    sequence for that date, and the slug is a short kebab-case summary (3-5
    words). Create the directory if it does not exist. `eng/` is tracked in
    git — do not add it to `.gitignore` or `.git/info/exclude`.
    - For a split, allocate consecutive `NNN` values in execution order so the
      series reads in order on disk and `kwork` picks the plans up in turn.
      Give each plan a slug describing its own work, not the shared feature.
16. Write the plan from `assets/plan-template.md`.
    - Use the template as a scaffold, not a rigid form. Keep only the sections
      that apply, and add sections when the work needs more structure.
    - Every implementation task is a concrete, actionable bullet. A reader
      should be able to execute the plan without re-reading the codebase.
    - If refactoring is part of the plan, list refactoring tasks before feature
      tasks. Explain what each refactor achieves structurally.
    - Include a test plan section before the implementation tasks. Define what
      to test, at what level (unit, integration, e2e), and what the key
      assertions are. Focus on edge cases, error paths, and boundary conditions
      — not happy-path tests that merely restate the implementation. Tests
      should target public interfaces so they survive refactors. The implementer
      uses this test plan during implementation, so it must be specific enough
      to write meaningful tests.
    - Include validation steps: what tests to write, what commands to run, what
      to verify manually.
    - The plan states decisions, not options. Every choice the user made is
      written as the decision it is, with its reason. Do not preserve the
      alternatives, the questions that produced the decision, or a record of how
      the conversation went — a plan reads as a coherent document, not a Q&A
      transcript.
    - If a new question surfaces while writing, stop, ask the user, fold the
      answer into the relevant sections, and continue.
    - `Related code` must be concrete: repo-relative paths plus one-line reasons
      each file matters. Vague references like "the auth module" are not useful.
17. Write every plan in a series now, and make each one stand alone.
    - Fill in each plan's `Sequence` section: its position in the series, the
      state the earlier plans leave behind, and what it defers to later ones.
    - Scope the rest of each plan to its own work. Its test plan covers the
      behavior it adds, and its validation must be runnable when that plan alone
      is done.
    - The implementer of the third plan reads the third plan, not the series.
      Restate the context it needs instead of pointing back at earlier plans.

### Phase 6 — Review the plan architecture

18. Run an architectural review pass on each written plan before handing it off
    for implementation.
    - Launch a dedicated architecture-review subagent when it adds value;
      otherwise perform the review locally.
    - Subagents start with fresh context, so include all necessary context in
      the review prompt.
    - Read `assets/architecture-review-prompt.md`, then compose the actual
      review prompt with the concrete plan path, repo guidance docs, and the
      most relevant files or modules from `Related code`.
    - The reviewer should evaluate whether the plan fits the current
      architecture cleanly and should look specifically for hierarchy,
      abstraction, modularization, encapsulation, and SOLID problems before code
      is written.
    - Instruct the reviewer to focus on architectural drift and structural
      oversights, not cosmetic style feedback.
    - For a series, give one reviewer the whole set so it can judge the cut
      points too: whether each plan leaves the repository working, whether any
      plan depends on a later one, and whether a boundary splits work that
      belongs together.
19. Act on the review findings.
    - If the review reports issues worth fixing, update the plan to address
      them. Fold the fixes into the relevant sections instead of appending a
      transcript of the review.
    - If the fixes materially change the architecture, sequencing, or scope, run
      the architectural review again on the updated plan.
    - If the review shows a cut point is wrong, move the boundary and rewrite
      the affected plans. Do not patch around a bad seam.
    - If the review raises a concern you cannot settle yourself, ask the user,
      then fold their answer into the plan. Do not leave it in the plan as an
      open question.
    - Repeat until the plan is structurally sound.
20. After the review loop is complete, print the final plan paths in execution
    order and stop.
21. Suggest starting the `kwork` skill in a fresh session or with cleared
    context, one session per plan. Planning conversations consume significant
    context, and a fresh implementation session preserves room for the actual
    coding work.
22. Never code here.
