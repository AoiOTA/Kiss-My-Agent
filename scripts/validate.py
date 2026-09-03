#!/usr/bin/env python3
"""Cross-platform static validation for the KISS My Agent repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    print("validation failed: Python 3.11 or newer is required", file=sys.stderr)
    raise SystemExit(1)

import tomllib


DEFAULT_ROLE_NAMES = ("kiss_explorer", "kiss_coder", "kiss_reviewer")
PROJECT_HOMEPAGE = "https://github.com/AoiOTA/Kiss-My-Agent"
PROJECT_REPOSITORY = f"{PROJECT_HOMEPAGE}.git"
PROJECT_PAGES = "https://aoiota.github.io/Kiss-My-Agent/"
PROJECT_PAGES_ZH = f"{PROJECT_PAGES}zh-CN/"
DEFAULT_ROLE_CONTRACTS = {
    "kiss_explorer": {
        "model": "gpt-5.6-sol",
        "model_reasoning_effort": "high",
        "sandbox_mode": "read-only",
        "instruction_fragments": (
            "Investigate only the assigned",
            "Do not modify files, Git, outputs, data, processes, or external state.",
        ),
    },
    "kiss_coder": {
        "model": "gpt-5.6-sol",
        "model_reasoning_effort": "high",
        "sandbox_mode": "workspace-write",
        "instruction_fragments": (
            "Implement only the assigned",
            "Preserve unrelated user and agent changes.",
            "Stop and report if ownership",
        ),
    },
    "kiss_reviewer": {
        "model": "gpt-5.6-sol",
        "model_reasoning_effort": "xhigh",
        "sandbox_mode": "read-only",
        "instruction_fragments": (
            "Independently review only the assigned",
            "Report material findings",
            "Do not modify files, Git, outputs, data, processes, or external state.",
        ),
    },
}
ALLOWED_SANDBOX_MODES = {"read-only", "workspace-write", "danger-full-access"}
COMMAND_FENCE_LANGUAGES = {
    "bash",
    "console",
    "powershell",
    "pwsh",
    "sh",
    "shell",
    "toml",
}
DOC_PAIRS = (
    ("README.md", "README.zh-CN.md"),
    ("CONTRIBUTING.md", "CONTRIBUTING.zh-CN.md"),
    ("SECURITY.md", "SECURITY.zh-CN.md"),
    ("docs/INSTALLATION.md", "docs/INSTALLATION.zh-CN.md"),
    ("docs/CONFIGURATION.md", "docs/CONFIGURATION.zh-CN.md"),
    ("docs/EXTENDING.md", "docs/EXTENDING.zh-CN.md"),
    ("docs/FAQ.md", "docs/FAQ.zh-CN.md"),
    ("docs/TESTING.md", "docs/TESTING.zh-CN.md"),
)
PUBLIC_INVOCATION_SOURCES = tuple(dict.fromkeys(
    path
    for group in (
        *DOC_PAIRS,
        ("AGENTS.md",),
        (
            "skills/kiss-my-agent/SKILL.md",
            "skills/kiss-my-agent-setup/SKILL.md",
        ),
        ("tests/scenarios.md",),
    )
    for path in group
))
SETUP_INVOCATION_SOURCES = tuple(
    path
    for english, chinese in DOC_PAIRS
    if english in {
        "README.md",
        "docs/INSTALLATION.md",
        "docs/TESTING.md",
    }
    for path in (english, chinese)
)
QUALIFIED_DECISION_INVOCATION = "$kiss-my-agent:kiss-my-agent"
QUALIFIED_SETUP_INVOCATION = "$kiss-my-agent:kiss-my-agent-setup"
ALLOWED_PUBLIC_INVOCATIONS = frozenset({
    QUALIFIED_DECISION_INVOCATION,
    QUALIFIED_SETUP_INVOCATION,
})
PUBLIC_INVOCATION_TOKEN = re.compile(r"\$kiss-my-agent[A-Za-z0-9_:-]*")


class ValidationError(Exception):
    """A repository invariant is not satisfied."""


def fail(message: str) -> None:
    raise ValidationError(message)


def warn(message: str) -> None:
    print(f"validation warning: {message}", file=sys.stderr)


def load_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def require_files(root: Path) -> None:
    required = {
        "AGENTS.md",
        "README.md",
        "README.zh-CN.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CONTRIBUTING.zh-CN.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        "SECURITY.zh-CN.md",
        ".editorconfig",
        ".gitattributes",
        ".gitignore",
        ".github/CODEOWNERS",
        ".github/ISSUE_TEMPLATE/bug-report.md",
        ".github/ISSUE_TEMPLATE/config.yml",
        ".github/ISSUE_TEMPLATE/documentation.md",
        ".github/ISSUE_TEMPLATE/feature-request.md",
        ".github/ISSUE_TEMPLATE/rule-or-case-proposal.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/workflows/validate.yml",
        ".github/workflows/pages.yml",
        ".codex-plugin/plugin.json",
        ".codex/config.toml",
        ".codex/agents/kiss_explorer.toml",
        ".codex/agents/kiss_coder.toml",
        ".codex/agents/kiss_reviewer.toml",
        ".agents/plugins/marketplace.json",
        "skills/kiss-my-agent/SKILL.md",
        "skills/kiss-my-agent/references/rules/engineering-decisions.md",
        "skills/kiss-my-agent/references/rules/experiments-and-evidence.md",
        "skills/kiss-my-agent/references/cases/minimal-fix-vs-new-system.md",
        "skills/kiss-my-agent/references/cases/degraded-safety-vs-hidden-failure.md",
        "skills/kiss-my-agent/references/cases/product-contract-provenance-vs-agent-proof.md",
        "skills/kiss-my-agent/references/cases/verification-coordination-vs-workflow-platform.md",
        "skills/kiss-my-agent-setup/SKILL.md",
        "skills/kiss-my-agent-setup/assets/v0.1-agents/kiss_explorer.toml",
        "skills/kiss-my-agent-setup/assets/v0.1-agents/kiss_coder.toml",
        "skills/kiss-my-agent-setup/assets/v0.1-agents/kiss_reviewer.toml",
        "skills/kiss-my-agent-setup/setup-lifecycle.md",
        "skills/kiss-my-agent-setup/configure-agents.md",
        "assets/kiss-my-agent-hero.png",
        "examples/config.example.toml",
        "requirements-site.txt",
        "site/template.html",
        "site/style.css",
        "tests/fixtures/layered-project/AGENTS.md",
        "tests/fixtures/layered-project/component-a/AGENTS.md",
        "tests/fixtures/layered-project/component-b/subsystem/AGENTS.override.md",
        "tests/fixtures/v0.1-managed-project/.codex/config.toml",
        "tests/fixtures/v0.1-managed-project/.codex/agents/kiss_explorer.toml",
        "tests/fixtures/v0.1-managed-project/.codex/agents/kiss_coder.toml",
        "tests/fixtures/v0.1-managed-project/.codex/agents/kiss_reviewer.toml",
        "tests/fixtures/v0.1-managed-project/AGENTS.md",
        "tests/scenarios.md",
        "tests/test_build_site.py",
        "tests/test_setup.py",
        "tests/test_test_all.py",
        "scripts/build_site.py",
        "scripts/test_all.py",
        "scripts/validate.py",
        "scripts/validate.sh",
        "scripts/validate.ps1",
    }
    required.update(path for pair in DOC_PAIRS for path in pair)
    missing = sorted(relative for relative in required if not (root / relative).is_file())
    if missing:
        fail("missing required files: " + ", ".join(missing))


def validate_retired_paths(root: Path) -> None:
    if (root / ".sandbox").exists():
        fail("retired .sandbox directory is present")
    retired_stage_script = "stage-" + "sandbox.sh"
    if (root / "scripts" / retired_stage_script).exists():
        fail(f"retired {retired_stage_script} is present")


def validate_repository_config(root: Path) -> None:
    config_path = root / ".codex/config.toml"
    config = load_toml(config_path)
    if set(config) != {"model", "model_reasoning_effort", "features", "agents"}:
        fail(
            ".codex/config.toml must contain only the master model/effort and "
            "the features and agents tables"
        )
    if config["model"] != "gpt-5.6-sol":
        fail(".codex/config.toml must set master model = 'gpt-5.6-sol'")
    if config["model_reasoning_effort"] != "max":
        fail(".codex/config.toml must set master model_reasoning_effort = 'max'")
    features = config["features"]
    if not isinstance(features, dict) or set(features) != {"multi_agent"}:
        fail(".codex/config.toml features table must contain only multi_agent")
    if features["multi_agent"] is not True:
        fail(".codex/config.toml must set features.multi_agent = true")
    agents = config["agents"]
    if not isinstance(agents, dict) or set(agents) != {"enabled"}:
        fail(".codex/config.toml agents table must contain only enabled; role files are discovered")
    if agents["enabled"] is not True:
        fail(".codex/config.toml must set agents.enabled = true")


def validate_roles(root: Path) -> None:
    required_keys = {"name", "description", "developer_instructions"}
    optional_string_keys = {"model", "model_reasoning_effort", "sandbox_mode"}
    role_paths = sorted((root / ".codex/agents").glob("*.toml"))
    if not role_paths:
        fail("no role definitions found in .codex/agents")

    names: dict[str, Path] = {}
    roles: dict[str, tuple[Path, dict[str, object]]] = {}
    for path in role_paths:
        data = load_toml(path)
        missing_keys = required_keys - set(data)
        if missing_keys:
            fail(f"missing role keys in {path.relative_to(root)}: {sorted(missing_keys)}")
        for key in required_keys:
            if not isinstance(data[key], str) or not data[key].strip():
                fail(f"empty or non-string role field {key} in {path.relative_to(root)}")
        for key in optional_string_keys:
            if key in data and (not isinstance(data[key], str) or not data[key].strip()):
                fail(f"empty or non-string role field {key} in {path.relative_to(root)}")
        if "sandbox_mode" in data and data["sandbox_mode"] not in ALLOWED_SANDBOX_MODES:
            fail(f"unsupported sandbox_mode in {path.relative_to(root)}: {data['sandbox_mode']}")

        role_name = data["name"]
        if role_name in names:
            fail(
                f"duplicate role name {role_name!r} in "
                f"{names[role_name].relative_to(root)} and {path.relative_to(root)}"
            )
        names[role_name] = path
        roles[role_name] = (path, data)
        if path.stem != role_name:
            if role_name in DEFAULT_ROLE_NAMES:
                fail(f"default role name does not match filename in {path.relative_to(root)}")
            warn(
                f"role filename {path.name!r} differs from identity name {role_name!r}; "
                "the TOML name is authoritative"
            )

    for role_name in DEFAULT_ROLE_NAMES:
        expected_path = root / f".codex/agents/{role_name}.toml"
        role = roles.get(role_name)
        if role is None or role[0] != expected_path:
            fail(f"default role must be defined by .codex/agents/{role_name}.toml")
        path, data = role
        contract = DEFAULT_ROLE_CONTRACTS[role_name]
        if data.get("sandbox_mode") != contract["sandbox_mode"]:
            fail(
                f"default role {role_name} must set sandbox_mode = "
                f"{contract['sandbox_mode']!r}"
            )
        if data.get("model") != contract["model"]:
            fail(
                f"default role {role_name} must set model = {contract['model']!r}"
            )
        if data.get("model_reasoning_effort") != contract["model_reasoning_effort"]:
            fail(
                f"default role {role_name} must set model_reasoning_effort = "
                f"{contract['model_reasoning_effort']!r}"
            )
        instructions = data["developer_instructions"]
        missing_fragments = [
            fragment
            for fragment in contract["instruction_fragments"]
            if fragment not in instructions
        ]
        if missing_fragments:
            fail(
                f"default role responsibility boundary missing in {path.relative_to(root)}: "
                + ", ".join(missing_fragments)
            )


def require_nonempty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"empty or non-string field: {field}")
    return value


def validate_distribution_interfaces(root: Path) -> None:
    manifest_path = root / ".codex-plugin/plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        fail("plugin manifest must be a JSON object")
    if manifest.get("name") != "kiss-my-agent":
        fail("unexpected plugin manifest name")
    version = require_nonempty_string(manifest.get("version"), "plugin.version")
    if not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version):
        fail("plugin.version must be a stable semantic version")
    for key in ("description", "homepage", "repository", "license"):
        require_nonempty_string(manifest.get(key), f"plugin.{key}")
    if manifest["homepage"] != PROJECT_HOMEPAGE or manifest["repository"] != PROJECT_REPOSITORY:
        fail("plugin homepage and repository must identify the canonical GitHub project")
    if manifest["license"] != "MIT":
        fail("plugin.license must match the repository MIT license")
    if manifest.get("skills") != "./skills/":
        fail("plugin.skills must expose ./skills/")
    author = manifest.get("author")
    if not isinstance(author, dict):
        fail("plugin.author must be an object")
    author_name = require_nonempty_string(author.get("name"), "plugin.author.name")
    if author_name != "AoiOTA":
        fail("unexpected plugin author")
    keywords = manifest.get("keywords")
    if not isinstance(keywords, list) or not keywords:
        fail("plugin.keywords must be a non-empty list")
    for keyword in keywords:
        require_nonempty_string(keyword, "plugin.keywords[]")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail("plugin.interface must be an object")
    require_nonempty_string(interface.get("displayName"), "plugin.interface.displayName")
    for key in (
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "websiteURL",
    ):
        require_nonempty_string(interface.get(key), f"plugin.interface.{key}")
    if interface["developerName"] != author_name:
        fail("plugin.interface.developerName must match plugin.author.name")
    if interface["websiteURL"] != manifest["homepage"]:
        fail("plugin.interface.websiteURL must match plugin.homepage")
    if interface["category"] != "Developer Tools":
        fail("plugin.interface.category must be Developer Tools")
    if interface.get("capabilities") != ["Read", "Write"]:
        fail("plugin.interface.capabilities must declare only Read and Write")
    default_prompts = interface.get("defaultPrompt")
    if not isinstance(default_prompts, list) or not 1 <= len(default_prompts) <= 3:
        fail("plugin.interface.defaultPrompt must contain one to three prompts")
    for prompt in default_prompts:
        require_nonempty_string(prompt, "plugin.interface.defaultPrompt[]")
    unsupported_capabilities = {"apps", "mcpServers", "hooks", "assets"} & set(manifest)
    if unsupported_capabilities:
        fail(
            "skills-only plugin must not declare unsupported capabilities: "
            + ", ".join(sorted(unsupported_capabilities))
        )

    marketplace_path = root / ".agents/plugins/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    if not isinstance(marketplace, dict) or marketplace.get("name") != "kiss-my-agent":
        fail("unexpected marketplace identity")
    marketplace_interface = marketplace.get("interface")
    if not isinstance(marketplace_interface, dict):
        fail("marketplace.interface must be an object")
    require_nonempty_string(
        marketplace_interface.get("displayName"), "marketplace.interface.displayName"
    )
    if marketplace_interface["displayName"] != interface["displayName"]:
        fail("marketplace display name must match the plugin manifest")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail("marketplace must expose exactly one plugin")
    plugin = plugins[0]
    if not isinstance(plugin, dict) or plugin.get("name") != manifest["name"]:
        fail("marketplace plugin identity must match the plugin manifest")
    source = plugin.get("source")
    if not isinstance(source, dict):
        fail("marketplace plugin source must be an object")
    if source.get("source") != "url":
        fail("marketplace plugin source must use the Git URL interface")
    if source.get("url") != manifest["repository"]:
        fail("marketplace plugin URL must match plugin.repository")
    if source.get("ref") != f"v{version}":
        fail("marketplace plugin ref must match plugin.version")
    policy = plugin.get("policy")
    if not isinstance(policy, dict):
        fail("marketplace plugin policy must be an object")
    if policy.get("installation") != "AVAILABLE" or policy.get("authentication") != "ON_INSTALL":
        fail("marketplace plugin policy must be AVAILABLE with ON_INSTALL authentication")
    if plugin.get("category") != "Developer Tools":
        fail("marketplace plugin category must be Developer Tools")


def validate_setup_interface(root: Path) -> None:
    skill_path = root / "skills/kiss-my-agent-setup/SKILL.md"
    skill = skill_path.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if not frontmatter:
        fail("invalid setup skill frontmatter")
    fields: dict[str, str] = {}
    for line in frontmatter.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            fail("invalid setup skill frontmatter line")
        fields[key.strip()] = value.strip()
    if fields.get("name") != "kiss-my-agent-setup":
        fail("unexpected setup skill name")
    if not fields.get("description"):
        fail("empty setup skill description")
    for token in ("setup", "check", "remove", "configure", "project", "global"):
        if token not in skill:
            fail(f"setup skill interface missing: {token}")
    links = set(re.findall(r"\[[^\]\n]+\]\(([^)]+)\)", skill))
    expected_links = {
        "setup-lifecycle.md",
        "configure-agents.md",
    }
    if links != expected_links:
        fail("setup skill must route exactly to its lifecycle and configuration references")
    scripts = skill_path.parent / "scripts"
    published_sources = [] if not scripts.exists() else [
        path
        for path in scripts.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    ]
    if published_sources:
        fail("setup skill must not require bundled executable scripts")
    lifecycle = (skill_path.parent / "setup-lifecycle.md").read_text(
        encoding="utf-8"
    )
    for token in (
        "The master owns orchestration",
        "must delegate delegable bulk exploration",
        "Multiple instances of any role",
        "Coordination is flat by default",
        "independent subsystem needs substantial parallel work",
        "direct aggregation would pollute the master's context",
        "bounded department-lead assignment",
        "workers must not delegate again",
        "at most one intermediate management layer",
        "no deep nesting",
        "must not silently take over delegated work",
        "ordinary single-conversation execution",
        "executive-only workflow cannot staff delegated work",
        "Static setup cannot observe a higher-precedence `false`",
        "initial defaults, not enforcement",
        "all four managed config paths",
        "four managed config assignment lines",
        "explicit value or `inherit`",
        "Never silently substitute a fallback model or effort",
        "either the current bundled seed or the corresponding known v0.1 seed",
    ):
        if token not in lifecycle:
            fail(f"setup lifecycle compatibility contract missing: {token}")
    configure = (skill_path.parent / "configure-agents.md").read_text(
        encoding="utf-8"
    )
    for token in (
        "<unique Host project or active workspace root>/.codex/agents",
        "non-empty `CODEX_HOME`",
        "multiple roots or no unique root",
        "absolute role-directory path",
        "agents.default_subagent_model",
        "agents.default_subagent_reasoning_effort",
        "reapplies the parent turn's live sandbox and approval overrides",
    ):
        if token not in configure:
            fail(f"Agent configuration contract missing: {token}")


def validate_site_interfaces(root: Path) -> None:
    requirements = [
        line.strip()
        for line in (root / "requirements-site.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if len(requirements) != 1 or not re.fullmatch(r"Markdown==\d+\.\d+\.\d+", requirements[0]):
        fail("requirements-site.txt must pin exactly one Markdown release")

    template = (root / "site/template.html").read_text(encoding="utf-8")
    for token in ("<html", "<meta", "<main", "lang"):
        if token not in template:
            fail(f"site template interface missing: {token}")
    if not (root / "site/style.css").read_text(encoding="utf-8").strip():
        fail("site/style.css must not be empty")

    workflow = (root / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    for token in (
        "scripts/build_site.py",
        "actions/checkout@v7",
        "actions/setup-python@v7",
        "actions/configure-pages@v6",
        "actions/upload-pages-artifact@v5",
        "actions/deploy-pages@v5",
    ):
        if token not in workflow:
            fail(f"Pages workflow interface missing: {token}")

    validation_workflow = (root / ".github/workflows/validate.yml").read_text(
        encoding="utf-8"
    )
    for token in (
        'python: ["3.11", "3.12"]',
        "actions/checkout@v7",
        "actions/setup-python@v7",
        "python scripts/test_all.py",
        "requirements-site.txt",
    ):
        if token not in validation_workflow:
            fail(f"validation workflow interface missing: {token}")


def validate_collaboration_interfaces(root: Path) -> None:
    codeowners = (root / ".github/CODEOWNERS").read_text(encoding="utf-8").strip()
    if codeowners != "* @AoiOTA":
        fail("CODEOWNERS must route repository review to @AoiOTA")

    editorconfig = (root / ".editorconfig").read_text(encoding="utf-8")
    for token in ("root = true", "charset = utf-8", "end_of_line = lf"):
        if token not in editorconfig:
            fail(f"editor configuration interface missing: {token}")

    chooser = (root / ".github/ISSUE_TEMPLATE/config.yml").read_text(encoding="utf-8")
    for token in (
        "blank_issues_enabled: false",
        "/discussions/categories/q-a",
        "/discussions/categories/ideas",
        "/security/advisories/new",
    ):
        if token not in chooser:
            fail(f"issue chooser interface missing: {token}")

    for relative in (
        ".github/ISSUE_TEMPLATE/bug-report.md",
        ".github/ISSUE_TEMPLATE/documentation.md",
        ".github/ISSUE_TEMPLATE/feature-request.md",
        ".github/ISSUE_TEMPLATE/rule-or-case-proposal.md",
    ):
        template = (root / relative).read_text(encoding="utf-8")
        if not re.match(r"\A---\n.*?\n---\n", template, re.DOTALL):
            fail(f"issue template frontmatter missing: {relative}")

    contributing = (root / "CONTRIBUTING.md").read_text(encoding="utf-8")
    for token in (
        "python3 scripts/validate.py",
        "tests.test_setup",
        "python scripts/test_all.py",
        "Dogfooding KISS My Agent",
        "Squash and merge",
        "v0.2.4 Release Process",
    ):
        if token not in contributing:
            fail(f"contributor interface missing: {token}")

    release_sequence = (
        "git pull --ff-only origin main\n"
        "python3 scripts/test_all.py\n"
        "git tag -a v0.2.4"
    )
    if release_sequence not in contributing:
        fail("v0.2.4 release sequence is incomplete or out of order")

    security = (root / "SECURITY.md").read_text(encoding="utf-8")
    if "supports only its latest formal GitHub Release" not in security:
        fail("security policy must identify the supported release policy")


def validate_example_config(root: Path) -> None:
    config = load_toml(root / "examples/config.example.toml")
    for key in ("model", "model_reasoning_effort", "model_verbosity", "review_model", "approval_policy"):
        if key in config and (not isinstance(config[key], str) or not config[key].strip()):
            fail(f"invalid example config field: {key}")
    has_sandbox_mode = "sandbox_mode" in config
    has_default_permissions = "default_permissions" in config
    if has_sandbox_mode and has_default_permissions:
        fail("example config must not combine sandbox_mode and default_permissions")
    if has_sandbox_mode and config["sandbox_mode"] not in ALLOWED_SANDBOX_MODES:
        fail("invalid example config sandbox_mode")
    if has_default_permissions and (
        not isinstance(config["default_permissions"], str)
        or not config["default_permissions"].strip()
    ):
        fail("invalid example config default_permissions")
    if config.get("model") != "gpt-5.6-sol":
        fail("example config must set the master model default")
    if config.get("model_reasoning_effort") != "max":
        fail("example config must set the master reasoning effort default")
    features = config.get("features")
    agents = config.get("agents")
    if not isinstance(features, dict) or features.get("multi_agent") is not True:
        fail("example config must enable features.multi_agent")
    if not isinstance(agents, dict) or agents.get("enabled") is not True:
        fail("example config must enable agents.enabled")
    workspace_write = config.get("sandbox_workspace_write")
    if workspace_write is not None:
        if not isinstance(workspace_write, dict):
            fail("invalid example config sandbox_workspace_write table")
        if config.get("sandbox_mode") != "workspace-write":
            fail("sandbox_workspace_write requires sandbox_mode = workspace-write")


def validate_skill(root: Path) -> None:
    skill_path = root / "skills/kiss-my-agent/SKILL.md"
    skill = skill_path.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if not frontmatter:
        fail("invalid skill frontmatter")
    fields: dict[str, str] = {}
    for line in frontmatter.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            fail("invalid skill frontmatter line")
        fields[key.strip()] = value.strip()
    if fields.get("name") != "kiss-my-agent":
        fail("unexpected skill name")
    if not fields.get("description"):
        fail("empty skill description")
    if "reversible probe" not in fields["description"]:
        fail("skill description missing the reversible-probe decision trigger")

    skill_links = set(re.findall(r"\[[^\]\n]+\]\(([^)]+)\)", skill))
    expected_links = {
        "references/rules/engineering-decisions.md",
        "references/rules/experiments-and-evidence.md",
        "references/cases/minimal-fix-vs-new-system.md",
        "references/cases/degraded-safety-vs-hidden-failure.md",
        "references/cases/product-contract-provenance-vs-agent-proof.md",
        "references/cases/verification-coordination-vs-workflow-platform.md",
    }
    if skill_links != expected_links:
        fail(
            "skill routing links differ from the expected Rule/Case targets: "
            + ", ".join(sorted(skill_links))
        )

    rule_dir = skill_path.parent / "references/rules"
    case_dir = skill_path.parent / "references/cases"
    expected_rules = {"engineering-decisions.md", "experiments-and-evidence.md"}
    expected_cases = {
        "minimal-fix-vs-new-system.md",
        "degraded-safety-vs-hidden-failure.md",
        "product-contract-provenance-vs-agent-proof.md",
        "verification-coordination-vs-workflow-platform.md",
    }
    if {path.name for path in rule_dir.glob("*.md")} != expected_rules:
        fail("unexpected Rule file set")
    if {path.name for path in case_dir.glob("*.md")} != expected_cases:
        fail("unexpected Case file set")

    case_headings = (
        "## Goal",
        "## Consumer",
        "## Minimum mechanism to retain",
        "## Mechanism to reject",
        "## Deletion counterfactual",
        "## Legitimate exception",
    )
    for case_path in sorted(case_dir.glob("*.md")):
        headings = tuple(
            line
            for line in case_path.read_text(encoding="utf-8").splitlines()
            if line.startswith("## ")
        )
        if headings != case_headings:
            fail(f"case structure invalid: {case_path.relative_to(root)}")


def contains_invocation(text: str, invocation: str) -> bool:
    return invocation in PUBLIC_INVOCATION_TOKEN.findall(text)


def validate_public_invocations(root: Path) -> None:
    for relative in PUBLIC_INVOCATION_SOURCES:
        text = (root / relative).read_text(encoding="utf-8")
        for match in PUBLIC_INVOCATION_TOKEN.finditer(text):
            if match.group(0) not in ALLOWED_PUBLIC_INVOCATIONS:
                line = text.count("\n", 0, match.start()) + 1
                fail(f"invalid Skill invocation in {relative}:{line}: {match.group(0)}")

    for relative in SETUP_INVOCATION_SOURCES:
        text = (root / relative).read_text(encoding="utf-8")
        if not contains_invocation(text, QUALIFIED_SETUP_INVOCATION):
            fail(f"qualified setup invocation missing from {relative}")

    skill_relative = "skills/kiss-my-agent/SKILL.md"
    skill = (root / skill_relative).read_text(encoding="utf-8")
    if not contains_invocation(skill, QUALIFIED_DECISION_INVOCATION):
        fail(f"qualified self-invocation missing from {skill_relative}")


def markdown_targets(text: str) -> list[str]:
    return re.findall(r"!?\[[^\]\n]*\]\(([^)]+)\)", text)


def local_target(path: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>").split(maxsplit=1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    path_part = target.split("#", 1)[0].split("?", 1)[0]
    if not path_part:
        return None
    return (path.parent / path_part).resolve()


def stable_anchors(path: Path, text: str) -> tuple[str, ...]:
    anchors = tuple(
        re.findall(
            r'^\s*<a\s+id="([a-z0-9]+(?:-[a-z0-9]+)*)"\s*></a>\s*$',
            text,
            re.MULTILINE,
        )
    )
    if len(anchors) != len(set(anchors)):
        fail(f"duplicate stable anchor in {path}")
    return anchors


def command_blocks(path: Path, text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        opening = re.fullmatch(r"\s*(`{3,}|~{3,})([^\s`]*)\s*", lines[index])
        if not opening:
            index += 1
            continue
        marker = opening.group(1)
        language = opening.group(2).casefold()
        content: list[str] = []
        index += 1
        closing = rf"\s*{re.escape(marker[0])}{{{len(marker)},}}\s*"
        while index < len(lines) and not re.fullmatch(closing, lines[index]):
            content.append(lines[index])
            index += 1
        if index == len(lines):
            fail(f"unterminated fenced code block in {path}")
        if language in COMMAND_FENCE_LANGUAGES:
            blocks.append((language, "\n".join(content)))
        index += 1
    return blocks


def validate_bilingual_documents(root: Path) -> None:
    for english_relative, chinese_relative in DOC_PAIRS:
        english_path = root / english_relative
        chinese_path = root / chinese_relative
        english = english_path.read_text(encoding="utf-8")
        chinese = chinese_path.read_text(encoding="utf-8")

        if english_relative == "README.md":
            expected_pages_links = {PROJECT_PAGES, PROJECT_PAGES_ZH}
            english_links = set(markdown_targets(english))
            chinese_links = set(markdown_targets(chinese))
            if not expected_pages_links <= english_links or not expected_pages_links <= chinese_links:
                fail("README language links must use the verified Pages URLs")
        else:
            english_links = {
                target
                for raw_target in markdown_targets(english)
                if (target := local_target(english_path, raw_target)) is not None
            }
            chinese_links = {
                target
                for raw_target in markdown_targets(chinese)
                if (target := local_target(chinese_path, raw_target)) is not None
            }
            if (
                chinese_path.resolve() not in english_links
                or english_path.resolve() not in chinese_links
            ):
                fail(f"bilingual cross-links missing for {english_relative} and {chinese_relative}")

        english_anchors = stable_anchors(english_path.relative_to(root), english)
        chinese_anchors = stable_anchors(chinese_path.relative_to(root), chinese)
        if not english_anchors:
            fail(f"no explicit stable anchors in bilingual pair {english_relative}")
        if english_anchors != chinese_anchors:
            fail(f"stable anchors differ in bilingual pair {english_relative}")
        if command_blocks(english_path.relative_to(root), english) != command_blocks(
            chinese_path.relative_to(root), chinese
        ):
            fail(f"command code blocks differ in bilingual pair {english_relative}")

    english_readme = (root / "README.md").read_text(encoding="utf-8")
    chinese_readme = (root / "README.zh-CN.md").read_text(encoding="utf-8")
    hero_pattern = re.compile(r"\A!\[[^\]\n]+\]\(assets/kiss-my-agent-hero\.png\)")
    if not hero_pattern.search(english_readme) or not hero_pattern.search(chinese_readme):
        fail("README hero must use a relative path and non-empty alt text")


def validate_document_interfaces(root: Path) -> None:
    installation = (root / "docs/INSTALLATION.md").read_text(encoding="utf-8")
    for interface_name in (
        "kiss-my-agent",
        "kiss-my-agent-setup",
        "kiss_explorer",
        "kiss_coder",
        "kiss_reviewer",
        "AGENTS.override.md",
        "codex plugin marketplace add",
        "configure agents for this project",
        "codex plugin marketplace upgrade kiss-my-agent",
        "/skills",
    ):
        if interface_name not in installation:
            fail(f"installation interface missing: {interface_name}")
    configuration = (root / "docs/CONFIGURATION.md").read_text(encoding="utf-8")
    for config_key in (
        "features.multi_agent",
        "agents.enabled",
        "model",
        "model_reasoning_effort",
        "sandbox_mode",
    ):
        if config_key not in configuration:
            fail(f"configuration key guidance missing: {config_key}")
    for token in (
        "model = \"gpt-5.6-sol\"",
        "model_reasoning_effort = \"max\"",
        "`kiss_explorer` | Read-only investigation | `gpt-5.6-sol` | `high`",
        "`kiss_coder` | Bounded implementation and state changes | `gpt-5.6-sol` | `high`",
        "`kiss_reviewer` | Independent read-only review | `gpt-5.6-sol` | `xhigh`",
        "initial defaults, not enforcement",
        "parent turn's live sandbox and approval overrides",
        "ordinary single-conversation execution",
        "Coordination is flat by default",
        "at most one intermediate management layer",
        "bounded department-lead assignment",
        "Every shared file or resource still has one writer or operator",
        "highest-precedence CLI override",
        "never silently substitutes a fallback model or effort",
    ):
        if token not in configuration:
            fail(f"configuration behavior guidance missing: {token}")


def validate_fixtures(root: Path) -> int:
    fixture = root / "tests/fixtures/layered-project"
    fixture_markers = {
        fixture / "AGENTS.md": "fixture-root",
        fixture / "component-a/AGENTS.md": "component-a",
        fixture / "component-b/subsystem/AGENTS.override.md": "subsystem-override",
    }
    for path, marker in fixture_markers.items():
        if marker not in path.read_text(encoding="utf-8"):
            fail(f"effective-instruction fixture marker missing: {marker}")
    v010_fixture = root / "tests/fixtures/v0.1-managed-project"
    v010_assets = root / "skills/kiss-my-agent-setup/assets"
    for role_name in DEFAULT_ROLE_NAMES:
        legacy_path = v010_fixture / f".codex/agents/{role_name}.toml"
        asset_path = v010_assets / f"v0.1-agents/{role_name}.toml"
        if asset_path.read_bytes() != legacy_path.read_bytes():
            fail(f"Skill-owned v0.1 remove seed differs from project fixture: {role_name}")
        legacy = load_toml(legacy_path)
        asset = load_toml(asset_path)
        if asset.get("name") != role_name:
            fail(f"Skill-owned v0.1 remove seed identity differs from filename: {role_name}")
        if "model_reasoning_effort" in legacy or "model" in legacy:
            fail(f"v0.1 role fixture contains a current model setting: {role_name}")
    effective_chain = [
        root / "AGENTS.md",
        fixture / "AGENTS.md",
        fixture / "component-b/subsystem/AGENTS.override.md",
    ]
    return sum(len(path.read_bytes()) for path in effective_chain)


ARCHIVE_EXCLUDED_DIRECTORIES = {
    ".cache",
    ".git",
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "_site",
    "cache",
    "node_modules",
    "venv",
}


def repository_paths(root: Path) -> list[Path]:
    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
        )
        return [
            root / os.fsdecode(relative)
            for relative in sorted(set(result.stdout.rstrip(b"\0").split(b"\0")))
            if relative
        ]

    paths: list[Path] = []
    for directory, names, filenames in os.walk(root):
        names[:] = sorted(
            name for name in names if name not in ARCHIVE_EXCLUDED_DIRECTORIES
        )
        base = Path(directory)
        paths.extend(
            base / name
            for name in sorted(filenames)
            if not name.endswith(".pyc")
        )
    return paths


def repository_text_files(root: Path) -> list[Path]:
    text_files: list[Path] = []
    for path in repository_paths(root):
        if not path.is_file():
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        text_files.append(path)
    return text_files


def validate_trailing_whitespace(root: Path, text_files: list[Path]) -> None:
    offenders: list[str] = []
    for path in text_files:
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            if line.endswith((" ", "\t")):
                offenders.append(f"{path.relative_to(root)}:{line_number}")
    if offenders:
        fail(
            "trailing whitespace violates .editorconfig:\n"
            + "\n".join(offenders)
        )


def validate_hygiene(root: Path, text_files: list[Path]) -> None:
    legacy_skill_name = "research" + "-mvp-" + "engineering"
    retired_staging_pattern = "stage-" + "sandbox|\\." + "sandbox/"
    legacy_user_skill_pattern = re.escape("$CODEX_HOME/" + "skills/kiss-my-agent")
    forbidden_patterns = [
        ("retired staging workflow", re.compile(retired_staging_pattern, re.IGNORECASE)),
        ("legacy user Skill path", re.compile(legacy_user_skill_pattern, re.IGNORECASE)),
        (
            "private underscored project identifier",
            re.compile(r"(?<![A-Za-z0-9])" + "bio" + "_nav" + r"(?![A-Za-z0-9])", re.IGNORECASE),
        ),
        (
            "private compact project identifier",
            re.compile(r"(?<![A-Za-z0-9])" + "bio" + "nav" + r"(?![A-Za-z0-9])", re.IGNORECASE),
        ),
        (
            "specific middleware identifier",
            re.compile(r"(?<![A-Za-z0-9_])r" + "os" + r"(?:\d+)?(?![A-Za-z0-9_])", re.IGNORECASE),
        ),
        (
            "specific simulator identifier",
            re.compile(r"(?<![A-Za-z0-9_])" + "isa" + "ac" + r"(?![A-Za-z0-9_])", re.IGNORECASE),
        ),
        ("private user path", re.compile(re.escape("/home/" + "lyb"), re.IGNORECASE)),
    ]
    offenders: list[str] = []
    for path in text_files:
        text = path.read_text(encoding="utf-8")
        hits = [label for label, pattern in forbidden_patterns if pattern.search(text)]
        if legacy_skill_name.casefold() in text.casefold():
            hits.append("retired skill name")
        if hits:
            offenders.append(f"{path.relative_to(root)}: {', '.join(hits)}")
    if offenders:
        fail("repository hygiene violations:\n" + "\n".join(offenders))
    symlinks = [
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_symlink() and ".git" not in path.parts
    ]
    if symlinks:
        fail("repository symlinks are not expected: " + ", ".join(map(str, symlinks)))


def validate_relative_links(root: Path, text_files: list[Path]) -> None:
    broken_links: list[str] = []
    for path in (candidate for candidate in text_files if candidate.suffix.casefold() == ".md"):
        for raw_target in markdown_targets(path.read_text(encoding="utf-8")):
            target = raw_target.strip().strip("<>").split(maxsplit=1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue
            if path_part.startswith("/"):
                broken_links.append(f"{path.relative_to(root)}: absolute link {target}")
                continue
            resolved = (path.parent / path_part).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                broken_links.append(f"{path.relative_to(root)}: link escapes repository {target}")
                continue
            if not resolved.exists():
                broken_links.append(f"{path.relative_to(root)}: missing {target}")
    if broken_links:
        fail("relative link violations:\n" + "\n".join(broken_links))


def validate_hero(root: Path) -> tuple[int, int, int]:
    hero_data = (root / "assets/kiss-my-agent-hero.png").read_bytes()
    if len(hero_data) < 10_000 or len(hero_data) > 10 * 1024 * 1024:
        fail(f"hero file size is implausible: {len(hero_data)} bytes")
    if hero_data[:8] != b"\x89PNG\r\n\x1a\n" or hero_data[12:16] != b"IHDR":
        fail("hero is not a valid PNG header")
    width, height = struct.unpack(">II", hero_data[16:24])
    if width < 1200 or height < 400:
        fail(f"hero dimensions are too small: {width}x{height}")
    return width, height, len(hero_data)


def validate(root: Path) -> None:
    require_files(root)
    validate_retired_paths(root)
    validate_repository_config(root)
    validate_roles(root)
    validate_distribution_interfaces(root)
    validate_setup_interface(root)
    validate_site_interfaces(root)
    validate_collaboration_interfaces(root)
    validate_example_config(root)
    validate_skill(root)
    validate_public_invocations(root)
    validate_bilingual_documents(root)
    validate_document_interfaces(root)
    chain_bytes = validate_fixtures(root)
    text_files = repository_text_files(root)
    validate_trailing_whitespace(root, text_files)
    validate_hygiene(root, text_files)
    validate_relative_links(root, text_files)
    width, height, hero_bytes = validate_hero(root)
    print(f"effective-chain-bytes={chain_bytes}")
    print(f"hero={width}x{height}:{hero_bytes}-bytes")
    print(f"bilingual-pairs={len(DOC_PAIRS)}")
    print("static-validation=PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root (defaults to the parent of this script directory)",
    )
    return parser.parse_args()


def main() -> int:
    root = parse_args().root.resolve()
    try:
        validate(root)
    except (json.JSONDecodeError, tomllib.TOMLDecodeError, ValidationError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
