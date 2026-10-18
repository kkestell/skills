#!/usr/bin/env python3
"""Send one discussion turn to a pinned CLI agent and preserve its session."""

import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import uuid


MAX_TURNS = 6
MODELS = {
    "claude": "fable",
    "codex": "gpt-6.1-sol",
    # OpenCode's catalog ID for DeepSeek V4.1 Flash.
    "opencode": "deepseek/deepseek-flash",
}
RULES = Path(__file__).resolve().parents[1] / "references/discussion-rules.md"
# Read-only git forms OpenCode may run; any other shell command is denied.
OPENCODE_SHELL = [
    "git log *", "git show *", "git diff *", "git status *", "git blame *",
    "git grep *", "git ls-files *", "git rev-parse *",
]


def command(state):
    agent = state["agent"]
    session = state["session_id"]
    if agent == "claude":
        args = [
            "claude", "-p", "--model", MODELS[agent], "--effort", "high",
            "--output-format", "json",
            # dontAsk denies any call that would prompt, so only workspace reads
            # and Claude Code's built-in read-only shell commands run.
            "--tools", "Read,Grep,Glob,Bash", "--permission-mode", "dontAsk",
            "--disallowedTools", "Edit,Write,NotebookEdit",
            "--disable-slash-commands",
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
        ]
        args += ["--resume", session] if session else ["--session-id", state["claude_id"]]
        return args
    if agent == "codex":
        args = ["codex", "exec"] + (["resume"] if session else [])
        args += [
            "--model", MODELS[agent], "--json", "--skip-git-repo-check",
            "-c", 'model_provider="openai"',
            "-c", 'model_reasoning_effort="high"',
            # Resume reads these overrides too, so every turn stays read-only.
            "-c", 'sandbox_mode="read-only"', "-c", 'approval_policy="never"',
            "-c", 'web_search="disabled"',
        ]
        return args + ([session, "-"] if session else ["-"])
    args = [
        "opencode", "run", "--model", MODELS[agent], "--variant", "max",
        "--format", "json", "--agent", "kdiscuss",
    ]
    return args + (["--session", session] if session else [])


def environment(agent):
    env = os.environ.copy()
    if agent == "opencode":
        # Merge runtime overrides without writing the user's OpenCode config.
        config = json.loads(env.get("OPENCODE_CONFIG_CONTENT", "{}"))
        config["share"] = "disabled"
        # The last matching rule wins, so specific rules follow the defaults.
        shell = {"*": "deny", **dict.fromkeys(OPENCODE_SHELL, "allow")}
        shell.update({"*>*": "deny", "*--output*": "deny"})
        config.setdefault("agent", {})["kdiscuss"] = {
            "mode": "primary",
            "permission": {
                "*": "deny", "read": "allow", "glob": "allow", "grep": "allow",
                "list": "allow", "bash": shell, "external_directory": "deny",
            },
            "prompt": (
                "Discuss the supplied proposal. Inspect the workspace with read-only "
                "tools to verify claims. Do not modify anything."
            ),
        }
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps(config)
    return env


def parse_reply(agent, output, state):
    if agent == "claude":
        result = json.loads(output)
        if not isinstance(result, dict):
            raise ValueError("Claude returned an unexpected JSON result")
        session = result.get("session_id")
        if session:
            check_session(state, session)
        if result.get("is_error") or result.get("subtype") != "success":
            raise ValueError("Claude failed: " + str(result.get("result") or result))
        if session != state["claude_id"]:
            raise ValueError("Claude returned an unexpected session ID")
        return result.get("result", "").strip()

    replies = []
    complete = False
    errors = []
    for line in output.splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if not isinstance(event, dict):
            raise ValueError("The CLI returned an unexpected JSON event")
        kind = event.get("type")
        session = event.get("thread_id") if agent == "codex" else event.get("sessionID")
        if session:
            check_session(state, session)
        if kind in ("error", "turn.failed"):
            errors.append(str(event.get("error") or event.get("message") or event))
        if agent == "codex":
            item = event.get("item", {})
            if kind == "item.completed" and item.get("type") == "agent_message":
                # Commentary is not the final answer when the CLI supplies a phase.
                if item.get("phase") != "commentary":
                    replies.append(item.get("text", ""))
            complete |= kind == "turn.completed"
        else:
            part = event.get("part", {})
            if kind == "text":
                replies.append(part.get("text", ""))
            complete |= kind == "step_finish" and part.get("reason") == "stop"
    if errors:
        raise ValueError("; ".join(errors))
    if not complete:
        raise ValueError("The CLI did not report a completed turn")
    return "\n\n".join(replies).strip()


