#!/usr/bin/env python3
"""Measure one plan, work, and review cycle from its artifacts, Git history, and Claude Code sessions, and post the result."""

import argparse
import collections
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


TELEMETRY_REPO = "kkestell/skills-telemetry"
SKILL_NAMES = ("kplan", "kwork", "kreview", "kauto", "kexplain", "kdiscuss", "kpr")
STAGES = ("kplan", "kwork", "kreview")
# The line each skill's final response contains, which ends its window in a session.
FINAL_RESPONSE = {"kplan": "**Plan:**", "kwork": "**Work log:**", "kreview": "**Review:**"}
SKILLS_DIR = Path(__file__).resolve().parents[2]
KINDS = {"plan": "plans", "work": "work", "review": "reviews"}
TEMPLATE_SKILLS = {"plan": "kplan", "work": "kwork", "review": "kreview"}
SEQUENCE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{3}-")
PLAN_REFERENCE = re.compile(r"agents/plans/([\w.-]+)\.md")
LIST_ITEM = re.compile(r"^(?:[-*+]|\d+[.)])\s+\S")
FINDING_HEADING = re.compile(r"^F\d+\.\s")
TABLE_ROW = re.compile(r"^\|\s*(F\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|")
TEST_PATH = re.compile(r"(^|/)(tests?|spec|specs|__tests__)(/|$)|_test\.|\.test\.|\.spec\.|Tests?\.")
SLASH_COMMAND = re.compile(r"<command-name>/(k[a-z]+)</command-name>(?:.*?<command-args>(.*?)</command-args>)?", re.S)
SKILL_MENTION = re.compile(r"[/`](kplan|kwork|kreview|kexplain|kpr|kdiscuss)\b")
ACCOUNT = re.compile(r"account (\S+)")


def git(root, *args, check=True):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if check and result.returncode:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


# Artifacts


def resolve_plan(artifact):
    """Return the repository root and the plan path, relative to it, for a plan, work log, or review."""
    artifact = artifact.resolve()
    if not artifact.is_file():
        raise ValueError(f"Not a file: {artifact}")
    root = Path(git(artifact.parent, "rev-parse", "--show-toplevel").strip())
    relative = artifact.relative_to(root).as_posix()
    if relative.startswith("agents/plans/"):
        return root, relative
    match = PLAN_REFERENCE.search(artifact.read_text())
    if match and (root / "agents/plans" / f"{match.group(1)}.md").is_file():
        return root, f"agents/plans/{match.group(1)}.md"
    candidate = root / "agents/plans" / artifact.name
    if candidate.is_file():
        return root, candidate.relative_to(root).as_posix()
    raise ValueError(f"{relative} names no plan in agents/plans/")


def slug_of(path):
    return SEQUENCE.sub("", Path(path).stem)


def find_related(root, plan, directory):
    """Work logs or reviews that name the plan, or failing that share its slug."""
    folder = root / "agents" / directory
    if not folder.is_dir():
        return []
    files = sorted(f for f in folder.glob("*.md") if not f.name.startswith("_"))
    named = [f for f in files if plan in f.read_text()]
    if named:
        return [f.relative_to(root).as_posix() for f in named]
    slug = slug_of(plan)
    return [f.relative_to(root).as_posix() for f in files if slug_of(f) == slug]


def sections(text):
    """Split Markdown into (title, [(heading, body lines)]) on second-level headings."""
    title = None
    parts = []
    heading = None
    body = []
    fenced = False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("# ") and title is None:
            title = line[2:].strip()
            continue
        if not fenced and line.startswith("## "):
            if heading is not None:
                parts.append((heading, body))
            heading, body = line[3:].strip(), []
            continue
        if heading is not None:
            body.append(line)
    if heading is not None:
        parts.append((heading, body))
    return title, parts


def items(lines):
    """Top-level list items in a section, or paragraphs when the section has no list."""
    listed = paragraphs = 0
    fenced = in_paragraph = False
    for line in lines:
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if LIST_ITEM.match(line):
            listed += 1
        if line.strip():
            paragraphs += not in_paragraph
            in_paragraph = True
        else:
            in_paragraph = False
    return listed or paragraphs


