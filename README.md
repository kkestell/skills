# Claude Code Skills

## Install

```bash
claude plugin marketplace add kkestell/skills
claude plugin install skills@kskills
```

Update:

```bash
claude plugin marketplace update kskills
claude plugin update kskills
```

## Skills

| Skill         | What it does                                                   |
| ------------- | -------------------------------------------------------------- |
| `kbrainstorm` | Explore a fuzzy problem before committing to a plan            |
| `kplan`       | Write a concrete plan from an idea, bug report, or brainstorm  |
| `kwork`       | Build the plan in a worktree off `main`                        |
| `kverify`     | Check the work against the plan                                |
| `kmerge`      | Merge the worktree back to `main`                              |
| `kcommit`     | Clean, deliberate commits                                      |
| `krust`       | Rust-specific guidelines (required before editing `.rs` files) |

## Usage

Each phase gets its own session. Brainstorm is optional; plan, work, verify, and merge should be run in order.

```
/kbrainstorm <description>
/kplan <@brainstorm | description>
/kwork <@plan>
/kverify <worktree>
/kmerge <worktree>
```

## Output

| Skill          | Writes to                    |
| -------------- | ---------------------------- |
| `/kbrainstorm` | `docs/internal/brainstorms/` |
| `/kplan`       | `docs/internal/plans/`       |
| `/kwork`       | `.worktrees/`                |

Worktrees branch off `main`; `/kverify` and `/kmerge` operate on them.
