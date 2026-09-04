import argparse
import io
import re
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
        args.groups = ["core"]

        with self.assertRaisesRegex(ValueError, "--claude, --codex, --copilot"):
            profiles.sync_skills(args)


class SkillGroupSelectionTests(unittest.TestCase):
    def test_groups_may_be_comma_or_space_separated(self):
        self.assertEqual(
            profiles.selected_skill_groups(["core,ext", "wip"]),
            ["core", "ext", "wip"],
        )

    def test_duplicate_groups_are_ignored(self):
        self.assertEqual(
            profiles.selected_skill_groups(["core,ext", "core"]),
            ["core", "ext"],
        )

    def test_unknown_group_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown skill group 'other'.*core, ext, wip"):
            profiles.selected_skill_groups(["core,other"])

    def test_empty_group_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "skill groups cannot be empty"):
            profiles.selected_skill_groups(["core,"])


class SyncSkillsTests(unittest.TestCase):
    def setUp(self):
        self.repository = tempfile.TemporaryDirectory()
        self.home = tempfile.TemporaryDirectory()
        self.addCleanup(self.repository.cleanup)
        self.addCleanup(self.home.cleanup)

        self.repository_root = Path(self.repository.name)
        self.home_directory = Path(self.home.name)
        (self.repository_root / "skills/core/current-skill").mkdir(parents=True)
        (self.repository_root / "skills/core/current-skill/SKILL.md").touch()

    def run_sync(self, harnesses, groups=("core",)):
        calls = []

        def runner(command, *, check):
            calls.append((command, check))

        with redirect_stdout(io.StringIO()):
            profiles.sync_repository_skills(
                harnesses,
                groups,
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
                str(self.repository_root / "skills/core"),
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

    def test_only_selected_groups_are_installed(self):
        ext_skill = self.repository_root / "skills/ext/extra-skill"
        ext_skill.mkdir(parents=True)
        (ext_skill / "SKILL.md").touch()

        calls = self.run_sync(["codex"], ["core"])

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0][4], str(self.repository_root / "skills/core"))

    def test_each_selected_group_is_installed(self):
        ext_skill = self.repository_root / "skills/ext/extra-skill"
        ext_skill.mkdir(parents=True)
        (ext_skill / "SKILL.md").touch()

        calls = self.run_sync(["codex"], ["core", "ext"])

        self.assertEqual(len(calls), 2)
        self.assertEqual(
            [call[0][4] for call in calls],
            [
                str(self.repository_root / "skills/core"),
                str(self.repository_root / "skills/ext"),
            ],
        )

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
            [
                *profiles.SKILLS_CLI,
                "remove",
                "--skill",
                "removed-skill",
                "--agent",
                "github-copilot",
                "--global",
                "--yes",
            ],
        )

    def test_skills_from_unselected_groups_are_removed(self):
        ext_skill = self.repository_root / "skills/ext/extra-skill"
        ext_skill.mkdir(parents=True)
        (ext_skill / "SKILL.md").touch()
        canonical = self.home_directory / profiles.CANONICAL_SKILLS
        (canonical / "extra-skill").mkdir(parents=True)

        calls = self.run_sync(["codex"], ["core"])

        self.assertEqual(len(calls), 2)
        self.assertIn("extra-skill", calls[1][0])

    def test_missing_selected_group_is_reported(self):
        with self.assertRaisesRegex(FileNotFoundError, "skill group directory not found"):
            self.run_sync(["claude"], ["ext"])

    def test_missing_skills_directory_is_reported(self):
        skill_directory = self.repository_root / "skills/core/current-skill"
        (skill_directory / "SKILL.md").unlink()
        skill_directory.rmdir()
        (self.repository_root / "skills/core").rmdir()
        (self.repository_root / "skills").rmdir()

        with self.assertRaisesRegex(FileNotFoundError, "skills directory not found"):
            self.run_sync(["claude"])


class CoreSkillDependencyTests(unittest.TestCase):
    @staticmethod
    def mentions_skill(contents, name):
        pattern = rf"(?<![\w-]){re.escape(name)}(?![\w-])"
        return re.search(pattern, contents) is not None

    def test_skill_reference_boundaries_do_not_match_larger_words(self):
        self.assertTrue(self.mentions_skill("Use kmarkdown here", "kmarkdown"))
        self.assertFalse(self.mentions_skill("notkmarkdown", "kmarkdown"))
        self.assertFalse(self.mentions_skill("kmarkdownish", "kmarkdown"))

    def test_core_skills_do_not_reference_ext_skills(self):
        core_directory = profiles.REPOSITORY_ROOT / "skills/core"
        ext_directory = profiles.REPOSITORY_ROOT / "skills/ext"
        ext_skill_names = [path.name for path in ext_directory.iterdir() if path.is_dir()]

        references = []
        for path in core_directory.rglob("*"):
            if not path.is_file():
                continue
            contents = path.read_text(errors="ignore")
            for name in ext_skill_names:
                if self.mentions_skill(contents, name):
                    references.append(f"{path.relative_to(profiles.REPOSITORY_ROOT)} -> {name}")

        self.assertEqual(references, [])


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