def template_text(root, kind):
    local = root / "agents" / KINDS[kind] / "_template.md"
    if local.is_file():
        return local.read_text(), local.relative_to(root).as_posix()
    bundled = SKILLS_DIR / TEMPLATE_SKILLS[kind] / "assets/_template.md"
    if bundled.is_file():
        return bundled.read_text(), f"{TEMPLATE_SKILLS[kind]}/assets/_template.md"
    return None, None


def conformance(root, kind, text, headings):
    """Compare an artifact's structure with the template it should follow."""
    template, source = template_text(root, kind)
    if template is None:
        return {"template": None}
    _, template_sections = sections(template)
    expected = [h for h, _ in template_sections if not FINDING_HEADING.match(h)]
    present = set(headings)
    missing = [h for h in expected if h not in present]
    extra = [h for h in headings if h not in expected and not FINDING_HEADING.match(h)]
    guidance = []
    fenced = False
    for line in template.splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        stripped = line.strip()
        if fenced or len(stripped) < 40 or stripped.startswith(("#", "|", "-", "*", "`")):
            continue
        if stripped in text:
            guidance.append(stripped[:70])
    return {"template": source, "missing": missing, "extra": extra, "guidance_left": guidance}


def findings(parts):
    """Findings from the review's summary table, or from finding headings when the table is absent."""
    found = []
    seen = set()
    for heading, body in parts:
        if heading != "Summary":
            continue
        for line in body:
            match = TABLE_ROW.match(line)
            if match and match.group(1) not in seen:
                seen.add(match.group(1))
                found.append({
                    "id": match.group(1), "severity": match.group(2).strip(),
                    "category": match.group(3).strip(), "fix": match.group(4).strip(),
                    "title": match.group(5).strip(),
                })
    if found:
        return found
    for heading, body in parts:
        if not FINDING_HEADING.match(heading):
            continue
        identifier = heading.split(".")[0]
        meta = next((l for l in body if "·" in l), "")
        fields = [f.strip() for f in meta.split("·")]
        found.append({
            "id": identifier, "severity": fields[0] if fields else "",
            "category": fields[1] if len(fields) > 1 else "",
            "fix": fields[2] if len(fields) > 2 else "",
            "title": heading[len(identifier) + 1:].strip(),
        })
    return found


def artifact(root, relative, kind):
    text = (root / relative).read_text()
    title, parts = sections(text)
    headings = [h for h, _ in parts]
    counts = {h: items(body) for h, body in parts}
    report = {
        "path": relative, "title": title, "bytes": len(text.encode()),
        "words": len(text.split()), "lines": text.count("\n") + (not text.endswith("\n")),
        "headings": headings, "items": counts,
        "conformance": conformance(root, kind, text, headings),
    }
    if kind == "review":
        report["findings"] = findings(parts)
        report["gaps"] = counts.get("Scope and coverage", 0)
        report["checks"] = counts.get("Checks run", 0)
    if kind == "work":
        report["departures"] = counts.get("Departures from the plan", 0)
        report["decisions"] = counts.get("Decisions", 0)
        report["follow_up"] = counts.get("Follow-up work", 0)
        report["checks"] = counts.get("Checks run", 0)
        report["manual"] = counts.get("Manual verification", 0)
    if kind == "plan":
        report["tasks"] = counts.get("Implementation plan", 0)
        report["tests"] = counts.get("Test plan", 0)
        report["decisions"] = counts.get("Decisions", 0)
        report["related"] = counts.get("Related code", 0)
    return report


# Code change


def numstat(root, *args):
    added = removed = tests = 0
    files = []
    for line in git(root, *args, "--", ".", ":(exclude)agents").splitlines():
        fields = line.split("\t")
        if len(fields) != 3 or not fields[0].isdigit():
            continue
        a, r, path = int(fields[0]), int(fields[1]), fields[2]
        added += a
        removed += r
        if TEST_PATH.search(path):
            tests += a + r
        files.append(path)
    return added, removed, tests, files


