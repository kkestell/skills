import argparse
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import profiles


class HarnessSelectionTests(unittest.TestCase):
    def parse(self, arguments):
        parser = argparse.ArgumentParser()
        profiles.add_harness_flags(parser)
        return parser.parse_args(arguments)

    def test_flags_select_the_named_harnesses(self):
        args = self.parse(["--claude", "--codex"])

        self.assertEqual(profiles.selected_harnesses(args), ["claude", "codex"])

    def test_no_flags_selects_every_harness(self):
        args = self.parse([])

        self.assertEqual(profiles.selected_harnesses(args), ["claude", "codex", "copilot"])

    def test_harness_directories_sit_under_the_home_directory(self):
        home_directory = Path("/home/example")

        self.assertEqual(
            [profiles.harness_directory(harness, home_directory) for harness in profiles.HARNESSES],
            [
                home_directory / ".claude",
                home_directory / ".codex",
                home_directory / ".copilot",
            ],
        )

    def test_sync_requires_at_least_one_harness(self):
        args = self.parse([])

        with self.assertRaisesRegex(ValueError, "--claude, --codex, --copilot"):
            profiles.sync_skills(args)


class SyncSkillsTests(unittest.TestCase):
    def setUp(self):
        self.repository = tempfile.TemporaryDirectory()
        self.home = tempfile.TemporaryDirectory()
        self.addCleanup(self.repository.cleanup)
        self.addCleanup(self.home.cleanup)

        self.repository_root = Path(self.repository.name)
        self.home_directory = Path(self.home.name)
        (self.repository_root / "skills/current-skill").mkdir(parents=True)

    def run_sync(self, harnesses):
        calls = []

        def runner(command, *, check):
            calls.append((command, check))

        with redirect_stdout(io.StringIO()):
            profiles.sync_repository_skills(
                harnesses,
                repository_root=self.repository_root,
                home_directory=self.home_directory,
                runner=runner,
            )

        return calls

    def test_install_names_the_agent_of_every_chosen_harness(self):
        calls = self.run_sync(["claude", "codex"])

        self.assertEqual(len(calls), 1)
        command, check = calls[0]
        self.assertEqual(
            command,
            [
                *profiles.SKILLS_CLI,
                "add",
                str(self.repository_root / "skills"),
                "--skill",
                "*",
                "--agent",
                "claude-code",
                "codex",
                "--global",
                "--yes",
            ],
        )
        self.assertTrue(check)

    def test_skills_missing_from_this_repo_are_removed(self):
        (self.home_directory / "sub/current-skill").mkdir(parents=True)
        (self.home_directory / "sub/removed-skill").mkdir()
        canonical = self.home_directory / profiles.CANONICAL_SKILLS
        canonical.parent.mkdir(parents=True, exist_ok=True)
        (self.home_directory / "sub").rename(canonical)

        calls = self.run_sync(["copilot"])

        self.assertEqual(len(calls), 2)
        self.assertEqual(
            calls[1][0],
            [*profiles.SKILLS_CLI, "remove", "--skill", "removed-skill", "--global", "--yes"],
        )

    def test_missing_skills_directory_is_reported(self):
        for path in (self.repository_root / "skills").iterdir():
            path.rmdir()
        (self.repository_root / "skills").rmdir()

        with self.assertRaisesRegex(FileNotFoundError, "skills directory not found"):
            self.run_sync(["claude"])


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.TemporaryDirectory()
        self.addCleanup(self.home.cleanup)
        self.home_directory = Path(self.home.name)

    def write(self, relative_path, text):
        path = self.home_directory / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_claude_reads_hooks_and_mcp_servers_from_its_own_files(self):
        directory = profiles.harness_directory("claude", self.home_directory)
        self.write(
            ".claude/settings.json",
            '{"hooks": {"Stop": [{"matcher": "*", "hooks": [{"command": "say done"}]}]}}',
        )
        self.write(".claude.json", '{"mcpServers": {"context7": {}}}')

        hooks = [line for _source, hooks in profiles.hook_configs("claude", directory) for line in profiles.hook_lines(hooks)]

        self.assertEqual(hooks, ["Stop[*] say done"])
        self.assertEqual(profiles.mcp_inventory("claude", directory), ["context7"])

    def test_codex_sees_skills_installed_in_the_canonical_directory(self):
        directory = profiles.harness_directory("codex", self.home_directory)
        self.write(f"{profiles.CANONICAL_SKILLS}/kwork/SKILL.md", "---\nname: kwork\n---\n")

        self.assertEqual(profiles.skill_inventory("codex", directory), ["kwork"])

    def test_claude_ignores_the_canonical_directory(self):
        directory = profiles.harness_directory("claude", self.home_directory)
        self.write(f"{profiles.CANONICAL_SKILLS}/kwork/SKILL.md", "---\nname: kwork\n---\n")

        self.assertEqual(profiles.skill_inventory("claude", directory), [])


if __name__ == "__main__":
    unittest.main()
