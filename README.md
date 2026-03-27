# Claude Code Skills

## Install

```bash
claude plugin marketplace add kkestell/skills
claude plugin install k@k
```

Update:

```bash
claude plugin marketplace update k
claude plugin update k@k
```

## Skills

| Skill        | What it does                                                   |
| ------------ | -------------------------------------------------------------- |
| `init`       | Initialize `.k/` directory (once per repo)                     |
| `start-task` | Create a task branch and task context for new work             |
| `brainstorm` | Explore a fuzzy problem before committing to a plan            |
| `research`   | Research one topic and save a reusable task note               |
| `plan`       | Write a concrete plan from an idea, bug report, or brainstorm  |
| `work`       | Execute the plan on the active task branch                     |
| `verify`     | Check the work against the plan                                |
| `end-task`   | Merge the task branch back to `main`                           |
| `commit`     | Clean, deliberate commits                                      |
| `deslop`     | Audit user-facing docs for AI slop                             |
| `go-lang`    | Go-specific guidelines (required before editing `.go` files)   |
| `rust-lang`  | Rust-specific guidelines (required before editing `.rs` files) |

## Usage

Each phase gets its own session when you use a separate workspace. `init` is run once per repo. `start-task` now asks whether to create a sibling worktree or work in place on a task branch, and in workspace mode it will try to open Claude in a terminal rooted at that worktree. Brainstorm is optional; plan, work, verify, and end-task should then be run in that chosen task repo.

```
/k:init
/k:start-task <topic>    # asks whether to create a workspace
# -- if you chose a workspace, continue in the new Claude terminal session there --
/k:brainstorm <description>
/k:research <topic>      # optional, repeat during brainstorm/plan/work
/k:plan <@brainstorm | description>
/k:work <@plan>
/k:verify
/k:end-task
```


## Skill Matrix

| Skill | Reads | Writes / effects | Runs / uses | Invokes / hands off |
| ----- | ----- | ---------------- | ----------- | ------------------- |
| `/k:init` | repo root | `.k/tasks/`, `.k/.gitignore`, `.k/tasks/.gitkeep` | `init/scripts/init.sh` | optional `/k:commit` for new `.k/` |
| `/k:start-task` | task description, `.k/`, workspace preference | optional sibling worktree, feature branch, `.k/current_task.json`, `.k/tasks/<task_id>/` | `start-task/scripts/start-task.sh` | current session or new Claude terminal session, then `/k:brainstorm`, `/k:plan`, or `/k:work` |
| `/k:brainstorm` | `.k/current_task.json`, feature description, `CLAUDE.md`, similar repo code, optional `research/*.md` | `<docs_path>/brainstorm.md` | `brainstorm/assets/brainstorm-template.md` | `/k:research`, loops on itself, or proceeds to `/k:plan` |
| `/k:research` | `.k/current_task.json`, one research topic, repo code, local docs, optional web sources | `<docs_path>/research/<topic-slug>.md` | `research/assets/research-template.md` | reused by `/k:brainstorm`, `/k:plan`, and `/k:work` |
| `/k:plan` | `.k/current_task.json`, feature description, `CLAUDE.md`, similar code, issues, PRs, optional `brainstorm.md`, optional `research/*.md`, optional external docs | `<docs_path>/plan.md` | `plan/assets/plan-template.md` | `/k:research`, then `/k:work` |
| `/k:work` | `.k/current_task.json`, input doc or `plan.md`, linked references, optional `research/*.md`, `CLAUDE.md` | code, tests, config, docs, plan checkboxes, todo state | repo quality commands | `/k:research`, `/k:commit`, `/k:go-lang`, `/k:rust-lang`, then `/k:verify` or `/k:end-task` |
| `/k:verify` | `.k/current_task.json`, plan/brainstorm, `git status`, `git log main..HEAD`, `git diff main...HEAD`, `CLAUDE.md` | verification report to the user | `verify/scripts/find_intent_docs.sh`, `verify/assets/verification-report-template.md` | `/k:rust-lang`, `/k:deslop`, back to `/k:work`, `/k:commit`, or onward to `/k:end-task` |
| `/k:end-task` | `.k/current_task.json`, original repo `main` when using a workspace, `CLAUDE.md` | merge to `main`, retain optional workspace for post-merge validation, delete branch only when safe | `end-task/scripts/end-task.sh` | none |
| `/k:commit` | `CLAUDE.md`, `git status`, `git diff`, `git diff --staged` | checkpoint commit on the feature branch | repo quality commands | none |
| `/k:deslop` | audit target(s), user-facing docs | audit findings reported to the user | repo markdown scan, `deslop/references/slop_tells.md`, `deslop/assets/audit-report-template.md` | usually from `/k:verify` |
| `/k:go-lang` | relevant `.go` files | none | relevant guidance files under `go-lang/resources/` | usually from `/k:work` |
| `/k:rust-lang` | relevant `.rs` files | optional compliance comment in Rust files | relevant guidance files under `rust-lang/resources/` | from `/k:work` and `/k:verify` |

## Files Written

| Command | Main files written |
| ------- | ------------------ |
| `/k:init` | `.k/`, `.k/tasks/`, `.k/.gitignore`, `.k/tasks/.gitkeep` |
| `/k:start-task` | optional sibling worktree, `.k/current_task.json`, `.k/tasks/<task_id>/` |
| `/k:brainstorm` | `.k/tasks/<task_id>/brainstorm.md` |
| `/k:research` | `.k/tasks/<task_id>/research/<topic-slug>.md` |
| `/k:plan` | `.k/tasks/<task_id>/plan.md` |
| `/k:work` | code/tests/config/docs as needed, plus plan checkbox updates |
| `/k:end-task` | merges into `main`, retains any optional workspace for post-merge validation, deletes branch only when safe |
