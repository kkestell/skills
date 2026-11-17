# K Skills

For how the brief, plan, work, and review skills fit into a project, see [An Agentic Development Workflow](docs/workflow.md).

## Skills

Skill definitions and their supporting files live in `skills/`.

Each artifact directory may contain a `_template.md`; if it does, the skill uses it, otherwise the skill falls back to its built-in default template.

### `/kbrief`

Works out with you what a change should do and why, one question at a time. Writes a brief to `.agents/briefs/` recording the outcome, your decisions and their reasons, the options you turned down, and what is out of scope. Shows you the brief to confirm, then stages it without committing.

### `/kplan`

Plans a code or behavior change from a brief, or from a request small and clear enough to need none. Sends an ambiguous or large request to `/kbrief` instead. Writes a plan to `.agents/plans/`, shows you its **Check your assumptions** list so you can change any entry, and stages the plan without committing.

### `/kwork`

Implements a plan and writes a work log to `.agents/work/`. Stages the work log and code changes without committing.

### `/kdiscuss <claude|codex|opencode> <topic or artifact path>`

Refines a plan, argument, or idea with another agent in a persistent conversation. Updates supplied plans with agreed improvements, reports unresolved questions, and ends with an overview of the exchange and a one- or two-sentence summary of each message. Uses Claude Code with Fable and high effort, Codex with GPT-6.1 Sol and high effort, or OpenCode with DeepSeek V4.1 Flash from the DeepSeek provider and max effort. Requires the selected CLI and its authentication to be configured.

### `/kreview`

Reviews code in a diff, branch, commit, or files and fixes every finding. When the change has a brief, also checks that it delivers the brief's outcome, keeps its decisions, and stays within its scope. Fixes trivial findings directly and asks the user to decide the rest before fixing them. Writes a review to `.agents/reviews/` and stages it with the fixes without committing.

### `/kdeslop`

Audits the current repository for dead code, duplication, broken guarantees, over-engineering, hollow tests, and misleading comments or docs. Runs parallel area reviewers, independently verifies and deduplicates their findings, and writes a review grouped by severity to `.agents/reviews/`. Stages only the review, fixes nothing, and starts no follow-up work.

### `/kpr <url>`

Reviews a GitHub pull request. Checks whether the implementation is proportionate before delegating to `/kreview`, using the diff for straightforward changes and a temporary clone for complex ones. Reports a proposed verdict and actionable comments in chat, then removes the temporary clone. Does not change the PR or post without approval.

### `/kexplain`

Explains a plan or a change in staged changes, a diff, branch, or commit. Writes a self-contained HTML overview to `.agents/explanations/` that shows the architecture with diagrams, uses little code, and flags anything overengineered, speculative, or needlessly complex. Stages it when it explains something staged.

### `/ktask`

Delegates a change stage by stage from Hypercube or another agent orchestration tool. Starts an Opus 5.5 agent at high effort for each of `/kplan`, `/kwork`, and `/kreview`, all in the same checkout, plus one for `/kbrief` when the planner reports the request needs a brief; each asks the user directly for any decision it needs. The review agent fixes every finding. Checks that the plan, work log, review, and code are staged, then commits everything as one commit.

## Workflows

The steps can share one session or each run in a fresh one.

### Implement a task

1. `/kplan add CSV export`
2. `/kwork .agents/plans/2026-09-25-001-export.md`
3. `/kreview staged changes for .agents/plans/2026-09-25-001-export.md`
4. `/kexplain staged changes`
5. `/ktelemetry .agents/plans/2026-09-25-001-export.md`
6. Commit.

Ideally, the brief (when needed), plan, work log, code changes, review, fixes, and explanation land in one commit. When a plan task needs a commit partway through, such as a deploy, `/kwork` makes it and the rest lands in a later commit. The telemetry step records how the cycle went and is only for the repository owner.

### Work out a larger change first

1. `/kbrief add CSV export`
2. `/kplan .agents/briefs/2026-09-25-001-export.md`
3. Continue as in Implement a task.

The brief lands in the same commit as the plan and code.

### Delegate a task stage by stage

1. `/ktask add CSV export`

Each stage runs in its own agent, including `/kbrief` when the request needs one. The brief (when needed), plan, code changes, work log, and review land in one commit, with every finding fixed, unless a plan task needs an earlier commit.

### Refine a plan before implementation

1. `/kplan add CSV export`
2. `/kdiscuss claude .agents/plans/2026-09-25-001-export.md`
3. `/kwork .agents/plans/2026-09-25-001-export.md`

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
