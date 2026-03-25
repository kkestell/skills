---
name: kplan
description: Transform feature descriptions into well-structured project plans following conventions
---

## Arguments
[feature description, bug report, or improvement idea]

# Create a plan for a new feature or bug fix

## Introduction

**Note:** To get the current date for document timestamps, run `date +"%Y-%m-%d"` or `date +"%Y-%m-%d-%H-%M-%S"` for full timestamps.

Transform feature descriptions, bug reports, or improvement ideas into well-structured markdown files that follow project conventions and best practices. This command provides flexible detail levels to match your needs.

## Feature Description

<feature_description> #$ARGUMENTS </feature_description>

**If the feature description above is empty, ask the user:** "What would you like to plan? Please describe the feature, bug fix, or improvement you have in mind."

Do not proceed until you have a clear feature description from the user.

## Main Tasks

### 1. Local Research

Scan the repository to understand the project's conventions, existing patterns, and any documented learnings:

- Look for similar features in the codebase
- Check for established patterns and conventions
- Review CLAUDE.md for project-specific guidance

These findings inform the next step.

### 1.5. Research Decision

Based on signals from Step 1, decide on external research.

**High-risk topics → always research.** Security, payments, external APIs, data privacy. The cost of missing something is too high. This takes precedence over speed signals.

**Strong local context → skip external research.** Codebase has good patterns, CLAUDE.md has guidance, user knows what they want. External research adds little value.

**Uncertainty or unfamiliar territory → research.** User is exploring, codebase has no examples, new technology. External perspective is valuable.

**Announce the decision and proceed.** Brief explanation, then continue. User can redirect if needed.

Examples:
- "Your codebase has solid patterns for this. Proceeding without external research."
- "This involves payment processing, so I'll research current best practices first."

### 1.5b. External Research (Conditional)

**Only run if Step 1.5 indicates external research is valuable.**
Search for relevant documentation and best practices online related to the feature.

### 1.6. Consolidate Research

After all research steps complete, consolidate findings:
- Document relevant file paths from repo research (e.g., `app/services/example_service.rb:42`)
- Note external documentation URLs and best practices (if external research was done)
- List related issues or PRs discovered
- Capture CLAUDE.md conventions

**Optional validation:** Briefly summarize findings and ask if anything looks off or missing before proceeding to planning.

### 1.7. Carry Forward Related Design Docs

- If this plan comes from a brainstorm, add a `Related documents` section near the top of the plan with the exact repo-relative brainstorm path (for example, `docs/internal/brainstorms/2026-03-23-14-05-19-user-onboarding-brainstorm.md`)
- Preserve that path exactly; `/kwork` uses it to checkpoint the plan and brainstorm together on `main` before creating a worktree
- If there is no related brainstorm document, omit this section rather than guessing

### 2. Issue Planning & Structure

**Title & Categorization:**

- [ ] Draft clear, searchable issue title using conventional format (e.g., `feat: Add user authentication`, `fix: Cart total calculation`)
- [ ] Determine issue type and prefix: `feat` (new feature), `fix` (bug fix), `refactor` (code restructuring)
- [ ] Convert title to filename: add the current local timestamp prefix in `YYYY-MM-DD-HH-MM-SS` format, strip prefix colon, kebab-case, add `-plan` suffix
  - Example: `feat: Add User authentication` → `2026-01-21-14-30-45-feat-add-user-authentication-plan.md`
  - Keep it descriptive (3-5 words after prefix) so plans are findable by context

**Filename examples:**

- ✅ `docs/internal/plans/2026-02-03-16-45-12-fix-checkout-race-condition-plan.md`
- ❌ `docs/internal/plans/2026-03-10-08-05-59-refactor-api-client-extraction-plan.md` (too vague - what feature?)
- ❌ `docs/internal/plans/feat-user-auth-plan.md` (missing timestamp prefix)
- ❌ `docs/internal/plans/2026-01-15-09:30:00-feat-thing-plan.md` (colons in timestamp, not descriptive)
- ❌ `docs/internal/plans/2026-01-15-10-22-33-feat-new-feature-plan.md` (too vague - what feature?)

## Finish

After writing the plan file, print the path and stop. Do not prompt for next steps.

The plan stays in the main checkout at this stage. If `/kwork` later executes from an untracked or modified plan, it must checkpoint that plan and any referenced brainstorm on `main` before creating the feature worktree.

**For Rust code:** If this plan involves writing or modifying Rust code (`.rs` files), invoke `/krust` before implementation to ensure compliance with Rust development guidelines.

NEVER CODE! Just research and write the plan.
