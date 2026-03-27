---
name: start-task
description: Create a task branch plus `.k/current_task.json` context for new work, optionally in a separate worktree. Use after `/k:init`, before `/k:brainstorm`, `/k:plan`, or `/k:work`.
argument-hint: "[task description or topic slug]"
disable-model-invocation: true
---

## Workflow

1. Read `<task_description> $ARGUMENTS </task_description>`.
   - If it is empty, ask what the user is working on and stop.
2. Derive a 3-5 word kebab-case slug.
   - If the input is already a valid slug, use it directly.
3. Verify prerequisites.
   - Check that `.k/` exists; otherwise tell the user to run `/k:init` first.
4. Choose the worktree mode.
   - If the user has not already made their preference clear, ask whether they want a separate worktree or to work in place on a branch in the current repo.
   - The goal here is not to start implementation. It is to establish clean task context and the right worktree shape.
   - Separate worktrees are useful when isolation matters; in-place mode is fine when the user wants to stay in the current repo session.
5. Run `bash "${CLAUDE_SKILL_DIR}/scripts/start-task.sh" <task-slug> <worktree|in-place>`.
   - Treat the script as responsible for repo cleanliness checks, branch creation, worktree creation when needed, task docs setup, `.k/current_task.json`, and terminal handoff only for the separate worktree flow.
6. Capture and report `branch_name`, `mode`, `worktree_path`, and `docs_path` from script output.
   - Report the resulting paths clearly so the next skill invocation has the right context immediately.
7. Hand off to the right session.
   - If `mode=worktree`, tell the user Claude should open in a new terminal session rooted in the worktree. On macOS this is currently iTerm2-only; on Linux it uses terminal-launcher detection and falls back to a manual instruction if needed.
   - Worktree mode should hand the user directly into a terminal that is already in the worktree and ready to run Claude.
   - If `mode=in-place`, tell the user they can continue in the current session.
   - From that session, continue with `/k:brainstorm`, `/k:plan`, or `/k:work`.
