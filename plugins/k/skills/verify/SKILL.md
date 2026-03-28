---
name: verify
description: Verify completed work against its plan or brainstorm, run the repo's quality gates, invoke supporting skills when needed, and confirm merge readiness before `/end-task`.
argument-hint: "[plan path or verification target]"
disable-model-invocation: true
---

## Workflow

1. Run this after implementation and before `/end-task`.
   - Do not make product changes unless the user explicitly asks.
2. Read `.k/current_task.json` for `original_repo_path` and `docs_path`.
   - If it is missing, stop.
3. Read `<verification_target> $ARGUMENTS </verification_target>`, then build the verification surface.
   - Check `git status --short`. If the repo is dirty, ask about running `/commit` first. Do not recommend `/end-task` while the worktree is dirty.
   - Resolve plan and brainstorm with `bash "${CLAUDE_SKILL_DIR}/scripts/find_intent_docs.sh" "<docs_path>" [user-path]`; ask if it cannot resolve confidently.
   - Read the plan and brainstorm fully.
   - Inspect the full work scope using `original_repo_path` as the reference for `main` comparisons:
     ```
     git log --stat --decorate main..HEAD
     git diff --stat main...HEAD
     git diff main...HEAD
     ```
   - Include any uncommitted changes in the verification surface rather than silently ignoring them.
4. Invoke supporting skills when relevant.
   - If changed files include `*.rs` files, invoke `/rust-lang` before judging implementation quality.
   - If changed files include user-facing documentation (README, guides, public docs), invoke `/deslop` with those specific paths. Skip `.k/tasks/` and other working docs unless the user explicitly asks.
   - Treat severe or misleading public-doc findings as blockers; minor style nits are non-blocking.
5. Run the repo's canonical quality gates.
   - Use the build, lint, formatter-check, type-check, and test commands from `CLAUDE.md` or project config. Prefer the repo's own commands over ad hoc substitutes.
   - Do not silently skip a check category — explain why it does not apply if you skip it.
   - Verify appropriate test coverage for new functionality.
   - Treat any failing check as a blocker.
6. Judge completeness against the intent docs.
   - Compare the delivered work against the plan or brainstorm, not just the diff.
   - Every planned deliverable should be implemented. No half-implemented features or placeholder stubs.
   - Edge cases called out in the plan or brainstorm should not be skipped without explanation.
   - New functionality should have tests matching the project's conventions.
   - Required documentation, config, or schema updates should be included.
   - Prioritize: broken behavior, risky omissions, false confidence from incomplete tests, merge blockers. List highest-severity issues first with file references.
7. Final cleanliness check.
   - Run `git status --short` again. If dirty, ask about `/commit`. Do not recommend `/end-task` while dirty.
8. Write the final report using `${CLAUDE_SKILL_DIR}/assets/verification-report-template.md`.
   - Report branch name, docs used, commits reviewed, checks, findings by severity, cleanliness, test coverage, and merge readiness.
   - If clean and blocker-free, offer `/end-task`.
   - Otherwise summarize what must be fixed or whether `/commit` is needed first.
