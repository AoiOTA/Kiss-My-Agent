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
    ".codex/agents/explorer.toml",
    ".codex/agents/coder.toml",
    ".codex/agents/review.toml",
    ".agents/skills/kiss-my-agent/SKILL.md",
    ".agents/skills/kiss-my-agent/references/rules/engineering-decisions.md",
    ".agents/skills/kiss-my-agent/references/rules/experiments-and-evidence.md",
    ".agents/skills/kiss-my-agent/references/cases/minimal-fix-vs-new-system.md",
    ".agents/skills/kiss-my-agent/references/cases/degraded-safety-vs-hidden-failure.md",
    ".agents/skills/kiss-my-agent/references/cases/product-contract-provenance-vs-agent-proof.md",
    ".agents/skills/kiss-my-agent/references/cases/verification-coordination-vs-workflow-platform.md",
    "assets/kiss-my-agent-hero.png",
    "docs/INSTALLATION.md",
    "docs/EXTENDING.md",
    "docs/FAQ.md",
    "tests/fixtures/layered-project/AGENTS.md",
    "tests/fixtures/layered-project/component-a/AGENTS.md",
    "tests/fixtures/layered-project/component-b/subsystem/AGENTS.override.md",
    "tests/scenarios.md",
    "scripts/stage-sandbox.sh",
    "scripts/validate.sh",
]
missing = [path for path in required if not (root / path).is_file()]
if missing:
    raise SystemExit("missing required files: " + ", ".join(missing))

expected_roles = {
    "explorer": ("gpt-5.6-sol", "medium", "read-only"),
    "coder": ("gpt-5.6-sol", "high", "workspace-write"),
    "review": ("gpt-5.6-sol", "xhigh", "read-only"),
}
expected_keys = {
    "name",
    "description",
    "model",
    "model_reasoning_effort",
    "sandbox_mode",
    "developer_instructions",
}
for role, expected in expected_roles.items():
    path = root / ".codex" / "agents" / f"{role}.toml"
    with path.open("rb") as stream:
        data = tomllib.load(stream)
    if set(data) != expected_keys:
        raise SystemExit(f"unexpected keys in {path.relative_to(root)}: {sorted(set(data) ^ expected_keys)}")
    actual = (data["model"], data["model_reasoning_effort"], data["sandbox_mode"])
    if data["name"] != role or actual != expected:
        raise SystemExit(f"invalid role settings in {path.relative_to(root)}")
    if not data["description"].strip() or not data["developer_instructions"].strip():
        raise SystemExit(f"empty role text in {path.relative_to(root)}")

skill_path = root / ".agents/skills/kiss-my-agent/SKILL.md"
skill = skill_path.read_text(encoding="utf-8")
frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
if not frontmatter:
    raise SystemExit("invalid skill frontmatter")
fields = {}
for line in frontmatter.group(1).splitlines():
    key, separator, value = line.partition(":")
    if not separator:
        raise SystemExit("invalid skill frontmatter line")
    fields[key.strip()] = value.strip()
if set(fields) != {"name", "description"}:
    raise SystemExit("skill frontmatter must contain only name and description")
if fields["name"] != "kiss-my-agent":
    raise SystemExit("unexpected skill name")
for required_phrase in (
    "non-obvious decision",
    "Do not use for an already-decided implementation",
    "Invoke this skill explicitly as `$kiss-my-agent`",
    "Do not read all rules or cases",
):
    if required_phrase not in skill:
        raise SystemExit(f"skill routing phrase missing: {required_phrase}")

rule_dir = skill_path.parent / "references/rules"
case_dir = skill_path.parent / "references/cases"
if {path.name for path in rule_dir.glob("*.md")} != {
    "engineering-decisions.md",
    "experiments-and-evidence.md",
}:
    raise SystemExit("skill must contain exactly the two expected rules")
if {path.name for path in case_dir.glob("*.md")} != {
    "minimal-fix-vs-new-system.md",
    "degraded-safety-vs-hidden-failure.md",
    "product-contract-provenance-vs-agent-proof.md",
    "verification-coordination-vs-workflow-platform.md",
}:
    raise SystemExit("skill must contain exactly the four expected cases")

engineering = (rule_dir / "engineering-decisions.md").read_text(encoding="utf-8")
for phrase in (
    "Silent Rent Test",
    "single-caller",
    "A supported conclusion that no change is needed",
    "cannot justify one another as a cluster",
    "non-exhaustive semantic map, not a keyword gate",
    "Agent uncertainty and rule vocabulary are not product requirements",
    "top-level lifecycle owner",
    "Five-question review",
    "Goal and stop boundary",
):
    if phrase not in engineering:
        raise SystemExit(f"engineering rule phrase missing: {phrase}")
mechanism_rows = [
    line
    for line in engineering.splitlines()
    if line.startswith("| ") and line not in {"| Class | Semantics to examine |", "| --- | --- |"}
]
if len(mechanism_rows) != 12:
    raise SystemExit(f"expected 12 mechanism rows, found {len(mechanism_rows)}")

