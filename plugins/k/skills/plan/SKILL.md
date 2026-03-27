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
   - Scan the repo for similar code, established patterns, conventions, related issues or PRs, and `CLAUDE.md` guidance.
   - Existing code and project guidance usually reveal the real constraints faster than outside research.
5. Decide whether more research is needed.
   - Use `/research` whenever the plan needs evidence beyond obvious local patterns.
   - Skip extra research when strong local patterns already exist and the user has clear intent.
   - Research when uncertain, when the codebase has no examples, or when the technology or behavior is unfamiliar.
   - For security, payments, external APIs, and data privacy questions, always research instead of guessing.
6. Consolidate the implementation context.
   - Pick a small set of repo-relative `Related code` references.
   - Include the research note paths you actually relied on.
   - If `<docs_path>/brainstorm.md` or research docs exist, add them under `Related documents`.
   - Carry forward only the documents that are genuinely relevant to implementation.
7. Write `<docs_path>/plan.md` from `${CLAUDE_SKILL_DIR}/assets/plan-template.md`.
   - Use the template as a scaffold, not a rigid form.
   - Keep only the sections that apply, and add sections when they would make execution clearer.
   - Add actionable checkboxes, validation steps, and open questions.
   - Keep `Related code` concrete: repo-relative paths plus one-line reasons each file matters.
   - The finished plan should make execution straightforward: clear tasks, clear validation, and clear unknowns.
8. After writing, print the plan path and stop.
9. Never code here.
