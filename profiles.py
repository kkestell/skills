#!/usr/bin/env python3

import argparse
import json
import shlex
import subprocess
import tomllib
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent
SKILLS_CLI = ("npx", "-y", "skills@latest")
CANONICAL_SKILLS = ".agents/skills"
SKILL_GROUPS = ("core", "ext", "wip")

# The harnesses this script understands: the directory under the home directory
# where each keeps its configuration, and the name the skills CLI installs it
# by. A --<name> flag selects the harness on every command.
HARNESSES = {
    "claude": {"directory": ".claude", "agent": "claude-code"},
    "codex": {"directory": ".codex", "agent": "codex"},
    "copilot": {"directory": ".copilot", "agent": "github-copilot"},
}


def harness_directory(harness, home_directory=None):
    home_directory = home_directory or Path.home()
    return home_directory / HARNESSES[harness]["directory"]


def selected_harnesses(args):
    """Harnesses named by --<name> flags, or every harness when none are given."""
    chosen = [harness for harness in HARNESSES if getattr(args, harness)]
    return chosen or list(HARNESSES)


def selected_skill_groups(values):
    """Normalize comma- or space-separated skill groups in argument order."""
    selected = []
    for value in values:
        for group in value.split(","):
            group = group.strip()
            if not group:
                raise ValueError("skill groups cannot be empty")
            if group not in SKILL_GROUPS:
                choices = ", ".join(SKILL_GROUPS)
                raise ValueError(f"unknown skill group '{group}'; choose from: {choices}")
            if group not in selected:
                selected.append(group)
    return selected


def hook_configs(harness, directory):
    if harness == "claude":
        paths = [directory / "settings.json"]
    elif harness == "codex":
        paths = [directory / "hooks.json", directory / "config.toml"]
    else:
        paths = [directory / "settings.json", *(directory / "hooks").glob("*.json")]

    for path in paths:
        if not path.is_file():
            continue
        with path.open("rb") as file:
            data = tomllib.load(file) if path.suffix == ".toml" else json.load(file)
        yield path, data.get("hooks", {})


def read_json(path):
    if not path.is_file():
        return {}
    with path.open() as file:
        return json.load(file)


def read_toml(path):
    if not path.is_file():
        return {}
    with path.open("rb") as file:
        return tomllib.load(file)


def skill_files(root):
    directories = [root]
    visited = set()

    while directories:
        directory = directories.pop()
        try:
            stat = directory.stat()
        except OSError:
            continue

        identity = (stat.st_dev, stat.st_ino)
        if identity in visited:
            continue
        visited.add(identity)

        skill_file = directory / "SKILL.md"
        if skill_file.is_file():
            yield skill_file

        try:
            directories.extend(path for path in directory.iterdir() if path.is_dir())
        except OSError:
            continue


def plugin_inventory(harness, directory):
    settings = read_json(directory / "settings.json")
    enabled = settings.get("enabledPlugins", {})

    if harness == "claude":
        known = read_json(directory / "plugins/known_marketplaces.json")
        installed = read_json(directory / "plugins/installed_plugins.json").get("plugins", {})
        marketplaces = set(known) | set(settings.get("extraKnownMarketplaces", {}))
        plugin_ids = set(installed) | set(enabled)
        roots = {
            plugin_id: [Path(item["installPath"]) for item in items if item.get("installPath")]
            for plugin_id, items in installed.items()
        }
    elif harness == "codex":
        config = read_toml(directory / "config.toml")
        marketplaces = {"openai-curated", *config.get("marketplaces", {})}
        configured = config.get("plugins", {})
        plugin_ids = set(configured)
        enabled = {
            plugin_id: value.get("enabled", True) if isinstance(value, dict) else bool(value)
            for plugin_id, value in configured.items()
        }
        roots = {}
        for plugin_id in plugin_ids:
            name, _, marketplace = plugin_id.partition("@")
            roots[plugin_id] = [directory / "plugins/cache" / marketplace / name]
    else:
        marketplaces = {"copilot-plugins", "awesome-copilot"}
        marketplaces |= set(settings.get("extraKnownMarketplaces", {}))
        roots = {}
        installed_root = directory / "installed-plugins"
        for marketplace in installed_root.iterdir() if installed_root.is_dir() else []:
            if not marketplace.is_dir() or marketplace.name.startswith("."):
                continue
            for plugin in marketplace.iterdir():
                if plugin.is_dir() and not plugin.name.startswith("."):
                    plugin_id = f"{plugin.name}@{marketplace.name}"
                    roots[plugin_id] = [plugin]
        plugin_ids = set(roots) | set(enabled)

    plugins = [(plugin_id, enabled.get(plugin_id, True), roots.get(plugin_id, [])) for plugin_id in plugin_ids]
    return sorted(marketplaces), sorted(plugins)


def skill_inventory(harness, directory):
    roots = [(directory / "skills", "", "")]
    if harness in {"codex", "copilot"}:
        roots.append((directory.parent / CANONICAL_SKILLS, "", ""))

    for plugin_id, is_enabled, plugin_roots in plugin_inventory(harness, directory)[1]:
        suffix = " (disabled)" if not is_enabled else ""
        roots.extend((root, f"{plugin_id}:", suffix) for root in plugin_roots)

    skills = set()
    for root, prefix, suffix in roots:
        if not root.is_dir():
            continue
        for skill_file in skill_files(root):
            name = skill_file.parent.name
            skills.add(f"{prefix}{name}{suffix}")
    return sorted(skills)


