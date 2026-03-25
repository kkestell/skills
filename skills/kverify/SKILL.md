---
name: kverify
description: Verify completed work in a dedicated worktree against its plan or brainstorm, run all relevant checks, invoke language-specific skills, and confirm the branch is clean before merge
---

## Arguments
[optional plan path, brainstorm path, worktree path, or feature branch name]

# Verify Worktree Before Merge

Use this skill near the end of `/kwork`, after implementation is complete and before `/kmerge`.
Default to verifying a dedicated feature worktree. Only verify `main` if the user explicitly confirms that is what they want.

The goal is to verify three things:
- The branch is reviewable and merge-ready
- The implemented work matches the plan or brainstorm intent
- The worktree is clean before handoff

Do not make product changes as part of verification unless the user explicitly asks. This skill is for validation, reporting, and merge readiness.

## Inputs

<verification_target> #$ARGUMENTS </verification_target>

If `<verification_target>` is provided, treat it as the strongest hint for locating the relevant worktree and related docs.

If it is empty, use worktree-first resolution:

- Start by looking for a dedicated worktree under `<repo_root>/.worktrees/`
- Prefer the worktree whose feature branch has the most recent commit relative to `main`
- Treat "committed to recently" as "has commits on `main..branch_name`", preferring the newest such commit
- If no dedicated worktree has recent feature-branch commits, ask the user whether they mean `main`
- Do not silently default to the primary checkout on `main`

## Shared Conventions

These should match `/kwork` and `/kmerge`:

- Base branch: `main`
- Worktree root: `<repo_root>/.worktrees/`
- Feature branch: `feature/<timestamp>-<topic-slug>`
- Plans live under `docs/internal/plans/`
- Brainstorms live under `docs/internal/brainstorms/`

## Phase 1: Resolve Verification Target and Cleanliness First

Before running deeper verification:

1. Resolve repo root and list candidate worktrees
   ```bash
   repo_root=$(git rev-parse --show-toplevel)
   pwd
   git worktree list --porcelain
   ```
2. Resolve `worktree_path` and `branch_name`
   - If the user passed a worktree path, use it directly
   - If the user passed a feature branch name, map it to a worktree from `git worktree list`
   - If no target was passed, inspect dedicated worktrees under `<repo_root>/.worktrees/` and choose the one with the most recent commit on `main..branch_name`
   - If no dedicated worktree qualifies, stop and ask: `I don't see a recently committed feature worktree. Did you mean main?`
   - If the user confirms `main`, set `worktree_path="$repo_root"` and `branch_name=main`
3. Confirm the selected target is valid
   - Normal `/kverify` runs should use a path under `<repo_root>/.worktrees/`
   - The branch should normally match `feature/<timestamp>-<topic-slug>`
   - If the selected target is the primary checkout, only continue after explicit user confirmation that `main` is the intended verification target
4. Check whether the selected checkout is clean
   ```bash
   git -C "$worktree_path" status --short
   ```

If the selected checkout is dirty, pause and ask the user whether they want to run `/kcommit` before proceeding.

If the selected checkout is not a dedicated worktree and the user has not explicitly confirmed `main`, do not continue.

Do not continue until the user explicitly confirms how to proceed.

## Phase 2: Find the Plan and Brainstorm Scope

Locate the documents that define the intended work.

Use this order:

1. If the user passed a plan or brainstorm path, use it
2. Inspect branch-only changes for matching docs
   ```bash
   git -C "$worktree_path" diff --name-only main...HEAD -- docs/internal/plans docs/internal/brainstorms
   git -C "$worktree_path" log --name-only --format=oneline main..HEAD -- docs/internal/plans docs/internal/brainstorms
   ```
3. Inspect current uncommitted changes for matching docs
   ```bash
   git -C "$worktree_path" status --short -- docs/internal/plans docs/internal/brainstorms
   ```
4. If a plan is found, read it first and look for a `Related documents` section pointing to a brainstorm
5. If only a brainstorm is found, use that as intent and note that no plan was available

