#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd -P)

bash -n "$repo_root/scripts/"*.sh

python3 - "$repo_root" <<'PY'
from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

try:
    import tomllib
except ImportError as exc:
    raise SystemExit("python3 with tomllib is required") from exc

root = Path(sys.argv[1]).resolve()

required = [
    "AGENTS.md",
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    ".gitignore",
    ".github/ISSUE_TEMPLATE/bug-report.md",
    ".github/ISSUE_TEMPLATE/rule-or-case-proposal.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
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
    "docs/INSTALLATION.md",
    "docs/CONFIGURATION.md",
    "docs/EXTENDING.md",
    "docs/FAQ.md",
    "examples/config.example.toml",
    "tests/fixtures/layered-project/AGENTS.md",
    "tests/fixtures/layered-project/component-a/AGENTS.md",
    "tests/fixtures/layered-project/component-b/subsystem/AGENTS.override.md",
    "tests/scenarios.md",
    "scripts/validate.sh",
]
missing = [relative for relative in required if not (root / relative).is_file()]
if missing:
    raise SystemExit("missing required files: " + ", ".join(missing))

if (root / ".sandbox").exists():
    raise SystemExit("retired .sandbox directory is present")
retired_stage_script = "stage-" + "sandbox.sh"
if (root / "scripts" / retired_stage_script).exists():
    raise SystemExit(f"retired {retired_stage_script} is present")
if (root / ".codex/config.toml").exists():
    raise SystemExit("repository must not ship an active .codex/config.toml")

role_files = {
    "kiss_explorer": root / ".codex/agents/kiss_explorer.toml",
    "kiss_coder": root / ".codex/agents/kiss_coder.toml",
    "kiss_reviewer": root / ".codex/agents/kiss_reviewer.toml",
}
retired_role_files = [
    root / ".codex/agents/explorer.toml",
    root / ".codex/agents/coder.toml",
    root / ".codex/agents/review.toml",
]
if any(path.exists() for path in retired_role_files):
    raise SystemExit("retired generic KISS role file is present")

required_role_keys = {
    "name",
    "description",
    "developer_instructions",
}
allowed_sandbox_modes = {"read-only", "workspace-write", "danger-full-access"}
for role_name, path in role_files.items():
    with path.open("rb") as stream:
        data = tomllib.load(stream)
    missing_keys = required_role_keys - set(data)
    if missing_keys:
        raise SystemExit(f"missing role keys in {path.relative_to(root)}: {sorted(missing_keys)}")
    if data["name"] != role_name:
        raise SystemExit(f"role name does not match filename in {path.relative_to(root)}")
    for key in ("description", "developer_instructions"):
        if not isinstance(data[key], str) or not data[key].strip():
            raise SystemExit(f"empty or non-string role field {key} in {path.relative_to(root)}")
    for key in ("model", "model_reasoning_effort"):
        if key in data and (not isinstance(data[key], str) or not data[key].strip()):
            raise SystemExit(f"empty or non-string role field {key} in {path.relative_to(root)}")
    if "sandbox_mode" in data and data["sandbox_mode"] not in allowed_sandbox_modes:
        raise SystemExit(f"unsupported sandbox_mode in {path.relative_to(root)}: {data['sandbox_mode']}")

example_config_path = root / "examples/config.example.toml"
with example_config_path.open("rb") as stream:
    example_config = tomllib.load(stream)
for key in ("model", "model_reasoning_effort", "model_verbosity", "review_model", "approval_policy"):
    if key in example_config and (not isinstance(example_config[key], str) or not example_config[key].strip()):
        raise SystemExit(f"invalid example config field: {key}")
has_sandbox_mode = "sandbox_mode" in example_config
has_default_permissions = "default_permissions" in example_config
if has_sandbox_mode and has_default_permissions:
    raise SystemExit("example config must not combine sandbox_mode and default_permissions")
