---
name: kcommit
description: Stage intentional changes and create a deliberate, well-formed git commit. Use when work is ready to checkpoint, especially if files are ambiguous, quality checks still need to be run, or commit hygiene matters.
disable-model-invocation: true
---

# Commit

Stage and commit changes following quality and style rules.

## Step 1: Run Quality Checks

Check CLAUDE.md for project-specific commands, then run all that apply: tests, linter, formatter (check mode), type checker.

Do not proceed to staging if any check fails. Fix the issues first.

## Step 2: Review What's Changed

```bash
git status
git diff
```

Identify every modified, added, or deleted file.

## Step 3: Stage Deliberately

**Never use `git add .`** — always stage files by name.

Stage freely: source code, tests, migrations, config, and assets that are intentional parts of this change.

**Ask the user before staging:**

- Temporary or scratch files (`*.tmp`, `*.log`, debug scripts)
- Build artifacts or test output (`coverage/`, `tmp/`, `dist/`)
- Plan files, brainstorm docs, or other markdown not part of the feature
- Any file that looks unintentionally modified

```bash
git add <specific files>
git diff --staged   # Confirm exactly what will be committed
```

## Step 4: Write the Commit Message

Follow the 7 rules:

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood — "Add feature" not "Added feature"
6. Wrap the body at 72 characters
7. Use the body to explain _what_ and _why_, not _how_

**No type prefixes.** No `feat:`, `fix:`, or any conventional-commit prefixes.

**No attribution.** No `Co-Authored-By` or agent attribution lines.

### Examples

```
# Good
Add email validation to user registration

# Good — with body
Replace session store with Redis

Cookie-based sessions hit the 4KB limit for users with large
permission sets. Redis removes the size cap and reduces
per-request payload.

# Bad
Added email validation        ← past tense
Adds email validation         ← third person
feat: add email validation    ← type prefix
```

## Step 5: Commit

```bash
git commit -m "$(cat <<'EOF'
Subject line here

Body here if needed. Explain what and why.
Wrap at 72 characters.
EOF
)"
```
