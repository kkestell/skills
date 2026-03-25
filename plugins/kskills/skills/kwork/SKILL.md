---
name: kwork
description: Execute a repo plan systematically. Use after `/kplan` (and `/kstart`), ideally in a fresh or compacted chat session, to implement the plan, test continuously, update plan checkboxes, commit logical chunks, and prepare a merge-ready branch.
argument-hint: "[plan file, specification, or todo file path]"
disable-model-invocation: true
---

# Work Plan Execution

Execute a work plan systematically. The focus is on shipping complete features: understand requirements, follow existing patterns, maintain quality throughout.

## Workflow Context

This skill is part of a structured workflow: kinit -> kstart -> kbrainstorm -> kplan -> **kwork** -> kverify -> kend.
You are currently in the **kwork** step. You are working in a git worktree, not the original repository.

### Current Task
!`cat .k/current_task.json 2>/dev/null || echo '{"error": "No current task. Run /kstart first."}'`

## Input Document

<input_document> $ARGUMENTS </input_document>

If no input document is provided, look for a plan at `<docs_path>/plan.md` (read `docs_path` from `.k/current_task.json`).

## Phase 1: Quick Start

### 1. Read Plan and Clarify

Read the work document completely, including any references or links. If anything is unclear, ask clarifying questions now — better to ask than build the wrong thing. Get user approval to proceed.

### 2. Verify Setup

Confirm dependencies and project setup. Verify tests/lint run before major edits.

### 3. Create Todo List

Use TodoWrite to break the plan into actionable tasks. Include testing tasks. Keep tasks specific and completable.

## Phase 2: Execute

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
   - Branch name
   - Any follow-up work needed
3. Ask: "Do you want me to run `/kverify` now, or `/kend` to merge?"

## Principles

- **Start fast** — clarify once, then execute
- **The plan is your guide** — follow its references, don't reinvent
- **Test as you go** — continuous testing prevents big surprises
- **Commit frequently** — small, tested, logical chunks
- **Ship complete features** — don't leave things 80% done
