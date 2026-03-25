---
name: kwork
description: Execute work plans efficiently while maintaining quality and finishing features
---

## Arguments
[plan file, specification, or todo file path]

# Work Plan Execution Command

Execute a work plan efficiently while maintaining quality and finishing features.

## Introduction

This command takes a work document (plan, specification, or todo file) and executes it systematically. The focus is on **shipping complete features** by understanding requirements quickly, following existing patterns, and maintaining quality throughout.

## Input Document

<input_document> #$ARGUMENTS </input_document>

## Worktree Conventions (Required)

Use this exact format for every `/kwork` execution:

- Base branch: `main`
- Worktree root: `<repo_root>/.worktrees/`
- Timestamp format: `YYYY-MM-DD-HH-MM-SS` (local time)
- Topic slug: kebab-case, lowercase letters/numbers/dashes only
- Work ID: `<timestamp>-<topic-slug>`
- Feature branch: `feature/<work-id>`
- Worktree path: `<repo_root>/.worktrees/<work-id>`

Examples:
- Branch: `feature/2026-03-24-11-42-09-billing-export-retry`
- Path: `/path/to/repo/.worktrees/2026-03-24-11-42-09-billing-export-retry`

## Execution Workflow

### Phase 1: Quick Start

1. **Read Plan and Clarify**

   - Read the work document completely
   - Review any references or links provided in the plan
   - If anything is unclear or ambiguous, ask clarifying questions now
   - Get user approval to proceed
   - **Do not skip this** - better to ask questions now than build the wrong thing

2. **Setup Environment**

   Before creating a dedicated worktree, checkpoint planning docs on `main` if needed.

   **Required pre-worktree checkpoint:**
   - If `input_document` is a plan under `docs/internal/plans/` and that plan is untracked or has uncommitted changes in the main checkout, commit it on `main` before `git worktree add`
   - If that plan references a brainstorm doc (for example in a `Related documents` section) and that brainstorm file is untracked or modified, include it in the same checkpoint commit
   - Stage and commit only the plan/brainstorm docs needed for this work; never bundle unrelated changes
   - If the plan does not explicitly reference a brainstorm, do not guess broadly; only include documents that are clearly tied to this work
   - Create the worktree only after this checkpoint commit exists, so the new branch starts with the correct plan/brainstorm history

   Suggested checkpoint flow from the main checkout:

   ```bash
   repo_root=$(git rev-parse --show-toplevel)
   plan_path="<repo-relative-plan-path>"
   brainstorm_path="<repo-relative-brainstorm-path-if-referenced>"

   # Inspect document state on main
   git -C "$repo_root" status --short -- "$plan_path"
   git -C "$repo_root" status --short -- "$brainstorm_path"  # only if referenced

   # If the plan is untracked or modified, checkpoint the plan and related brainstorm together
   git -C "$repo_root" add -- "$plan_path"
   git -C "$repo_root" add -- "$brainstorm_path"             # only if referenced and dirty
   git -C "$repo_root" diff --cached -- "$plan_path"
   git -C "$repo_root" diff --cached -- "$brainstorm_path"   # only if staged
   git -C "$repo_root" commit -m "docs: checkpoint plan for <topic>"
   ```

   After that checkpoint, create the dedicated worktree and do all implementation there:

   ```bash
   # 1) Resolve repo root and create worktree root directory
   repo_root=$(git rev-parse --show-toplevel)
   mkdir -p "$repo_root/.worktrees"

   # 2) Build consistent names
   timestamp=$(date +"%Y-%m-%d-%H-%M-%S")
   topic_slug="<kebab-case-topic>"  # derive from plan title or feature intent
   work_id="${timestamp}-${topic_slug}"
   branch_name="feature/${work_id}"
   worktree_path="$repo_root/.worktrees/${work_id}"

   # 3) Create feature worktree from updated main and enter it
   git -C "$repo_root" worktree add -b "$branch_name" "$worktree_path" main
   cd "$worktree_path"
   ```

   Setup requirements:
   - Do not implement on the main checkout; implement only in the worktree path
   - Confirm dependencies and project setup in the worktree
   - Verify tests/lint commands run before major edits
   - If branch/path already exists, regenerate `timestamp` and retry

3. **Create Todo List**
   - Use TodoWrite to break plan into actionable tasks
   - Include dependencies between tasks
   - Prioritize based on what needs to be done first
   - Structure tasks into logical chunks that can be tested and committed independently
   - Include testing and quality check tasks
   - Keep tasks specific and completable

