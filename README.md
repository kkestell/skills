# Claude Code Skills

## Install

```bash
claude plugin marketplace add kkestell/skills
claude plugin install kskills@kskills
```

Update:

```bash
claude plugin marketplace update kskills
claude plugin update kskills
```

## Skills

| Skill        | What it does                                                   |
| ------------ | -------------------------------------------------------------- |
| `kinit`      | Initialize `.k/` directory (once per workspace)                |
| `kstart`     | Create a worktree and task context for new work                |
| `kbrainstorm`| Explore a fuzzy problem before committing to a plan            |
| `kplan`      | Write a concrete plan from an idea, bug report, or brainstorm  |
| `kwork`      | Execute the plan in the worktree                               |
| `kverify`    | Check the work against the plan                                |
| `kend`       | Merge the worktree back to `main` and clean up                 |
| `kcommit`    | Clean, deliberate commits                                      |
| `krust`      | Rust-specific guidelines (required before editing `.rs` files) |

## Usage

Each phase gets its own session. `kinit` is run once per workspace. `kstart` creates the worktree; brainstorm is optional; plan, work, verify, and end should be run in order within the worktree.

```
/kinit
/kstart <topic>           # creates worktree, opens VS Code
# -- new session in worktree --
/kbrainstorm <description>
/kplan <@brainstorm | description>
/kwork <@plan>
/kverify
/kend
```

## Output

| Skill          | Writes to                              |
| -------------- | -------------------------------------- |
| `/kinit`       | `.k/`, `.k/tasks/`, `.k/.gitignore`   |
| `/kstart`      | Sibling worktree, `.k/current_task.json`, `.k/tasks/<task-id>/` |
| `/kbrainstorm` | `.k/tasks/<task-id>/brainstorm.md`     |
| `/kplan`       | `.k/tasks/<task-id>/plan.md`           |

Worktrees branch off `main`; `/kverify` and `/kend` operate on them.
