# Agent Skills

A workflow system for structured software development with AI assistance.

Examples below use Claude Code's `/skill-name` syntax. In Codex, invoke the same
directly installed skill as `$skill-name`.

## The Essence

These skills are meant to work together: `/kplan` decides what the right change
is, and `/kwork` carries it through to a finished result.

- `/kplan` is design-first thinking. Its job is not to rush into implementation,
  but to clarify the real problem, explore how the change fits the architecture,
  research unknowns when needed, and write a plan another session can execute
  cleanly. Use it when the request is fuzzy, the design matters, or you want to
  avoid coding your way into a mess.
- `/kwork` is disciplined execution. It takes a concrete plan, starts from a
  clean repo, implements the work end-to-end, validates it, delegates review to
  `/kreview`, and commits once the whole thing is genuinely done. Use it when
  you want more than a patch and are aiming to ship a complete, verified slice
  of work.
- `/kreview` is independent verification. It runs completeness and
  code-simplification review passes over a body of work, catching omissions,
  hacks, and unnecessary complexity that the implementer would miss. Called
  automatically by `/kwork`, but can also be invoked standalone.

## Core Workflow: `/kplan` → `/kwork`

### 1. `/kplan`

Brainstorms with you, explores the codebase, and produces a concrete
implementation plan.

```text
/kplan add OAuth2 support for GitHub
```

**Output:** Creates `eng/plans/YYYY-MM-DD-NNN-slug.md` in the repository.

The plan includes:

- Goal and scope
- Implementation tasks
- Related code references
- Validation steps
- Open questions

**Tip:** Start `/kwork` in a fresh session when possible to preserve context for
implementation.

### 2. `/kwork`

Implements the plan end-to-end, validates with parallel subagent review, and
commits.

```text
/kwork @eng/plans/2026-04-07-001-oauth-github.md
```

**Workflow:**

1. Pre-flight: Verify clean git state
2. Orientation: Read plan, build the task list
3. Execution: Implement task-by-task, code-first then fix tests
4. Validate: Run full test suite + `/kreview` for parallel subagent reviews
   (completeness + code simplification)
5. Commit: Single commit with all validated work

## Supporting Skills

### `/kinit`

Explores a repo and bootstraps `AGENTS.md` so future sessions have a shared
orientation doc.

```text
/kinit .
```

### `/kreview`

Runs independent completeness and code-simplification review passes over a body
of work.

```text
/kreview @eng/plans/2026-04-07-001-oauth-github.md --files src/auth/github.ts,src/auth/tokens.ts,tests/auth/github.test.ts --tasks "Add GitHub OAuth2 provider","Add token refresh"
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

## Plan Storage

Generated docs live under `eng/` at the repository root:

- `eng/plans/` for implementation plans
- `eng/todo/` for follow-up docs
- `eng/handoff/` for session handoff notes

`eng/` is tracked in git and committed alongside the code it describes.

Plan files use the naming convention:

```
YYYY-MM-DD-NNN-slug.md
│          │   │
│          │   └── Short kebab-case description (3-5 words)
│          └────── Zero-padded sequence number for that date
└───────────────── Date the plan was created
```
