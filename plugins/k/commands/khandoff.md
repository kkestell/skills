---
name: khandoff
description: Write a handoff document summarizing this session for future agents/sessions.
---

Write a handoff document summarizing this session for future agents/sessions.

## Steps

1. Determine today's date (use the `currentDate` context if available).

2. List the existing files under `!`echo ~/.k/workspaces/${PWD//\//_}`/handoff/` to find the highest sequence number already used today, then increment by one. Format: `NNN` (zero-padded to 3 digits, starting at `001`).

3. Use the current session name, otherwise derive a short kebab-case topic slug from the main subject of this session (e.g. `eth-brownie-optimization`, `filter-sol-wsol-command`).

4. Use the filename: `!`echo ~/.k/workspaces/${PWD//\//_}`/handoff/YYYY-MM-DD-NNN-<slug>.md` where NNN is the largest existing NNN plus one for that specific day (e.g. 2026-03-23-001, 2026-03-23-002, 2026-03-24-001, etc). Create the directory if it does not exist.

5. Write the handoff document to the confirmed path. It should include:
   - **What was accomplished** — concrete deliverables, commands added, files changed
   - **Key decisions** — architectural choices, trade-offs, things that were explicitly ruled out and why
   - **Important context for future sessions** — data locations, known pre-existing failures, branch status, anything a fresh agent would need to pick up the work without re-discovering it

   Match the style and depth of the existing handoff docs in `!`echo ~/.k/workspaces/${PWD//\//_}`/handoff/`.
