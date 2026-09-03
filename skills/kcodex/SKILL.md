---
name: kcodex
description: Delegate a task to Codex headlessly with `codex exec`, let Codex work autonomously, then rewrite only Codex's final response for the user. Use when the user asks to hand work to Codex, delegate to Codex, use the Codex CLI, or wants Codex to perform a task without the current agent duplicating the work. Do not use when the user asks the current agent itself to perform or independently verify the task.
argument-hint: "[task to delegate to Codex]"
---

# Codex Delegate

Act as a thin dispatcher. Minimize the current agent's token use.

## Rules

1. Do not investigate, plan, inspect files, read the repository, or solve the
   task yourself before delegating.
2. Pass the user's actual task to Codex with only the minimal wrapper below.
3. Run Codex once and let it work autonomously.
4. Do not supervise Codex while it works.
5. Do not independently inspect Codex's changes, run tests, read diffs, check
   git status, or verify Codex's claims afterward unless the user explicitly
   asked for verification.
6. After Codex exits, read only its streamed agent messages. The last agent
   message is Codex's final report and is the source material.
7. Rewrite that final response into clear, concise language for the user.
8. Preserve substantive facts, filenames, commands, results, caveats, and
   unresolved problems.
9. Remove verbosity, repetition, canned sections, excessive explanation, and
   awkward model prose.
10. Do not add analysis or claims that were not present in Codex's result.
11. Do not mention this delegation workflow unless it is relevant to an error or
    limitation.
12. If Codex fails or produces no usable final response, report the failure
    directly. Do not take over the task unless the user asks.

## Invocation

Run from the directory in which the task should be performed:

```bash
codex exec \
  --ephemeral \
  --sandbox workspace-write \
  --json \
  - <<'KCODEX_TASK' \
  | jq -r --unbuffered 'select(.type == "item.completed" and .item.type == "agent_message") | .item.text'
Complete the following task autonomously. Work until it is finished. Use your tools as needed. Do not ask the user questions. Do not create or use git worktrees; work directly in the current checkout. While you work, output a concise one-line progress update at least every 5 minutes saying what you are doing. Make any necessary edits and run whatever checks you judge appropriate. Finish with a concise final report containing what you did, relevant validation results, and any unresolved issues.

TASK:
<USER_TASK>
KCODEX_TASK
```

The `--json` + `jq` pipeline is required. It prints each completed agent message
as Codex produces it, ending with the final report. `--ephemeral` prevents the
delegated run from persisting a session.

Replace `<USER_TASK>` with the user's task as faithfully and compactly as
possible.

Do not add repository context that Codex can discover itself.

Do not tell Codex how to solve the task unless the user supplied those
instructions.

Keep the default `workspace-write` sandbox for tasks confined to the current
workspace. If the task genuinely needs another writable directory, prefer a
narrowly scoped `--add-dir`. Use a broader sandbox only when the user's request
requires it and the surrounding environment authorizes it. Never use
`--dangerously-bypass-approvals-and-sandbox` unless the delegated process runs
inside an externally hardened environment.

## Verification

If the user explicitly requests verification, first delegate normally. After
Codex finishes, perform only the verification the user requested. Do not redo
Codex's entire investigation or implementation.

## Final response

Treat Codex's final report—the last agent message in the filtered stream—as the
source material.

Rewrite it for clarity and brevity. Do not re-investigate the task merely to
improve the wording.

If Codex reports successful work, state the result directly. If Codex reports
uncertainty or failure, preserve that qualification.