Do not guess broadly. If multiple candidate plans or brainstorms exist and the correct one is unclear, ask the user to choose before continuing.

## Phase 3: Build the Verification Context

Read the discovered plan and brainstorm carefully, then inspect the full work scope:

- All commits on the feature branch relative to `main`
  ```bash
  git -C "$worktree_path" log --stat --decorate main..HEAD
  ```
- The aggregate diff relative to `main`
  ```bash
  git -C "$worktree_path" diff --stat main...HEAD
  git -C "$worktree_path" diff main...HEAD
  ```
- Any uncommitted changes still present in the worktree

Treat both committed work and uncommitted changes as part of the verification surface.

## Phase 4: Invoke Language-Specific Skills

If the changed files include language-specific ecosystems with extra rules, invoke the relevant skill before judging implementation quality.

Examples:
- Rust code changed (`*.rs`) -> invoke `/krust` before continuing

If no language-specific skill applies, continue with normal verification.

## Phase 5: Run the Full Quality Gate

Use `CLAUDE.md`, project scripts, and standard repo conventions to determine the right commands.

Run all relevant checks that apply to this repository:

- Build or compile step
- Linters
- Formatter in check mode
- Type checker
- Unit tests
- Integration tests
- Any other required static or validation checks in the repo

Typical command discovery sources:
- `CLAUDE.md`
- `package.json`
- `pyproject.toml`
- `Cargo.toml`
- `Makefile`
- language-specific task runners already used by the repo

Rules:
- Prefer the repo's canonical commands over ad hoc substitutes
- Do not silently skip a major check category without explaining why it did not apply
- For new functionality, verify that the project has the appropriate automated test coverage for its setup: unit tests, integration tests, or both
- If the repo does not clearly distinguish unit vs. integration tests, follow its existing testing pattern and say what you verified
- If any required check fails, report it as a blocking finding

## Phase 6: Verify Completeness Against Intent

Compare the implemented work against the plan and brainstorm, not just whether tests pass.

Specifically verify:
- Every planned deliverable appears to be implemented
- No plan checkbox was marked complete without corresponding code or behavior
- No feature is obviously half-implemented
- No important edge case called out in the docs was skipped without explanation
- There are no placeholder implementations, stubs, cheats, fake success paths, or commented-out core logic
- New functionality has unit and/or integration tests, whichever matches the project's test setup and existing conventions
- Tests cover the meaningful behavior that was added or changed
- Existing documentation/config/schema updates required by the plan or change were included
- Do not expect or create brand-new documentation files during normal verification; instead, flag missing updates to existing docs as a finding

Act like a code reviewer here. Prioritize:
- Broken or missing behavior
- Risky omissions
- False confidence from incomplete tests
- Merge blockers

When reporting findings, list the highest-severity issues first and include file references.

## Phase 7: Re-check Cleanliness

Before merge handoff, the working tree must be clean:

```bash
git -C "$worktree_path" status --short
```

If it is not clean, ask the user whether they want to run `/kcommit` before merge.

Do not recommend `/kmerge` while the worktree is dirty.

## Phase 8: Offer Merge Handoff

If:
- The work is being verified from a dedicated worktree
- The relevant checks passed
- No blocking completeness issues remain
- The working tree is clean

Then offer:

`/kmerge <worktree_path>`

If the user explicitly chose to verify `main`, do not offer `/kmerge`; report the verification result without merge handoff.

If any blocker remains, summarize what must be fixed before merge instead of offering `/kmerge`.

## Output Summary

When complete, report:

- Worktree path and branch name
- Plan used, if any
- Brainstorm used, if any
- Commits reviewed (`main..HEAD`)
- Checks run and their outcomes
- Findings, ordered by severity
- Whether the working tree is clean
- Whether test coverage for new functionality was adequate for the repo's test setup
- Whether existing documentation needed updates and whether those updates were present
- Whether the work is ready for `/kmerge`, or whether this was a user-confirmed `main` verification with no merge handoff
