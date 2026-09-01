#!/usr/bin/env python3

import argparse
import json
import os
import shlex
import subprocess
import tomllib
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent
SKILLS_CLI = ("npx", "-y", "skills@latest")
PROFILE_DIRECTORIES = {
    "personal": (".claude", ".codex"),
    "work": (".claude-strib", ".codex-strib"),
}
SYNC_TARGETS = {
    "personal": ("personal",),
    # Work machines keep both the personal and Star Tribune profiles current.
    "work": ("personal", "work"),
}

profiles = {
    "claude": [f"~/{directories[0]}" for directories in PROFILE_DIRECTORIES.values()],
    "codex": [f"~/{directories[1]}" for directories in PROFILE_DIRECTORIES.values()],
    "copilot": ["~/.copilot"],
}


def hook_configs(provider, directory):
    if provider == "claude":
        paths = [directory / "settings.json"]
    elif provider == "codex":
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


def plugin_inventory(provider, directory):
    settings = read_json(directory / "settings.json")
    enabled = settings.get("enabledPlugins", {})

    if provider == "claude":
        known = read_json(directory / "plugins/known_marketplaces.json")
        installed = read_json(directory / "plugins/installed_plugins.json").get("plugins", {})
        marketplaces = set(known) | set(settings.get("extraKnownMarketplaces", {}))
        plugin_ids = set(installed) | set(enabled)
        roots = {
            plugin_id: [Path(item["installPath"]) for item in items if item.get("installPath")]
            for plugin_id, items in installed.items()
        }
    elif provider == "codex":
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


def skill_inventory(provider, directory):
    roots = [(directory / "skills", "", "")]
    if provider in {"codex", "copilot"}:
        roots.append((Path.home() / ".agents/skills", "", ""))

    for plugin_id, is_enabled, plugin_roots in plugin_inventory(provider, directory)[1]:
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


def mcp_inventory(provider, directory):
    if provider == "claude":
        default_directory = Path.home() / ".claude"
        config_path = (
            directory.parent / ".claude.json"
            if directory == default_directory
            else directory / ".claude.json"
        )
        servers = read_json(config_path).get("mcpServers", {})
    elif provider == "codex":
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


def profile_inventory(provider, directory):
    hooks = []
    for _source, configured_hooks in hook_configs(provider, directory):
        hooks.extend(hook_lines(configured_hooks))

    marketplaces, plugins = plugin_inventory(provider, directory)
    return {
        "hooks": set(hooks),
        "marketplaces": set(marketplaces),
        "plugins": {
            f"{name}{' (disabled)' if not enabled else ''}"
            for name, enabled, _roots in plugins
        },
        "skills": set(skill_inventory(provider, directory)),
        "MCP servers": set(mcp_inventory(provider, directory)),
    }


def print_hooks(_args):
    for provider, directories in profiles.items():
        for configured_path in directories:
            directory = Path(configured_path).expanduser()
            lines = []
            try:
                for _source, hooks in hook_configs(provider, directory):
                    lines.extend(hook_lines(hooks))
            except (OSError, ValueError, TypeError) as error:
                lines = [f"error: {error}"]

            if not lines:
                print(f"{provider} {configured_path}: none")
                continue
            print(f"{provider} {configured_path}")
            for line in lines:
                print(f"  {line}")


def print_plugins(_args):
    for provider, directories in profiles.items():
        for configured_path in directories:
            try:
                marketplaces, plugins = plugin_inventory(provider, Path(configured_path).expanduser())
                lines = [f"marketplace {name}" for name in marketplaces]
                lines += [f"plugin {name}{' (disabled)' if not enabled else ''}" for name, enabled, _ in plugins]
            except (OSError, ValueError, TypeError) as error:
                lines = [f"error: {error}"]
            print_lines(provider, configured_path, lines)


def print_skills(_args):
    for provider, directories in profiles.items():
        for configured_path in directories:
            try:
                skills = skill_inventory(provider, Path(configured_path).expanduser())
                lines = [f"skill {name}" for name in skills]
            except (OSError, ValueError, TypeError) as error:
                lines = [f"error: {error}"]
            print_lines(provider, configured_path, lines)


def run_skills_cli(arguments, claude_directory, codex_directory, runner):
    environment = os.environ.copy()
    environment["CLAUDE_CONFIG_DIR"] = str(claude_directory)
    environment["CODEX_HOME"] = str(codex_directory)
    runner([*SKILLS_CLI, *arguments], check=True, env=environment)


