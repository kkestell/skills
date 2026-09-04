---
name: kroadmap
description: "Create or update eng/roadmap.md with user-directed milestones, scope, ordering, and completion gates. Use when defining, changing, or recording the project roadmap; do not invoke merely to read it."
argument-hint: "[roadmap change, or blank to create/review the roadmap]"
---

## Workflow

This skill owns changes to `eng/roadmap.md`. Reading the roadmap does not
require it.

### Establish the roadmap work

1. Resolve `<roadmap_work> $ARGUMENTS </roadmap_work>` and the repository root.
   Confirm that the path is a Git repository.
2. Require `docs/spec.md`. If it is missing, stop and tell the user to run
   `kspec` before creating or changing the roadmap.
3. Read `AGENTS.md`, `docs/spec.md`, and `eng/roadmap.md` when it exists.
   Inspect source, tests, plans, and history only as needed to establish current
   status or dependencies.
4. Confirm that `docs/spec.md` settles the behavior needed for the proposed
   roadmap work. If material behavior is missing or ambiguous, stop, name the
   gap, and tell the user to resolve it with `kspec`. A file's existence alone
   does not make it sufficient.
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
   - Keep detailed build scope and gates for the current milestone.
   - Describe the next milestone at a high level.
   - Keep later work as an ordered list of distinct milestones.
   - After the first milestone is complete, keep exactly one concise summary of
     the most recently completed milestone and remove its previous detail.
8. A milestone is a logical outcome large enough to name. Divide the current
   milestone into tasks with concrete build scope and gates that prove the task
   complete against `docs/spec.md`.
9. Order milestones, tasks, and later work by position in the file. Do not
   number them; completed work can then be removed without renumbering what
   remains.
10. Record scope and gates, not implementation design, standard repository
    commands, or duplicated specification rules. Plans own the implementation of
    bounded slices.
11. Mark work complete only when repository evidence proves it. Preserve
    unrelated roadmap content, never leave template prompts in the written file,
    and do not turn a possible future feature into a commitment.
12. Report what changed and ask the next unresolved roadmap question, if one
    remains.

## Principles

- The user owns product direction; the agent may recommend ordering from real
  dependencies.
- The specification owns behavior, architecture owns durable design, and the
  roadmap owns build order and completion gates.
- Describe work by its outcome outside the roadmap, never by a milestone or task
  number.
