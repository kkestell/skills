"""Tests for measuring a plan, work, and review cycle from artifacts, Git, and session files."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import telemetry


PLAN = "agents/plans/2026-10-20-001-export.md"
WORK = "agents/work/2026-10-20-001-export.md"
REVIEW = "agents/reviews/2026-10-20-002-export-second-pass.md"


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True,
                   env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
                        "GIT_COMMITTER_EMAIL": "t@t", "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"})


def write(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def record(kind, when, **fields):
    return {"type": kind, "timestamp": f"2026-10-20T{when}Z", **fields}


def assistant(when, request, content, usage=None, model="claude-fable-5-1"):
    usage = usage or {"input_tokens": 10, "output_tokens": 20, "cache_read_input_tokens": 1000,
                      "cache_creation_input_tokens": 100, "output_tokens_details": {"thinking_tokens": 5}}
    return record("assistant", when, requestId=request, effort="high",
                  message={"model": model, "usage": usage, "content": content})


def user(when, content, **fields):
    return record("user", when, message={"role": "user", "content": content}, **fields)


def slash(when, skill, args):
    return user(when, f"<command-name>/{skill}</command-name>\n<command-args>{args}</command-args>")


class CycleTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name).resolve() / "project"
        self.root.mkdir()
        git(self.root, "init", "-q")
        write(self.root, PLAN, "# CSV export\n\n## Goal\n\nExport.\n\n## Decisions\n\nOne paragraph.\n\n"
              "Another paragraph.\n\n## Test plan\n\n- Exports a row.\n- Rejects a bad path.\n\n"
              "## Implementation plan\n\n1. Add the writer.\n2. Wire the command.\n")
        write(self.root, "src/export.py", "def export():\n    return 1\n")
        write(self.root, "tests/test_export.py", "def test_export():\n    assert True\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-q", "-m", "Add CSV export")
        write(self.root, WORK, f"# CSV export\n\n## Plan\n\n`{PLAN}`\n\n## Summary\n\nDone.\n\n"
              "## Departures from the plan\n\n- Skipped the bad path test.\n\n## Checks run\n\n- `pytest` — passed.\n")
        write(self.root, REVIEW, f"# CSV export review\n\n## Scope and coverage\n\nStaged changes for `{PLAN}`.\n\n"
              "Gaps:\n\n- Windows paths.\n\n## Summary\n\n| ID | Severity | Category | Fix | Title |\n"
              "| -- | -- | -- | -- | -- |\n| F1 | High | Correctness | Fixed | Drops the header |\n"
              "| F2 | Low | Testing | Fixed | No bad path test |\n\n## F1. Drops the header\n\nHigh · Correctness · Fixed\n\n"
              "## F2. No bad path test\n\nLow · Testing · Fixed\n\n## Checks run\n\n- `pytest` — passed.\n\n"
              "## Verdict\n\nFixed.\n")
        write(self.root, "src/export.py", "def export():\n    return 2\n\n\ndef header():\n    return 'h'\n")
        self.sessions = Path(self.directory.name) / "sessions"
        (self.sessions / "main" / "subagents").mkdir(parents=True)

    def tearDown(self):
        self.directory.cleanup()

    def args(self, artifact=PLAN, commit=()):
        return argparse.Namespace(artifact=self.root / artifact, commit=list(commit), sessions=self.sessions)

    def session(self, name, lines):
        path = self.sessions / f"{name}.jsonl" if "/" not in name else self.sessions / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(line) + "\n" for line in lines))

    def test_resolves_the_plan_from_a_work_log_or_review_and_finds_related_artifacts(self):
        for artifact in (PLAN, WORK, REVIEW):
            with self.subTest(artifact=artifact):
                root, plan = telemetry.resolve_plan(self.root / artifact)
                self.assertEqual((root, plan), (self.root, PLAN))
        self.assertEqual(telemetry.find_related(self.root, PLAN, "work"), [WORK])
        self.assertEqual(telemetry.find_related(self.root, PLAN, "reviews"), [REVIEW])

    def test_measures_staged_changes_when_the_review_is_staged(self):
        git(self.root, "add", ".")
        report = telemetry.measure(self.args())
        self.assertEqual(report["code"]["mode"], "staged")
        self.assertEqual((report["code"]["added"], report["code"]["removed"], report["code"]["files"]), (5, 1, 1))
        self.assertEqual(report["plan"]["tasks"], 2)
        self.assertEqual(report["plan"]["tests"], 2)
        self.assertEqual(report["plan"]["decisions"], 2)
        self.assertEqual(report["work"][0]["departures"], 1)
        review = report["reviews"][0]
        self.assertEqual([f["id"] for f in review["findings"]], ["F1", "F2"])
        self.assertEqual(review["findings"][0]["severity"], "High")
        self.assertEqual(review["gaps"], 1)
        self.assertIn("Verdict", review["headings"])

    def test_adds_commits_made_during_the_cycle_to_the_staged_changes(self):
        git(self.root, "add", "src/export.py")
        git(self.root, "commit", "-q", "-m", "Deploy")
        sha = telemetry.git(self.root, "rev-parse", "--short", "HEAD").strip()
        write(self.root, "src/late.py", "x = 1\n")
        git(self.root, "add", ".")
        report = telemetry.measure(self.args(commit=[sha]))
        self.assertEqual(report["code"]["mode"], "staged")
        self.assertEqual((report["code"]["added"], report["code"]["removed"], report["code"]["files"]), (6, 1, 2))
        self.assertIn(f"**Measured from:** staged changes, `{sha} Deploy`", telemetry.markdown(report))

    def test_measures_the_commits_that_added_the_artifacts_once_committed(self):
        git(self.root, "add", ".")
        git(self.root, "commit", "-q", "-m", "Implement and review")
        report = telemetry.measure(self.args(REVIEW))
        self.assertEqual(report["code"]["mode"], "commits")
        self.assertEqual(len(report["code"]["commits"]), 2)
        self.assertEqual((report["code"]["added"], report["code"]["removed"]), (9, 1))
        self.assertEqual(report["code"]["test_lines"], 2)
        markdown = telemetry.markdown(report)
        self.assertIn("# project: CSV export", markdown)
        self.assertIn("| F1 | High | Correctness | Fixed | Drops the header |", markdown)
        self.assertIn("**No session found for:** kplan, kwork, kreview", markdown)

    def test_reports_template_conformance(self):
        report = telemetry.measure(self.args())
        review = report["reviews"][0]["conformance"]
        self.assertEqual(review["missing"], [])
        self.assertEqual(review["extra"], [])
        work = report["work"][0]["conformance"]
        self.assertIn("Manual verification", work["missing"])
        write(self.root, WORK, (self.root / WORK).read_text() + "\n## Notes\n\nKeep the log short. Record what "
              "the plan and the diff do not show. Delete unused headings and placeholder text, including this guidance.\n")
        work = telemetry.measure(self.args())["work"][0]["conformance"]
        self.assertEqual(work["extra"], ["Notes"])
        self.assertEqual(len(work["guidance_left"]), 1)

    def test_attributes_session_windows_to_stages(self):
        plan_text = [{"type": "text", "text": f"Planned.\n\n**Plan:** `{PLAN}`\n\n**Next:** `/kwork {PLAN}`"}]
        self.session("main", [
            record("ai-title", "10:00:00", aiTitle="Export work"),
            slash("10:00:01", "kplan", "add CSV export"),
            user("10:00:02", "Use commas.", origin={"kind": "human"}),
            assistant("10:00:03", "r1", [{"type": "tool_use", "name": "AskUserQuestion",
                                         "input": {"questions": [{"question": "Quote fields?"}]}}]),
            assistant("10:00:03", "r1", [{"type": "text", "text": "Asking."}]),
            assistant("10:00:04", "r2", [{"type": "tool_use", "name": "Write", "input": {"file_path": str(self.root / PLAN)}}]),
            record("system", "10:00:05", subtype="turn_duration", durationMs=4000),
            assistant("10:00:06", "r3", plan_text),
            user("10:05:00", "Unrelated chat after the plan.", origin={"kind": "human"}),
            assistant("10:05:01", "r4", [{"type": "text", "text": "Sure."}]),
            slash("10:10:00", "kwork", PLAN),
            record("system", "10:10:01", subtype="compact_boundary", compactMetadata={"preTokens": 150000}),
            assistant("10:10:02", "r5", [{"type": "tool_use", "name": "Bash", "input": {"command": "cat > src/export.py <<'EOF'\nx\nEOF"}}]),
            assistant("10:10:03", "r6", [{"type": "tool_use", "name": "Agent", "input": {"description": "Review"}}]),
            assistant("10:10:04", "r7", [{"type": "text", "text": f"Built.\n\n**Work log:** `{WORK}`"}]),
            slash("10:20:00", "kplan", "something else entirely"),
            assistant("10:20:01", "r8", [{"type": "tool_use", "name": "Bash", "input": {"command": f"cat {PLAN}"}}]),
            record("cost-state", "10:20:02", totalCostUSD=1.5, modelUsage={"claude-fable-5-1": {}}),
        ])
        self.session("main/subagents/agent-1.jsonl", [
            user("10:10:03", f"Run the `/kreview` skill with `staged changes for {PLAN}`.", isSidechain=True),
            assistant("10:10:05", "s1", [{"type": "tool_use", "name": "Bash", "input": {"command": "git diff --cached"}}],
                      model="claude-opus-5-5"),
            assistant("10:10:06", "s2", [{"type": "text", "text": f"Reviewed.\n\n**Review:** `{REVIEW}`"}],
                      model="claude-opus-5-5"),
        ])
        report = telemetry.measure(self.args())
        stages = {(w["skill"], w["subagent"]): w for w in report["stages"]}
        self.assertEqual(set(stages), {("kplan", False), ("kwork", False), ("kreview", True)})
        plan = stages[("kplan", False)]
        self.assertEqual((plan["prompts"], plan["questions"], plan["turns"], plan["active_ms"]), (1, 1, 1, 4000))
        self.assertEqual(len(plan["requests"]), 3, "usage is counted once per request")
        self.assertEqual((plan["input"], plan["output"], plan["thinking"]), (30, 60, 15))
        self.assertEqual(plan["end"].strftime("%H:%M:%S"), "10:00:06", "the window ends at the final response")
        work = stages[("kwork", False)]
        self.assertEqual((work["compactions"], work["compaction_tokens"], work["agents"]), (1, 150000, 1))
        review = stages[("kreview", True)]
        self.assertEqual((review["prompts"], review["models"]), (0, {"claude-opus-5-5"}))
        self.assertEqual(report["sessions"][0]["cost_usd"], 1.5)
        self.assertEqual(report["sessions"][0]["stages"], ["kplan", "kwork", "kreview"])
        markdown = telemetry.markdown(report)
        self.assertIn("| kreview (subagent) | `main` | user |", markdown)
        self.assertNotIn("No session found", markdown)


if __name__ == "__main__":
    unittest.main()
