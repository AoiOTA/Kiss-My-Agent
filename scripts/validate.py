#!/usr/bin/env python3
"""Cross-platform static validation for the KISS My Agent repository."""

from __future__ import annotations

import argparse
import re
import struct
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    print("validation failed: Python 3.11 or newer is required", file=sys.stderr)
    raise SystemExit(1)

import tomllib


ROLE_NAMES = ("kiss_explorer", "kiss_coder", "kiss_reviewer")
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


class ValidationError(Exception):
    """A repository invariant is not satisfied."""


def fail(message: str) -> None:
    raise ValidationError(message)


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
        ".gitattributes",
        ".gitignore",
        ".github/ISSUE_TEMPLATE/bug-report.md",
        ".github/ISSUE_TEMPLATE/rule-or-case-proposal.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/workflows/validate.yml",
        ".codex/config.toml",
        ".codex/agents/kiss_explorer.toml",
        ".codex/agents/kiss_coder.toml",
        ".codex/agents/kiss_reviewer.toml",
        ".agents/skills/kiss-my-agent/SKILL.md",
        ".agents/skills/kiss-my-agent/references/rules/engineering-decisions.md",
        ".agents/skills/kiss-my-agent/references/rules/experiments-and-evidence.md",
        ".agents/skills/kiss-my-agent/references/cases/minimal-fix-vs-new-system.md",
        ".agents/skills/kiss-my-agent/references/cases/degraded-safety-vs-hidden-failure.md",
        ".agents/skills/kiss-my-agent/references/cases/product-contract-provenance-vs-agent-proof.md",
        ".agents/skills/kiss-my-agent/references/cases/verification-coordination-vs-workflow-platform.md",
        "assets/kiss-my-agent-hero.png",
        "examples/config.example.toml",
        "tests/fixtures/layered-project/AGENTS.md",
        "tests/fixtures/layered-project/component-a/AGENTS.md",
        "tests/fixtures/layered-project/component-b/subsystem/AGENTS.override.md",
        "tests/scenarios.md",
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
    retired_roles = ("explorer.toml", "coder.toml", "review.toml")
    if any((root / ".codex/agents" / name).exists() for name in retired_roles):
        fail("retired generic KISS role file is present")


def validate_repository_config(root: Path) -> None:
    config_path = root / ".codex/config.toml"
    config = load_toml(config_path)
    if set(config) != {"agents"}:
        fail(".codex/config.toml must contain only the agents table")
    agents = config["agents"]
    if not isinstance(agents, dict) or set(agents) != {"enabled", *ROLE_NAMES}:
        fail(".codex/config.toml agents table must contain enabled and the three KISS roles")
    if agents["enabled"] is not True:
        fail(".codex/config.toml must set agents.enabled = true")
    for role_name in ROLE_NAMES:
        registration = agents[role_name]
        if not isinstance(registration, dict) or set(registration) != {"description", "config_file"}:
            fail(f"invalid minimal registration for {role_name} in .codex/config.toml")
        description = registration["description"]
        if not isinstance(description, str) or not description.strip():
            fail(f"invalid registration description for {role_name} in .codex/config.toml")
        expected_path = f"agents/{role_name}.toml"
        if registration["config_file"] != expected_path:
            fail(f"invalid config_file registration for {role_name} in .codex/config.toml")
        if not (config_path.parent / expected_path).is_file():
            fail(f"registered role file does not exist: {expected_path}")


def validate_roles(root: Path) -> None:
    required_keys = {"name", "description", "developer_instructions"}
    for role_name in ROLE_NAMES:
        path = root / f".codex/agents/{role_name}.toml"
        data = load_toml(path)
        missing_keys = required_keys - set(data)
        if missing_keys:
            fail(f"missing role keys in {path.relative_to(root)}: {sorted(missing_keys)}")
        if data["name"] != role_name:
            fail(f"role name does not match filename in {path.relative_to(root)}")
        for key in ("description", "developer_instructions"):
            if not isinstance(data[key], str) or not data[key].strip():
                fail(f"empty or non-string role field {key} in {path.relative_to(root)}")
        for key in ("model", "model_reasoning_effort"):
            if key in data and (not isinstance(data[key], str) or not data[key].strip()):
                fail(f"empty or non-string role field {key} in {path.relative_to(root)}")
        if "sandbox_mode" in data and data["sandbox_mode"] not in ALLOWED_SANDBOX_MODES:
            fail(f"unsupported sandbox_mode in {path.relative_to(root)}: {data['sandbox_mode']}")


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
    workspace_write = config.get("sandbox_workspace_write")
    if workspace_write is not None:
        if not isinstance(workspace_write, dict):
            fail("invalid example config sandbox_workspace_write table")
        if config.get("sandbox_mode") != "workspace-write":
            fail("sandbox_workspace_write requires sandbox_mode = workspace-write")


def validate_skill(root: Path) -> None:
    skill_path = root / ".agents/skills/kiss-my-agent/SKILL.md"
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
        if chinese_path.resolve() not in english_links or english_path.resolve() not in chinese_links:
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
        "kiss_explorer",
        "kiss_coder",
        "kiss_reviewer",
        "AGENTS.override.md",
        "$HOME/.agents/skills",
        "/skills",
    ):
        if interface_name not in installation:
            fail(f"installation interface missing: {interface_name}")
    configuration = (root / "docs/CONFIGURATION.md").read_text(encoding="utf-8")
    for config_key in (
        "model_context_window",
        "model_auto_compact_token_limit",
        "agents.max_concurrent_threads_per_session",
        "sandbox_mode",
        "approval_policy",
    ):
        if config_key not in configuration:
            fail(f"configuration key guidance missing: {config_key}")


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
    effective_chain = [
        root / "AGENTS.md",
        fixture / "AGENTS.md",
        fixture / "component-b/subsystem/AGENTS.override.md",
    ]
    return sum(len(path.read_bytes()) for path in effective_chain)


def repository_text_files(root: Path) -> list[Path]:
    text_files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        text_files.append(path)
    return text_files


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
    validate_example_config(root)
    validate_skill(root)
    validate_bilingual_documents(root)
    validate_document_interfaces(root)
    chain_bytes = validate_fixtures(root)
    text_files = repository_text_files(root)
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
    except (tomllib.TOMLDecodeError, ValidationError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