def code_change(root, artifacts, commits):
    """Lines changed outside agents/, from the index plus any given commits, or from the commits that added the artifacts."""
    staged = set(git(root, "diff", "--cached", "--name-only").splitlines())
    mode = "staged" if artifacts & staged else "commits"
    if mode == "staged":
        added, removed, tests, files = numstat(root, "diff", "--cached", "--numstat")
    else:
        added = removed = tests = 0
        files = []
        if not commits:
            for path in sorted(artifacts):
                for sha in git(root, "log", "--diff-filter=A", "--format=%H", "--", path).split():
                    if sha not in commits:
                        commits.append(sha)
    described = []
    for sha in commits:
        a, r, t, f = numstat(root, "show", "--numstat", "--format=", sha)
        added += a
        removed += r
        tests += t
        files.extend(p for p in f if p not in files)
        described.append(git(root, "show", "--no-patch", "--format=%h %s", sha).strip())
    return {"mode": mode, "commits": described, "added": added, "removed": removed,
            "test_lines": tests, "files": len(files)}


# Sessions


def sessions_dir(root):
    encoded = re.sub(r"[^A-Za-z0-9-]", "-", str(root))
    return Path.home() / ".claude/projects" / encoded


def timestamp(record):
    value = record.get("timestamp")
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def records(path):
    with path.open() as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                yield record


def blocks(record):
    content = (record.get("message") or {}).get("content")
    if isinstance(content, list):
        return [b for b in content if isinstance(b, dict)]
    return []


def tool_uses(record):
    for block in blocks(record):
        if block.get("type") == "tool_use":
            yield block.get("name"), block.get("input") or {}


def marker(record, first):
    """The k-skill a record invokes and its arguments, or None."""
    if record.get("type") == "user":
        content = (record.get("message") or {}).get("content")
        if isinstance(content, str):
            match = SLASH_COMMAND.search(content)
            if match and match.group(1) in SKILL_NAMES:
                return match.group(1), match.group(2) or ""
            if first and record.get("isSidechain"):
                match = SKILL_MENTION.search(content)
                if match:
                    return match.group(1), content
    if record.get("type") == "assistant":
        for name, inputs in tool_uses(record):
            if name == "Skill" and inputs.get("skill") in SKILL_NAMES:
                return inputs["skill"], inputs.get("args") or ""
    return None


def is_prompt(record):
    """A message the user typed, as opposed to a tool result, a command, or a subagent's brief."""
    if record.get("type") != "user" or record.get("isMeta") or record.get("isCompactSummary"):
        return False
    if record.get("isSidechain") or "toolUseResult" in record:
        return False
    content = (record.get("message") or {}).get("content")
    if isinstance(content, str):
        return not content.lstrip().startswith(("<command-name>", "<local-command", "<command-message>"))
    if isinstance(content, list):
        return bool(content) and all(
            isinstance(b, dict) and b.get("type") in ("text", "image") for b in content)
    return False


def bash_writes(command, path):
    """Whether a shell command redirects, copies, moves, or stages into the artifact path."""
    target = re.escape(path)
    pattern = rf"(?:>\s*|\btee\s+(?:-a\s+)?|\b(?:mv|cp)\s+\S+\s+|\bgit add\b[^\n|;&]*\s)[\"']?\S*{target}"
    return re.search(pattern, command) is not None


def writes_artifact(record, artifacts):
    """Whether an assistant record writes one of the cycle's artifacts or reports it as a result."""
    for name, inputs in tool_uses(record):
        if name in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
            path = str(inputs.get("file_path") or "")
            if any(path.endswith(a) for a in artifacts):
                return True
        if name == "Bash":
            command = str(inputs.get("command") or "")
            if any(bash_writes(command, a) for a in artifacts):
                return True
    for block in blocks(record):
        if block.get("type") == "text":
            text = block.get("text") or ""
            if any(f"**{label}" in text and a in text for label in ("Plan:", "Work log:", "Review:")
                   for a in artifacts):
                return True
    return False


