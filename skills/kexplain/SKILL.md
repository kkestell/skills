---
name: kexplain
description: "Explain a plan in `agents/plans/` or a code change in staged changes, a diff, branch, or commit by writing a self-contained HTML overview in `agents/explanations/` that shows the architecture with diagrams and flags overengineering, speculation, and needless complexity. Use to help the user understand and sanity-check a plan or change, not to review it line by line or modify it. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it."
argument-hint: "[plan path or changes to explain]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Give the user the big picture of a plan or a code change so they can understand it and sanity-check it quickly: what it does and why, which parts of the system it touches, how those parts fit together, and how that compares to the system before. Flag anything that looks overengineered, needlessly complex, speculative, or out of proportion to the problem. Write one self-contained HTML page. Do not change the plan or the code.

Plans and changes written by agents are detailed enough that excess hides in them. A reader working through every task or every line misses it. This page exists to put the shape of the work and its excess in front of the reader.

## Choose what to explain

1. Read `<explain_scope> $ARGUMENTS </explain_scope>`. If it is empty, explain the staged changes. If the scope is a plan, or the staged changes are only a plan, explain the plan. Ask only when there is nothing to explain or the scope is ambiguous.
2. Read the plan or the changes, then the code around them: the components they touch, callers, dependencies, data flow, configuration, and tests. Read any plan, work log, or review in `agents/` that covers the change, and the request or ticket behind it when one is cited. Learn how the system works today well enough to describe it.

## Find what to flag

3. Judge the plan or change against the problem it solves. Flag:
   - Overengineering: abstractions, layers, interfaces, registries, or generic mechanisms with one use.
   - Speculation: work for a need nobody stated, such as extension points, options, configuration, or compatibility code for callers that do not exist.
   - Excess edge-case handling: validation, fallbacks, retries, or error paths for cases that cannot happen or do not matter.
   - Needless complexity: new components, state, dependencies, or steps where a smaller change to the existing code would do.
   - Scope creep: work the request did not ask for, and for a code change, departures from its plan.
4. For each flag, name where it lives, what it adds, and the simpler alternative. Flag only what the code, plan, or request supports, and do not pad the list. When there is nothing to flag, say so in one sentence.

## Decide what to show

5. Put the flags right after the summary, so the reader sees them first. Then explain the system: the components involved, how they connect, how data or control moves between them, and how that differs before and after. For a plan, "after" is what the plan will build. Follow the change, not a fixed outline.
6. Let diagrams carry the explanation. Use a block diagram for components and their connections, a flowchart or sequence diagram for flow, and a state diagram for a lifecycle. When the structure changes, show it before and after. Mark the parts that are new, changed, or flagged. Keep each diagram to about ten nodes, and split a larger system into an overview and a closer view. Lay a short chain out left to right. Do not add visuals for decoration.
7. Use very few code excerpts. Describe components, responsibilities, and interfaces in prose and diagrams. Quote code only when a few specific lines are the point, such as a flagged edge case or a key interface, and keep each excerpt to a few lines. Do not walk through the diff or the plan's tasks one by one.

## Write

8. Write in a neutral technical register, as in documentation maintained by the team that owns the code. Keep sentences short and words ordinary. Put one idea in each paragraph. Define a term the first time you use it. Break a complex idea into small steps and explain each before combining them.
9. Use the names the code, the plan, and the repository use. Do not coin a term, nickname a mechanism, or give an existing thing a new name. If something has no name, describe it in plain words each time.
10. Describe what the code does, not what it is like. No analogies, metaphors, or personification: code does not ask, want, know, decide, refuse, hand back, climb, or linger; it returns, raises, calls, checks, and stores. No colloquial phrases or punchlines such as "the short version", "the catch", "under the hood", "a handful", or "in flight". No em dashes.
11. Do not address the reader as "you" or write as "we". Keep judgment in the flags. Elsewhere, do not evaluate the change or the code: no "healthy", "clean", "simple", "elegant", "surprisingly", or "notably". State each flag directly, without hedging, such as "`ExporterRegistry` holds one exporter; `export_csv` could call `CsvExporter` directly." Do not hedge with "essentially", "basically", "simply", or "just".
12. Write full sentences in an even rhythm. Do not set up a contrast only to reverse it in the next sentence, vary sentence length for effect, or open a bullet or paragraph with a slogan or fragment such as "History headlines freeze." A heading names its subject, such as "The history lookup", not a framing such as "The short version" or "A worked example".
13. Respect the reader's time. Lead with the main point. Leave out what the reader does not need to understand the change. Scale the page to the change: a small change gets a short page.
14. Label each code excerpt with its file path and, when it matters, whether it is from before the change, after it, or proposed in the plan. Do not add line numbers or commit hashes. Highlight the lines that matter.
15. Keep code and diagrams visible without a click. Use interaction only for steppers and animations.
16. The page is for the reader of the change. Do not describe how you wrote it: what you ran or could not run, what you checked, or which files you read.
17. Make every claim, snippet, and diagram match the code and the plan. Check anything you are unsure of before you write it.

## Build the page

18. Read `agents/explanations/_template.html`, or this skill's `assets/_template.html` if the workspace has none, and build the page from it. Keep the template's head, base styles, and scripts as they are, and write the page inside `<main>`. Add CSS only for elements the template does not style, in the existing style block, and keep any JavaScript inline. Do not reference local files.
19. Write the page to `agents/explanations/`. Name the file `YYYY-MM-DD-NNN-slug.html`, using the next sequence for the day.
20. Render the page with headless Chrome and fix what is wrong. On macOS the binary is `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`; on Linux try `google-chrome` or `chromium`. If there is no Chrome, skip this step.

    ```sh
    "$CHROME" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=10000 --window-size=1200,6000 --screenshot=/tmp/explanation.png "file://$PWD/agents/explanations/<file>.html"
    "$CHROME" --headless --disable-gpu --virtual-time-budget=10000 --dump-dom "file://$PWD/agents/explanations/<file>.html" > /tmp/explanation.dom.html
    ```

    Look at the screenshot: diagrams are drawn and readable, any code is highlighted with marked lines banded, and nothing overlaps or overflows. In the dumped DOM, every `pre.mermaid` must contain an `<svg>` with a `viewBox`, and the text `Syntax error` must not appear.

## Stage

21. If what you explained is staged, stage the explanation with it. Do not stage anything else. Do not commit.
22. Give the final response and stop.

## Final response

When the explanation is written, reply in the form below and nothing else.

```markdown
One or two sentences saying, in plain words, what the plan or change does.

**Flags:**

- `ExporterRegistry` holds one exporter; call `CsvExporter` directly.
- Retry loop around a local file write.

**Explanation:** `agents/explanations/YYYY-MM-DD-NNN-slug.html`
```

Give each flag one short line. If there are none, write `**Flags:** None.`
