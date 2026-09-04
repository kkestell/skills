# Roadmap

The order in which the project is built. This file records scope and gates, not
design. `eng/architecture.md` holds durable design when it exists.

Every milestone compares its implemented behavior against the corresponding
sections of `docs/spec.md`. The gates listed under each task are the behavior
that task must prove on top of that.

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

**Gates**

- {What must be true before this task counts as done.}
- {What must be true before this task counts as done.}

### {Task}

**Build**

- {What to do.}

**Gates**

- {What must be true before this task counts as done.}

## Next milestone: {milestone}

{As above: what it makes possible, an example, and what it leaves out. Detailed
tasks and gates can wait until it becomes the current milestone.}

## Later work

Each of these is its own milestone, implemented in dependency order through one
or more plans. Each begins by confirming that `docs/spec.md` fully specifies its
behavior, then extends everything it affects together.

- {Later milestone.}
- {Later milestone.}

{Any abstraction that must not be built in advance for these, and what to do
instead.}

## Out of scope

- {Something the project will not do.}
- {Something the project will not do.}