def new_window(skill, args, path, started, driver, subagent):
    return {
        "skill": skill, "args": args[:200], "file": path.name, "subagent": subagent, "driver": driver,
        "start": started, "end": started, "closed": False, "sealed": False, "requests": set(), "input": 0, "output": 0,
        "thinking": 0, "cache_read": 0, "cache_write": 0, "models": set(), "efforts": set(),
        "tools": collections.Counter(), "prompts": 0, "questions": 0, "turns": 0,
        "active_ms": 0, "compactions": 0, "compaction_tokens": 0, "agents": 0,
        "versions": set(), "branches": set(), "relevant": False,
    }


def segment(path, plan, artifacts, subagent=False, driver=None):
    """Split one transcript into windows that start at each k-skill invocation."""
    needle = Path(plan).stem
    windows = []
    window = None
    session = {"id": path.stem, "title": None, "cost": None}
    first = True
    for record in records(path):
        kind = record.get("type")
        if kind == "ai-title":
            session["title"] = record.get("aiTitle")
        if kind == "cost-state":
            session["cost"] = record
        when = timestamp(record)
        started = marker(record, first)
        first = False
        if started:
            skill, args = started
            if skill == "kauto":
                driver = "kauto"
            window = new_window(skill, args, path, when, driver if skill != "kauto" else None, subagent)
            window["relevant"] = needle in args
            windows.append(window)
            continue
        if window is None or window["sealed"]:
            continue
        if window["closed"]:
            # The turn's duration record arrives after the final response that closed the window.
            if kind == "system" and record.get("subtype") == "turn_duration":
                window["turns"] += 1
                window["active_ms"] += record.get("durationMs") or 0
            elif kind in ("user", "assistant"):
                window["sealed"] = True
            continue
        if when:
            window["end"] = when
        if record.get("version"):
            window["versions"].add(record["version"])
        if record.get("gitBranch"):
            window["branches"].add(record["gitBranch"])
        if kind == "assistant":
            message = record.get("message") or {}
            request = record.get("requestId") or message.get("id") or record.get("uuid")
            usage = message.get("usage") or {}
            if request not in window["requests"] and usage:
                window["requests"].add(request)
                window["input"] += usage.get("input_tokens") or 0
                window["output"] += usage.get("output_tokens") or 0
                window["cache_read"] += usage.get("cache_read_input_tokens") or 0
                window["cache_write"] += usage.get("cache_creation_input_tokens") or 0
                window["thinking"] += (usage.get("output_tokens_details") or {}).get("thinking_tokens") or 0
            model = message.get("model")
            if model and not model.startswith("<"):
                window["models"].add(model)
            if record.get("effort"):
                window["efforts"].add(record["effort"])
            for name, inputs in tool_uses(record):
                window["tools"][name] += 1
                if name == "AskUserQuestion":
                    window["questions"] += len(inputs.get("questions") or []) or 1
                if name == "Agent":
                    window["agents"] += 1
            if writes_artifact(record, artifacts):
                window["relevant"] = True
            final = FINAL_RESPONSE.get(window["skill"])
            if final and any(final in (b.get("text") or "") for b in blocks(record) if b.get("type") == "text"):
                window["closed"] = True
        elif kind == "user" and is_prompt(record):
            window["prompts"] += 1
        elif kind == "system":
            if record.get("subtype") == "turn_duration":
                window["turns"] += 1
                window["active_ms"] += record.get("durationMs") or 0
            if record.get("subtype") == "compact_boundary":
                window["compactions"] += 1
                window["compaction_tokens"] += (record.get("compactMetadata") or {}).get("preTokens") or 0
    return session, windows, driver