def sync_repository_skills(
    target,
    repository_root=None,
    home_directory=None,
    runner=subprocess.run,
):
    if target not in SYNC_TARGETS:
        raise ValueError(f"unknown sync target: {target}")

    repository_root = repository_root or REPOSITORY_ROOT
    home_directory = home_directory or Path.home()
    skills_directory = repository_root / "skills"
    canonical_directory = home_directory / ".agents/skills"

    if not skills_directory.is_dir():
        raise FileNotFoundError(f"skills directory not found: {skills_directory}")

    selected_profiles = [PROFILE_DIRECTORIES[name] for name in SYNC_TARGETS[target]]
    resolved_profiles = [
        (home_directory / claude_name, home_directory / codex_name)
        for claude_name, codex_name in selected_profiles
    ]

    add_arguments = [
        "add",
        str(skills_directory),
        "--skill",
        "*",
        "--agent",
        "claude-code",
        "codex",
        "--global",
        "--yes",
    ]
    for claude_directory, codex_directory in resolved_profiles:
        print(f"Installing skills into {claude_directory} and {codex_directory}")
        run_skills_cli(
            add_arguments,
            claude_directory,
            codex_directory,
            runner,
        )

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
        if (skills_directory / name).is_dir():
            continue

        print(f"Removing skill no longer in this repo: {name}")
        for claude_directory, codex_directory in resolved_profiles:
            run_skills_cli(
                ["remove", "--skill", name, "--global", "--yes"],
                claude_directory,
                codex_directory,
                runner,
            )


def sync_skills(args):
    sync_repository_skills(args.target)


def print_mcp(_args):
    for provider, directories in profiles.items():
        for configured_path in directories:
            try:
                servers = mcp_inventory(provider, Path(configured_path).expanduser())
                lines = [f"server {name}" for name in servers]
            except (OSError, ValueError, TypeError) as error:
                lines = [f"error: {error}"]
            print_lines(provider, configured_path, lines)


def print_diff(_args):
    compared = False
    for provider, directories in profiles.items():
        if len(directories) < 2:
            continue

        baseline_path = directories[0]
        try:
            baseline = profile_inventory(provider, Path(baseline_path).expanduser())
        except (OSError, ValueError, TypeError) as error:
            baseline = None
            baseline_error = error

        for configured_path in directories[1:]:
            compared = True
            heading = f"{provider} {baseline_path} -> {configured_path}"
            if baseline is None:
                print(f"{heading}\n  error reading {baseline_path}: {baseline_error}")
                continue

            try:
                inventory = profile_inventory(provider, Path(configured_path).expanduser())
            except (OSError, ValueError, TypeError) as error:
                print(f"{heading}\n  error reading {configured_path}: {error}")
                continue

            differences = []
            for category in baseline:
                removed = sorted(baseline[category] - inventory[category])
                added = sorted(inventory[category] - baseline[category])
                if removed or added:
                    differences.append((category, removed, added))

            if not differences:
                print(f"{heading}: identical")
                continue

            print(heading)
            for category, removed, added in differences:
                print(f"  {category}")
                for item in removed:
                    print(f"    - {item}")
                for item in added:
                    print(f"    + {item}")

    if not compared:
        print("no providers have multiple profiles to compare")


def print_lines(provider, configured_path, lines):
    if not lines:
        print(f"{provider} {configured_path}: none")
        return
    print(f"{provider} {configured_path}")
    for line in lines:
        print(f"  {line}")


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(required=True)
    hooks = commands.add_parser("hooks", help="list configured hooks")
    hooks.set_defaults(func=print_hooks)
    plugins = commands.add_parser("plugins", help="list marketplaces and plugins")
    plugins.set_defaults(func=print_plugins)
    skills = commands.add_parser("skills", help="list installed skills")
    skills.set_defaults(func=print_skills)
    sync = commands.add_parser(
        "sync-skills",
        help="sync repository skills into personal or work profiles",
    )
    sync.add_argument(
        "target",
        choices=SYNC_TARGETS,
        help="personal syncs the default profiles; work syncs default and Star Tribune profiles",
    )
    sync.set_defaults(func=sync_skills)
    mcp = commands.add_parser("mcp", help="list configured MCP servers")
    mcp.set_defaults(func=print_mcp)
    diff = commands.add_parser("diff", help="compare profiles for each provider")
    diff.set_defaults(func=print_diff)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
