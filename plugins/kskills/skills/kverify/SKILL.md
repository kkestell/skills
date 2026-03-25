---
name: kverify
description: Verify completed implementation work in a dedicated worktree against its plan or brainstorm, run the repo's relevant quality checks, invoke language-specific skills when needed, and confirm the branch is clean before `/kmerge`. Use near the end of `/kwork` before merging.
argument-hint: "[worktree path, plan path, or feature branch name]"
disable-model-invocation: true
---

# Verify Worktree Before Merge

Run near the end of `/kwork`, after implementation and before `/kmerge`. Verify merge readiness, alignment with the plan or brainstorm, and worktree cleanliness.

Do not make product changes during verification unless the user explicitly asks.

## Inputs

<verification_target> $ARGUMENTS </verification_target>

### Resolve target

If a target is provided, use it. Otherwise:

- Look for dedicated worktrees under `<repo_root>/.worktrees/`
- Prefer the one with the most recent commits on `main..branch_name`
- If none qualifies, ask the user whether they mean `main`
- Never silently default to the primary checkout on `main`

Confirm the worktree is clean (`git -C "$worktree_path" status --short`). If dirty, ask about running `/kcommit` first.

## Phase 1: Find the Plan and Brainstorm

Prefer `${CLAUDE_SKILL_DIR}/scripts/find_intent_docs.sh "$worktree_path" [user_doc_path]` to surface candidate plan and brainstorm files. If it cannot resolve confidently, ask the user.

Locate design documents that define the intended work:

1. Use any path the user provided
2. Check branch-only changes: `git -C "$worktree_path" diff --name-only main...HEAD -- docs/internal/plans docs/internal/brainstorms`
3. Check uncommitted changes in those directories
4. If a plan is found, look for a `Related documents` section pointing to a brainstorm
5. If only a brainstorm exists, use it as intent

If multiple candidates exist and the right one is unclear, ask the user.

## Phase 2: Build Verification Context

Read the plan and brainstorm, then inspect the full work scope:

```bash
git -C "$worktree_path" log --stat --decorate main..HEAD
git -C "$worktree_path" diff --stat main...HEAD
git -C "$worktree_path" diff main...HEAD
```

Include any uncommitted changes in the verification surface.

## Phase 3: Language and Content Skills

If changed files include language ecosystems with extra rules (e.g., `*.rs` files → invoke `/krust`), do so before judging implementation quality.

If changed files include user-facing documentation, invoke `/kdeslop` with the changed doc paths rather than auditing the whole repo. Skip `docs/internal/` and other working docs unless the user explicitly asks. Treat severe or misleading public-doc findings as blockers; minor style nits are non-blocking.

## Phase 4: Quality Gate

Run all applicable checks: build, lint, formatter (check mode), type checker, tests. Use CLAUDE.md and project config to determine commands.

- Prefer the repo's canonical commands over ad hoc substitutes
- Don't silently skip a check category — explain why it doesn't apply
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
git -C "$worktree_path" status --short
```

If dirty, ask about `/kcommit`. Do not recommend `/kmerge` while the worktree is dirty.

## Phase 7: Merge Handoff

If the work is in a dedicated worktree, checks passed, no blockers remain, and the worktree is clean — offer `/kmerge <worktree_path>`.

If verifying `main` by user request, report results without merge handoff.

If blockers remain, summarize what must be fixed.

## Output Summary

Use `${CLAUDE_SKILL_DIR}/assets/verification-report-template.md` as the default report shape.

Report: worktree path, branch name, plan/brainstorm used, commits reviewed, checks and outcomes, findings by severity, cleanliness, test coverage assessment, merge readiness.
