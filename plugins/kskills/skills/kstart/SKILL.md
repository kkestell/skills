---
name: kstart
description: Create a worktree and task context for a new piece of work. Sets up the `.k/current_task.json` context file and opens VS Code in the new worktree. Use after `/kinit`, before `/kbrainstorm` or `/kplan`.
argument-hint: "[task description or topic slug]"
disable-model-invocation: true
---

# Start a New Task

Create a dedicated worktree and task context for a new piece of work.

## Input

<task_description> $ARGUMENTS </task_description>

If the task description is empty, ask the user what they're working on. Do not proceed without one.

## Step 1: Derive Slug

Convert the task description into a kebab-case slug (3-5 words, lowercase, hyphens only). If the input is already a valid kebab-case slug, use it directly.

## Step 2: Verify Prerequisites

Check that `.k/` exists. If not, tell the user to run `/kinit` first and stop.

## Step 3: Create Worktree

Run the kstart script:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/kstart.sh" <task-slug>
```

The script will:
- Verify a clean working directory
- Create the worktree at a sibling directory
- Create the task docs directory under `.k/tasks/`
- Write `.k/current_task.json` in the worktree
- Open VS Code in the worktree

## Step 4: Handoff

Tell the user:

1. VS Code is opening in the new worktree
2. They should **start a new Claude Code session** in that VS Code window
3. From there, they can run `/kbrainstorm`, `/kplan`, or `/kwork`

Report the worktree path, branch name, and task docs directory.
