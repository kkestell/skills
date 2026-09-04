---
name: kplan
description: Explore how a code change fits the repository, resolve material decisions, and write a concise implementation plan in `eng/plans/`. Use when the user wants to plan code work or requests a significant behavior change. Do not use it to write or update documentation such as a roadmap, specification, design note, or README.
argument-hint: "[feature idea, bug report, or improvement to explore]"
---

## Workflow

This skill produces an implementation plan. It never implements the plan.

### Establish the work

1. Resolve `<feature_description> $ARGUMENTS </feature_description>`.
   - When it is present, use it as the proposed work.
   - When it is empty, infer the next slice from the repository source that owns
     work ordering. Inspect plans, history, and code only when needed to
     distinguish the next unimplemented slice.
   - Continue without confirmation when the user has already authorized planning
     the next repository-defined slice. Ask one focused question only when the
     next work remains ambiguous.
2. Read the authoritative requirement sources first.
   - When the specification, roadmap, or another named source already defines
     the behavior, scope, and acceptance gates, treat it as sufficient.
   - Reference those sources from the plan. Do not restate their contents.
3. Resolve only decisions that can change the implementation.
   - Ask the user one question at a time when product or language behavior is
     genuinely unsettled.
   - Update the document that owns the decision before the plan depends on it.
   - Compare alternatives only when the repository leaves a real choice. Follow
     an established local pattern directly when it already settles the design.

### Explore and size

4. Inspect the smallest useful part of the repository.
   - Find the attachment points, adjacent patterns, affected public boundaries,
     and tests.
   - Use targeted searches and file ranges. Do not dump whole directories or
     reread guidance already present in the session.
   - Check architectural fit directly. Do not produce a separate PHAME,
     pre-mortem, scoring, or steelman report.
5. Size the work for one `kwork` session.
   - Split only when one session cannot implement, test, validate, and commit
     the change comfortably.
   - Cut at coherent boundaries. Each plan must leave the repository working and
     depend only on earlier plans.
   - Prefer the fewest plans that fit.

### Write

6. Name each plan `eng/plans/YYYY-MM-DD-NNN-slug.md`, using the next sequence
   for the day.
7. Write from `assets/plan-template.md`.
   - Plans are slim by default. Prefer 300–800 words, and use fewer when the
     specification and roadmap already settle the work.
   - Keep only information the implementer needs to execute this slice:
     source-of-truth references, concrete file-oriented tasks, decisions not
     obvious from those sources, and tests unique to the change.
   - Do not copy language rules, roadmap scope, architecture guidance,
     repository instructions, conversation history, rejected alternatives,
     generic risks, standard validation commands, or follow-up work owned by the
     roadmap.
   - Use concrete bullets. Add detail only where an implementer could otherwise
     make a materially wrong choice.
   - For a series, make each plan independently executable without repeating the
     shared specification or roadmap.
8. Print the final plan paths in execution order and stop.
   - Do not review the plan locally or with a subagent.
   - Suggest one fresh `kwork` session per plan.