### Phase 2: Execute

All code changes and test commands in this phase run from the worktree path created in Phase 1.

1. **Task Execution Loop**

   For each task in priority order:

   ```
   while (tasks remain):
     - Mark task as in_progress in TodoWrite
     - Read any referenced files from the plan
     - Look for similar patterns in codebase
     - Implement following existing conventions
     - Write tests for new functionality
     - Run tests after changes
     - Mark task as completed in TodoWrite
     - Mark off the corresponding checkbox in the plan file ([ ] → [x])
     - If this creates a complete, tested logical chunk, commit it immediately
   ```

   **IMPORTANT**: Always update the original plan document by checking off completed items. Use the Edit tool to change `- [ ]` to `- [x]` for each task you finish. This keeps the plan as a living document showing progress and ensures no checkboxes are left unchecked.

2. **Commit Early and Often (Required)**

   Build momentum with small, meaningful commits. Do not wait until the end.

   **Commit when:**
   - A logical unit is complete (one behavior, one fix, one slice of a feature)
   - Relevant tests for that unit pass
   - The change can be described clearly in one commit message

   **Do not commit when:**
   - The work is half-finished and not testable
   - Tests for the changed behavior are failing
   - Unrelated changes are mixed into the same diff

   **Chunking strategy:**
   - Break work into vertical slices that can be validated independently
   - Prefer multiple small commits over one large mixed commit
   - Keep each commit scoped to one concern (model, service, UI behavior, etc.)
   - Run targeted tests before each commit; run broader suite as you integrate

   **Per-commit mini workflow (mirror `/kcommit` essence):**
   - Run relevant quality checks for the chunk (tests, lint, formatter check mode, type checks where applicable)
   - If any check fails, do not stage or commit; fix issues first
   - Review `git status` and `git diff`
   - Stage deliberately with `git add <specific files>` (never `git add .`)
   - Confirm staged content with `git diff --staged`
   - Write a commit message using the 7 rules, then commit

3. **Follow Existing Patterns**

   - The plan should reference similar code - read those files first
   - Match naming conventions exactly
   - Reuse existing components where possible
   - Follow project coding standards (see CLAUDE.md)
   - When in doubt, grep for similar implementations

4. **Test Continuously**

   - Run relevant tests after each significant change
   - Don't wait until the end to test
   - Fix failures immediately
   - Add new tests for new functionality

5. **Figma Design Sync** (if applicable)

   For UI work with Figma designs:

   - Implement components following design specs
   - Use figma-design-sync agent iteratively to compare
   - Fix visual differences identified
   - Repeat until implementation matches design

6. **Track Progress**
   - Keep TodoWrite updated as you complete tasks
   - Note any blockers or unexpected discoveries
   - Create new tasks if scope expands
   - Keep user informed of major milestones

### Phase 3: Quality Check

1. **Run Core Quality Checks**

   Always run before submitting:

   ```bash
   # Run full test suite (use project's test command)
   # Examples: bin/rails test, npm test, pytest, go test, etc.

   # Run linting (per CLAUDE.md)
   # Use linting-agent before final handoff
   ```

2. **Consider Reviewer Agents** (Optional)

   Use for complex, risky, or large changes:

   - **code-simplicity-reviewer**: Check for unnecessary complexity
   - **kieran-rails-reviewer**: Verify Rails conventions (Rails projects)
   - **performance-oracle**: Check for performance issues
   - **security-sentinel**: Scan for security vulnerabilities
   - **cora-test-reviewer**: Review test quality (Rails projects with comprehensive test coverage)

   Run reviewers in parallel with Task tool:

   ```
   Task(code-simplicity-reviewer): "Review changes for simplicity"
   Task(kieran-rails-reviewer): "Check Rails conventions"
   ```

   Present findings to user and address critical issues.

3. **Final Validation**
   - All TodoWrite tasks marked completed
   - All tests pass
   - Linting passes
   - Code follows existing patterns
   - Figma designs match (if applicable)
   - No console errors or warnings

### Phase 4: Ship It

