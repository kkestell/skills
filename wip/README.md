# Work in Progress

Skills in this directory are unfinished. They are **not installed** —
`profiles.py` installs only `skills/`, so nothing here reaches a Claude Code or
Codex profile.

`npm run check` still validates them, so an in-progress skill cannot rot into
invalid frontmatter while it waits here.

Promote a skill by moving its directory into `skills/` and documenting it in
[`../README.md`](../README.md) and [`../skills/README.md`](../skills/README.md).

## `kresearch`

Researches a topic across comparable GitHub projects and writes a plan, verified
notes, and synthesis under `docs/dev/research/`.

```text
/kresearch how do comparable coding agents handle permission escalation
```

`kresearch` still writes under `docs/dev/`; `skills/` has since moved its
generated docs to `eng/`. Reconcile that when promoting.
