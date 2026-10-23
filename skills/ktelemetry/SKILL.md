---
name: ktelemetry
description: "Measure a completed plan, work, and review cycle and post the measurements and an assessment as an issue in the private `kkestell/skills-telemetry` repository, to improve the skills later. Use after `/kreview` when a plan, work log, and review exist, or on an older cycle. Fails for anyone without access to that repository. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it."
argument-hint: "[plan, work log, or review path]"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Record how one plan, work, and review cycle went, so the skills can be improved from evidence rather than memory. The bundled script measures what can be measured from the artifacts, Git, and Claude Code session files, including stages that ran in other sessions or before a compaction. You add the judgments it cannot make. The result is one issue in `kkestell/skills-telemetry`.

## Check access

1. Run the check below, replacing the script path with its absolute installed location. If it fails, report that the telemetry repository is not accessible and stop. Do not post anywhere else, scrub the data, or ask for another destination.

   ```bash
   python3 /path/to/ktelemetry/scripts/telemetry.py check
   ```

## Establish the cycle

2. Read `<artifact> $ARGUMENTS </artifact>`. It names a plan, work log, or review in `agents/`. If it is empty and exactly one review is staged, use that review. Otherwise ask which cycle to measure and stop.
3. Run the measurement and save its output; it is the first part of the issue body:

   ```bash
   python3 /path/to/ktelemetry/scripts/telemetry.py measure <artifact> > "$telemetry_dir/issue.md"
   ```

   The script resolves the plan, finds the work logs and reviews that name it, measures the staged changes when the review is staged and otherwise the commits that added the artifacts, and reads the project's Claude Code sessions in `~/.claude/projects/`. Pass `--commit <sha>` one or more times to add commits made during the cycle, such as one a work log records, to the staged changes, or to measure a different code change once committed; and `--json` to inspect the raw measurements. For a cycle committed in the past, point it at the plan; nothing else is needed.
4. Read the measured output, then read the plan, every work log, and every review it names, and the code change it measured. If the output says no session was found for a stage, that stage ran where this machine has no transcript; say so in the assessment and do not guess at its cost.

## Assess

5. Append the sections below to the issue body. Base every judgment on the artifacts and the code, and keep each entry to one or two sentences. Do not restate the measurements.

   ```markdown
   ## Where findings should have been caught

   | ID | Stage   | Why                                                                                         |
   | -- | ------- | ------------------------------------------------------------------------------------------- |
   | F1 | plan    | The plan never considered closing a listener outside the event loop.                        |
   | F2 | work    | The plan's test plan named this case and the work log claims it; the test did not cover it. |
   | F3 | neither | A property of the host's network that only running the test on another machine reveals.     |

   ## Plan against outcome

   - Plan test items with no corresponding test in the change, by name.
   - Plan tasks the work departed from, and whether the work log recorded the departure.
   - Review findings that contradict a plan decision, by ID.

   ## Skill improvements

   - One concrete change to a skill or template that would have prevented a finding, saved a stage effort, or removed a template deviation, with the finding or measurement that motivates it.
   ```

   Under the first heading, assign each finding to `plan` when a decision or test the plan should have settled was missing, `work` when the plan covered it and the implementation or work log did not follow it, and `neither` when neither stage could reasonably have caught it. If the review has no findings, write `No findings.` and omit the table. Under Skill improvements, write `None.` when nothing stands out; do not invent one.

## Post

6. Create the issue. Use the measured output's first heading as the title, and the project name as the label:

   ```bash
   python3 /path/to/ktelemetry/scripts/telemetry.py post --title "<project>: <plan title>" --label <project> --body-file "$telemetry_dir/issue.md"
   ```

   The script picks a logged-in `gh` account that can see the repository, creates the label if it is missing, and prints the issue URL. Do not change anything in the project, stage anything, or commit.
7. Give the final response and stop.

## Final response

When the issue exists, reply in the form below and nothing else. Lead with the main point and write plainly.

```markdown
One or two sentences saying what the cycle cost and what stood out.

**Issue:** https://github.com/kkestell/skills-telemetry/issues/NN

**Stages found:** kplan, kwork, kreview · **Not found:** none
```

List under Not found any stage with no session on this machine, or `none`.
