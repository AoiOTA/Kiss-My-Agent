from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SETUP_SKILL = REPOSITORY / "skills" / "kiss-my-agent-setup" / "SKILL.md"
LIFECYCLE = SETUP_SKILL.parent / "references" / "setup-lifecycle.md"
CONFIGURE = SETUP_SKILL.parent / "references" / "configure-agents.md"
ROLE_DIRECTORY = REPOSITORY / ".codex" / "agents"
V010_FIXTURE = REPOSITORY / "tests" / "fixtures" / "v0.1-managed-project"

BEGIN_MARKER = "<!-- BEGIN KISS MY AGENT MANAGED BLOCK -->"
END_MARKER = "<!-- END KISS MY AGENT MANAGED BLOCK -->"
CONFIG_MARKER = "# KISS My Agent managed"
V010_MANAGED_BLOCK = f"""{BEGIN_MARKER}
## KISS My Agent

People own the goal, architecture, acceptance criteria, non-goals, and stop boundary. Multi-agent work is available by default, but an explicit user instruction or effective configuration that disables it takes precedence. Select dynamically only from the current Host-exposed role catalog; `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` are initial seeds that users may remove, rename, or replace, not a fixed team or workflow. Keep one operator for each shared resource, preserve unrelated changes, prefer the smallest sufficient change, propagate internal failures, and state evidence only at the level actually reached.
{END_MARKER}"""


def fenced_blocks(text: str, language: str) -> list[str]:
    pattern = re.compile(rf"```{re.escape(language)}\n(.*?)\n```", re.DOTALL)
    return pattern.findall(text)


class SetupContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SETUP_SKILL.read_text(encoding="utf-8")
        cls.lifecycle = LIFECYCLE.read_text(encoding="utf-8")
        cls.configure = CONFIGURE.read_text(encoding="utf-8")

    def test_entrypoint_routes_each_public_action_to_one_reference(self) -> None:
        self.assertIn("references/setup-lifecycle.md", self.skill)
        self.assertIn("references/configure-agents.md", self.skill)
        for action in ("setup", "check", "remove", "configure"):
            self.assertIn(action, self.skill)

        executable_lines = re.findall(
            r"(?mi)^\s*(?:python(?:3)?|py\s+-3|node|npm|npx|bun|deno)\b.*$",
            self.skill + "\n" + self.lifecycle + "\n" + self.configure,
        )
        self.assertEqual([], executable_lines)
        scripts = SETUP_SKILL.parent / "scripts"
        published_sources = [] if not scripts.exists() else [
            path
            for path in scripts.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        ]
        self.assertEqual([], published_sources)

    def test_lifecycle_preserves_v010_managed_block(self) -> None:
        markdown_blocks = fenced_blocks(self.lifecycle, "markdown")
        self.assertEqual(1, len(markdown_blocks))
        self.assertEqual(V010_MANAGED_BLOCK, markdown_blocks[0])
        self.assertEqual(1, self.lifecycle.count(BEGIN_MARKER))
        self.assertEqual(1, self.lifecycle.count(END_MARKER))

    def test_lifecycle_config_fragment_is_valid_and_owned(self) -> None:
        toml_blocks = fenced_blocks(self.lifecycle, "toml")
        self.assertEqual(1, len(toml_blocks))
        config = tomllib.loads(toml_blocks[0])
        self.assertIs(config["features"]["multi_agent"], True)
        self.assertIs(config["agents"]["enabled"], True)
        self.assertEqual(2, toml_blocks[0].count(CONFIG_MARKER))

    def test_seed_roles_remain_valid_and_unique(self) -> None:
        expected_modes = {
            "kiss_explorer": "read-only",
            "kiss_coder": "workspace-write",
            "kiss_reviewer": "read-only",
        }
        found: dict[str, str] = {}
        for path in sorted(ROLE_DIRECTORY.glob("*.toml")):
            with path.open("rb") as stream:
                role = tomllib.load(stream)
            for field in ("name", "description", "developer_instructions"):
                self.assertIsInstance(role.get(field), str, (path, field))
                self.assertTrue(role[field].strip(), (path, field))
            name = role["name"]
            self.assertNotIn(name, found)
            found[name] = role.get("sandbox_mode", "")

        self.assertEqual(expected_modes, found)

    def test_configure_is_limited_to_existing_role_runtime_fields(self) -> None:
        self.assertIn("Do not create, delete, rename, copy, or restore roles", self.configure)
        for field in ("model", "model_reasoning_effort", "sandbox_mode"):
            self.assertIn(f"`{field}`", self.configure)
        for required_field in ("name", "description", "developer_instructions"):
            self.assertIn(f"`{required_field}`", self.configure)
        self.assertNotRegex(self.configure, r"\bgpt-[0-9]")
        self.assertIn("`default_permissions`", self.configure)
        self.assertIn("`sandbox_workspace_write`", self.configure)

    def test_configure_requires_preview_and_full_access_confirmation(self) -> None:
        self.assertIn("show it before mutation", self.configure)
        self.assertIn("separate explicit confirmation", self.configure)
        self.assertIn("danger-full-access", self.configure)
        self.assertIn("start a new Codex session", self.configure)

    def test_check_statuses_and_evidence_boundary_are_explicit(self) -> None:
        for status in (
            "structurally-valid",
            "disabled",
            "absent",
            "incomplete",
            "conflict",
        ):
            self.assertIn(f"`{status}`", self.lifecycle)
        self.assertIn("File success is static setup evidence only", self.lifecycle)
        self.assertIn("Never claim project trust", self.lifecycle)

    def test_v010_conflict_recovery_and_concurrency_invariants_are_retained(self) -> None:
        self.assertIn("Do not apply this cross-scope rejection to `remove`", self.lifecycle)
        self.assertIn("re-read every planned target", self.lifecycle)
        self.assertIn("already-written target", self.lifecycle)
        self.assertIn("pending target", self.lifecycle)
        self.assertIn("directory created by this operation", self.lifecycle)
        self.assertIn("whether marked or unmarked", self.lifecycle)
        self.assertIn("marker controls remove ownership only", self.lifecycle)

    def test_codex_home_and_outdated_state_rules_are_explicit(self) -> None:
        self.assertIn("non-empty `CODEX_HOME`", self.lifecycle)
        self.assertIn("current user's `~/.codex`", self.lifecycle)
        self.assertIn("`current`, `outdated`, or `absent`", self.lifecycle)
        self.assertIn("Define a setup trace", self.lifecycle)
        self.assertIn("managed block is well-formed but `outdated`", self.lifecycle)
        self.assertIn("sole active workspace root", self.lifecycle)
        self.assertIn("multiple roots", self.lifecycle)

    def test_v010_managed_project_fixture_matches_current_compatibility_contract(self) -> None:
        config_text = (V010_FIXTURE / ".codex" / "config.toml").read_text(
            encoding="utf-8"
        )
        config = tomllib.loads(config_text)
        self.assertIs(config["features"]["multi_agent"], True)
        self.assertIs(config["agents"]["enabled"], True)
        self.assertEqual(2, config_text.count(CONFIG_MARKER))

        instructions = (V010_FIXTURE / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Keep this user-owned text.", instructions)
        start = instructions.index(BEGIN_MARKER)
        end = instructions.index(END_MARKER, start) + len(END_MARKER)
        self.assertEqual(V010_MANAGED_BLOCK, instructions[start:end])

        fixture_roles = V010_FIXTURE / ".codex" / "agents"
        for source in sorted(ROLE_DIRECTORY.glob("*.toml")):
            self.assertEqual(source.read_bytes(), (fixture_roles / source.name).read_bytes())


if __name__ == "__main__":
    unittest.main()
