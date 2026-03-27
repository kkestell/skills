---
name: init
description: Initialize the `.k/` structure used by the k workflow. Run once per repo; safe to rerun.
argument-hint: ""
disable-model-invocation: true
---

## Workflow

1. Run `bash "${CLAUDE_SKILL_DIR}/scripts/init.sh"`.
   - Treat the script as responsible for creating the `.k/` directory structure, including `.k/tasks/`, `.k/.gitignore`, and `.k/tasks/.gitkeep`.
2. Capture and report `repo_root`, `k_dir`, and `already_existed`.
   - This skill is idempotent. Rerunning it should be safe.
3. If `already_existed=false`, ask whether to commit the new `.k/` files now.
   - If the user says yes, stage only `.k/` and commit.
   - Keep the scope narrow: initialize the workflow structure, but do not bundle unrelated repo changes into the follow-up commit.
   - The only commit prompt here is for the new `.k/` files themselves.
4. If `already_existed=true`, report that the repository is already initialized and no action is needed.
