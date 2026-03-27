---
name: research
description: Research one repo, library, dependency, API, or web topic and save the findings as a reusable task note. Use from `/k:brainstorm`, `/k:plan`, or `/k:work` whenever a question needs evidence.
argument-hint: "[research topic]"
disable-model-invocation: true
---

## Workflow

1. Read `.k/current_task.json`; if it is missing, stop and tell the user to run `/k:start-task`.
2. Read `<research_topic> $ARGUMENTS </research_topic>`; if it is empty, ask and stop.
3. Resolve `docs_path` from `.k/current_task.json`, then choose the note path under `<docs_path>/research/<topic-slug>.md`.
   - Keep one file per topic so the notes stay reusable from `/k:brainstorm`, `/k:plan`, and `/k:work`.
   - If the user asks for multiple topics, create multiple files.
   - If revisiting a topic, update the existing note instead of creating a duplicate.
4. Gather evidence.
   - Prefer repo code, local docs, and existing task docs first.
   - Use web research only when local context is not enough.
   - Research should reduce uncertainty and feed the workflow, not turn into implementation work.
5. Write the note using `${CLAUDE_SKILL_DIR}/assets/research-template.md`.
   - Fill in the topic, summary of findings, example code or patterns, references, and optional open questions.
   - References may include repo-relative paths, issue or PR links, docs URLs, library pages, or commit hashes.
6. Print the saved research path or paths and stop.
   - Do not implement product changes here; research and document only.
