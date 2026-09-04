# AGENTS.md

THIS FILE MUST BE KEPT UP TO DATE AT ALL TIMES

{Two or three sentences saying what the project is and what this repository
holds. Omit when the repository does not establish this yet.}

## Project Documents

- `docs/spec.md` defines product behavior. Use the `kspec` skill whenever
  creating or modifying it. Reading it does not require the skill.
- `eng/architecture.md` defines the implementation's durable design and
  boundaries. It may not exist yet.
- `eng/roadmap.md` defines what gets built and in what order. Use the `kroadmap`
  skill whenever creating or modifying it. Reading it does not require the
  skill.
- `eng/plans/` holds bounded implementation plans produced by `kplan` and
  executed by `kwork`.

The specification and roadmap are created when the project needs them. `kplan`
requires both and will direct the user to the appropriate skill when either is
missing. The architecture document is not required to begin planning.

## Tech Stack

- **Language(s):** {language and version, plus any runtime dependency policy}
- **Frameworks:** {frameworks and versions; omit if none}
- **Build system:** {build tool}
- **Tooling:** {formatter, linter, type checker, and test runner}

{Omit this section when the repository does not establish a tech stack yet.}

## Codebase Map

- {Each major source, test, documentation, or engineering directory and what it
  holds.}

{Omit this section when there is no codebase to map yet.}

## Commands

- Build: `{command}`
- Run: `{command}`
- Test: `{command}`
- Lint: `{command}`
- Format: `{command}`
- Type-check: `{command}`

{Omit commands that do not apply. Omit this section when no commands can be
verified. Use subsections only when distinct parts of the project have different
toolchains.}

## Project Rules

### Answering

Be short. Say the thing and stop.

A few sentences is the normal length of a reply. Most questions need one or two.
Never write five paragraphs where one would do. If a reply is running long, cut
whole points rather than compressing them into denser sentences.

Write plainly. Ordinary words, ordinary sentences, one idea each. Say it the way
you would say it out loud to someone sitting next to you. No throat-clearing
before the answer, no summary of what you just did after it, no restating the
question, no listing the options you considered and rejected.

Do not be clever or cryptic. Do not stack clauses onto a sentence with dashes
and semicolons; start a new sentence. Do not invent names for things that
already have names. Prefer the concrete: name the file, the function, the value.

When you need a decision, ask one plain question.

This governs replies. Files you write follow the repository's documentation
rules.

### Project priorities

This project is optimized for clarity, correctness, and ease of reasoning rather
than execution speed. Treat simplicity as a maintained project invariant, not a
cleanup activity.

When `docs/spec.md` exists, read it before making behavioral decisions. It is
authoritative where explicit. Use `kspec` to resolve or record missing behavior
before implementation depends on it.

When `eng/architecture.md` exists, read it before changing the program's
structure. Do not invent architectural constraints when it does not exist.

Build software in narrow, end-to-end vertical slices. A feature is not
implemented until every part of the codebase it touches, and their tests, agree
on it. Do not reserve names, add extension points, or build infrastructure for
hypothetical future features.

Use `kplan` to plan substantial work and `kwork` to execute an implementation
plan. Both `docs/spec.md` and `eng/roadmap.md` must exist before planning
begins.

Preserve unrelated working-tree changes. Never commit unless the user asks for a
commit explicitly.

### One home for every fact

Every fact lives in exactly one place. `docs/spec.md` defines behavior,
`eng/architecture.md` defines durable design, `eng/roadmap.md` defines what gets
built next, and this file defines how to work in the repository. Reference a
fact owned by another document instead of restating or summarizing it.
