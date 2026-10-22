---
name: kexplain
description: "Explain code changes in staged changes, a diff, branch, or commit by writing a self-contained HTML walkthrough in `agents/explanations/`, with prose, code, diagrams, and other visual aids. Use to help the user understand a change, not to review or modify it. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it."
argument-hint: "[changes to explain]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Help the user understand a change: what it does, why, how it fits into the rest of the system, and how things worked before compared to how they work now. Write one self-contained HTML page that walks through it. Do not change the code.

## Choose what to explain

1. Read `<explain_scope> $ARGUMENTS </explain_scope>`. If it is empty, explain the staged changes. Ask only when there is nothing to explain or the scope is ambiguous.
2. Read the changes, then the code around them: callers, dependencies, data flow, configuration, and tests. Read any plan, work log, or review in `agents/` that covers the change. Learn how the system worked before the change well enough to describe it.

## Decide what to show

3. Decide what the reader needs to understand and in what order. Usually that is what the change does and why, then the part of the system it touches, then how that part worked before and how it works now. Follow the change, not a fixed outline.
4. Use a visual aid when it makes an idea easier to grasp than prose would: a diagram for structure or flow, before and after code side by side, an animation or step-through for something that unfolds over time, a chart for real quantities. Do not add visuals for decoration. Keep a diagram to about ten nodes, and lay a short chain out left to right.

## Write

5. Write in a neutral technical register, as in documentation maintained by the team that owns the code. Keep sentences short and words ordinary. Put one idea in each paragraph. Define a term the first time you use it. Break a complex idea into small steps and explain each before combining them.
6. Use the names the code and the repository use. Do not coin a term, nickname a mechanism, or give an existing thing a new name. If something has no name in the code, describe it in plain words each time.
7. Describe what the code does, not what it is like. No analogies, metaphors, or personification: code does not ask, want, know, decide, refuse, hand back, climb, or linger; it returns, raises, calls, checks, and stores. No colloquial phrases or punchlines such as "the short version", "the catch", "under the hood", "a handful", or "in flight". No em dashes.
8. Do not address the reader as "you" or write as "we". Do not evaluate the change or the code: no "healthy", "clean", "simple", "elegant", "surprisingly", or "notably". Do not hedge with "essentially", "basically", "simply", or "just".
9. Write full sentences in an even rhythm. Do not set up a contrast only to reverse it in the next sentence, vary sentence length for effect, or open a bullet or paragraph with a slogan or fragment such as "History headlines freeze." A heading names its subject, such as "The history lookup", not a framing such as "The short version" or "A worked example".
10. Respect the reader's time. Lead with the main point. Leave out what the reader does not need to understand the change. Do not walk through the diff line by line. Scale the page to the change: a small change gets a short page.
11. Quote real code in short excerpts. Label each excerpt with its file path and, when it matters, whether it is from before or after the change. Do not add line numbers or commit hashes. Highlight the lines that matter.
12. Keep code and diagrams visible without a click. Use interaction only for steppers and animations.
13. The page is for the reader of the change. Do not describe how you wrote it: what you ran or could not run, what you checked, or which files you read.
14. Make every claim, snippet, and diagram match the code. Check anything you are unsure of before you write it.

## Build the page

15. Read `agents/explanations/_template.html`, or this skill's `assets/_template.html` if the workspace has none, and build the page from it. Keep the template's head, base styles, and scripts as they are, and write the page inside `<main>`. Add CSS only for elements the template does not style, in the existing style block, and keep any JavaScript inline. Do not reference local files.
16. Write the page to `agents/explanations/`. Name the file `YYYY-MM-DD-NNN-slug.html`, using the next sequence for the day.
17. Render the page with headless Chrome and fix what is wrong. On macOS the binary is `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`; on Linux try `google-chrome` or `chromium`. If there is no Chrome, skip this step.

    ```sh
    "$CHROME" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=10000 --window-size=1200,6000 --screenshot=/tmp/explanation.png "file://$PWD/agents/explanations/<file>.html"
    "$CHROME" --headless --disable-gpu --virtual-time-budget=10000 --dump-dom "file://$PWD/agents/explanations/<file>.html" > /tmp/explanation.dom.html
    ```

    Look at the screenshot: code is highlighted, marked lines are banded, diagrams and steppers are drawn and readable, and nothing overlaps or overflows. In the dumped DOM, every `pre.mermaid` must contain an `<svg>` with a `viewBox`, and the text `Syntax error` must not appear.

## Stage

18. If you explained staged changes, stage the explanation with them. Do not stage anything else. Do not commit.
19. Give the final response and stop.

## Final response

When the explanation is written, reply in the form below and nothing else.

```markdown
One or two sentences saying, in plain words, what the change does.

**Explanation:** `agents/explanations/YYYY-MM-DD-NNN-slug.html`
```
