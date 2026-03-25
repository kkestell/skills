# Restructure Workflow Around kinit/kstart/kend and .k/ Directory

## Goal

Replace the current ad-hoc worktree creation (inside `/kwork`) with a structured workflow where `/kstart` creates the worktree and task context up front, all mid-workflow skills read that context from `.k/current_task.json`, and `/kend` merges and cleans up. Maximize use of shell scripts over inline bash.

## Desired outcome

The new workflow:

```
0. /kinit          (once per workspace — creates .k/ directory)
1. /kstart [topic] (creates worktree + task context, opens VS Code)
2. /kbrainstorm    (optional, writes to task docs dir)
3. /kplan          (writes to task docs dir)
4. /kwork          (executes, no longer creates worktrees)
5. /kverify        (checks work)
6. /kend           (merges worktree back to main, cleans up)
```

Each mid-workflow skill (kbrainstorm, kplan, kwork, kverify, kend) embeds `.k/current_task.json` and understands the workflow context.

## Related code

- `plugins/kskills/skills/kwork/scripts/create_worktree.sh` — Current worktree creation logic; will be replaced by kstart script
- `plugins/kskills/skills/kmerge/scripts/resolve_merge_target.sh` — Merge target resolution; basis for kend script
- `plugins/kskills/skills/kmerge/SKILL.md` — Current merge skill; replaced by kend
- `plugins/kskills/skills/kwork/SKILL.md` — Currently creates worktrees; needs worktree creation removed
- `plugins/kskills/skills/kbrainstorm/SKILL.md` — Writes to `docs/internal/brainstorms/`; needs to write to task docs dir
- `plugins/kskills/skills/kplan/SKILL.md` — Writes to `docs/internal/plans/`; needs to write to task docs dir
- `plugins/kskills/skills/kverify/SKILL.md` — References `.worktrees/` conventions; needs `.k/current_task.json` context
- `plugins/kskills/skills/kverify/scripts/find_intent_docs.sh` — Finds plan/brainstorm in `docs/internal/`; needs update for `.k/tasks/`

## Current state

- Worktrees are created by `/kwork` under `<repo_root>/.worktrees/<timestamp>-<slug>`
- Feature branches follow `feature/<timestamp>-<slug>` pattern
- Brainstorm docs go to `docs/internal/brainstorms/`, plans to `docs/internal/plans/`
- No `.k/` directory convention exists
- No `current_task.json` context file exists
- `/kmerge` handles merge; no `/kend` or `/kstart` or `/kinit` exist
- Skills don't know they're running in a worktree — they discover it ad-hoc

## Constraints

