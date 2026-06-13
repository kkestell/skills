# Research Plan: <topic>

## Metadata

- Date: <YYYY-MM-DD>
- Current repo: <path or repo>
- Original topic: <user topic>
- Clarified question: <clean actionable question>
- Output directory: `.k/research/YYYY-MM-DD-<topic-slug>/`

## Comparable Projects

List the comps from `.k/research/comps.json` in research order.

| Repo       | Language   | Stars | Why it is comparable                     |
| ---------- | ---------- | ----: | ---------------------------------------- |
| owner/repo | TypeScript | 12345 | Same problem domain and framework family |

## Scope

Research:

- <dimension or behavior to inspect>
- <dimension or behavior to inspect>

Do not research:

- <non-goal>

## Research Questions

- <specific question all repos should answer>
- <specific question all repos should answer>

## Per-Repo Instructions

For each comp:

1. Clone the repo into a temp directory.
2. Inspect files, docs, tests, configuration, and history relevant to the clarified question.
3. Write notes to `.k/research/YYYY-MM-DD-<topic-slug>/notes-<owner>_<repo>.md`.
4. Spawn a verifier subagent after writing notes. The verifier checks factual support, citations, and missed obvious evidence.
5. Revise notes if verification finds material issues.

## Notes Template

Every notes file must use this structure:

```markdown
# Notes: owner/repo

## Metadata

- Repo: owner/repo
- URL: https://github.com/owner/repo
- Language: <language>
- Researched at: <timestamp>
- Verification: <pending | passed | revised after verifier findings | blocked>

## Executive Answer

<Short answer to the clarified research question for this repo.>

## Relevant Files And Evidence

| Path           | Evidence        | Why it matters                    |
| -------------- | --------------- | --------------------------------- |
| `path/to/file` | <observed fact> | <connection to research question> |

## Implementation Details

<How this repo handles the researched topic, with concrete code/docs references.>

## Design Tradeoffs

<Benefits, costs, constraints, and failure modes of this repo's approach.>

## Transferability To Current Repo

<What appears reusable, what does not transfer, and why.>

## Gaps Or Uncertainty

<Missing evidence, ambiguous behavior, inaccessible data, or assumptions.>

## Verifier Findings

<Summary of verifier result and any changes made after verification.>
```
