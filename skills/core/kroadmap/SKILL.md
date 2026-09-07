---
name: kroadmap
description: "Create or update eng/roadmap.md with user-directed milestones, implementation tasks, scope, ordering, and completion gates. Use when defining, changing, or recording the project roadmap; do not invoke merely to read it."
argument-hint: "[roadmap change, or blank to plan the next milestone]"
---

## Workflow

This skill owns changes to `eng/roadmap.md`. Reading the roadmap does not
require it.

### Establish the roadmap work

1. Resolve `<roadmap_work> $ARGUMENTS </roadmap_work>` and the repository root.
   Confirm that the path is a Git repository.
2. Require `docs/spec.md`. If it is missing, invoke `kspec` to establish the
   behavior needed for the requested roadmap work, then resume this workflow.
3. Read `AGENTS.md`, `docs/spec.md`, and `eng/roadmap.md` when it exists.
   Inspect source, tests, plans, and history only as needed to establish current
   status or dependencies.
   With no arguments, plan the milestone after the current milestone using the
   roadmap's established order. Define its tasks and completion gates even when
   the current milestone is unfinished. Keep it under Next until repository
   evidence proves the current milestone complete, then promote it. If the
   roadmap has no current milestone, plan the first pending milestone. Existing
   roadmap direction is sufficient authorization for this planning. If no
   roadmap or next direction exists, establish direction under step 5.
4. Confirm that `docs/spec.md` settles the behavior needed for the proposed
   roadmap work. If material behavior is missing or ambiguous, invoke `kspec`
   in the same session, scoped to the decisions needed for the selected
   milestone. Ask only the questions needed to unblock that milestone, one at
   a time, using existing decisions where available. Once those decisions are
   recorded in the specification, resume planning its tasks, example, and
   completion gates. Leave unrelated specification questions for later work.
5. Treat product direction and priority as the user's decisions.
   - When the request already states the desired work and order, record it
     directly.
   - When direction is unclear, ask one question at a time. Offer a recommended
     dependency order when the specification supports one, but do not silently
     invent milestones or priorities.
   - Confirm a new roadmap's direction before writing it.

### Write eng/roadmap.md

6. Create `eng/` when needed and use `assets/roadmap-template.md` for a new
   file. Use the project name in the title when it is established; otherwise
   keep the neutral `Roadmap` title. Remove sections that do not apply instead
   of inventing work to fill them.
7. Keep the roadmap forward-looking.
   - Keep ordered implementation tasks and gates for the current milestone.
   - Keep the next milestone's ordered tasks and gates once planned; until then,
     describe it at a high level.
   - Keep later work as an ordered list of distinct milestones.
   - After the first milestone is complete, keep exactly one concise summary of
     the most recently completed milestone and remove its previous detail.
8. A milestone is an integrated outcome made up of bounded implementation tasks.
   Define the selected milestone's tasks here, with scope clear enough for
   `kwork` to plan briefly and implement one task at a time. A milestone must
   have its tasks defined before implementation begins. Collect completion
   gates at the milestone boundary against `docs/spec.md`. Tasks may be
   intermediate implementation steps; they do not each need a standalone
   deliverable.
9. Order milestones, tasks, and later work by position in the file. Do not
   number them; completed work can then be removed without renumbering what
   remains.
10. Record scope and gates, not implementation design, standard repository
    commands, or duplicated specification rules. `kwork` works out implementation
    steps in context.
11. Mark work complete only when repository evidence proves it. Preserve
    unrelated roadmap content, never leave template prompts in the written file,
    and do not turn a possible future feature into a commitment.
12. Report what changed and ask the next unresolved roadmap question, if one
    remains.

## Principles

- The user owns product direction; the agent may recommend ordering from real
  dependencies.
- The specification owns behavior, architecture owns durable design, and the
  roadmap owns task creation, task scope, build order, and completion gates.
- Describe work by its outcome outside the roadmap, never by a milestone or task
  number.
