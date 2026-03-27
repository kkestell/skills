---
name: commit
description: Stage intentional changes and create a clean git commit with deliberate staging, required quality checks, and a well-formed message.
---

## Workflow

1. Read `CLAUDE.md` for project-specific quality commands, then run every applicable check before staging.
   - Run tests, linter, formatter check mode, and type checks where relevant.
   - If any quality check fails, fix the issues before continuing. Do not checkpoint broken work.
2. Review the full change set with `git status` and `git diff`.
   - Account for every modified, added, and deleted file before staging anything.
3. Stage deliberately by file name only.
   - Never use `git add .`.
   - Stage source code, tests, migrations, config, and assets freely when they are intentional parts of the same change.
   - Keep unrelated work out of the same commit, even if it is already sitting in the working tree.
   - Ask before staging temporary files, build output, test artifacts, working docs, or anything that looks unintentionally modified.
   - After staging, inspect `git diff --staged` and confirm the staged set is coherent and intentional.
4. Write the commit message only after the staged set is correct.
   - Separate subject from body with a blank line.
   - Keep the subject at 50 characters or fewer.
   - Capitalize the subject and do not end it with a period.
   - Use the imperative mood.
   - Wrap the body at 72 characters.
   - Explain what changed and why, not how.
   - Do not use `feat:` or `fix:` prefixes.
   - Do not add attribution lines.
   - Good:

```text
Add email validation to user registration
```

   - Good:

```text
Replace session store with Redis

Cookie-based sessions hit the 4KB limit for users with large
permission sets. Redis removes the size cap and reduces
per-request payload.
```

   - Bad: `Added email validation`
   - Bad: `Adds email validation`
   - Bad: `feat: add email validation`
5. Run `git commit` only when the change is a clean logical unit that can stand on its own.