if has_sandbox_mode and example_config["sandbox_mode"] not in allowed_sandbox_modes:
    raise SystemExit("invalid example config sandbox_mode")
if has_default_permissions and (
    not isinstance(example_config["default_permissions"], str)
    or not example_config["default_permissions"].strip()
):
    raise SystemExit("invalid example config default_permissions")
example_agents = example_config.get("agents")
if not isinstance(example_agents, dict):
    raise SystemExit("invalid example config agents table")
workspace_write_config = example_config.get("sandbox_workspace_write")
if workspace_write_config is not None:
    if not isinstance(workspace_write_config, dict):
        raise SystemExit("invalid example config sandbox_workspace_write table")
    if example_config.get("sandbox_mode") != "workspace-write":
        raise SystemExit("sandbox_workspace_write requires sandbox_mode = workspace-write")
for role_name in role_files:
    registration = example_agents.get(role_name)
    if not isinstance(registration, dict):
        raise SystemExit(f"missing example config registration for {role_name}")
    if registration.get("config_file") != f"agents/{role_name}.toml":
        raise SystemExit(f"invalid config_file registration for {role_name}")
    if not isinstance(registration.get("description"), str) or not registration["description"].strip():
        raise SystemExit(f"invalid registration description for {role_name}")

skill_path = root / ".agents/skills/kiss-my-agent/SKILL.md"
skill = skill_path.read_text(encoding="utf-8")
frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
if not frontmatter:
    raise SystemExit("invalid skill frontmatter")
frontmatter_fields = {}
for line in frontmatter.group(1).splitlines():
    key, separator, value = line.partition(":")
    if not separator:
        raise SystemExit("invalid skill frontmatter line")
    frontmatter_fields[key.strip()] = value.strip()
if frontmatter_fields.get("name") != "kiss-my-agent":
    raise SystemExit("unexpected skill name")
if not frontmatter_fields.get("description"):
    raise SystemExit("empty skill description")

