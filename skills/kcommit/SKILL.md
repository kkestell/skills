---
name: kcommit
description: Stage files and create a well-formed commit — runs quality checks, asks about ambiguous files, and follows the 7 rules of great commit messages
---

# Commit

Stage and commit changes following quality and style rules.

## Step 1: Run Quality Checks

Before staging anything, run all available quality checks. Check CLAUDE.md for project-specific commands, then run what applies:

```bash
# Tests
# e.g. bin/rails test, npm test, pytest, go test ./...

# Linter
# e.g. bin/rubocop, npm run lint, golangci-lint run, ruff check .

# Formatter (check mode, don't auto-fix without intent)
# e.g. prettier --check ., gofmt -l ., mix format --check-formatted

# Type checker
# e.g. npx tsc --noEmit, mypy ., pyright
```

**Do not proceed to staging if any check fails.** Fix the issues first, then return to Step 1.

## Step 2: Review What's Changed

```bash
git status
git diff
```

Identify every modified, added, or deleted file.

## Step 3: Stage Deliberately

**Never use `git add .`** — always stage files by name.

**Stage freely:** source code, tests, migrations, config, and assets that are intentional parts of this change.

**Ask the user before staging any of these:**
- Temporary or scratch files (`*.tmp`, `*.log`, debug scripts)
- Test output, coverage reports, or build artifacts (`coverage/`, `tmp/`, `dist/`, `.nyc_output/`)
- Plan files, brainstorm docs, or other markdown not part of the feature
- Any file that looks unintentionally modified

```bash
git add <specific files>
git diff --staged   # Confirm exactly what will be committed
```

## Step 4: Write the Commit Message

Follow the 7 rules:

1. **Separate subject from body with a blank line**
2. **Limit the subject line to 50 characters**
3. **Capitalize the subject line**
4. **Do not end the subject line with a period**
5. **Use the imperative mood** — "Add feature" not "Added feature" or "Adds feature"
6. **Wrap the body at 72 characters**
7. **Use the body to explain *what* and *why*, not *how***

### Format

```
Short imperative summary under 50 chars

Optional body. Explain what changed and why —
not how. Wrap lines at 72 characters.
```

**No type prefixes.** Do not use `feat:`, `fix:`, `Feat:`, or any conventional-commit prefixes.

**No attribution.** Do not add `Co-Authored-By`, `🤖 Generated with`, or any agent attribution lines.

### Examples

```
# Good
Add email validation to user registration

# Good — with body
Replace session store with Redis

Cookie-based sessions were hitting the 4KB limit for users
with large permission sets. Redis store removes the size cap
and reduces per-request payload.

# Bad — wrong mood
Added email validation        ← past tense
Adds email validation         ← third person
feat: add email validation    ← type prefix
WIP: email validation         ← not a complete change
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

For single-line messages:
```bash
git commit -m "Add email validation to user registration"
```
