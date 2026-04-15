---
name: kcommit
description: Safety-check staged/unstaged changes then commit all outstanding work with a well-formed commit message.
---

Commit all outstanding work in the repo after verifying nothing sensitive or unwanted is included.

## Steps

### 1. Assess the working tree

Run `git status` and `git diff --stat HEAD` to get a full picture of:

- Staged changes
- Unstaged changes
- Untracked files

### 2. Screen for sensitive files

Inspect every file that would be included in the commit (staged, unstaged, and untracked). Flag any file that looks like it may contain credentials, secrets, or private data:

- `.env`, `.env.*`, `*.env` files
- Files named `secrets.*`, `credentials.*`, `token.*`, `api-key.*`, `private-key.*`, or similar
- Files containing patterns like `-----BEGIN * PRIVATE KEY-----`, `AWS_SECRET`, `GITHUB_TOKEN`, `password =`, etc.
- SSH keys (`id_rsa`, `id_ed25519`, `*.pem`, `*.p12`, `*.pfx`)
- Browser-stored credential files

If any sensitive files are found:

- List them clearly.
- **Do not commit.** Stop and ask the user whether to add them to `.gitignore`, delete them, or handle them another way.
- Only continue after the user confirms the sensitive files are resolved.

### 3. Screen for build output and temp files

Look for files that should not be committed:

- Compiled output: `*.o`, `*.class`, `*.pyc`, `__pycache__/`, `*.dSYM/`, `dist/`, `build/`, `.build/`
- Package caches: `node_modules/`, `.gradle/`, `.m2/`, `Pods/` (unless the project intentionally commits them)
- Editor/OS noise: `.DS_Store`, `Thumbs.db`, `*.swp`, `*.swo`, `.idea/`, `.vscode/`
- Temp files: `tmp/`, `temp/`, `*.tmp`, `*.log`
- Test/coverage artifacts: `coverage/`, `.nyc_output/`, `*.lcov`

If any such files are found:

- List them clearly and explain why they should not be committed.
- Offer to add the appropriate patterns to `.gitignore`.
- If the user agrees, update `.gitignore` before continuing. Do not commit the unwanted files.
- If the user disagrees and wants to commit them anyway, proceed — but note the concern.

### 4. Stage all remaining changes

Once the working tree is clean of sensitive and unwanted files, stage everything that should be committed:

```
git add -A
```

If any files were intentionally excluded in step 2 or 3, use `git add --patch` or targeted `git add <path>` instead of `-A`, so excluded files stay out.

### 5. Understand the changes

Read the diff to understand what is being committed:

```
git diff --cached
```

Read enough of the changed files to understand the purpose and scope of the work. Do not write a commit message from filenames alone.

### 6. Write the commit message

Follow the 7 rules of great commit messages:

1. **Separate subject from body with a blank line**
2. **Limit the subject line to 50 characters**
3. **Capitalize the subject line**
4. **Do not end the subject line with a period**
5. **Use the imperative mood** — "Add feature", "Fix bug", "Refactor handler", not "Added" or "Adds"
6. **Wrap the body at 72 characters**
7. **Use the body to explain _what_ and _why_, not _how_** — the diff shows how; the message should explain intent and context

Additional guidance:

- The subject line should complete the sentence: "If applied, this commit will…"
- The body is optional for trivial changes but valuable for any change where the "why" is not obvious.
- Reference ticket numbers or issues in the body when relevant (e.g., `Fixes #42`).
- Do **not** include any AI-tool attribution lines (no "Co-Authored-By: Claude", no "Generated with Claude Code", etc.).

### 7. Commit

Run:

```
git commit -m "$(cat <<'EOF'
<subject line>

<body paragraphs, if needed, wrapped at 72 chars>
EOF
)"
```

### 8. Confirm

Run `git show --stat HEAD` and report:

- The commit hash and subject
- The files changed and lines added/removed
- Any follow-up the user should be aware of (e.g., files excluded from the commit that still need attention)
