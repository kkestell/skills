---
name: kreview
description: >
  Review code for violations of hierarchy, abstraction, modularization,
  encapsulation, and simplification. Use this skill whenever the user asks for
  a design review, architecture review, code quality audit, or wants feedback
  on the structural health of their codebase. Also trigger when the user asks
  about coupling, cohesion, encapsulation issues, abstraction leaks, layering
  problems, or asks to simplify, clean up, tidy, or polish recent changes.
argument-hint: "[file, directory, or glob pattern to review]"
---

## Overview

**Hierarchy**, **Abstraction**, **Modularization**, and **Encapsulation** are not independent rules but interlocking facets of the same discipline: building systems that humans can understand, change, and trust.

This skill reports violations only. It does not change code as part of the review.

The default review lenses are:

- **Hierarchy**
- **Abstraction**
- **Modularization**
- **Encapsulation**

When the user asks to **simplify**, **clean up**, **tidy**, or **polish**, add a fifth lens:

- **Simplify**

## Compatibility

- Treat all paths in this skill as relative to the skill directory unless the host environment provides its own skill-directory variable.
- In Claude-style environments, `${CLAUDE_SKILL_DIR}` may point at this directory. In Codex-style environments, resolve the sibling `references/` and `assets/` paths directly from this `SKILL.md`.
- If the host environment has a dedicated "ask user" tool, you may use it. Otherwise ask the user directly in a normal message.
- If delegation or subagents are unavailable, disallowed, or unnecessary, perform the review locally. Do not make helper agents a requirement for using this skill.

## Workflow

1. **Determine scope and review lenses.**
   - If the user provided `$ARGUMENTS`, review that file, directory, or glob.
   - Always include the four core lenses: hierarchy, abstraction, modularization, and encapsulation.
   - If the request is to simplify, clean up, tidy, or polish code, also include the **Simplify** lens.
   - For simplify-style requests, inspect `git diff`. If there are staged changes, inspect `git diff HEAD` so staged and unstaged edits are both visible.
   - If that diff is empty, fall back to the user-provided target. If there is no target, review the most relevant source files in the working directory rather than generated code, vendor directories, or test fixtures.
   - For non-simplify review requests, prefer the files changed recently or the area the user has been working in rather than trying to review an entire large codebase.

2. **Read the reference material.**
   - The core principles each have a reference file in `references/` next to this `SKILL.md`:
     - `hierarchy.md` — layering, inheritance depth, containment, dependency direction
     - `abstraction.md` — interface clarity, level mixing, leaky abstractions
     - `modularization.md` — cohesion, coupling, module boundaries, god modules
     - `encapsulation.md` — data hiding, invariant protection, public surface area
   - For simplify-style requests, also read `simplify.md` — unnecessary complexity, redundant work, duplication, incidental state, and cleanup opportunities worth reporting.

3. **Review the target through each selected lens.**
   - If the host environment supports helper agents and the user has explicitly asked for or permitted delegation, you may split the work into parallel reviewers, one per selected lens. Each reviewer:
     - Reads its reference file to calibrate what to look for
     - Reviews the target code through that single lens
     - Returns findings as a JSON array using the schema below
   - Otherwise, perform the selected lens passes yourself and use the same JSON schema for your intermediate notes.

4. **Review prompt template.** Use this prompt for each helper reviewer or local lens pass, substituting the principle name and reference path:

   ```text
   You are reviewing code for violations of the **{PRINCIPLE}** design principle.

   First, read the reference guide:
   {skill_dir}/references/{principle}.md

   Then review the following code:
   {target files/directories}

   For each violation you find, return a JSON array of objects with these fields:
   - "principle": "{PRINCIPLE}"
   - "severity": one of "Critical", "High", "Medium", "Low"
   - "location": file path and line number or range (e.g., "src/auth/handler.go:45-78")
   - "anti_pattern": the name of the anti-pattern from the reference (e.g., "Leaky abstraction")
   - "finding": a concise description of the specific violation (1-2 sentences)
   - "suggestion": a concrete, actionable recommendation to fix it (1-2 sentences)

   Calibrate severity using the guide in the reference file. Be specific — quote
   code, name symbols, cite line numbers. Do not flag things that are merely
   stylistic preferences or that tooling (linters, formatters) already handles.
   Focus on structural design issues that affect comprehensibility, changeability,
   or correctness.

   If you find no violations for this principle, return an empty array: []

   Return ONLY the JSON array, no surrounding text.
   ```

5. **Finish the review.**
   - Collect and merge the JSON arrays from all selected lens passes into a single list. Deduplicate overlaps and keep the more specific or higher-severity finding when two reviews flag the same root problem.
   - Format the report with `assets/review-template.md`. Group by principle and sort by severity.
   - If a selected principle has no findings, include the section header with "No issues found" rather than omitting it.
   - If the simplify lens was not part of the request, omit the Simplify section from the final report.
   - Report violations only. Do not apply fixes unless the user separately asks for implementation work.
