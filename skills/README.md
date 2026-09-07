# Agent Skills

A workflow system for structured software development with AI assistance.

Examples below use Claude Code's `/skill-name` syntax. In Codex, invoke the same
directly installed skill as `$skill-name`.

## The Essence

These skills are meant to work together: `/kspec` defines behavior, `/kroadmap`
orders the work, and `/kwork` plans briefly in context, implements one task,
and validates the result in the same session.

- `/kspec` creates and updates the product specification by resolving behavior
  with the user one decision at a time.
- `/kroadmap` creates and updates user-directed milestones, scope, order, and
  completion gates.
- `/kwork` selects a roadmap task, reads the owning documents and relevant code,
  forms a short checklist in context, then implements and validates it. It does
  not write a plan file. Checks match the task's risk and integration boundary;
  commits require user authorization.
- `/kreview` is independent verification. It runs completeness and
  code-simplification review passes over a body of work, catching omissions,
  hacks, and unnecessary complexity that the implementer would miss. Use it once
  across a completed milestone; `/kwork` does not review individual tasks.

## Core Workflow: `/kspec` → `/kroadmap` → `/kwork`

### 1. `/kspec`

Creates or updates `docs/spec.md` through an interactive product-specification
process. It is used for changes, not ordinary reading.

```text
/kspec define how authentication failures are reported
```

### 2. `/kroadmap`

Creates or updates `eng/roadmap.md` from user-directed priorities and the
specification. It is used for changes, not ordinary reading.

```text
/kroadmap make GitHub authentication the current milestone
```

### 3. `/kwork`

Reads the required specification and roadmap, selects the requested task or the
next unimplemented task, and carries it through lightweight planning,
implementation, and validation. If a required document is missing or material
behavior is unsettled, it routes the decision through the owning skill.

```text
/kwork
/kwork add OAuth2 support for GitHub
```

**Workflow:**

1. Select one roadmap task and inspect the working tree, preserving existing work.
2. Read the owning documents and relevant code; form a short checklist in context.
3. Implement the task directly in the same session, without writing a plan file.
4. Run focused checks, with broad gates at the integrated feature or milestone
   boundary.
5. Report the result and any unfinished integration. Commit only when authorized.

## Supporting Skills

### `/kinit`

Explores a repository and bootstraps `AGENTS.md` with project orientation,
document ownership, and skill-routing rules. It does not invent or create the
project's specification, architecture, or roadmap.

```text
/kinit .
```

### `/kreview`

Runs independent completeness and code-simplification review passes over a body
of work.

```text
/kreview @eng/roadmap.md --files src/auth/github.ts,src/auth/tokens.ts,tests/auth/github.test.ts --tasks "Add GitHub OAuth2 provider","Add token refresh"
```

### `/ktask`

Handles bounded one-off work without creating a persisted implementation plan.

```text
/ktask rename the old env flag to the new config key
```

### `/khandoff`

Writes a handoff note summarizing the session — what was accomplished, what was
decided, and what a fresh agent needs to know — so the next session can pick the
work up without re-discovering it. Useful when context runs low mid-`/kwork`.

```text
/khandoff
```

### `/kskillissue`

Diagnoses a skill in this repository that steered an agent wrong, fixes the
responsible text, then commits, pushes, and reinstalls with `profiles.py`.

```text
/kskillissue kwork committed before running the review passes
```

### `/kdeslop`

Detects and fixes AI "slop" in prose. Audits the text one slop category at a
time — overused LLM vocabulary, empty significance claims, hollow rhetorical
constructions, formulaic structure, machine-formatting tells — then rewrites the
confirmed slop while preserving meaning and voice.

```text
/kdeslop @docs/overview.md
```

## Work Documents

`eng/roadmap.md` records the ordered work and completion gates. `/kwork` keeps
its implementation checklist in conversation context. Existing work documents
can be supplied as context without creating a new plan file.

Follow-up documents live in `eng/todo/`, and session handoff notes live in
`eng/handoff/`.
