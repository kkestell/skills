---
name: kjira
description: Create, update, view, and sprint-manage Jira issues in the Star Tribune DANG project using the `jira` CLI (ankitpokhrel/jira-cli). Use whenever the user wants to file a ticket, update/retitle an issue, edit a description, move issues into a sprint, look up an issue, or otherwise touch Jira. Triggers on "create a ticket", "update DANG-NNN", "add to the sprint", "file a bug/story/task", "what's in the current sprint".
argument-hint: "[what to do in Jira]"
---

# Jira (DANG project)

Uses the `jira` CLI (ankitpokhrel/jira-cli, `/opt/homebrew/bin/jira`) against
`https://minneapolisstartribune.atlassian.net`, project **DANG**, board **891**.

## Auth

The CLI reads the API token from the `JIRA_API_TOKEN` env var. Pull it from
`~/.jira/.env` (it is not committed elsewhere) and export it for every command:

```bash
export JIRA_API_TOKEN=$(grep '^JIRA_API_TOKEN=' ~/.jira/.env | cut -d= -f2-)
```

Identity is `kyle.kestell@startribune.com` (the Strib identity — assign and
report as this, never the Livefront account). For raw API calls, basic-auth as
`kyle.kestell@startribune.com:$JIRA_API_TOKEN`.

## Conventions

- **Preview before writing.** Show the user the summary + description of any
  ticket you're about to create or any edit to an existing ticket, and get
  explicit approval before running the write.
- Assign new tickets to `kyle.kestell@startribune.com` unless told otherwise.
- Name the relevant repo(s) in the description (e.g. `article-tagger`,
  `status-startribune-site`) — Jira issues don't carry a repo field.
- Write descriptions as markdown in a temp file; the CLI converts to ADF.

## Common commands

View / search:

```bash
jira issue view DANG-268 --plain          # human-readable
jira issue view DANG-268 --raw            # full JSON (sprint = customfield_10020)
jira sprint list --plain --columns ID,NAME,STATE --state active   # needs board.id in config
```

Create (body via `-T <file>` template; `--no-input` to skip prompts):

```bash
jira issue create -t Story \
  -s "Summary here (repo-name)" \
  -a kyle.kestell@startribune.com \
  -T /tmp/body.md --no-input
# prints the new DANG-NNN key + URL
```

Edit (note: `edit` has **no** `-T` flag — pipe the body via **stdin**):

```bash
cat /tmp/body.md | jira issue edit DANG-268 \
  -s "New summary" --no-input
```

Sprint membership (add up to 50 keys at once):

```bash
jira sprint add 4810 DANG-268 DANG-269 DANG-270
```

To find which sprint an issue is in, read `customfield_10020` from `--raw`
(holds `[{id,name,state,boardId,startDate,endDate}]`).

## Config gotchas

`~/.config/.jira/.config.yml` must list each issue type with an `id` (string)
**and** a `subtask` bool, plus `board.id`, or `jira issue create` panics
(`interface conversion: interface {} is nil`). Type IDs for DANG:

```
10103 Story   10100 Task   10102 Bug   10000 Epic   10213 Spike
```

Fetch current type IDs if they ever change:

```bash
curl -s -u "kyle.kestell@startribune.com:$JIRA_API_TOKEN" \
  "https://minneapolisstartribune.atlassian.net/rest/api/3/issue/createmeta/DANG/issuetypes" \
  | python3 -c "import sys,json;[print(t['id'],t['name']) for t in json.load(sys.stdin)['values']]"
```