evidence = (rule_dir / "experiments-and-evidence.md").read_text(encoding="utf-8")
for phrase in (
    "research question, primary variable, controlled variables, core metric, and invalid conditions",
    "Valid negative",
    "Invalid means",
    "Stale-artifact discrimination",
    "runtime ambiguity",
    "Record version identity",
    "Reuse existing evidence",
    "assign one writer/operator",
    "designated artifact store",
    "evidence labels defined in `AGENTS.md`",
):
    if phrase not in evidence:
        raise SystemExit(f"evidence rule phrase missing: {phrase}")

case_headings = (
    "## Goal",
    "## Consumer",
    "## Minimum mechanism to retain",
    "## Mechanism to reject",
    "## Deletion counterfactual",
    "## Legitimate exception",
)
for case_path in sorted(case_dir.glob("*.md")):
    text = case_path.read_text(encoding="utf-8")
    headings = tuple(line for line in text.splitlines() if line.startswith("## "))
    if headings != case_headings:
        raise SystemExit(f"case structure invalid: {case_path.relative_to(root)}")

english = (root / "README.md").read_text(encoding="utf-8")
chinese = (root / "README.zh-CN.md").read_text(encoding="utf-8")
english_sections = (
    "## Why",
    "## What You Get",
    "## 5-minute Quick Start",
    "## Three Ways to Adopt",
    "## How It Works",
    "## Core Principles",
    "## Three Small Examples",
    "## Project Structure",
    "## Validation Boundaries",
    "## Extending and Contributing",
    "## Limitations",
    "## FAQ",
    "## License",
)
chinese_sections = (
    "## 为什么需要它",
    "## 你将获得什么",
    "## 5 分钟快速开始",
    "## 三种采用方式",
    "## 工作方式",
    "## 核心原则",
    "## 三个小例子",
    "## 项目结构",
    "## 验证边界",
    "## 扩展与贡献",
    "## 限制",
    "## 常见问题",
    "## 许可证",
)

def require_order(text: str, headings: tuple[str, ...], label: str) -> None:
    positions = [text.find(heading) for heading in headings]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        raise SystemExit(f"missing or reordered {label} README sections")

require_order(english, english_sections, "English")
require_order(chinese, chinese_sections, "Chinese")
if "[简体中文](README.zh-CN.md)" not in english or "[English](README.md)" not in chinese:
    raise SystemExit("bilingual README cross-links missing")
hero_pattern = re.compile(r"\A!\[[^\]\n]+\]\(assets/kiss-my-agent-hero\.png\)")
if not hero_pattern.search(english) or not hero_pattern.search(chinese):
    raise SystemExit("README hero must use the relative path and non-empty alt text")
if english.count("img.shields.io") > 5 or chinese.count("img.shields.io") > 5:
    raise SystemExit("README badge count exceeds five")
badge_urls = re.findall(r"https://img\.shields\.io/badge/[^)\s]+", english + "\n" + chinese)
for disallowed_badge in ("coverage", "downloads", "stars", "release", "build-passing", "ci-passing"):
    if any(disallowed_badge in url.casefold() for url in badge_urls):
        raise SystemExit(f"unsupported README badge or claim token: {disallowed_badge}")

def bash_blocks(text: str) -> list[str]:
    return [block.strip() for block in re.findall(r"```bash\n(.*?)\n```", text, re.DOTALL)]

if bash_blocks(english) != bash_blocks(chinese):
    raise SystemExit("bilingual README bash commands differ")
for phrase in (
    "There is no automatic installer",
    "Other agent hosts have not been verified",
    "does not launch Codex",
    "authentication",
):
    if phrase not in english:
        raise SystemExit(f"English README limitation missing: {phrase}")

installation = (root / "docs/INSTALLATION.md").read_text(encoding="utf-8")
for phrase in (
    ".agents/skills/kiss-my-agent/",
    "$HOME/.agents/skills/kiss-my-agent/",
    "$CODEX_HOME/skills/kiss-my-agent/",
    "verified compatibility fallback",
    ".codex/agents/",
    "~/.codex/agents/",
    "Never overwrite an existing `AGENTS.md`",
    "Do not copy a `config.toml`",
    "Start a **new** Codex session",
    "/skills",
    "update the matching `expected_roles`",
):
    if phrase not in installation:
        raise SystemExit(f"installation fact missing: {phrase}")

community_checks = {
    "CONTRIBUTING.md": ("Local checks", "Change boundaries", "$kiss-my-agent"),
    "CODE_OF_CONDUCT.md": ("Contributor Covenant", "Enforcement Guidelines", "version 2.1"),
    "SECURITY.md": ("Reporting a vulnerability", "private vulnerability-reporting", "no releases"),
    ".github/ISSUE_TEMPLATE/bug-report.md": ("name: Bug report", "Expected behavior", "Reproduction"),
    ".github/ISSUE_TEMPLATE/rule-or-case-proposal.md": ("name: Rule or case proposal", "Current consumer", "Deletion counterfactual"),
    ".github/PULL_REQUEST_TEMPLATE.md": ("## Outcome", "## Validation", "## Complexity boundary"),
}
for relative, phrases in community_checks.items():
    text = (root / relative).read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in text:
            raise SystemExit(f"community document phrase missing in {relative}: {phrase}")

