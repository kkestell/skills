# [Component Name]

> Part of: [link to parent document]

## Purpose and Scope

What this component does, why it exists, and where it fits in the larger system. One paragraph.

### Non-Goals

What this component explicitly does not handle. Name the component that does, if applicable.

## Context

### Dependencies

What this component requires from other components or external systems.

| Dependency | What it provides | Interface |
|------------|------------------|-----------|
|            |                  |           |

### Dependents

What other components require from this one.

| Dependent | What it needs | Interface |
|-----------|---------------|-----------|
|           |               |           |

## Interface

The public contract this component exposes. Describe semantically: what operations are available, what goes in, what comes out, what errors are possible, and what constraints callers must respect.

For each operation or message:

### [Operation Name]

- **Purpose:**
- **Inputs:**
- **Outputs:**
- **Errors:**
- **Preconditions:**
- **Postconditions / Invariants:**

## Quality Attributes

Which quality attributes from the system-level architecture matter specifically for this component, and what they mean concretely here.

| Attribute | Requirement | Implication for design |
|-----------|-------------|------------------------|
|           |             |                        |

## Data Structures

The key types and structures at this level. Describe their shape, relationships, and invariants. Explain why they are shaped the way they are. Once implemented, link to the source file and name the type rather than duplicating the definition.

### [Structure Name]

- **Purpose:**
- **Shape:**
- **Invariants:**
- **Why this shape:**

## Internal Design

How this component is organized internally. Module/layer decomposition, state management approach, key algorithms (only non-obvious ones), and concurrency considerations.

## Error Handling and Failure Modes

How this component fails, how it recovers, and how it communicates failure to its dependents. Degradation strategy if applicable.

| Failure Mode | Detection | Recovery | Impact on Dependents |
|--------------|-----------|----------|----------------------|
|              |           |          |                      |

## Design Decisions

Decisions specific to this component, with alternatives that were considered and rejected.

### [Decision]

- **Context:**
- **Options considered:**
- **Choice:**
- **Rationale:**
- **Consequences:**

## Open Questions

Unresolved design questions for this component. Include enough context to resume the conversation.

- **Question:**
  **Context:**
  **Current thinking:**
