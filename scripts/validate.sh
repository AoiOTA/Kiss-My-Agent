#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd -P)

python3 - "$repo_root" <<'PY'
from __future__ import annotations

import re
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
    "LICENSE",
    ".gitignore",
    ".codex/agents/explorer.toml",
    ".codex/agents/coder.toml",
    ".codex/agents/review.toml",
    ".agents/skills/research-mvp-engineering/SKILL.md",
    ".agents/skills/research-mvp-engineering/references/rules/engineering-decisions.md",
    ".agents/skills/research-mvp-engineering/references/rules/experiments-and-evidence.md",
    ".agents/skills/research-mvp-engineering/references/cases/minimal-fix-vs-new-system.md",
    ".agents/skills/research-mvp-engineering/references/cases/degraded-safety-vs-hidden-failure.md",
    ".agents/skills/research-mvp-engineering/references/cases/product-contract-provenance-vs-agent-proof.md",
    ".agents/skills/research-mvp-engineering/references/cases/verification-coordination-vs-workflow-platform.md",
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

skill_path = root / ".agents" / "skills" / "research-mvp-engineering" / "SKILL.md"
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
if fields["name"] != "research-mvp-engineering":
    raise SystemExit("unexpected skill name")
for required_phrase in (
    "non-obvious decision",
    "Do not use for an already-decided implementation",
    "Do not read all rules or cases",
):
    if required_phrase not in skill:
        raise SystemExit(f"skill routing phrase missing: {required_phrase}")

engineering = (skill_path.parent / "references/rules/engineering-decisions.md").read_text(encoding="utf-8")
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

evidence = (skill_path.parent / "references/rules/experiments-and-evidence.md").read_text(encoding="utf-8")
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

case_dir = skill_path.parent / "references/cases"
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
for path in root.rglob("*"):
    if not path.is_file() or ".git" in path.parts or ".sandbox" in path.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    hits = [label for label, pattern in forbidden_patterns if pattern.search(text)]
    if hits:
        offenders.append(f"{path.relative_to(root)}: {', '.join(hits)}")
if offenders:
    raise SystemExit("repository hygiene violations:\n" + "\n".join(offenders))

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
    if not all(path.is_file() for path in staged_chain):
        raise SystemExit("staged sandbox effective instruction chain is incomplete")
    staged_bytes = sum(len(path.read_bytes()) for path in staged_chain)
    if staged_bytes != chain_bytes:
        raise SystemExit(f"staged sandbox chain bytes differ: expected {chain_bytes}, got {staged_bytes}")

print(f"effective-chain-bytes={chain_bytes}")
print("static-validation=PASS")
PY

printf 'validation=PASS\n'
