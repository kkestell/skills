# [Project Name]

## Vision

What this project is, who it is for, and why it exists. One or two paragraphs, not a mission statement.

## Goals

What the system must achieve to be considered successful. Be concrete.

-

## Non-Goals

What this system explicitly will not do, even though someone might reasonably expect it to. These prevent scope creep and clarify tradeoffs.

-

## Constraints

Technical, organizational, regulatory, or timeline constraints that bound the design space.

-

## System Context

How the system relates to its environment: users, external systems, integration points. A C4 Level 1 context diagram belongs here if the project warrants one.

## Solution Strategy

Fundamental technology choices, decomposition approach, and key architectural patterns. This is the "big bet" section: the decisions that are expensive to reverse and shape everything downstream.

-

## Building Blocks

The major components/modules of the system and their responsibilities. This table is the primary navigation mechanism for the architecture. Each entry should be 2-3 sentences summarizing the block's responsibility. Detail belongs in the linked component doc, not here.

When a building block has been discussed in any depth, it gets its own document. The index stays thin — if you are writing more than 3 sentences about a block here, it needs a component doc.

| Block | Responsibility | Document |
|-------|----------------|----------|
|       |                |          |

## Data Architecture

The core domain entities, their relationships, and why they are shaped the way they are. Key invariants and consistency rules. Once data structures exist in code, name them here and link to the source file rather than duplicating definitions.

## Crosscutting Concerns

Decisions that apply across multiple building blocks rather than belonging to any single one. Keep each concern to a short summary here. If a crosscutting concern grows beyond a paragraph or two, it gets its own document and a link from this section.

### Error Handling

### Observability

### Security and Authorization

### Configuration and Deployment

## Quality Attributes

Which quality attributes matter most for this system, ranked, with concrete targets. Not every attribute from the master list applies to every project. Name the ones that do and say what they mean here specifically.

| Attribute | Target | Rationale |
|-----------|--------|-----------|
|           |        |           |

## Key Scenarios

3-5 runtime scenarios that reveal how building blocks interact. Focus on scenarios that test architectural decisions, including at least one failure/error scenario.

### Scenario: [Name]

## Decisions

Important architectural decisions with rationale. Link to individual ADR documents for decisions that involved significant tradeoff analysis.

| Decision | Rationale | ADR |
|----------|-----------|-----|
|          |           |     |

## Risks and Technical Debt

Known risks with severity and mitigation strategy. Technical debt items that have been accepted deliberately.

-

## Open Questions

**System-level questions only.** Questions about a specific building block or component belong in that component's document, not here. This section is for questions that span multiple components, affect the overall architecture, or do not yet have a home because the relevant component has not been broken out yet.

Each question should have enough context that a reader (or an agent in a fresh session) can understand what was being discussed and where the conversation left off.

- **Question:**
  **Context:**
  **Current thinking:**

## Glossary

Domain and technical terms that have specific meaning in this project.

| Term | Definition |
|------|------------|
|      |            |
