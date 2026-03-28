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
   - Ask one question at a time using `AskUserQuestion`.
   - Move from broad to narrow: purpose and users first, then constraints, edge cases, dependencies, deadlines, and success criteria.
   - Prefer multiple choice when natural options exist — it's faster for the user and forces you to think about the realistic possibilities.
   - Keep a running list of assumptions and validate them explicitly before moving on.
   - Ask about success criteria: how will the user know this worked?
   - Treat constraints as creative inputs, not annoyances. They often determine which approaches are actually viable.
   - Continue until the idea is clear or the user says "proceed."
7. Research when the brainstorm needs evidence.
   - If repo, library, dependency, or web questions come up, invoke `/research` for each topic and use the saved notes before continuing.
8. Explore and narrow the solution space.
   - Diverge before converging. Generate 4-5 plausible approaches without judgment first. Draw from repo patterns, analogous domains, inversion of the obvious solution, and the simplest thing that could work.
   - Stress-test the strongest options: "Imagine this failed in six months. What went wrong?" Name 1-2 realistic failure modes per candidate.
   - Present the 2-3 strongest approaches with: brief description (2-3 sentences), pros, cons, failure modes, and when it's best suited.
   - Lead with your recommendation and why. Prefer simpler approaches (YAGNI).
   - Ask the user which approach they prefer.
9. Write `<docs_path>/brainstorm.md` using `${CLAUDE_SKILL_DIR}/assets/brainstorm-template.md`.
   - Keep only the headings that apply.
   - Include relevant research note paths when useful.
   - Key sections: How Might We, Why This Approach, Assumptions (validated), Constraints, Key Decisions, Failure Modes, Open Questions, and research references.
   - Keep sections concise — 200-300 words max per section.
10. Never code here. End by asking whether the user wants to refine the brainstorm further, proceed to `/plan`, or stop.