def chosen_source(files: set[str], fallback: str) -> str:
    if "AGENTS.override.md" in files:
        return "AGENTS.override.md"
    if "AGENTS.md" in files:
        return "AGENTS.md"
    return fallback

if chosen_source({"AGENTS.md", "AGENTS.override.md"}, "fallback") != "AGENTS.override.md":
    raise SystemExit("override precedence failed")
if chosen_source({"AGENTS.md"}, "fallback") != "AGENTS.md":
    raise SystemExit("standard instruction precedence failed")
if chosen_source(set(), "fallback") != "fallback":
    raise SystemExit("fallback precedence failed")

fixture = root / "tests/fixtures/layered-project"
root_text = (fixture / "AGENTS.md").read_text(encoding="utf-8")
a_text = (fixture / "component-a/AGENTS.md").read_text(encoding="utf-8")
b_text = (fixture / "component-b/subsystem/AGENTS.override.md").read_text(encoding="utf-8")
if "fixture-root" not in root_text or "component-a" not in a_text or "subsystem-override" not in b_text:
    raise SystemExit("effective-instruction fixture markers missing")

legacy_skill_name = "research" + "-mvp-" + "engineering"
forbidden_patterns = [
    ("private underscored project identifier", re.compile(r"(?<![A-Za-z0-9])" + "bio" + "_nav" + r"(?![A-Za-z0-9])", re.IGNORECASE)),
    ("private compact project identifier", re.compile(r"(?<![A-Za-z0-9])" + "bio" + "nav" + r"(?![A-Za-z0-9])", re.IGNORECASE)),
    ("specific middleware identifier", re.compile(r"(?<![A-Za-z0-9_])r" + "os" + r"(?:\d+)?(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("specific simulator identifier", re.compile(r"(?<![A-Za-z0-9_])" + "isa" + "ac" + r"(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("specific navigation identifier", re.compile(r"(?<![A-Za-z0-9_])" + "nav" + "2" + r"(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("specific sensor identifier", re.compile(r"(?<![A-Za-z0-9_])" + "contact" + "sensor" + r"(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("specific storage identifier", re.compile(r"(?<![A-Za-z0-9_])n" + "as" + r"(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("private storage path", re.compile(re.escape("/mnt/" + "nas_home"), re.IGNORECASE)),
    ("private user path", re.compile(re.escape("/home/" + "lyb"), re.IGNORECASE)),
]
offenders = []
markdown_files = []
for path in root.rglob("*"):
    if not path.is_file() or ".git" in path.parts or ".sandbox" in path.parts:
        continue
    if path.suffix.casefold() == ".md":
        markdown_files.append(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    hits = [label for label, pattern in forbidden_patterns if pattern.search(text)]
    if legacy_skill_name.casefold() in text.casefold():
        hits.append("retired skill name")
    if hits:
        offenders.append(f"{path.relative_to(root)}: {', '.join(hits)}")
if offenders:
    raise SystemExit("repository hygiene violations:\n" + "\n".join(offenders))

link_pattern = re.compile(r"!?\[[^\]\n]*\]\(([^)]+)\)")
broken_links = []
for path in markdown_files:
    text = path.read_text(encoding="utf-8")
    for raw_target in link_pattern.findall(text):
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

effective_chain = [root / "AGENTS.md", fixture / "AGENTS.md", fixture / "component-b/subsystem/AGENTS.override.md"]
chain_bytes = sum(len(path.read_bytes()) for path in effective_chain)

staged_project = root / ".sandbox/project"
if staged_project.exists():
    staged_target = staged_project / "fixture/component-b/subsystem"
    if not (staged_project / ".git").is_dir():
        raise SystemExit("staged sandbox project is not an isolated project root")
    staged_chain = [
        staged_project / "AGENTS.md",
        staged_project / "fixture/AGENTS.md",
        staged_target / "AGENTS.override.md",
    ]
    staged_required = [
        staged_project / ".agents/skills/kiss-my-agent/SKILL.md",
        staged_project / ".codex/agents/explorer.toml",
        staged_project / ".codex/agents/coder.toml",
        staged_project / ".codex/agents/review.toml",
        *staged_chain,
    ]
    if not all(path.is_file() for path in staged_required):
        raise SystemExit("staged sandbox project content is incomplete")
    staged_bytes = sum(len(path.read_bytes()) for path in staged_chain)
    if staged_bytes != chain_bytes:
        raise SystemExit(f"staged sandbox chain bytes differ: expected {chain_bytes}, got {staged_bytes}")
    if (staged_project / ".agents/skills" / legacy_skill_name).exists():
        raise SystemExit("staged sandbox contains the retired skill directory")

print(f"effective-chain-bytes={chain_bytes}")
print(f"hero={width}x{height}:{len(hero_data)}-bytes")
print("static-validation=PASS")
PY

printf 'validation=PASS\n'
