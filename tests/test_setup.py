from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from unittest import mock


REPOSITORY = Path(__file__).resolve().parents[1]
SETUP_PATH = REPOSITORY / "skills" / "kiss-my-agent-setup" / "scripts" / "setup.py"
SPEC = importlib.util.spec_from_file_location("kiss_my_agent_setup", SETUP_PATH)
assert SPEC is not None and SPEC.loader is not None
setup_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = setup_module
SPEC.loader.exec_module(setup_module)


class SetupTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.project = root / "project"
        self.project.mkdir()
        self.codex_home = root / "codex-home"
        self.seed_dir = REPOSITORY / ".codex" / "agents"

    def manager(self, scope: str = "project"):
        return setup_module.SetupManager(
            scope,
            self.project,
            self.codex_home,
            seed_dir=self.seed_dir,
        )

    def role_path(self, name: str = "kiss_explorer.toml") -> Path:
        return self.project / ".codex" / "agents" / name

    def run_cli(self, command: str) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        arguments = [
            command,
            "--scope",
            "project",
            "--target",
            str(self.project),
            "--codex-home",
            str(self.codex_home),
        ]
        with redirect_stdout(output):
            code = setup_module.main(arguments)
        return code, json.loads(output.getvalue())

    def test_pristine_project_setup_and_static_check(self) -> None:
        result = self.manager().setup()

        self.assertEqual("configured", result["status"])
        self.assertEqual(set(setup_module.ROLE_FILES), set(result["installed_roles"]))
        config = (self.project / ".codex" / "config.toml").read_text()
        self.assertIn("multi_agent = true # KISS My Agent managed", config)
        self.assertIn("enabled = true # KISS My Agent managed", config)
        self.assertIn(setup_module.MANAGED_BLOCK, (self.project / "AGENTS.md").read_text())
        check = self.manager().check()
        self.assertTrue(check["static_only"])
        self.assertEqual("current", check["agents_managed_block"])
        self.assertEqual(set(setup_module.ROLE_FILES), set(check["roles"]))

    def test_existing_comments_and_true_values_remain_unowned(self) -> None:
        config_path = self.project / ".codex" / "config.toml"
        config_path.parent.mkdir()
        original = (
            b"# keep this comment\n[features]\n"
            b"multi_agent = true # user value\n\n"
            b"[agents]\nenabled = true\n"
        )
        config_path.write_bytes(original)

        result = self.manager().setup()

        self.assertEqual("configured", result["status"])
        self.assertEqual(original, config_path.read_bytes())
        check = self.manager().check()
        self.assertFalse(check["config"]["features.multi_agent"]["managed"])
        self.assertFalse(check["config"]["agents.enabled"]["managed"])

    def test_existing_false_is_preserved_and_reported_disabled(self) -> None:
        config_path = self.project / ".codex" / "config.toml"
        config_path.parent.mkdir()
        config_path.write_text("[features]\nmulti_agent = false # intentional\n")

        result = self.manager().setup()

        self.assertEqual("disabled", result["status"])
        self.assertEqual(["features.multi_agent"], result["disabled"])
        self.assertIn("multi_agent = false # intentional", config_path.read_text())
        self.assertIn("enabled = true # KISS My Agent managed", config_path.read_text())
        self.assertEqual("disabled", self.manager().check()["status"])
        code, check = self.run_cli("check")
        self.assertEqual(0, code)
        self.assertEqual("disabled", check["status"])

    def test_check_blank_target_is_absent_and_nonzero(self) -> None:
        code, check = self.run_cli("check")

        self.assertEqual(1, code)
        self.assertEqual("absent", check["status"])

    def test_check_partial_managed_artifact_is_incomplete_and_nonzero(self) -> None:
        config_path = self.project / ".codex" / "config.toml"
        config_path.parent.mkdir()
        config_path.write_text(
            "[features]\nmulti_agent = true # KISS My Agent managed\n"
        )

        code, check = self.run_cli("check")

        self.assertEqual(1, code)
        self.assertEqual("incomplete", check["status"])

    def test_check_after_remove_is_absent_and_nonzero(self) -> None:
        self.manager().setup()
        self.manager().remove()

        code, check = self.run_cli("check")

        self.assertEqual(1, code)
        self.assertEqual("absent", check["status"])

    def test_nested_agent_tables_are_preserved_when_parent_key_is_inserted(self) -> None:
        config_path = self.project / ".codex" / "config.toml"
        config_path.parent.mkdir()
        nested = (
            '[agents.custom]\n'
            'description = "keep"\n'
            'config_file = "agents/custom.toml"\n'
        )
        config_path.write_text(nested)

        self.manager().setup()

        configured = config_path.read_text()
        self.assertIn(nested, configured)
        self.assertIn("[agents]\nenabled = true # KISS My Agent managed", configured)

    def test_existing_table_without_final_newline_gets_separate_managed_assignment(self) -> None:
        config_path = self.project / ".codex" / "config.toml"
        config_path.parent.mkdir()
        cases = (
            (
                "[features]\nfoo = true",
                "foo = true\nmulti_agent = true # KISS My Agent managed\n",
            ),
            (
                "[features]\nmulti_agent = true\n[agents]\nfoo = true",
                "foo = true\nenabled = true # KISS My Agent managed\n",
            ),
        )
        for content, expected in cases:
            with self.subTest(content=content):
                config_path.write_text(content)
                self.manager().setup()
                configured = config_path.read_text()
                self.assertIn(expected, configured)
                self.assertNotIn("truemulti_agent", configured)
                self.assertNotIn("trueenabled", configured)
                self.manager().remove()

    def test_crlf_and_unicode_comments_are_preserved(self) -> None:
        config_path = self.project / ".codex" / "config.toml"
        config_path.parent.mkdir()
        original = "# 用户注释\r\n[features]\r\nmulti_agent = true\r\n".encode()
        config_path.write_bytes(original)

        self.manager().setup()

        configured = config_path.read_bytes()
        self.assertTrue(configured.startswith(original))
        self.assertIn(b"[agents]\r\nenabled = true # KISS My Agent managed\r\n", configured)

    def test_malformed_and_unknown_shape_fail_before_changes(self) -> None:
        config_path = self.project / ".codex" / "config.toml"
        config_path.parent.mkdir()
        for content in ("[features\n", 'features = { multi_agent = true }\n'):
            with self.subTest(content=content):
                config_path.write_text(content)
                with self.assertRaises(setup_module.SetupError):
                    self.manager().setup()
                self.assertEqual(content, config_path.read_text())
                self.assertFalse((self.project / "AGENTS.md").exists())

    def test_role_name_collision_fails_without_changes(self) -> None:
        agents_dir = self.project / ".codex" / "agents"
        agents_dir.mkdir(parents=True)
        collision = agents_dir / "renamed.toml"
        collision.write_text(
            'name = "kiss_explorer"\n'
            'description = "custom"\n'
            'developer_instructions = "custom instructions"\n'
        )

        with self.assertRaises(setup_module.SetupError):
            self.manager().setup()

        self.assertIn('name = "kiss_explorer"', collision.read_text())
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_existing_same_filename_and_name_custom_role_is_preserved(self) -> None:
        agents_dir = self.project / ".codex" / "agents"
        agents_dir.mkdir(parents=True)
        custom = self.role_path()
        custom_bytes = (
            b'name = "kiss_explorer"\n'
            b'description = "my custom explorer"\n'
            b'developer_instructions = "custom instructions"\n'
        )
        custom.write_bytes(custom_bytes)

        result = self.manager().setup()

        self.assertEqual(custom_bytes, custom.read_bytes())
        self.assertIn("kiss_explorer.toml", result["preserved_roles"])
        self.assertEqual(2, len(result["installed_roles"]))

    def test_repeated_setup_is_noop(self) -> None:
        self.manager().setup()
        tracked = [
            self.project / ".codex" / "config.toml",
            self.project / "AGENTS.md",
            *(self.role_path(name) for name in setup_module.ROLE_FILES),
        ]
        before = {path: path.read_bytes() for path in tracked}

        result = self.manager().setup()

        self.assertFalse(result["changed"])
        self.assertEqual(before, {path: path.read_bytes() for path in tracked})

    def test_deleted_default_role_is_not_restored_after_managed_block_exists(self) -> None:
        self.manager().setup()
        deleted = self.role_path("kiss_reviewer.toml")
        deleted.unlink()
        agents_path = self.project / "AGENTS.md"
        agents_path.write_text(
            agents_path.read_text().replace("## KISS My Agent", "## stale managed text")
        )

        result = self.manager().setup()

        self.assertFalse(deleted.exists())
        self.assertNotIn("kiss_reviewer.toml", result["installed_roles"])
        self.assertIn(setup_module.MANAGED_BLOCK, agents_path.read_text())
        self.assertEqual("structurally-valid", self.manager().check()["status"])

    def test_remove_preserves_modified_role_and_unowned_config(self) -> None:
        config_path = self.project / ".codex" / "config.toml"
        config_path.parent.mkdir()
        config_path.write_text("# user\n[features]\nmulti_agent = true\n")
        self.manager().setup()
        modified = self.role_path("kiss_coder.toml")
        modified_bytes = modified.read_bytes() + b"\n# user modification\n"
        modified.write_bytes(modified_bytes)

        result = self.manager().remove()

        self.assertEqual(modified_bytes, modified.read_bytes())
        self.assertEqual(["kiss_coder.toml"], result["preserved_modified_roles"])
        self.assertFalse(self.role_path("kiss_explorer.toml").exists())
        self.assertFalse(self.role_path("kiss_reviewer.toml").exists())
        self.assertNotIn(setup_module.MANAGED_BLOCK, (self.project / "AGENTS.md").read_text())
        config = config_path.read_text()
        self.assertIn("multi_agent = true", config)
        self.assertNotIn("enabled = true", config)

    def test_override_rejected(self) -> None:
        override = self.project / "AGENTS.override.md"
        override.write_text("override\n")

        with self.assertRaises(setup_module.SetupError):
            self.manager().setup()

        self.assertEqual("override\n", override.read_text())
        self.assertFalse((self.project / ".codex").exists())

    def test_project_and_global_role_catalogs_cannot_duplicate_seed_names(self) -> None:
        self.manager("project").setup()

        with self.assertRaises(setup_module.SetupError):
            self.manager("global").setup()

        self.assertFalse(self.codex_home.exists())

    def test_global_scope_writes_only_under_codex_home(self) -> None:
        other_project = Path(self.temporary.name) / "other-project"
        other_project.mkdir()
        manager = setup_module.SetupManager(
            "global", other_project, self.codex_home, seed_dir=self.seed_dir
        )

        manager.setup()

        self.assertTrue((self.codex_home / "config.toml").is_file())
        self.assertTrue((self.codex_home / "AGENTS.md").is_file())
        self.assertTrue((self.codex_home / "agents" / "kiss_coder.toml").is_file())
        self.assertEqual([], list(other_project.iterdir()))

    def test_symlinked_managed_path_is_rejected(self) -> None:
        external = Path(self.temporary.name) / "external.toml"
        external.write_text("# external\n")
        codex_dir = self.project / ".codex"
        codex_dir.mkdir()
        try:
            (codex_dir / "config.toml").symlink_to(external)
        except OSError as error:
            self.skipTest(f"symlink creation is unavailable: {error}")

        with self.assertRaises(setup_module.SetupError):
            self.manager().setup()

        self.assertEqual("# external\n", external.read_text())
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_replace_failure_rolls_back_all_completed_changes(self) -> None:
        real_replace = setup_module.os.replace
        calls = 0

        def fail_second_replace(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected replace failure")
            return real_replace(source, destination)

        with mock.patch.object(setup_module.os, "replace", side_effect=fail_second_replace):
            with self.assertRaises(OSError):
                self.manager().setup()

        self.assertFalse((self.project / ".codex").exists())
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_concurrent_change_is_preserved_while_earlier_write_rolls_back(self) -> None:
        real_replace = setup_module.os.replace
        agents_path = self.project / "AGENTS.md"
        calls = 0

        def change_next_target(source, destination):
            nonlocal calls
            calls += 1
            result = real_replace(source, destination)
            if calls == 1:
                agents_path.write_text("concurrent user content\n")
            return result

        with mock.patch.object(setup_module.os, "replace", side_effect=change_next_target):
            with self.assertRaises(setup_module.SetupError):
                self.manager().setup()

        self.assertEqual("concurrent user content\n", agents_path.read_text())
        self.assertFalse((self.project / ".codex" / "config.toml").exists())


if __name__ == "__main__":
    unittest.main()
