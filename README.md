# k Workflow Plugin for Claude Code

`k` is a structured workflow plugin for longer-lived coding work. It gives Claude a task lifecycle (`init`, `start-task`, `brainstorm`, `plan`, `work`, `verify`, `end-task`) plus supporting skills for research, commit hygiene, doc review, and language-specific guidance.

Task state lives under `.k/`, including:

- `.k/current_task.json`
- `.k/tasks/<task_id>/brainstorm.md`
- `.k/tasks/<task_id>/plan.md`
- `.k/tasks/<task_id>/research/*.md`

## Install

```bash
claude plugin marketplace add kkestell/skills
claude plugin install k@kkestell
```

Update:

```bash
claude plugin marketplace update kkestell
claude plugin update k@kkestell
```

Uninstall:

```bash
claude plugin uninstall k@kkestell
claude plugin marketplace remove kkestell
```

## Workflow Skills

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

## Supporting Skills

| Skill       | What it does                                                   |
| ----------- | -------------------------------------------------------------- |
| `commit`     | Clean, deliberate commits                                      |
| `deslop`     | Audit user-facing docs for AI slop                             |
| `go-lang`    | Go-specific guidelines (required before editing `.go` files)   |
| `rust-lang`  | Rust-specific guidelines (required before editing `.rs` files) |

## Usage

Run `init` once per repo, then use `start-task` to choose whether the task should run in a sibling worktree or in-place on a task branch. `brainstorm` is optional; `research` can be used from `brainstorm`, `plan`, or `work` whenever the task needs evidence.

Claude currently exposes these as plain slash commands like `/init` and `/start-task`, with `(k)` shown in the picker. `/k:init` is not a valid invocation.

```
/init
/start-task <topic>    # asks whether to create a worktree
# -- if you chose a worktree, continue in the new Claude terminal session there --
/brainstorm <description>
/research <topic>      # optional, repeat during brainstorm/plan/work
/plan <@brainstorm | description>
/work <@plan>
/verify
/end-task
```

Use `/commit` during `/work` whenever a tested logical chunk is ready to checkpoint.

## Workflow Notes

- `start-task` can create either a sibling worktree or an in-place task branch.
- In worktree mode, the script tries to open Claude in a terminal rooted at that worktree.
- On macOS, terminal auto-launch currently supports iTerm2.
- On Linux, terminal auto-launch uses `xdg-terminal-exec`, then `x-terminal-emulator`, then `xterm`.
- If auto-launch is unavailable, the script falls back to a manual `cd <worktree> && claude` instruction.
- `end-task` retains a separate worktree after merging so post-merge validation can still run cleanly on `main`.
- Supporting skills like `/commit`, `/deslop`, `/go-lang`, and `/rust-lang` are usually invoked from `/work` or `/verify`, not used as the main workflow spine.


## Skill Matrix

| Skill | Reads | Writes / effects | Runs / uses | Invokes / hands off |
| ----- | ----- | ---------------- | ----------- | ------------------- |
| `/init` | repo root | `.k/tasks/`, `.k/.gitignore`, `.k/tasks/.gitkeep` | `init/scripts/init.sh` | optional `/commit` for new `.k/` |
| `/start-task` | task description, `.k/`, worktree preference | optional sibling worktree, feature branch, `.k/current_task.json`, `.k/tasks/<task_id>/` | `start-task/scripts/start-task.sh` | current session or new Claude terminal session, then `/brainstorm`, `/plan`, or `/work` |
| `/brainstorm` | `.k/current_task.json`, feature description, `CLAUDE.md`, similar repo code, optional `research/*.md` | `<docs_path>/brainstorm.md` | `brainstorm/assets/brainstorm-template.md` | `/research`, loops on itself, or proceeds to `/plan` |
| `/research` | `.k/current_task.json`, one research topic, repo code, local docs, optional web sources | `<docs_path>/research/<topic-slug>.md` | `research/assets/research-template.md` | reused by `/brainstorm`, `/plan`, and `/work` |
| `/plan` | `.k/current_task.json`, feature description, `CLAUDE.md`, similar code, issues, PRs, optional `brainstorm.md`, optional `research/*.md`, optional external docs | `<docs_path>/plan.md` | `plan/assets/plan-template.md` | `/research`, then `/work` |
| `/work` | `.k/current_task.json`, input doc or `plan.md`, linked references, optional `research/*.md`, `CLAUDE.md` | code, tests, config, docs, plan checkboxes, todo state | repo quality commands | `/research`, `/commit`, `/go-lang`, `/rust-lang`, then `/verify` or `/end-task` |
| `/verify` | `.k/current_task.json`, plan/brainstorm, `git status`, `git log main..HEAD`, `git diff main...HEAD`, `CLAUDE.md` | verification report to the user | `verify/scripts/find_intent_docs.sh`, `verify/assets/verification-report-template.md` | `/rust-lang`, `/deslop`, back to `/work`, `/commit`, or onward to `/end-task` |
| `/end-task` | `.k/current_task.json`, original repo `main` when using a worktree, `CLAUDE.md` | merge to `main`, retain optional worktree for post-merge validation, delete branch only when safe | `end-task/scripts/end-task.sh` | none |
| `/commit` | `CLAUDE.md`, `git status`, `git diff`, `git diff --staged` | checkpoint commit on the feature branch | repo quality commands | none |
| `/deslop` | audit target(s), user-facing docs | audit findings reported to the user | repo markdown scan, `deslop/references/slop_tells.md`, `deslop/assets/audit-report-template.md` | usually from `/verify` |
| `/go-lang` | relevant `.go` files | none | relevant guidance files under `go-lang/resources/` | usually from `/work` |
| `/rust-lang` | relevant `.rs` files | optional compliance comment in Rust files | relevant guidance files under `rust-lang/resources/` | from `/work` and `/verify` |

## Files Written

| Command | Main files written |
| ------- | ------------------ |
| `/init` | `.k/`, `.k/tasks/`, `.k/.gitignore`, `.k/tasks/.gitkeep` |
| `/start-task` | optional sibling worktree, `.k/current_task.json`, `.k/tasks/<task_id>/` |
| `/brainstorm` | `.k/tasks/<task_id>/brainstorm.md` |
| `/research` | `.k/tasks/<task_id>/research/<topic-slug>.md` |
| `/plan` | `.k/tasks/<task_id>/plan.md` |
| `/work` | code/tests/config/docs as needed, plus plan checkbox updates |
| `/end-task` | merges into `main`, retains any optional worktree for post-merge validation, deletes branch only when safe |
