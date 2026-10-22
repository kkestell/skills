# K Skills

For how the plan, work, and review skills fit into a project, see [An Agentic Development Workflow](docs/workflow.md).

## Skills

Skill definitions and their supporting files live in `skills/`.

Each artifact directory may contain a `_template.md`; if it does, the skill uses it, otherwise the skill falls back to its built-in default template.

### `/kplan`

Plans a code or behavior change. Writes a plan to `agents/plans/` and stages it without committing.

### `/kwork`

Implements a plan and writes a work log to `agents/work/`. Stages the work log and code changes without committing.

### `/kdiscuss <claude|codex|opencode> <topic or artifact path>`

Refines a plan, argument, or idea with another agent in a persistent conversation. Updates supplied plans with agreed improvements, reports unresolved questions, and ends with an overview of the exchange and a one- or two-sentence summary of each message. Uses Claude Code with Fable and high effort, Codex with GPT-6.1 Sol and high effort, or OpenCode with DeepSeek V4.1 Flash from the DeepSeek provider and max effort. Requires the selected CLI and its authentication to be configured.

### `/kreview`

Reviews code in a diff, branch, commit, or files and fixes every finding. Fixes trivial findings directly and asks the user to decide the rest before fixing them. Writes a review to `agents/reviews/` and stages it with the fixes without committing.

### `/kpr <url>`

Reviews a GitHub pull request. Checks whether the implementation is proportionate before delegating to `/kreview`, using the diff for straightforward changes and a temporary clone for complex ones. Reports a proposed verdict and actionable comments in chat, then removes the temporary clone. Does not change the PR or post without approval.

### `/kexplain`

Explains a change in staged changes, a diff, branch, or commit. Writes a self-contained HTML walkthrough with prose, code, diagrams, and other visual aids to `agents/explanations/`, and stages it when it explains staged changes.

### `/kauto`

Plans, implements, and reviews a change without stopping for user input. Runs `/kplan` and `/kwork`, runs `/kreview` in a subagent that makes the review's decisions itself, and commits. Ends with a summary of the design and architecture decisions it made.

## Workflows

The steps can share one session or each run in a fresh one.

### Implement a task

1. `/kplan add CSV export`
2. `/kwork agents/plans/2026-09-25-001-export.md`
3. `/kreview staged changes for agents/plans/2026-09-25-001-export.md`
4. `/kexplain staged changes`
5. Commit.

The plan, work log, code changes, review, fixes, and explanation land in one commit.

### Implement a task autonomously

1. `/kauto add CSV export`

The plan, code changes, and review land in one commit, with every finding fixed.

### Refine a plan before implementation

1. `/kplan add CSV export`
2. `/kdiscuss claude agents/plans/2026-09-25-001-export.md`
3. `/kwork agents/plans/2026-09-25-001-export.md`

Use `codex` or `opencode` in the discussion step to choose another agent. The initiating agent evaluates each reply and develops the proposal; the helper preserves the other agent's session for up to six replies, including final confirmation.

## Global install

From a local checkout:

```bash
npx skills add /path/to/skills -g -a claude-code -a codex -s '*'
```

From GitHub:

```bash
npx skills add kkestell/skills -g -a claude-code -a codex -s '*'
```
