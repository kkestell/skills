---
name: kresearch
description: "Research a technical topic across comparable open-source GitHub projects: identify comps, clarify the question, delegate verified per-repo investigation to subagents, and synthesize the findings. Use when the user wants to learn how similar projects solve a problem, compare implementation approaches across codebases, or gather evidence-backed prior art before a design decision. Writes comps, a plan, per-repo notes, and a summary under `.k/research/`."
argument-hint: "[topic or question to research]"
disable-model-invocation: true
---

## Workflow

### Input

1. Read `<research_topic> $ARGUMENTS </research_topic>`. If it is empty, ask what topic or question to research and stop.
2. Work from the current repository root. Use today's date from the runtime context.
3. Clarify the topic (Phase 1) before naming anything, then create a short kebab-case topic slug from the clarified topic. Use only lowercase letters, numbers, and hyphens.
4. Use `.k/research/YYYY-MM-DD-<topic-slug>/` for this run. If that directory already exists, treat the run as a continuation unless the user asks for a fresh one.

### Phase 1 - Clarify Research Topic

5. Expand, clean up, and elaborate the user's topic into an actionable research question without changing its meaning.
6. If the topic is ambiguous in a way that would change what gets researched, ask one focused question at a time. Do not start the research until the ambiguity is resolved.
7. If the topic is clear enough, proceed and record the clarified question for use in the comp search and the plan.

### Phase 2 - Identify Comparable Projects

8. Look for `.k/research/YYYY-MM-DD-<topic-slug>/comps.json`.
9. If it exists, read it first. Use the listed repos unless they are clearly stale, inaccessible, or irrelevant to the current repository.
10. If it does not exist, delegate the search to a subagent. If subagent tools are not visible, use tool discovery if available. If subagents are still unavailable, stop and ask the user whether to proceed locally. Pass the clarified research question to the subagent and instruct it to:

- Infer the current project profile from local files: README, package/build manifests, lockfiles, source layout, primary language, major frameworks, and the problem the repo solves.
- Search GitHub for projects comparable to the current repository and relevant to the clarified research question: same language, same major libraries/frameworks when possible, and roughly the same product/problem domain.
- Prefer the GitHub CLI when available. Check `gh search repos --help` for current field names, then search by several targeted queries sorted by stars.
- If `gh` is unavailable, use the GitHub REST API directly with `curl`. Use `GITHUB_TOKEN` when present to avoid low rate limits.
- Exclude the current repo, archived repos, forks unless the fork is the meaningful upstream, docs-only repos, toy demos, and repos that do not solve a comparable problem.
- Select five comps, sorted by popularity and broad impact, while keeping relevance as the first filter.
- Gather the metadata below for each comp and return the comps as valid, pretty-printed JSON (or write it directly to `.k/research/YYYY-MM-DD-<topic-slug>/comps.json` if its filesystem shares the parent workspace).

11. For each comp, gather as much of this metadata as practical:

```json
[
  {
    "name": "OpenCode",
    "repo": "anomalyco/opencode",
    "url": "https://github.com/anomalyco/opencode",
    "description": "The open source coding agent.",
    "stars": 170770,
    "forks": 20455,
    "contributors": 454,
    "commits_30d": 1590,
    "last_commit": "2026-06-06",
    "language": "TypeScript"
  }
]
```

Use `null` for fields that cannot be obtained after reasonable effort. Write valid, pretty-printed JSON to `.k/research/YYYY-MM-DD-<topic-slug>/comps.json`. If the subagent returned the comps instead of writing the file, write it yourself at that path.

### Phase 3 - Write Research Plan

12. Read [research-plan-template.md](assets/research-plan-template.md).
13. Write `.k/research/YYYY-MM-DD-<topic-slug>/plan.md`.
14. Include:

- Original user topic.
- Clarified research question.
- Comparable projects from `.k/research/YYYY-MM-DD-<topic-slug>/comps.json`.
- Scope and non-goals.
- Research dimensions each subagent should inspect.
- Concrete instructions for cloning repos to temp directories.
- A notes template that every subagent must follow.
- The expected notes path for each comp: `.k/research/YYYY-MM-DD-<topic-slug>/notes-<owner>_<repo>.md`, where `<owner>_<repo>` is the GitHub owner and repo name sanitized for a filename.

### Phase 4 - Do the Research

15. Use subagents for the per-repo research. If subagent tools are not visible, use tool discovery if available. If subagents are still unavailable, stop and ask the user whether to proceed locally.
16. Run one research subagent per comp, preferably in parallel.
17. Build each research prompt from [repo-research-prompt.md](assets/repo-research-prompt.md) plus the written `plan.md` and that comp's metadata. Include [verification-prompt.md](assets/verification-prompt.md) so the research subagent can hand it to its verifier.
18. Each research subagent must:

- Clone its repo into a temp directory. Prefer shallow clones, but fetch history if the research question needs it.
- Inspect the implementation relevant to the clarified question.
- Write notes to `.k/research/YYYY-MM-DD-<topic-slug>/notes-<owner>_<repo>.md` using the plan's notes template.
- If the subagent filesystem is isolated from the parent workspace, return the final notes content and verification result so the parent agent can write the notes file at the exact expected path.
- Spawn a verifier subagent after writing the notes. The verifier reads the notes and cloned repo, checks evidence and citations, and reports factual gaps or unsupported claims.
- Revise the notes if the verifier finds material issues, then record verification status in the notes.

19. Do not synthesize until every selected comp has a notes file or a documented reason it could not be researched.

### Phase 5 - Synthesize

20. Read all `notes-*.md` files for the run.
21. Write `.k/research/YYYY-MM-DD-<topic-slug>/summary.md`.
22. The summary should include:

- The clarified research question and short answer.
- Cross-project patterns and meaningful divergences.
- Evidence-backed findings with repo/file references from the notes.
- Practical implications for the current repository.
- Risks, caveats, and gaps in the research.
- Follow-up questions or deeper research that would materially improve confidence.

23. Report the paths to `comps.json`, `plan.md`, all notes files, and `summary.md` (all under `.k/research/YYYY-MM-DD-<topic-slug>/`).

## Principles

- **Comparable before popular** - relevance is the filter; popularity only sorts plausible comps.
- **Clarify without drifting** - improve the user's question, but do not replace it with a different one.
- **Evidence over vibes** - notes and summaries should cite files, commits, docs, or observed behavior.
- **Independent verification** - every per-repo notes file gets a second-pass verifier before synthesis.
- **Synthesize, do not concatenate** - the final summary should compare and reason across repos, not paste notes together.