skill_links = set(re.findall(r"\[[^\]\n]+\]\(([^)]+)\)", skill))
expected_skill_links = {
    "references/rules/engineering-decisions.md",
    "references/rules/experiments-and-evidence.md",
    "references/cases/minimal-fix-vs-new-system.md",
    "references/cases/degraded-safety-vs-hidden-failure.md",
    "references/cases/product-contract-provenance-vs-agent-proof.md",
    "references/cases/verification-coordination-vs-workflow-platform.md",
}
if skill_links != expected_skill_links:
    raise SystemExit(
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
    raise SystemExit("unexpected Rule file set")
if {path.name for path in case_dir.glob("*.md")} != expected_cases:
    raise SystemExit("unexpected Case file set")

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
        raise SystemExit(f"case structure invalid: {case_path.relative_to(root)}")

english = (root / "README.md").read_text(encoding="utf-8")
chinese = (root / "README.zh-CN.md").read_text(encoding="utf-8")
if "[简体中文](README.zh-CN.md)" not in english or "[English](README.md)" not in chinese:
    raise SystemExit("bilingual README cross-links missing")
hero_pattern = re.compile(r"\A!\[[^\]\n]+\]\(assets/kiss-my-agent-hero\.png\)")
if not hero_pattern.search(english) or not hero_pattern.search(chinese):
    raise SystemExit("README hero must use a relative path and non-empty alt text")

def bash_blocks(text: str) -> list[str]:
    return [block.strip() for block in re.findall(r"```bash\n(.*?)\n```", text, re.DOTALL)]

if bash_blocks(english) != bash_blocks(chinese):
    raise SystemExit("bilingual README bash commands differ")

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
        raise SystemExit(f"installation interface missing: {interface_name}")

configuration = (root / "docs/CONFIGURATION.md").read_text(encoding="utf-8")
for config_key in (
    "model_context_window",
    "model_auto_compact_token_limit",
    "agents.max_concurrent_threads_per_session",
    "sandbox_mode",
    "approval_policy",
):
    if config_key not in configuration:
        raise SystemExit(f"configuration key guidance missing: {config_key}")

fixture = root / "tests/fixtures/layered-project"
fixture_markers = {
    fixture / "AGENTS.md": "fixture-root",
    fixture / "component-a/AGENTS.md": "component-a",
    fixture / "component-b/subsystem/AGENTS.override.md": "subsystem-override",
}
for path, marker in fixture_markers.items():
    if marker not in path.read_text(encoding="utf-8"):
        raise SystemExit(f"effective-instruction fixture marker missing: {marker}")

legacy_skill_name = "research" + "-mvp-" + "engineering"
retired_staging_pattern = "stage-" + "sandbox|\\." + "sandbox/"
legacy_user_skill_pattern = re.escape("$CODEX_HOME/" + "skills/kiss-my-agent")
forbidden_patterns = [
    ("retired staging workflow", re.compile(retired_staging_pattern, re.IGNORECASE)),
    ("legacy user Skill path", re.compile(legacy_user_skill_pattern, re.IGNORECASE)),
    ("private underscored project identifier", re.compile(r"(?<![A-Za-z0-9])" + "bio" + "_nav" + r"(?![A-Za-z0-9])", re.IGNORECASE)),
    ("private compact project identifier", re.compile(r"(?<![A-Za-z0-9])" + "bio" + "nav" + r"(?![A-Za-z0-9])", re.IGNORECASE)),
    ("specific middleware identifier", re.compile(r"(?<![A-Za-z0-9_])r" + "os" + r"(?:\d+)?(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("specific simulator identifier", re.compile(r"(?<![A-Za-z0-9_])" + "isa" + "ac" + r"(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("private user path", re.compile(re.escape("/home/" + "lyb"), re.IGNORECASE)),
]
text_files = []
offenders = []
for path in root.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    text_files.append(path)
    hits = [label for label, pattern in forbidden_patterns if pattern.search(text)]
    if legacy_skill_name.casefold() in text.casefold():
        hits.append("retired skill name")
    if hits:
        offenders.append(f"{path.relative_to(root)}: {', '.join(hits)}")
if offenders:
    raise SystemExit("repository hygiene violations:\n" + "\n".join(offenders))

symlinks = [
    path.relative_to(root)
    for path in root.rglob("*")
    if path.is_symlink() and ".git" not in path.parts
]
if symlinks:
    raise SystemExit("repository symlinks are not expected: " + ", ".join(map(str, symlinks)))

link_pattern = re.compile(r"!?\[[^\]\n]*\]\(([^)]+)\)")
broken_links = []
for path in (path for path in text_files if path.suffix.casefold() == ".md"):
    for raw_target in link_pattern.findall(path.read_text(encoding="utf-8")):
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
    raise SystemExit("relative link violations:\n" + "\n".join(broken_links))

hero = root / "assets/kiss-my-agent-hero.png"
hero_data = hero.read_bytes()
if len(hero_data) < 10_000 or len(hero_data) > 10 * 1024 * 1024:
    raise SystemExit(f"hero file size is implausible: {len(hero_data)} bytes")
if hero_data[:8] != b"\x89PNG\r\n\x1a\n" or hero_data[12:16] != b"IHDR":
    raise SystemExit("hero is not a valid PNG header")
width, height = struct.unpack(">II", hero_data[16:24])
if width < 1200 or height < 400:
    raise SystemExit(f"hero dimensions are too small: {width}x{height}")

effective_chain = [
    root / "AGENTS.md",
    fixture / "AGENTS.md",
    fixture / "component-b/subsystem/AGENTS.override.md",
]
chain_bytes = sum(len(path.read_bytes()) for path in effective_chain)

print(f"effective-chain-bytes={chain_bytes}")
print(f"hero={width}x{height}:{len(hero_data)}-bytes")
print("static-validation=PASS")
PY

printf 'validation=PASS\n'
