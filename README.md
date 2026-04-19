# Agent Skills

A workflow system for structured software development with AI assistance.

## Install

Distributed as a Claude Code plugin via the `kkestell` marketplace. From inside Claude Code:

```text
/plugin marketplace add kkestell/skills
/plugin install k@kkestell
```

The first command registers the marketplace; the second installs the `k` plugin, which provides the `/kplan`, `/kwork`, `/kinit`, `/ktask`, `/kcommit`, and `/khandoff` commands.

To update later, run `/plugin marketplace update kkestell` followed by `/plugin install k@kkestell`.

## The Essence

These skills are meant to work together: `/kplan` decides what the right change is, and `/kwork` carries it through to a finished result.

- `/kplan` is design-first thinking. Its job is not to rush into implementation, but to clarify the real problem, explore how the change fits the architecture, research unknowns when needed, and write a plan another session can execute cleanly. Use it when the request is fuzzy, the design matters, or you want to avoid coding your way into a mess.
- `/kwork` is disciplined execution. It takes a concrete plan, starts from a clean repo, implements the work end-to-end, validates it, runs independent review passes, and commits once the whole thing is genuinely done. Use it when you want more than a patch and are aiming to ship a complete, verified slice of work.

## Core Workflow: `/kplan` → `/kwork`

### 1. `/kplan`

Brainstorms with you, explores the codebase, and produces a concrete implementation plan.

```text
/kplan add OAuth2 support for GitHub
```

**Output:** Creates `~/.k/workspaces/<repo-id>/plans/YYYY-MM-DD-NNN-slug.md`

The plan includes:
- Goal and scope
- Implementation tasks
- Related code references
- Validation steps
- Open questions

**Tip:** Start `/kwork` in a fresh session when possible to preserve context for implementation.

### 2. `/kwork`

Implements the plan end-to-end, validates with parallel subagent review, and commits.

```text
/kwork @~/.k/workspaces/<repo-id>/plans/2026-04-07-001-oauth-github.md
```

**Workflow:**
1. Pre-flight: Verify clean git state
2. Orientation: Read plan, verify baseline
3. Execution: Implement task-by-task, code-first then fix tests
4. Validate: Run full test suite + parallel subagent reviews (completeness + test quality)
5. Commit: Single commit with all validated work

### Handoff

If context runs low during `/kwork`, the agent can run `/khandoff` to capture the current state in a fresh-session-friendly handoff document.

## Supporting Skills

### `/kinit`

Explores a repo and bootstraps `AGENTS.md` so future sessions have a shared orientation doc.

```text
/kinit .
```

### `/ktask`

Handles bounded one-off work without creating a persisted implementation plan.

```text
/ktask rename the old env flag to the new config key
```

## Plan Storage

Generated docs live under `~/.k/workspaces/<repo-id>/`:

- `plans/` for implementation plans
- `todo/` for follow-up docs
- `handoff/` for session handoffs

Plan files use the naming convention:

```
YYYY-MM-DD-NNN-slug.md
│          │   │
│          │   └── Short kebab-case description (3-5 words)
│          └────── Zero-padded sequence number for that date
└───────────────── Date the plan was created
```

## Commands

### `/kcommit`

Stages and commits outstanding work after screening for secrets, junk files, and accidental artifacts.

### `/khandoff`

Writes a handoff note into `~/.k/workspaces/<repo-id>/handoff/` so another session can continue cleanly.
