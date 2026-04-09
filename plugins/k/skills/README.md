# Agent Skills

A workflow system for structured software development with AI assistance.

## Core Workflow: `/kplan` → `/kwork`

### 1. `/kplan`

Brainstorms with you, explores the codebase, and produces a concrete implementation plan.

```text
/kplan add OAuth2 support for GitHub
```

**Output:** Creates `docs/agents/plans/YYYY-MM-DD-NNN-slug.md`

The plan includes:
- Goal and scope
- Implementation tasks with checkboxes
- Related code references
- Validation steps
- Open questions

**Tip:** Start `/kwork` in a fresh session when possible to preserve context for implementation.

### 2. `/kwork`

Implements the plan end-to-end, validates with parallel subagent review, and commits.

```text
/kwork @docs/agents/plans/2026-04-07-001-oauth-github.md
```

**Workflow:**
1. Pre-flight: Verify clean git state
2. Orientation: Read plan, verify baseline
3. Execution: Implement task-by-task, code-first then fix tests
4. Validate: Run full test suite + parallel subagent reviews (completeness + test quality)
5. Commit: Single commit with all validated work

### Handoff

If context runs low during `/kwork`, the agent will offer to run `/handoff` to continue in a fresh session without losing progress.

## Supporting Skills

### `/kreview`

Reviews code for structural violations and simplification opportunities without changing code.

- Reports hierarchy, abstraction, modularization, and encapsulation issues
- Adds a simplify lens when the request is to simplify, clean up, tidy, or polish

```text
/kreview src/auth/
```

## Plan Storage

All plans live in `docs/agents/plans/` with the naming convention:

```
YYYY-MM-DD-NNN-slug.md
│          │   │
│          │   └── Short kebab-case description (3-5 words)
│          └────── Zero-padded sequence number for that date
└───────────────── Date the plan was created
```
