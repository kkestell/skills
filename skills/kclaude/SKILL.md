---
name: kclaude
description: Delegate a task to Claude Code headlessly with `claude -p`, let Claude work autonomously, then rewrite only Claude's final response for the user. Use when the user asks to hand work to Claude, delegate to Claude, use Claude Code, or wants Claude to perform a task without Codex duplicating the work. Do not use when the user asks Codex itself to perform or independently verify the task.
argument-hint: "[task to delegate to Claude Code]"
---

# Claude Delegate

Act as a thin dispatcher. Minimize Codex token use.

## Rules

1. Do not investigate, plan, inspect files, read the repository, or solve the task yourself before delegating.
2. Pass the user's actual task to Claude with only the minimal wrapper below.
3. Run Claude once and let it work autonomously.
4. Do not supervise Claude while it works.
5. Do not independently inspect Claude's changes, run tests, read diffs, check git status, or verify Claude's claims afterward unless the user explicitly asked for verification.
6. After Claude exits, read only its stdout. It contains Claude's progress updates followed by its final report; the final report is the source material.
7. Rewrite that final response into clear, concise language for the user.
8. Preserve substantive facts, filenames, commands, results, caveats, and unresolved problems.
9. Remove verbosity, repetition, canned sections, excessive explanation, and awkward model prose.
10. Do not add analysis or claims that were not present in Claude's result.
11. Do not mention this delegation workflow unless it is relevant to an error or limitation.
12. If Claude fails or produces no usable final response, report the failure directly. Do not take over the task unless the user asks.

## Invocation

Run from the directory in which the task should be performed:

```bash
claude -p \
  --model opus \
  --effort high \
  --permission-mode bypassPermissions \
  --no-session-persistence \
  --output-format stream-json --verbose \
  'Complete the following task autonomously. Work until it is finished. Use your tools as needed. Do not ask the user questions. Do not create or use git worktrees; work directly in the current checkout. While you work, output a concise one-line progress update at least every 5 minutes saying what you are doing. Make any necessary edits and run whatever checks you judge appropriate. Finish with a concise final report containing what you did, relevant validation results, and any unresolved issues.

TASK:
<USER_TASK>' \
  | jq -r --unbuffered 'select(.type=="assistant") | .message.content[]? | select(.type=="text") | .text'
```

The `stream-json` + `jq` pipe is required: plain text output prints nothing until Claude exits, so progress updates would never appear. This pipeline prints each of Claude's text messages to stdout the moment it is produced, ending with the final report.

Replace `<USER_TASK>` with the user's task as faithfully and compactly as possible.

Do not add repository context that Claude can discover itself.

Do not tell Claude how to solve the task unless the user supplied those instructions.

## Verification

If the user explicitly requests verification, first delegate normally. After Claude finishes, perform only the verification the user requested. Do not redo Claude's entire investigation or implementation.

## Final response

Treat Claude's final report — the text at the end of its stdout, after the progress updates — as the source material.

Rewrite it for clarity and brevity. Do not re-investigate the task merely to improve the wording.

If Claude reports successful work, state the result directly. If Claude reports uncertainty or failure, preserve that qualification.
