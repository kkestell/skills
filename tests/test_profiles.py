import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import profiles


class SyncSkillsTests(unittest.TestCase):
    def setUp(self):
        self.repository = tempfile.TemporaryDirectory()
        self.home = tempfile.TemporaryDirectory()
        self.addCleanup(self.repository.cleanup)
        self.addCleanup(self.home.cleanup)

        self.repository_root = Path(self.repository.name)
        self.home_directory = Path(self.home.name)
        (self.repository_root / "skills/current-skill").mkdir(parents=True)

    def run_sync(self, target):
        calls = []

        def runner(command, *, check, env):
            calls.append((command, check, env))

        with redirect_stdout(io.StringIO()):
            profiles.sync_repository_skills(
                target,
                repository_root=self.repository_root,
                home_directory=self.home_directory,
                runner=runner,
            )

        return calls

    def test_personal_sync_installs_only_into_default_profiles(self):
        calls = self.run_sync("personal")

        self.assertEqual(len(calls), 1)
        command, check, environment = calls[0]
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
        self.assertEqual(
            environment["CLAUDE_CONFIG_DIR"],
            str(self.home_directory / ".claude"),
        )
        self.assertEqual(environment["CODEX_HOME"], str(self.home_directory / ".codex"))

    def test_work_sync_installs_and_prunes_both_profile_pairs(self):
        (self.home_directory / ".agents/skills/current-skill").mkdir(parents=True)
        (self.home_directory / ".agents/skills/removed-skill").mkdir()

        calls = self.run_sync("work")

        self.assertEqual(len(calls), 4)
        profile_pairs = [
            (
                call[2]["CLAUDE_CONFIG_DIR"],
                call[2]["CODEX_HOME"],
            )
            for call in calls
        ]
        self.assertEqual(
            profile_pairs,
            [
                (str(self.home_directory / ".claude"), str(self.home_directory / ".codex")),
                (
                    str(self.home_directory / ".claude-strib"),
                    str(self.home_directory / ".codex-strib"),
                ),
                (str(self.home_directory / ".claude"), str(self.home_directory / ".codex")),
                (
                    str(self.home_directory / ".claude-strib"),
                    str(self.home_directory / ".codex-strib"),
                ),
            ],
        )
        for command, check, _environment in calls[2:]:
            self.assertEqual(
                command,
                [
                    *profiles.SKILLS_CLI,
                    "remove",
                    "--skill",
                    "removed-skill",
                    "--global",
                    "--yes",
                ],
            )
            self.assertTrue(check)


if __name__ == "__main__":
    unittest.main()
