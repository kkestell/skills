# k — Agent Skills

Skills for intentional, high-quality coding work, comparative research, and
prose editing.

The skills are designed to work together: `kplan` decides what the right change
is, and `kwork` carries it through to a finished, reviewed result. See
[skills/README.md](./skills/README.md) for the full workflow.

## Skills

| Skill          | What it does                                                                               |
| -------------- | ------------------------------------------------------------------------------------------ |
| `khandoff`     | Write a session handoff document for a future agent or session.                            |
| `kinit`        | Explore a repo and bootstrap an `AGENTS.md` orientation doc.                               |
| `kplan`        | Brainstorm a change, explore the codebase, and write a concrete implementation plan.       |
| `kwork`        | Execute a plan end to end: implement, validate with independent review passes, and commit. |
| `kreview`      | Run independent completeness and code-simplification review passes over a body of work.    |
| `ksimplify`    | Review a whole codebase for global simplification opportunities.                           |
| `kresearch`    | Research a technical topic across comparable open-source projects.                         |
| `ktask`        | Execute a bounded one-off task without a persisted plan or commit.                         |
| `krust`        | Apply the Rust API design guidelines when designing or reviewing public APIs.              |
| `kdeslop`      | Detect and fix AI "slop" in prose while preserving meaning and voice.                      |
| `kformat-docs` | Format Markdown with dprint and hard-wrap prose at 80 columns.                             |
| `kclaude`      | Delegate a task to Claude Code headlessly and report back its result.                      |
| `kwiki`        | Read, search, and edit pages on the private Wiki.js site.                                  |

## Install

Install every skill globally for Claude Code and Codex with Vercel's skills
installer:

```bash
npx skills add kkestell/skills --skill '*' --agent claude-code codex --global --yes
```

Install only selected skills by naming them:

```bash
npx skills add kkestell/skills --skill kplan kwork kreview --agent claude-code codex --global --yes
```

Install from a local checkout while developing:

```bash
npx skills add /absolute/path/to/skills --skill '*' --agent claude-code codex --global --yes
```

From inside a checkout, `make skills` installs every skill from that checkout
and removes any globally installed skill the checkout no longer defines.

Pull updates for globally installed skills with:

```bash
npx skills update --global
```

The skills are installed directly, without a Claude or Codex plugin namespace.
Use `kwork`, for example, instead of `k:kwork`.

## Repository layout

```text
skills/
  kplan/
    SKILL.md
    assets/
  kwork/
    SKILL.md
  ...
```

Each directory under `skills/` is a standalone skill. There are no plugin
manifests or marketplace catalogs.

## Development

Install the repository tooling and run the full validation suite:

```bash
npm install
npm run check
```

Validate one skill:

```bash
npm run validate -- skills/<skill-name>
```

See [AGENTS.md](./AGENTS.md) for authoring conventions.