1. **Create Commit**

   Commit remaining tested work in the smallest logical unit possible. In brief:

   ```bash
   # 1. Review everything modified
   git status
   git diff

   # 2. Stage source files deliberately — NOT git add .
   git add <specific files>
   # If temp files, test output, or unrelated markdown are modified → ask the user first

   # 2b. Verify exactly what is staged
   git diff --staged

   # 3. Commit following the 7 rules (no attribution)
   git commit -m "$(cat <<'EOF'
   Short imperative summary under 50 chars

   Explain what changed and why. Wrap at 72 chars.
   Focus on motivation, not implementation details.
   EOF
   )"
   ```

2. **Capture and Upload Screenshots for UI Changes** (REQUIRED for any UI work)

   For **any** design changes, new views, or UI modifications, you MUST capture and upload screenshots:

   **Step 1: Start dev server** (if not running)
   ```bash
   bin/dev  # Run in background
   ```

   **Step 2: Capture screenshots with agent-browser CLI**
   ```bash
   agent-browser open http://localhost:3000/[route]
   agent-browser snapshot -i
   agent-browser screenshot output.png
   ```
   See the `agent-browser` skill for detailed usage.

   **Step 3: Upload using imgup skill**
   ```bash
   skill: imgup
   # Then upload each screenshot:
   imgup -h pixhost screenshot.png  # pixhost works without API key
   # Alternative hosts: catbox, imagebin, beeimg
   ```

   **What to capture:**
   - **New screens**: Screenshot of the new UI
   - **Modified screens**: Before AND after screenshots
   - **Design implementation**: Screenshot showing Figma design match

   **IMPORTANT**: Include uploaded image URLs in the completion summary to the user.

3. **Notify User**
   - Summarize what was completed
   - Share tests and lint checks run
   - Share commit summary (what each commit covers)
   - Report worktree handoff details: `worktree_path` and `branch_name`
   - Note any follow-up work needed
   - Ask: "Do you want me to run `/kmerge <worktree_path>` now?"
   - Suggest next steps if applicable

---

## Key Principles

### Start Fast, Execute Faster

- Get clarification once at the start, then execute
- Don't wait for perfect understanding - ask questions and move
- The goal is to **finish the feature**, not create perfect process

### The Plan is Your Guide

- Work documents should reference similar code and patterns
- Load those references and follow them
- Don't reinvent - match what exists

### Test As You Go

- Run tests after each change, not at the end
- Fix failures immediately
- Continuous testing prevents big surprises

### Quality is Built In

- Follow existing patterns
- Write tests for new code
- Run linting before final handoff
- Commit frequently in tested logical chunks
- Keep all implementation isolated in a dedicated feature worktree
- Use reviewer agents for complex/risky changes only

### Ship Complete Features

- Mark all tasks completed before moving on
- Don't leave features 80% done
- A finished feature that ships beats a perfect feature that doesn't

## Quality Checklist

Before final handoff, verify:

- [ ] All clarifying questions asked and answered
- [ ] All TodoWrite tasks marked completed
- [ ] If the starting plan was untracked or modified, the plan and any referenced brainstorm were checkpoint-committed on `main` before worktree creation
- [ ] Work was done in a dedicated worktree (not on main checkout)
- [ ] Branch and worktree follow the standard naming convention
- [ ] Tests pass (run project's test command)
- [ ] Linting passes (use linting-agent)
- [ ] Formatter/type checks pass where applicable
- [ ] Code follows existing patterns
- [ ] Figma designs match implementation (if applicable)
- [ ] Before/after screenshots captured and uploaded (for UI changes)
- [ ] Work is split into logical, tested commits (no mixed unrelated changes)
- [ ] Commit messages follow the 7 rules (imperative, ≤50 char subject, body explains why, no attribution)
- [ ] User was offered `/kmerge` to merge this worktree into `main`

## When to Use Reviewer Agents

**Don't use by default.** Use reviewer agents only when:

- Large refactor affecting many files (10+)
- Security-sensitive changes (authentication, permissions, data access)
- Performance-critical code paths
- Complex algorithms or business logic
- User explicitly requests thorough review

For most features: tests + linting + following patterns is sufficient.

## Common Pitfalls to Avoid

- **Analysis paralysis** - Don't overthink, read the plan and execute
- **Skipping clarifying questions** - Ask now, not after building wrong thing
- **Ignoring plan references** - The plan has links for a reason
- **Working in the wrong checkout** - Never implement on main; always use the feature worktree
- **Testing at the end** - Test continuously or suffer later
- **Forgetting TodoWrite** - Track progress or lose track of what's done
- **80% done syndrome** - Finish the feature, don't move on early
- **Over-reviewing simple changes** - Save reviewer agents for complex work
