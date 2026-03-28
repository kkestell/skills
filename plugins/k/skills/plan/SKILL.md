---
name: plan
description: Turn clear requirements into a repo-specific markdown plan with tasks, related code, validation steps, and open questions. Use after `/brainstorm` or once scope is clear, before `/work`.
argument-hint: "[feature description, bug report, or improvement idea]"
disable-model-invocation: true
---

## Workflow

1. Read `.k/current_task.json`; if it is missing, stop and tell the user to run `/start-task`.
2. Read `<feature_description> $ARGUMENTS </feature_description>`; if it is empty, ask what they want to plan and stop.
3. Gather the task context before planning the work.
   - Read relevant notes under `<docs_path>/research/` if they already exist.
   - If `<docs_path>/brainstorm.md` exists, use it as input to the plan rather than restating the problem from scratch.
4. Research the repo locally first.
   - Look for similar features, established patterns, conventions, and `CLAUDE.md` guidance.
   - Check for related issues, PRs, or prior attempts at the same problem.
   - Read the files that will actually need to change, not just grep for keywords.
   - Existing code and project guidance usually reveal the real constraints faster than outside research.
5. Decide whether more research is needed and announce the decision.
   - **Always research:** security, payments, external APIs, data privacy — the cost of guessing wrong is too high.
   - **Skip research:** strong local patterns already exist, `CLAUDE.md` has guidance, and the user has clear intent.
   - **Research when uncertain:** unfamiliar territory, no codebase examples, new technology or library, ambiguous behavior.
   - State the decision briefly ("Local patterns are clear enough, skipping external research" or "Need to research X before planning") so the user can redirect if they disagree.
   - When research is needed, invoke `/research` for each topic and wait for the saved notes before continuing.
6. Optionally checkpoint with the user.
   - After local and external research, briefly summarize what you found and ask if anything looks off before writing the plan.
   - Skip this if the findings are straightforward and the path forward is obvious.
7. Consolidate the implementation context.
   - Pick a small set of repo-relative `Related code` references, each with a one-line reason why it matters.
   - Include the research note paths you actually relied on.
   - If `<docs_path>/brainstorm.md` or research docs exist, add them under `Related documents`.
   - Carry forward only the documents that are genuinely relevant to implementation.
8. Write `<docs_path>/plan.md` from `${CLAUDE_SKILL_DIR}/assets/plan-template.md`.
   - Use the template as a scaffold, not a rigid form. Keep only the sections that apply, and add sections when the work needs more structure.
   - Every implementation task gets an actionable checkbox. A reader should be able to execute the plan without re-reading the codebase.
   - Include validation steps: what tests to write, what commands to run, what to verify manually.
   - Include open questions for anything still unresolved after research.
   - `Related code` must be concrete: repo-relative paths plus one-line reasons each file matters. Vague references like "the auth module" are not useful.
9. After writing, print the plan path and stop.
10. Never code here.