def mcp_inventory(harness, directory):
    if harness == "claude":
        servers = read_json(directory.parent / ".claude.json").get("mcpServers", {})
    elif harness == "codex":
        servers = read_toml(directory / "config.toml").get("mcp_servers", {})
    else:
        servers = read_json(directory / "mcp-config.json").get("mcpServers", {})

    if not isinstance(servers, dict):
        raise TypeError("MCP servers configuration must be a table or object")
    return sorted(servers)


def hook_lines(hooks):
    for event, groups in hooks.items():
        if not isinstance(groups, list):
            continue
        for group in groups:
            if not isinstance(group, dict):
                continue
            matcher = group.get("matcher") or "*"
            handlers = group["hooks"] if isinstance(group.get("hooks"), list) else [group]
            for hook in handlers:
                if not isinstance(hook, dict):
                    continue
                action = next(
                    (hook[key] for key in ("command", "bash", "powershell", "url", "prompt", "tool") if hook.get(key)),
                    hook.get("type", "unknown"),
                )
                if hook.get("args"):
                    action += " " + shlex.join(map(str, hook["args"]))
                yield f"{event}[{matcher}] {action}"


def print_lines(harness, directory, lines):
    if not lines:
        print(f"{harness} {directory}: none")
        return
    print(f"{harness} {directory}")
    for line in lines:
        print(f"  {line}")


def report(args, describe):
    """Print one report per selected harness, collected by describe()."""
    for harness in selected_harnesses(args):
        directory = harness_directory(harness)
        try:
            lines = describe(harness, directory)
        except (OSError, ValueError, TypeError) as error:
            lines = [f"error: {error}"]
        print_lines(harness, directory, lines)


def print_hooks(args):
    def describe(harness, directory):
        lines = []
        for _source, hooks in hook_configs(harness, directory):
            lines.extend(hook_lines(hooks))
        return lines

    report(args, describe)


def print_plugins(args):
    def describe(harness, directory):
        marketplaces, plugins = plugin_inventory(harness, directory)
        lines = [f"marketplace {name}" for name in marketplaces]
        lines += [f"plugin {name}{'' if enabled else ' (disabled)'}" for name, enabled, _ in plugins]
        return lines

    report(args, describe)


def print_skills(args):
    report(args, lambda harness, directory: [f"skill {name}" for name in skill_inventory(harness, directory)])


def print_mcp(args):
    report(args, lambda harness, directory: [f"server {name}" for name in mcp_inventory(harness, directory)])


def sync_repository_skills(
    harnesses,
    groups,
    repository_root=None,
    home_directory=None,
    runner=subprocess.run,
):
    """Make the chosen harnesses contain exactly the selected skill groups."""
    repository_root = repository_root or REPOSITORY_ROOT
    home_directory = home_directory or Path.home()
    skills_directory = repository_root / "skills"
    canonical_directory = home_directory / CANONICAL_SKILLS

    if not skills_directory.is_dir():
        raise FileNotFoundError(f"skills directory not found: {skills_directory}")

    group_directories = []
    for group in groups:
        group_directory = skills_directory / group
        if not group_directory.is_dir():
            raise FileNotFoundError(f"skill group directory not found: {group_directory}")
        group_directories.append((group, group_directory))

    agents = [HARNESSES[harness]["agent"] for harness in harnesses]
    for group, group_directory in group_directories:
        print(f"Installing {group} skills into {', '.join(agents)}")
        runner(
            [
                *SKILLS_CLI,
                "add",
                str(group_directory),
                "--skill",
                "*",
                "--agent",
                *agents,
                "--global",
                "--yes",
            ],
            check=True,
        )

    selected_skills = {
        path.name
        for _group, group_directory in group_directories
        for path in group_directory.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }

    installed_skills = (
        sorted(
            path.name
            for path in canonical_directory.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
        if canonical_directory.is_dir()
        else []
    )
    for name in installed_skills:
        if name in selected_skills:
            continue

        print(f"Removing skill outside the selected groups: {name}")
        runner(
            [
                *SKILLS_CLI,
                "remove",
                "--skill",
                name,
                "--agent",
                *agents,
                "--global",
                "--yes",
            ],
            check=True,
        )


def sync_skills(args):
    harnesses = [harness for harness in HARNESSES if getattr(args, harness)]
    if not harnesses:
        flags = ", ".join(f"--{harness}" for harness in HARNESSES)
        raise ValueError(f"name at least one harness to install into: {flags}")
    sync_repository_skills(harnesses, selected_skill_groups(args.groups))


def add_harness_flags(parser):
    for harness in HARNESSES:
        parser.add_argument(
            f"--{harness}",
            action="store_true",
            help=f"include {harness} (~/{HARNESSES[harness]['directory']})",
        )
    return parser


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(required=True)

    inspect_commands = {
        "hooks": ("list configured hooks", print_hooks),
        "plugins": ("list marketplaces and plugins", print_plugins),
        "skills": ("list installed skills", print_skills),
        "mcp": ("list configured MCP servers", print_mcp),
    }
    for name, (help_text, function) in inspect_commands.items():
        command = commands.add_parser(name, help=f"{help_text} (default: every harness)")
        add_harness_flags(command).set_defaults(func=function)

    sync = commands.add_parser("sync-skills", help="install selected skill groups into the named harnesses")
    sync.add_argument(
        "groups",
        nargs="+",
        metavar="GROUP",
        help="skill groups to install, separated by commas or spaces: core, ext, wip",
    )
    add_harness_flags(sync).set_defaults(func=sync_skills)

    args = parser.parse_args()

    try:
        args.func(args)
    except (OSError, ValueError) as error:
        raise SystemExit(f"error: {error}")


if __name__ == "__main__":
    main()