def scan_sessions(directory, plan, artifacts):
    """Windows across the project's sessions and their subagents that worked on the plan."""
    needle = Path(plan).stem
    sessions = []
    stages = []
    if not directory.is_dir():
        return sessions, stages
    for path in sorted(directory.glob("*.jsonl")):
        subagents = sorted((directory / path.stem / "subagents").glob("*.jsonl"))
        if needle not in path.read_text(errors="replace") and not any(
                needle in s.read_text(errors="replace") for s in subagents):
            continue
        session, windows, driver = segment(path, plan, artifacts)
        for sub in subagents:
            _, more, _ = segment(sub, plan, artifacts, subagent=True, driver=driver)
            windows.extend(more)
        relevant = [w for w in windows if w["relevant"] and w["requests"] and w["skill"] in STAGES]
        if not relevant:
            continue
        for window in relevant:
            window["session"] = session["id"]
            stages.append(window)
        cost = session["cost"] or {}
        sessions.append({
            "id": session["id"], "title": session["title"],
            "cost_usd": cost.get("totalCostUSD"),
            "models": sorted(cost.get("modelUsage") or []),
            "stages": [w["skill"] for w in relevant],
        })
    stages.sort(key=lambda w: (w["start"] is None, w["start"] or datetime.min))
    return sessions, stages


def skill_fingerprints():
    prints = {}
    for name in (*STAGES, "ktelemetry"):
        path = SKILLS_DIR / name / "SKILL.md"
        if path.is_file():
            prints[name] = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    return prints


# Report


def serializable(value):
    if isinstance(value, dict):
        return {k: serializable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serializable(v) for v in value]
    if isinstance(value, set):
        return sorted(serializable(v) for v in value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, collections.Counter):
        return dict(value.most_common())
    return value


def number(value):
    return f"{value:,}" if isinstance(value, int) else "–"


