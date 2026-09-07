# Roadmap

The order in which the project is built. This file records scope and gates, not
design. `eng/architecture.md` holds durable design when it exists.

Every milestone compares its implemented behavior against the corresponding
sections of `docs/spec.md`. The milestone gates prove the integrated outcome.

## Most recently completed: {milestone}

{Two or three sentences naming what now works. Do not restate specified rules,
design, or code behavior owned elsewhere. Keep exactly one of these summaries
and replace it when the next milestone completes. Delete this section until the
project has completed its first milestone.}

## Current milestone: {milestone}

{What this milestone makes possible, and why it is one logical unit of work.}

```text
{A small example of the new behavior's input.}
```

```text
{What that example produces.}
```

{What this milestone deliberately does not do yet.}

### {Task}

**Build**

- {What to do.}
- {What to do.}

### {Task}

**Build**

- {What to do.}

### Milestone completion gates

- {What must work across the integrated feature.}
- {What semantic or architectural boundaries must be verified.}

## Next milestone: {milestone}

{As above: what it makes possible, an example, and what it leaves out. Define
its tasks and gates with kroadmap when it becomes the current milestone, before
planning begins.}

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
