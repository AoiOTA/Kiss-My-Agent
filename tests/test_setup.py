from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SETUP_SKILL = REPOSITORY / "skills" / "kiss-my-agent-setup" / "SKILL.md"
LIFECYCLE = SETUP_SKILL.parent / "setup-lifecycle.md"
CONFIGURE = SETUP_SKILL.parent / "configure-agents.md"
ROLE_DIRECTORY = REPOSITORY / ".codex" / "agents"
V010_FIXTURE = REPOSITORY / "tests" / "fixtures" / "v0.1-managed-project"
V010_ASSETS = SETUP_SKILL.parent / "assets"
BEGIN_MARKER = "<!-- BEGIN KISS MY AGENT MANAGED BLOCK -->"
END_MARKER = "<!-- END KISS MY AGENT MANAGED BLOCK -->"
CONFIG_MARKER = "# KISS My Agent managed"
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
        self.assertIn("](setup-lifecycle.md)", self.skill)
        self.assertIn("](configure-agents.md)", self.skill)
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

    def test_entrypoint_declares_static_runtime_execution_contract(self) -> None:
        """Static source assertions do not prove Host runtime behavior."""
        self.assertIn(
            "exact loaded `SKILL.md` directory as the tool workdir",
            self.skill,
        )
        self.assertIn("linked relative-path text as its path operand", self.skill)
        self.assertIn(
            "never reconstruct cache, marketplace, plugin, or version path components",
            self.skill,
        )
        self.assertIn("Run lifecycle mutations serially", self.skill)
        self.assertIn("one simple direct file operation per tool call", self.skill)
        self.assertIn("Do not batch mutations", self.skill)
        self.assertIn("generate compound shell commands", self.skill)
        self.assertIn("suppress diagnostics", self.skill)
        self.assertIn("one planned target", self.skill)
        self.assertIn("Inspect every tool or subprocess status", self.skill)
        self.assertIn("unexpected failure", self.skill)
        self.assertIn("stops forward work", self.skill)
        self.assertIn("If nothing changed, return immediately", self.skill)
        self.assertIn("exact-after-content guarded rollback or cleanup", self.skill)
        self.assertIn("preserve the original failure", self.skill)
        self.assertIn("report any rollback failure too", self.skill)
        self.assertIn("expected absence or no-match is not a failure", self.skill)
        self.assertIn("report it explicitly", self.skill)

    def test_lifecycle_publishes_one_current_managed_block(self) -> None:
        markdown_blocks = fenced_blocks(self.lifecycle, "markdown")
        self.assertEqual(1, len(markdown_blocks))
        self.assertTrue(markdown_blocks[0].startswith(BEGIN_MARKER))
        self.assertTrue(markdown_blocks[0].endswith(END_MARKER))
        self.assertIn("wait window ending without an update", markdown_blocks[0])
        self.assertIn("not an agent timeout or failure", markdown_blocks[0])
        self.assertIn("The master owns orchestration", markdown_blocks[0])
        self.assertIn("must delegate delegable bulk exploration", markdown_blocks[0])
        self.assertIn("Multiple instances of any role", markdown_blocks[0])
        self.assertIn("Coordination is flat by default", markdown_blocks[0])
        self.assertIn("independent subsystem needs substantial parallel work", markdown_blocks[0])
        self.assertIn("direct aggregation would pollute the master's context", markdown_blocks[0])
        self.assertIn("bounded department-lead assignment", markdown_blocks[0])
        self.assertIn("workers must not delegate again", markdown_blocks[0])
        self.assertIn("at most one intermediate management layer", markdown_blocks[0])
        self.assertIn("no deep nesting", markdown_blocks[0])
        self.assertIn("must not silently take over delegated work", markdown_blocks[0])
        self.assertIn("ordinary single-conversation execution", markdown_blocks[0])
        self.assertIn("reversible probe", markdown_blocks[0])
        self.assertIn("safety boundaries", markdown_blocks[0])
        self.assertLess(
            markdown_blocks[0].index("reversible probe"),
            markdown_blocks[0].index("Multi-agent work is available by default"),
        )
        self.assertEqual(1, self.lifecycle.count(BEGIN_MARKER))
        self.assertEqual(1, self.lifecycle.count(END_MARKER))

    def test_lifecycle_config_fragment_is_valid_and_owned(self) -> None:
        toml_blocks = fenced_blocks(self.lifecycle, "toml")
        self.assertEqual(1, len(toml_blocks))
        config = tomllib.loads(toml_blocks[0])
        self.assertEqual("gpt-5.6-sol", config["model"])
        self.assertEqual("max", config["model_reasoning_effort"])
        self.assertIs(config["features"]["multi_agent"], True)
        self.assertIs(config["agents"]["enabled"], True)
        self.assertEqual(4, toml_blocks[0].count(CONFIG_MARKER))

    def test_seed_roles_remain_valid_and_unique(self) -> None:
        expected_settings = {
            "kiss_explorer": ("gpt-5.6-sol", "high", "read-only"),
            "kiss_coder": ("gpt-5.6-sol", "high", "workspace-write"),
            "kiss_reviewer": ("gpt-5.6-sol", "xhigh", "read-only"),
        }
        found: dict[str, tuple[str, str, str]] = {}
        for path in sorted(ROLE_DIRECTORY.glob("*.toml")):
            with path.open("rb") as stream:
                role = tomllib.load(stream)
            for field in ("name", "description", "developer_instructions"):
                self.assertIsInstance(role.get(field), str, (path, field))
                self.assertTrue(role[field].strip(), (path, field))
            name = role["name"]
            self.assertNotIn(name, found)
            found[name] = (
                role.get("model", ""),
                role.get("model_reasoning_effort", ""),
                role.get("sandbox_mode", ""),
            )

        self.assertEqual(expected_settings, found)

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
        self.assertIn("Immediately before mutating each selected file", self.configure)
        self.assertIn("still equal its preview base", self.configure)
        self.assertIn("If a pending target differs", self.configure)
        self.assertIn("stop forward work", self.configure)
        self.assertIn("already-written files", self.configure)
        self.assertIn("exact after-content", self.configure)
        self.assertIn("preserve the original failure", self.configure)
        self.assertIn("start a new Codex session", self.configure)

    def test_configure_resolves_its_scope_without_lifecycle_reference(self) -> None:
        self.assertIn(
            "<unique Host project or active workspace root>/.codex/agents",
            self.configure,
        )
        self.assertIn("non-empty `CODEX_HOME`", self.configure)
        self.assertIn("current user's `~/.codex`", self.configure)
        self.assertIn("multiple roots or no unique root", self.configure)
        self.assertIn("do not write before that choice", self.configure)
        self.assertIn("absolute role-directory path", self.configure)

    def test_configure_inspects_only_selected_role_targets(self) -> None:
        self.assertIn("resolve only those targets", self.configure)
        self.assertIn("direct `.toml` child", self.configure)
        self.assertIn("Reject traversal", self.configure)
        self.assertIn("Do not list, read, or parse unselected role files", self.configure)
        self.assertIn("list only the direct `.toml` paths", self.configure)
        self.assertIn("without reading or parsing their contents", self.configure)
        self.assertIn("read and parse only those files", self.configure)
        self.assertIn("unselected role does not block this operation", self.configure)

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
        self.assertIn("executive-only workflow cannot staff delegated work", self.lifecycle)
        self.assertIn("Static setup cannot observe a higher-precedence `false`", self.lifecycle)

    def test_setup_ownership_and_concurrency_contract(self) -> None:
        self.assertIn("three exact bundled role targets", self.lifecycle)
        self.assertIn("Do not inspect other role files or another scope's roles", self.lifecycle)
        self.assertIn("Host owns role precedence", self.lifecycle)
        self.assertIn("name` to equal the target filename", self.lifecycle)
        self.assertIn("each exact bundled role target relevant to the action", self.lifecycle)
        self.assertIn("do not claim that the complete Host role catalog is valid", self.lifecycle)
        self.assertIn("any exact bundled role target with the matching identity", self.lifecycle)
        self.assertNotIn("Opposite role catalog", self.lifecycle)
        self.assertNotIn("opposite-catalog", self.lifecycle)
        self.assertNotIn("cross-scope rejection", self.lifecycle)
        self.assertNotIn("every role TOML", self.lifecycle)
        self.assertNotIn("complete role catalog", self.lifecycle)
        self.assertNotIn("another filename in the same catalog", self.lifecycle)
        self.assertIn("state a separate decision", self.lifecycle)
        self.assertIn("master model/effort pair", self.lifecycle)
        self.assertIn("each feature switch", self.lifecycle)
        self.assertIn("the Instructions target", self.lifecycle)
        self.assertIn("every Role", self.lifecycle)
        self.assertIn("re-read every planned target", self.lifecycle)
        self.assertIn("already-written target", self.lifecycle)
        self.assertIn("pending target", self.lifecycle)
        self.assertIn("directory created by this operation", self.lifecycle)
        self.assertIn("whether marked or unmarked", self.lifecycle)
        self.assertIn("marker controls remove ownership only", self.lifecycle)
        self.assertIn("initial defaults, not enforcement", self.lifecycle)
        self.assertIn("all four managed config paths", self.lifecycle)
        self.assertIn("exactly one mutually exclusive state", self.lifecycle)
        self.assertIn("When both top-level master keys are absent", self.lifecycle)
        self.assertIn("block state is `absent` or `outdated`", self.lifecycle)
        self.assertIn("block state is `current`, add neither", self.lifecycle)
        self.assertIn("absence records intentional user removal", self.lifecycle)
        self.assertIn("When either top-level master key already exists", self.lifecycle)
        self.assertIn("in every block state", self.lifecycle)
        self.assertIn("leave the other key absent as intentional inheritance", self.lifecycle)
        self.assertIn("four managed config assignment lines", self.lifecycle)
        self.assertIn("create each missing bundled role from its exact current plugin seed", self.lifecycle)
        self.assertIn("Preserve every existing correctly identified role byte-for-byte", self.lifecycle)
        self.assertIn("`user-owned/preserved`", self.lifecycle)
        self.assertIn("never modify, migrate, version-check, or replace an existing role", self.lifecycle)
        self.assertIn("Use the existing `configure agents` wizard", self.lifecycle)
        self.assertIn("either the current bundled seed or the corresponding known v0.1 seed", self.lifecycle)

    def test_role_assets_are_read_only_by_the_actions_that_consume_them(self) -> None:
        self.assertLess(
            self.lifecycle.index("exactly one mutually exclusive state"),
            self.lifecycle.index("`setup`: after classifying the managed block"),
        )
        self.assertIn(
            "`setup`: after classifying the managed block, read and identity-check a current seed only for a missing role",
            self.lifecycle,
        )
        self.assertIn("Do not read current seeds for existing roles or any known v0.1 seed", self.lifecycle)
        self.assertIn("`check`: do not read current or known v0.1 role assets", self.lifecycle)
        self.assertIn("`remove`: read current and known v0.1 role seeds as exact bytes", self.lifecycle)
        self.assertIn("Do not read role seed assets, compare role content to seeds", self.lifecycle)
        self.assertNotRegex(self.skill + self.lifecycle, r"(?i)native.{0,40}(?:copy|migration)")

    def test_codex_home_and_outdated_state_rules_are_explicit(self) -> None:
        self.assertIn("non-empty `CODEX_HOME`", self.lifecycle)
        self.assertIn("current user's `~/.codex`", self.lifecycle)
        self.assertIn("`absent`, `outdated`, or `current`", self.lifecycle)
        self.assertIn("Define a setup trace", self.lifecycle)
        self.assertIn("managed block is well-formed but `outdated`", self.lifecycle)
        self.assertIn("explicit value or `inherit`", self.lifecycle)
        self.assertIn("sole active workspace root", self.lifecycle)
        self.assertIn("multiple roots", self.lifecycle)
        self.assertIn("Never silently substitute a fallback model or effort", self.lifecycle)
        self.assertIn(
            "codex --config 'model=\"HOST_SUPPORTED_MODEL_ID\"'",
            self.lifecycle,
        )

    def test_v010_runtime_assets_are_directly_linked_and_identified(self) -> None:
        for role_name in ("kiss_explorer", "kiss_coder", "kiss_reviewer"):
            relative = f"assets/v0.1-agents/{role_name}.toml"
            self.assertIn(f"]({relative})", self.lifecycle)
            asset = (LIFECYCLE.parent / relative).resolve()
            self.assertTrue(asset.is_file(), asset)
            with asset.open("rb") as stream:
                self.assertEqual(role_name, tomllib.load(stream)["name"])
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
        current_block = fenced_blocks(self.lifecycle, "markdown")[0]
        self.assertNotEqual(current_block, instructions[start:end])

        fixture_roles = V010_FIXTURE / ".codex" / "agents"
        asset_roles = V010_ASSETS / "v0.1-agents"
        for source in sorted(ROLE_DIRECTORY.glob("*.toml")):
            fixture_bytes = (fixture_roles / source.name).read_bytes()
            asset_bytes = (asset_roles / source.name).read_bytes()
            self.assertEqual(fixture_bytes, asset_bytes, source.name)
            with (fixture_roles / source.name).open("rb") as stream:
                v010 = tomllib.load(stream)
            self.assertEqual(source.stem, v010["name"])
            self.assertNotIn("model", v010)
            self.assertNotIn("model_reasoning_effort", v010)

        self.assertIn("block state is `absent` or `outdated`", self.lifecycle)
        self.assertIn("replace only its interior and markers with the current block", self.lifecycle)
        self.assertIn("Preserve every existing correctly identified role byte-for-byte", self.lifecycle)


if __name__ == "__main__":
    unittest.main()
