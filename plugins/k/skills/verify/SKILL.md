---
name: verify
description: Verify completed work against its plan or brainstorm, run the repo's quality gates, invoke supporting skills when needed, and confirm merge readiness before `/end-task`.
argument-hint: "[plan path or verification target]"
disable-model-invocation: true
---

## Workflow

1. Run this after implementation and before `/end-task`.
   - Do not make product changes unless the user asks.
2. Read `.k/current_task.json` for `original_repo_path` and `docs_path`.
   - If it is missing, stop.
3. Read `<verification_target> $ARGUMENTS </verification_target>`, then build the verification surface.
   - Check `git status --short`; include uncommitted changes in the verification surface rather than silently ignoring them.
   - If the repo is dirty, do not recommend `/end-task`.
   - Resolve plan and brainstorm with `bash "${CLAUDE_SKILL_DIR}/scripts/find_intent_docs.sh" "<docs_path>" [user-path]`; ask if it cannot resolve confidently.
   - Read the plan and brainstorm, then inspect:
     - `git log --stat --decorate main..HEAD`
     - `git diff --stat main...HEAD`
     - `git diff main...HEAD`
4. Invoke supporting skills when relevant.
   - Prefer `/rust-lang` for changed `*.rs` files and `/deslop` for changed user-facing docs.
5. Run the repo's canonical quality gates.
   - Use the build, lint, formatter-check, type-check, and test commands from `CLAUDE.md` or project config.
   - Explain every skipped check.
   - Treat any failing check as a blocker.
6. Judge completeness against the intent docs.
   - Compare the delivered work against the plan or brainstorm, not just the diff.
   - Missing deliverables and half-finished features matter even when the code compiles.
   - Prioritize blockers, risky omissions, incomplete tests, and false confidence from partial coverage, with file references.
7. Write the final report using `${CLAUDE_SKILL_DIR}/assets/verification-report-template.md`.
   - Report branch name, docs used, commits reviewed, checks, findings by severity, cleanliness, test coverage, and merge readiness.
   - If clean and blocker-free, offer `/end-task`.
   - Otherwise summarize what must be fixed or whether `/commit` is needed first.
