---
name: kinit
description: Initialize a repository for the kskills workflow by creating the `.k/` directory structure. Run once per workspace. Idempotent.
argument-hint: ""
disable-model-invocation: true
---

# Initialize Workspace

Run the init script to create the `.k/` directory structure:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/kinit.sh"
```

If the script reports that `.k/` was created (not already present), ask the user whether to commit the new `.k/` directory now. If yes, stage and commit only the `.k/` directory files.

If `.k/` already existed, report that the workspace is already initialized and no action is needed.