def check_session(state, session):
    if state["session_id"] and state["session_id"] != session:
        raise ValueError("The CLI changed the discussion session")
    state["session_id"] = session


def save(path, state):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n")
    temporary.chmod(0o600)
    temporary.replace(path)


def run_turn(args, state, message):
    env = environment(state["agent"])
    process = subprocess.Popen(
        command(state), cwd=state["cwd"], env=env, text=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        output, diagnostic = process.communicate(message, timeout=args.timeout)
    except (subprocess.TimeoutExpired, KeyboardInterrupt):
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        raise ValueError("Turn interrupted; delivery is uncertain. Do not resend it.")
    try:
        reply = parse_reply(state["agent"], output, state)
    except ValueError as error:
        if process.returncode:
            raise ValueError(f"CLI exited {process.returncode}: {diagnostic.strip() or str(error)}") from error
        raise
    if process.returncode:
        raise ValueError(f"CLI exited {process.returncode}: {diagnostic.strip()}")
    if not state["session_id"] or not reply:
        raise ValueError("The CLI returned no session ID or no reply")
    return reply


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=MODELS)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=600, help="Seconds per CLI turn")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    message = sys.stdin.read().strip()
    if not message:
        parser.error("Provide a nonempty message on standard input")
    path = args.state.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix(".lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("Another turn is already using this state file")
        if path.exists():
            state = json.loads(path.read_text())
            if args.agent and args.agent != state["agent"]:
                parser.error("Cannot change agents during a discussion")
            if state["cwd"] != str(Path.cwd().resolve()):
                parser.error("Resume from the original workspace directory")
            if state["status"] != "ready":
                parser.error("Previous delivery is uncertain or failed; do not resend or restart")
            if not state["session_id"]:
                parser.error("No session ID to resume")
        else:
            if not args.agent:
                parser.error("--agent is required for the opening turn")
            state = {
                "agent": args.agent, "cwd": str(Path.cwd().resolve()),
                "session_id": None, "claude_id": str(uuid.uuid4()),
                "turns": 0, "status": "ready", "messages": [],
            }
            message = RULES.read_text().strip() + "\n\nOpening message:\n\n" + message
        if state["turns"] >= MAX_TURNS:
            parser.error("Six peer replies reached; finish with agreement or unresolved questions")
        if not shutil.which(state["agent"]):
            parser.error(f"Required CLI is not installed: {state['agent']}")
        message += f"\n\nPeer reply {state['turns'] + 1} of {MAX_TURNS}."
        if state["turns"] + 1 == MAX_TURNS:
            message += " This is the final reply; state agreement or the remaining disagreement."
        state["status"] = "pending"
        state["messages"].append({"role": "user", "content": message})
        save(path, state)
        try:
            reply = run_turn(args, state, message)
        except (OSError, ValueError) as error:
            state["status"] = "failed"
            state["error"] = str(error)
            save(path, state)
            print(f"Discussion stopped: {error}\nState: {path}", file=sys.stderr)
            return 1
        state["turns"] += 1
        state["status"] = "ready"
        state["messages"].append({"role": "assistant", "content": reply})
        save(path, state)
        print(reply)
        print(f"State: {path} · Peer replies: {state['turns']}/{MAX_TURNS}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f"Discussion stopped: {error}", file=sys.stderr)
        sys.exit(1)