- Scripts must handle all heavy lifting (user preference: scripts over inline bash)
- The `!` backtick syntax embeds shell command output in SKILL.md (e.g., `` !`cat .k/current_task.json` ``)
- `.k/current_task.json` must be gitignored (it's worktree-local context)
- Worktrees are sibling directories, not subdirectories (e.g., `~/src/ur-worktree-lua-extensions`)
- `/kinit` is run once per workspace; must be idempotent
- `/kstart` must open VS Code and instruct user to start a new session there
- Existing skills (`kcommit`, `krust`, `kdeslop`) are unchanged
- `kstart` must verify clean working directory before proceeding

## Approach

### Directory and file conventions

- `.k/` — created by `/kinit`, committed to repo
- `.k/tasks/` — empty dir, committed
- `.k/.gitignore` — contains `current_task.json`, committed
- `.k/current_task.json` — written by `/kstart` into the new worktree, gitignored
- `.k/tasks/<YYYYMMDDHHMMSS>-<slug>/` — task docs directory, created in worktree by `/kstart`

### current_task.json schema

```json
{
  "task_id": "20260325165023-lua-extensions",
  "original_repo_path": "/Users/kyle/src/ur",
  "docs_path": ".k/tasks/20260325165023-lua-extensions/"
}
```

### Worktree naming

Worktrees go in a sibling directory: `<workspace-parent>/<workspace-name>-worktree-<slug>`.

Branch naming stays `feature/<timestamp>-<slug>`.

### Skill embedding pattern

Each mid-workflow skill includes this block near the top:

```markdown
## Workflow Context

This skill is part of a structured workflow: kinit -> kstart -> kbrainstorm -> kplan -> kwork -> kverify -> kend.
You are currently in the **kplan** step. You are working in a git worktree, not the original repository.

### Current Task
!`cat .k/current_task.json 2>/dev/null || echo '{"error": "No current task. Run /kstart first."}'`
```

This tells the agent where it is in the flow, that it's in a worktree, and provides the task context.

### Key tradeoffs

- Sibling worktrees (vs subdirectories): cleaner separation, but requires absolute path in `current_task.json` to find original repo
- `.k/` committed to repo: slightly opinionated, but necessary for task docs to survive merge
- `current_task.json` gitignored: each worktree has its own, won't conflict

## Implementation plan

### New skills and scripts

- [x] **1. Create `kinit` skill and script**
  - `plugins/kskills/skills/kinit/SKILL.md` — Minimal skill that runs the init script, then asks about committing
  - `plugins/kskills/skills/kinit/scripts/kinit.sh` — Creates `.k/`, `.k/tasks/`, `.k/.gitignore` (with `current_task.json` entry). Idempotent (no error if already exists)
  - `plugins/kskills/skills/kinit/agents/openai.yaml`

- [x] **2. Create `kstart` skill and script**
  - `plugins/kskills/skills/kstart/SKILL.md` — If no argument, asks user for task description, then slugifies. Calls script. Tells user to open new session.
  - `plugins/kskills/skills/kstart/scripts/kstart.sh <task-slug>` — Verifies clean working directory, creates worktree at sibling path, creates `.k/tasks/<timestamp>-<slug>/`, writes `.k/current_task.json` in worktree, runs `code <worktree-path>`
  - `plugins/kskills/skills/kstart/agents/openai.yaml`

- [x] **3. Create `kend` skill and script (replaces kmerge)**
  - `plugins/kskills/skills/kend/SKILL.md` — Reads `current_task.json`, runs merge script, cleans up
  - `plugins/kskills/skills/kend/scripts/kend.sh` — Reads `current_task.json`, checks both worktree and original are clean, merges branch into main in original repo, removes worktree, deletes branch
  - `plugins/kskills/skills/kend/agents/openai.yaml`

### Modified skills

- [x] **4. Update `kbrainstorm`**
  - Add workflow context block with embedded `current_task.json`
  - Change output path from `docs/internal/brainstorms/<timestamp>-<slug>-brainstorm.md` to `<docs_path>/brainstorm.md` (read `docs_path` from current_task.json)
  - Remove timestamp generation (task already has a timestamp from kstart)

- [x] **5. Update `kplan`**
  - Add workflow context block with embedded `current_task.json`
  - Change output path from `docs/internal/plans/<timestamp>-<slug>-plan.md` to `<docs_path>/plan.md`
  - Remove timestamp generation
  - Update "Carry Forward Related Docs" to reference brainstorm at `<docs_path>/brainstorm.md`

- [x] **6. Update `kwork`**
  - Add workflow context block with embedded `current_task.json`
  - Remove Phase 1 Step 2 (checkpoint and create worktree) — this is now done by `/kstart`
  - Remove reference to `create_worktree.sh` script
  - Update plan path references to read from `docs_path`
  - Update Phase 4 to reference `/kend` instead of `/kmerge`
  - Simplify: agent is already in the worktree, just needs to read plan and execute

- [x] **7. Update `kverify`**
  - Add workflow context block with embedded `current_task.json`
  - Remove worktree discovery logic (it's in the current task context)
  - Use `original_repo_path` from context for `main` comparisons
  - Update intent doc search to look in `docs_path` from `current_task.json`
  - Update merge handoff to reference `/kend` instead of `/kmerge`

- [x] **8. Update `find_intent_docs.sh` for kverify**
  - Update to search `.k/tasks/` instead of `docs/internal/plans/` and `docs/internal/brainstorms/`
  - Accept task docs path as input parameter

### Cleanup

- [x] **9. Remove `kmerge` skill** — replaced by `kend`
  - Delete `plugins/kskills/skills/kmerge/` entirely

- [x] **10. Remove old `create_worktree.sh` from kwork** — replaced by `kstart.sh`
  - Delete `plugins/kskills/skills/kwork/scripts/create_worktree.sh`
  - Remove `plugins/kskills/skills/kwork/scripts/` directory if empty

- [x] **11. Update `plugin.json`** — if skill names are registered there (check if needed)

- [x] **12. Update `README.md`**
  - Update skill table to include `kinit`, `kstart`, `kend`; remove `kmerge`
  - Update workflow documentation and output table
  - Update install/usage sections

### Agent configs

- [x] **13. Create `openai.yaml` for kinit, kstart, kend**
  - Follow existing pattern: display_name, short_description, default_prompt, allow_implicit_invocation: false

## Validation

- Manual walkthrough: run `/kinit`, `/kstart test-task`, verify directory structure and `current_task.json`
- Verify `.k/.gitignore` correctly ignores `current_task.json`
- Verify worktree is created at correct sibling path
- Verify VS Code opens the worktree
- Verify each modified skill correctly embeds and reads `current_task.json`
- Verify `/kend` merges and cleans up correctly
- Verify brainstorm/plan docs are written to `.k/tasks/<task-id>/`

## Risks and follow-up

- Risk: Existing repos using old `docs/internal/` and `.worktrees/` conventions will need migration or dual support. Decision: clean break — old convention is gone. Users with in-flight work should finish with old workflow first.
- Risk: `code <path>` command may not be available if VS Code shell integration isn't installed. The script should check for it and provide a helpful error.
- Follow-up: Consider whether `kcommit` needs workflow context (probably not — it's generic).
- Follow-up: Consider whether `.k/tasks/` docs should be excluded from `/kdeslop` audit targets (like `docs/internal/` currently is in `list_audit_targets.sh`).