def duration(seconds):
    if seconds is None:
        return "–"
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60:02d}s"
    return f"{seconds // 3600}h {seconds % 3600 // 60:02d}m"


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(" -- " for _ in headers) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def markdown(report):
    plan, works, reviews, change = report["plan"], report["work"], report["reviews"], report["code"]
    out = [f"# {report['project']}: {plan['title'] or slug_of(plan['path'])}", ""]
    paths = [f"**Plan:** `{plan['path']}`"]
    paths += [f"**Work:** `{w['path']}`" for w in works] or ["**Work:** none"]
    paths += [f"**Review:** `{r['path']}`" for r in reviews] or ["**Review:** none"]
    out.append(" · ".join(paths))
    if change["mode"] == "staged":
        measured = "staged changes" + "".join(f", `{c}`" for c in change["commits"])
    elif change["commits"]:
        measured = "commits " + ", ".join(f"`{c}`" for c in change["commits"])
    else:
        measured = "no commits found"
    out.append(f"**Project:** `{report['root']}` · **Branch:** {report['branch']} · **Measured from:** {measured}")
    out.append("**Skills:** " + " · ".join(f"{k} `{v}`" for k, v in report["skills"].items()))
    out.append("")

    out += ["## Sizes", ""]
    rows = [["Plan", number(plan["bytes"]), number(plan["words"]), number(plan["lines"])]]
    rows += [["Work log", number(w["bytes"]), number(w["words"]), number(w["lines"])] for w in works]
    rows += [["Review", number(r["bytes"]), number(r["words"]), number(r["lines"])] for r in reviews]
    out.append(table(["Artifact", "Bytes", "Words", "Lines"], rows))
    out.append("")
    code_lines = change["added"] + change["removed"]
    out.append(f"**Code change:** +{change['added']} / −{change['removed']} lines in {change['files']} files, "
               f"{change['test_lines']} of them in tests, excluding `agents/`.")
    total = plan["bytes"] + sum(w["bytes"] for w in works) + sum(r["bytes"] for r in reviews)
    ratio = f"{total / code_lines:.0f}" if code_lines else "–"
    out.append(f"**Artifact bytes per changed code line:** {ratio} · "
               f"**Review bytes per plan byte:** {sum(r['bytes'] for r in reviews) / plan['bytes']:.1f}")
    out.append("")

    out += ["## Stages", ""]
    if report["stages"]:
        rows = []
        for w in report["stages"]:
            wall = (w["end"] - w["start"]).total_seconds() if w["start"] and w["end"] else None
            # Turn durations span a whole user turn, which under kauto covers every stage at once.
            interactive = w["turns"] and w["driver"] != "kauto"
            rows.append([
                w["skill"] + (" (subagent)" if w["subagent"] else ""), f"`{w['session'][:8]}`",
                w["driver"] or "user",
                f"{', '.join(sorted(w['models'])) or '–'} · {', '.join(sorted(w['efforts'])) or '–'}",
                duration(wall), duration(w["active_ms"] / 1000) if interactive else "–",
                w["turns"] if interactive else "–", w["prompts"], w["questions"], sum(w["tools"].values()), w["agents"],
                f"{w['compactions']} ({number(w['compaction_tokens'])} tokens)" if w["compactions"] else 0,
                number(w["input"]), number(w["cache_read"]), number(w["cache_write"]), number(w["output"]),
                number(w["thinking"]),
            ])
        out.append(table(["Stage", "Session", "Driver", "Model · effort", "Wall", "Active", "Turns", "Prompts",
                          "Questions", "Tool calls", "Subagents", "Compactions", "Input", "Cache read",
                          "Cache write", "Output", "Thinking"], rows))
        out.append("")
        tools = collections.Counter()
        for w in report["stages"]:
            tools.update(w["tools"])
        out.append("**Tool calls:** " + ", ".join(f"{n} {c}" for n, c in tools.most_common()))
        out.append("")
        rows = [[f"`{s['id'][:8]}`", s["title"] or "–", ", ".join(s["stages"]),
                 f"${s['cost_usd']:.2f}" if s["cost_usd"] is not None else "–",
                 ", ".join(s["models"]) or "–"] for s in report["sessions"]]
        out.append(table(["Session", "Title", "Stages here", "Whole-session cost", "Models"], rows))
        out.append("")
    found = {w["skill"] for w in report["stages"]}
    absent = [s for s in STAGES if s not in found]
    if absent:
        out.append(f"**No session found for:** {', '.join(absent)} (searched `{report['sessions_dir']}`).")
        out.append("")

    out += ["## Review findings", ""]
    for review in reviews:
        if len(reviews) > 1:
            out += [f"`{review['path']}`", ""]
        if review["findings"]:
            out.append(table(["ID", "Severity", "Category", "Fix", "Title"],
                             [[f["id"], f["severity"], f["category"], f["fix"], f["title"]]
                              for f in review["findings"]]))
            out.append("")
            severity = collections.Counter(f["severity"] for f in review["findings"])
            fixes = collections.Counter(f["fix"] for f in review["findings"])
            out.append(f"**By severity:** {', '.join(f'{c} {s}' for s, c in severity.most_common())} · "
                       f"**By fix label:** {', '.join(f'{c} {s}' for s, c in fixes.most_common())}")
        elif review["conformance"].get("extra"):
            out.append("No findings parsed: the review has no template summary table. Read it for the findings.")
        else:
            out.append("No findings.")
        out += [f"**Coverage gaps:** {review['gaps']} · **Checks run:** {review['checks']}", ""]
    if not reviews:
        out += ["No review.", ""]

    out += ["## Work log", ""]
    for work in works:
        out.append(f"**Departures:** {work['departures']} · **Decisions:** {work['decisions']} · "
                   f"**Follow-up:** {work['follow_up']} · **Checks run:** {work['checks']} · "
                   f"**Manual verification:** {work['manual']}")
    if not works:
        out.append("No work log.")
    out.append("")

    out += ["## Plan", ""]
    out.append(f"**Tasks:** {plan['tasks']} · **Test plan items:** {plan['tests']} · "
               f"**Decisions:** {plan['decisions']} · **Related code entries:** {plan['related']}")
    out.append("")

    out += ["## Template conformance", ""]
    rows = []
    for label, group in (("Plan", [plan]), ("Work log", works), ("Review", reviews)):
        for a in group:
            c = a["conformance"]
            if c.get("template") is None:
                rows.append([label, "–", "no template found", "", ""])
                continue
            rows.append([label, f"`{c['template']}`", ", ".join(c["missing"]) or "none",
                         ", ".join(c["extra"]) or "none", str(len(c["guidance_left"]))])
    out.append(table(["Artifact", "Template", "Missing sections", "Extra headings", "Guidance lines left in"], rows))
    out.append("")
    return "\n".join(out)


