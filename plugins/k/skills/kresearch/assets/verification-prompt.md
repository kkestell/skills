# Notes Verification Prompt

You are verifying one per-repo research notes file.

Inputs you will receive:

- Clarified research question.
- Research plan path and contents.
- Comparable repo clone path.
- Notes file path.

Check:

1. The notes answer the clarified research question for this repo.
2. Important claims are supported by concrete repo evidence.
3. File paths and cited artifacts exist in the clone.
4. The notes do not overstate transferability to the current repo.
5. Obvious relevant files, docs, tests, or configuration were not missed.
6. Uncertainty is marked where evidence is incomplete.

Return:

- Verdict: `PASS` or `ISSUES FOUND`.
- Findings with repo-relative file paths where applicable.
- Suggested note revisions.

Do not edit files. The research subagent owns revisions.
