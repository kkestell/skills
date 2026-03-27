---
name: brainstorm
description: Turn a fuzzy idea into a concrete direction through repo-aware dialogue, and tradeoffs. Creates a brainstorm doc. Use before `/plan` when scope is still moving.
argument-hint: "[feature idea or problem to explore]"
disable-model-invocation: true
---

## Workflow

1. Read `.k/current_task.json`; if it is missing, stop and tell the user to run `/start-task`.
2. Read `<feature_description> $ARGUMENTS </feature_description>`; if it is empty, ask what they want to explore and stop.
3. Decide whether brainstorming is actually needed.
   - If the request already has concrete scope, clear acceptance criteria, and constrained behavior, suggest skipping directly to `/plan`.
   - Brainstorming answers WHAT to build, not implementation HOW. Keep design and code-shape decisions for `/plan` and `/work`.
4. Gather local context before pushing the user for more detail.
   - Read relevant notes under `<docs_path>/research/` if they already exist so the brainstorm starts from known facts instead of re-asking settled questions.
   - Scan the repo for similar features, established patterns, adjacent code, and `CLAUDE.md` guidance.
5. Frame the problem before exploring solutions.
   - Reframe the problem as a "How might we..." question.
   - Start with "why" questions and go a few levels deep when needed. The stated request is often a proxy for the real problem.
6. Clarify the idea through collaborative dialogue.
   - Ask one question at a time.
   - Move from broad to narrow: purpose and users first, then constraints, edge cases, dependencies, deadlines, and success criteria.
   - Keep a running list of assumptions and validate them explicitly.
   - Treat constraints as creative inputs, not annoyances. They often determine which approaches are actually viable.
7. Research when the brainstorm needs evidence.
   - If repo, library, dependency, or web questions come up, invoke `/research` for each topic and use the saved notes before continuing.
8. Explore and narrow the solution space.
   - Diverge before converging. Generate 4-5 plausible approaches before recommending one.
   - Stress-test the strongest options with realistic failure modes, including what would make them fail in six months.
   - Prefer simpler approaches when two options satisfy the same need.
   - Narrow to 2-3 finalists with a recommendation.
9. Write `<docs_path>/brainstorm.md` using `${CLAUDE_SKILL_DIR}/assets/brainstorm-template.md`.
   - Keep only the headings that apply.
   - Include relevant research note paths when useful.
   - Keep the saved brainstorm focused on How Might We, Why This Approach, Assumptions, Constraints, Key Decisions, Failure Modes, Open Questions, and any relevant research references.
10. Never code here. End by asking whether the user wants to refine the brainstorm further, proceed to `/plan`, or stop.
