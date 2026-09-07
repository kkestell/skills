# Roadmap

The order in which the project is built. This file records scope and gates, not
design. `eng/architecture.md` holds durable design when it exists.

Every milestone compares its implemented behavior against the corresponding
sections of `docs/spec.md`. The milestone gates prove the integrated outcome.

## Completed milestone: {milestone}

{Retain each completed milestone's scope, checked-off tasks, example or source
link with its expected result, and completion gates. Use the same structure as
the current milestone below. Omit this section until a milestone is complete.}

## Current milestone: {milestone}

{What this milestone makes possible, and why it is one logical unit of work.}

```text
{A small example of the new behavior's input.}
```

```text
{What that example produces.}
```

{What this milestone deliberately does not do yet.}

### [ ] {Task}

**Build**

- {What to do.}
- {What to do.}

### [ ] {Task}

**Build**

- {What to do.}

### Milestone completion gates

- {What must work across the integrated feature.}
- {What semantic or architectural boundaries must be verified.}

## Next milestone: {milestone}

{As above: what it makes possible, an example, and what it leaves out. When
planning this milestone, include ordered tasks and completion gates using the
current milestone's structure. Keep it here until the current milestone is
complete.}

## Later work

Each of these is its own milestone. Before planning begins, confirm that
`docs/spec.md` settles its behavior and define its ordered tasks with kroadmap.

- {Later milestone.}
- {Later milestone.}

{Any abstraction that must not be built in advance for these, and what to do
instead.}

## Out of scope

- {Something the project will not do.}
- {Something the project will not do.}
