# k-Skills Workflow

These skills are a simple workflow for longer-lived coding work. The point is to keep each phase focused: explore the problem, write down the plan, do the work in isolation, verify it against the plan, then merge it cleanly.

The core ideas are straightforward. Use different contexts for different kinds of thinking. Write important decisions down instead of keeping them in chat history. Do code work in a worktree, not on `main`. Commit in small pieces. Verify against intent, not just whether tests happen to pass.

## Main Flow

| Skill | Use it for | Main output |
| --- | --- | --- |
| `kbrainstorm` | Optional. Figure out what to build when the problem is still fuzzy. | Brainstorm doc |
| `kplan` | Turn an idea or bug report into a concrete plan. | Plan doc |
| `kwork` | Execute the plan in a dedicated worktree. | Feature branch + commits |
| `kverify` | Check the work against the plan and run the quality gate. | Verification report |
| `kmerge` | Merge a clean, verified worktree back to `main`. | Merged change |

Typical path:

```text
(Optional) Brainstorm -> Plan -> Work -> Verify -> Merge
```

## Ground Rules

- Use a fresh session for `kbrainstorm`, `kplan`, and `kwork`.
- Keep planning docs on `main`.
- Do implementation in a dedicated worktree under `.worktrees/`.
- Skip phases that do not add value. If the work is already clear, start at `kplan` or `kwork`.
- Prefer existing repo patterns over inventing new ones.
- Test as you go.

## Supporting Skills

- `kcommit`: helps make clean, deliberate commits
- `krust`: required before editing any Rust code

Specialist skills exist for focused domains such as APIs, architecture, Kubernetes, WebSockets, pytest, and simplification work. Use them when the problem actually needs them.

## Example

Explore the problem if needed:

```
/kbrainstorm I'd like to add a user onboarding flow
```

```
# 2. In a fresh session, write the plan from the brainstorm doc
/kplan @THE_BRAINSTORM_FILENAME

# 3. In a fresh session, build from the plan
/kwork @THE_PLAN_FILENAME

# 4. Verify
/kverify .worktrees/2026-03-24-16-00-00-user-onboarding

# 5. Merge
/kmerge .worktrees/2026-03-24-16-00-00-user-onboarding
```