def measure(args):
    root, plan = resolve_plan(args.artifact)
    works = find_related(root, plan, "work")
    reviews = find_related(root, plan, "reviews")
    artifacts = {plan, *works, *reviews}
    directory = args.sessions or sessions_dir(root)
    sessions, stages = scan_sessions(directory, plan, artifacts)
    return {
        "project": root.name, "root": str(root),
        "branch": git(root, "rev-parse", "--abbrev-ref", "HEAD", check=False).strip() or "–",
        "skills": skill_fingerprints(),
        "plan": artifact(root, plan, "plan"),
        "work": [artifact(root, w, "work") for w in works],
        "reviews": [artifact(root, r, "review") for r in reviews],
        "code": code_change(root, artifacts, list(args.commit)),
        "sessions_dir": str(directory), "sessions": sessions, "stages": stages,
    }


# GitHub


def gh(args, token=None):
    env = dict(os.environ)
    if token:
        env["GH_TOKEN"] = token
    return subprocess.run(["gh", *args], capture_output=True, text=True, env=env)


def telemetry_account():
    """A (name, token) pair for a logged-in gh account that can see the telemetry repository."""
    status = gh(["auth", "status"])
    accounts = ACCOUNT.findall(status.stdout + status.stderr)
    if gh(["repo", "view", TELEMETRY_REPO, "--json", "nameWithOwner"]).returncode == 0:
        return "active account", None
    for name in accounts:
        token = gh(["auth", "token", "--user", name]).stdout.strip()
        if token and gh(["repo", "view", TELEMETRY_REPO, "--json", "nameWithOwner"], token).returncode == 0:
            return name, token
    raise ValueError(f"No logged-in gh account can see {TELEMETRY_REPO}; this skill is for its owner")


def check(_args):
    name, _ = telemetry_account()
    print(f"{TELEMETRY_REPO} via {name}")
    return 0


def post(args):
    body = args.body_file.read_text()
    if not body.strip():
        raise ValueError("The issue body is empty")
    _, token = telemetry_account()
    label = gh(["label", "create", args.label, "-R", TELEMETRY_REPO, "--force"], token)
    if label.returncode:
        raise ValueError(f"Could not create label {args.label}: {label.stderr.strip()}")
    issue = gh(["issue", "create", "-R", TELEMETRY_REPO, "--title", args.title, "--label", args.label,
                "--body-file", str(args.body_file)], token)
    if issue.returncode:
        raise ValueError(f"Could not create the issue: {issue.stderr.strip()}")
    print(issue.stdout.strip())
    return 0


def run_measure(args):
    report = measure(args)
    if args.json:
        print(json.dumps(serializable(report), indent=2))
    else:
        print(markdown(report))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    measuring = commands.add_parser("measure", help="Print the measured part of the issue as Markdown")
    measuring.add_argument("artifact", type=Path, help="A plan, work log, or review in agents/")
    measuring.add_argument("--commit", action="append", default=[], metavar="SHA",
                           help="Add these commits to the staged changes, or measure them instead of the artifact commits")
    measuring.add_argument("--sessions", type=Path, help="Claude Code project directory to scan instead of the default")
    measuring.add_argument("--json", action="store_true", help="Print the measurements as JSON")
    measuring.set_defaults(run=run_measure)
    checking = commands.add_parser("check", help=f"Exit 0 if a logged-in gh account can see {TELEMETRY_REPO}")
    checking.set_defaults(run=check)
    posting = commands.add_parser("post", help=f"Create an issue in {TELEMETRY_REPO}")
    posting.add_argument("--title", required=True)
    posting.add_argument("--label", required=True, help="Usually the project name")
    posting.add_argument("--body-file", required=True, type=Path)
    posting.set_defaults(run=post)
    args = parser.parse_args()
    return args.run(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Telemetry failed: {error}", file=sys.stderr)
        sys.exit(1)
