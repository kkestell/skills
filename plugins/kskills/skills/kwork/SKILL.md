---
name: kwork
description: Execute a repo plan in a dedicated worktree branched from `main`. Use after `/kplan`, ideally in a fresh or compacted chat session, to implement the plan, test continuously, update plan checkboxes, commit logical chunks, and prepare a merge-ready branch.
argument-hint: "[plan file, specification, or todo file path]"
disable-model-invocation: true
---

# Work Plan Execution

Execute a work plan systematically. The focus is on shipping complete features: understand requirements, follow existing patterns, maintain quality throughout.

## Input Document

<input_document> $ARGUMENTS </input_document>

All `/kwork` execution uses dedicated worktrees under `<repo_root>/.worktrees/` on `feature/<timestamp>-<topic-slug>` branches from `main`.

## Phase 1: Quick Start

### 1. Read Plan and Clarify

Read the work document completely, including any references or links. If anything is unclear, ask clarifying questions now — better to ask than build the wrong thing. Get user approval to proceed.

### 2. Checkpoint and Create Worktree

Before creating the worktree, checkpoint planning docs on `main` if needed:

- If the plan (`docs/internal/plans/`) is untracked or modified, commit it on `main`
- If the plan references a brainstorm doc (via `Related documents`), include that too if untracked or modified
- Stage only the plan/brainstorm docs; never bundle unrelated changes

Then derive a kebab-case topic slug from the plan title or filename and run `${CLAUDE_SKILL_DIR}/scripts/create_worktree.sh <topic-slug>`.

The script creates the worktree and prints `repo_root`, `branch_name`, and `worktree_path`. `cd` into the printed `worktree_path` before editing.

Confirm dependencies and project setup in the worktree. Verify tests/lint run before major edits.

### 3. Create Todo List

Use TodoWrite to break the plan into actionable tasks. Include testing tasks. Keep tasks specific and completable.

## Phase 2: Execute

All work happens in the worktree, never in the main checkout.

### Task Execution Loop

For each task in priority order:

1. Mark as in_progress in TodoWrite
2. Read referenced files and find similar patterns in the codebase
3. Implement following existing conventions
4. Write tests for new functionality
5. Run tests after changes
6. Mark as completed in TodoWrite
7. Check off the corresponding item in the plan file (`[ ]` → `[x]`)
8. If this completes a tested logical chunk, commit immediately

### Commit Early and Often

Build momentum with small, meaningful commits. Don't wait until the end.

**Commit when:** a logical unit is complete, its tests pass, and it can be described in one commit message.

**Don't commit when:** work is half-finished, tests are failing, or unrelated changes are mixed in.

Each commit follows `/kcommit` discipline: run quality checks, stage deliberately (never `git add .`), write a message using the 7 rules.

### Follow Existing Patterns

The plan template includes a `Related code` section — read those files first. Match naming conventions. Reuse existing components. Check CLAUDE.md for project standards.

### Test Continuously

Run relevant tests after each significant change. Fix failures immediately. Don't wait until the end.

## Phase 3: Quality Check

Run the full suite before handoff: tests, lint, formatter, type checks. Use CLAUDE.md for project-specific commands.

## Phase 4: Ship It

1. Commit any remaining tested work
2. Report to the user:
   - What was completed
   - Tests and lint results
   - Commit summary
   - Worktree path and branch name
   - Any follow-up work needed
3. Ask: "Do you want me to run `/kmerge <worktree_path>` now?"

## Principles

- **Start fast** — clarify once, then execute
- **The plan is your guide** — follow its references, don't reinvent
- **Test as you go** — continuous testing prevents big surprises
- **Commit frequently** — small, tested, logical chunks
- **Ship complete features** — don't leave things 80% done
