---
name: kverify
description: Verify completed implementation work against its plan or brainstorm, run the repo's relevant quality checks, invoke language-specific skills when needed, and confirm the branch is clean before `/kend`. Use near the end of `/kwork` before merging.
argument-hint: "[plan path or verification target]"
disable-model-invocation: true
---

# Verify Work Before Merge

Run near the end of `/kwork`, after implementation and before `/kend`. Verify merge readiness, alignment with the plan or brainstorm, and worktree cleanliness.

Do not make product changes during verification unless the user explicitly asks.

## Workflow Context

This skill is part of a structured workflow: kinit -> kstart -> kbrainstorm -> kplan -> kwork -> **kverify** -> kend.
You are currently in the **kverify** step. You are working in a git worktree, not the original repository.

### Current Task
!`cat .k/current_task.json 2>/dev/null || echo '{"error": "No current task. Run /kstart first."}'`

## Inputs

<verification_target> $ARGUMENTS </verification_target>

### Resolve target

Read `.k/current_task.json` to get `original_repo_path` and `docs_path`. Use `original_repo_path` as the reference for `main` comparisons.

Confirm the worktree is clean (`git status --short`). If dirty, ask about running `/kcommit` first.

## Phase 1: Find the Plan and Brainstorm

Use `${CLAUDE_SKILL_DIR}/scripts/find_intent_docs.sh` to surface candidate plan and brainstorm files. The script accepts the task docs path from `current_task.json`.

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/find_intent_docs.sh" "<docs_path>"
```

If it cannot resolve confidently, ask the user.

Look for:
1. `<docs_path>/plan.md`
2. `<docs_path>/brainstorm.md`
3. Any path the user provided as input

## Phase 2: Build Verification Context

Read the plan and brainstorm, then inspect the full work scope:

```bash
git log --stat --decorate main..HEAD
git diff --stat main...HEAD
git diff main...HEAD
```

Include any uncommitted changes in the verification surface.

## Phase 3: Language and Content Skills

If changed files include language ecosystems with extra rules (e.g., `*.rs` files -> invoke `/krust`), do so before judging implementation quality.

If changed files include user-facing documentation, invoke `/kdeslop` with the changed doc paths rather than auditing the whole repo. Skip `.k/tasks/` and other working docs unless the user explicitly asks. Treat severe or misleading public-doc findings as blockers; minor style nits are non-blocking.

## Phase 4: Quality Gate

Run all applicable checks: build, lint, formatter (check mode), type checker, tests. Use CLAUDE.md and project config to determine commands.

- Prefer the repo's canonical commands over ad hoc substitutes
- Don't silently skip a check category -- explain why it doesn't apply
- Verify appropriate test coverage for new functionality
- Report any failure as a blocking finding

## Phase 5: Verify Completeness Against Intent

Compare implemented work against the plan and brainstorm:

- Every planned deliverable is implemented
- No half-implemented features or placeholder stubs
- Edge cases called out in docs aren't skipped without explanation
- New functionality has tests matching the project's conventions
- Required documentation/config/schema updates are included

Prioritize: broken behavior, risky omissions, false confidence from incomplete tests, merge blockers. List highest-severity issues first with file references.

## Phase 6: Final Cleanliness Check

```bash
git status --short
```

If dirty, ask about `/kcommit`. Do not recommend `/kend` while the worktree is dirty.

## Phase 7: Merge Handoff

If checks passed, no blockers remain, and the worktree is clean -- offer `/kend`.

If blockers remain, summarize what must be fixed.

## Output Summary

Use `${CLAUDE_SKILL_DIR}/assets/verification-report-template.md` as the default report shape.

Report: branch name, plan/brainstorm used, commits reviewed, checks and outcomes, findings by severity, cleanliness, test coverage assessment, merge readiness.
