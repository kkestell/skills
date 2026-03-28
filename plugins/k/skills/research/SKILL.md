---
name: research
description: Research one repo, library, dependency, API, or web topic and save the findings as a reusable task note. Use from `/brainstorm`, `/plan`, or `/work` whenever a question needs evidence.
argument-hint: "[research topic]"
disable-model-invocation: true
---

## Workflow

1. Read `.k/current_task.json`; if it is missing, stop and tell the user to run `/start-task`.
2. Read `<research_topic> $ARGUMENTS </research_topic>`; if it is empty, ask and stop.
3. Resolve `docs_path` from `.k/current_task.json`, then choose the note path under `<docs_path>/research/<topic-slug>.md`.
   - Keep one file per topic so the notes stay reusable from `/brainstorm`, `/plan`, and `/work`.
   - If the user asks for multiple topics, create a separate file for each and research each one thoroughly.
   - If revisiting a topic, update the existing note instead of creating a duplicate.
4. Scope the research before starting.
   - State clearly what question or questions this research needs to answer.
   - Identify where the answers are likely to come from: repo code, local docs, library source, official API docs, web search.
   - If the topic is broad, break it into specific sub-questions first. Each sub-question should have a concrete answer when the research is done.
5. Gather evidence, starting local and going outward only when needed.
   - **Repo code first:** Read the actual files, not just grep hits. If the codebase has an existing implementation of the thing you're researching, read it end to end and document the patterns, types, and design choices. Skim is not research.
   - **Local docs and config:** Check `CLAUDE.md`, READMEs, doc comments, and any existing research notes that overlap.
   - **Library source and API docs:** When the question involves a dependency or API, read its actual documentation or source. Get the real types, real field names, real behavior — not a summary from memory.
   - **Web search:** Use when local sources are not enough. Prefer official documentation over blog posts. When you find useful information, capture it concretely: exact endpoints, exact type shapes, exact configuration, not paraphrases.
   - **Depth matters.** A research note that names a technique without showing the actual types, actual API shapes, actual code patterns, or actual edge cases is not useful. The note should contain enough concrete detail that the person reading it during `/plan` or `/work` does not need to re-research the same topic.
6. Write the note using `${CLAUDE_SKILL_DIR}/assets/research-template.md`.
   - Fill in the topic, summary of findings, example code or patterns, references, and open questions.
   - The summary should directly answer the questions scoped in step 4.
   - Include concrete examples: exact type definitions, exact API request/response shapes, exact code patterns from the repo or from documentation. Quote or reproduce them — do not paraphrase into vague descriptions.
   - References must be specific: repo-relative paths with line numbers, exact URLs, issue or PR links, commit hashes. "The OpenRouter docs" is not a reference.
   - Open questions should capture what the research did not resolve, so the next skill knows what is still uncertain.
7. Print the saved research path or paths and stop.
   - Do not implement product changes here; research and document only.
