# Work in Progress

Skills in this directory are unfinished. They are installed only when `wip` is
explicitly selected, for example `./profiles.py sync-skills wip --codex`.

`npm run check` still validates them, so an in-progress skill cannot rot into
invalid frontmatter while it waits here.

Promote a skill by moving its directory into `../core/` or `../ext/` and
documenting it in [`../../README.md`](../../README.md) and
[`../README.md`](../README.md).

## `kresearch`

Researches a topic across comparable GitHub projects and writes a plan, verified
notes, and synthesis under `docs/dev/research/`.

```text
/kresearch how do comparable coding agents handle permission escalation
```

`kresearch` still writes under `docs/dev/`; `skills/` has since moved its
generated docs to `eng/`. Reconcile that when promoting.
