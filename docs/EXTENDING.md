# Extending KISS My Agent

[English](EXTENDING.md) | [简体中文](EXTENDING.zh-CN.md)

[README](../README.md) · [Testing](TESTING.md) · [Contributing](../CONTRIBUTING.md)

<a id="scope"></a>
## Scope

Extend the repository only when a current recurring ambiguity is not covered. The goal is better decisions with less mechanism, not a larger handbook.

<a id="choose-owner"></a>
## Choose the Owner

- Change [`AGENTS.md`](../AGENTS.md) only for a short, permanent, broadly applicable boundary.
- Change a Rule when several current situations need the same reusable decision method.
- Add or revise a Case when one concrete contrast makes an existing Rule easier to apply.
- Change a standalone role TOML only when role ownership or real runtime needs change. Its `name` field is identity; the filename is only a convention.
- Change setup logic only when the explicit project/global managed scope or conflict policy changes.
- Change developer docs when installation, configuration, testing, security, or contribution facts change.

Do not duplicate one fact across owners. Rules extend `AGENTS.md`; Cases illustrate Rules without redefining them.

<a id="preserve-routing"></a>
## Preserve Precise Routing

The plugin-owned `$kiss-my-agent` Skill must remain non-catch-all. Routine implementation, mechanical edits, tests, builds, Git operations, lookups, and formatting stay outside the Skill. One ambiguity routes to one Rule and, only when useful, one Case. Keep `$kiss-my-agent-setup` separate and limited to explicit setup/check/remove operations.

<a id="add-rule"></a>
## Add a Rule

Identify at least two current situations needing the same method and explain why a permanent AGENTS boundary is insufficient. Keep the addition incremental, link it from the Skill only when the trigger can select it precisely, and avoid repeating existing failure, evidence, or ownership guidance.

<a id="add-case"></a>
## Add a Case

A Case keeps this exact section order:

1. Goal
2. Consumer
3. Minimum mechanism to retain
4. Mechanism to reject
5. Deletion counterfactual
6. Legitimate exception

It illustrates an existing Rule and creates no new requirement. Revise an existing Case when the same semantic contrast is already present.

<a id="update-runtime-docs"></a>
## Update Runtime and Docs

When changing public switches, standalone role discovery, or setup scope, keep `.codex/config.toml`, `.codex/agents/`, plugin metadata, setup implementation, Configuration, Installation, Testing, both READMEs, and the annotated example consistent. `.codex/config.toml` owns only the two public enablement switches and never enumerates role files. The three seeds are not a closed catalog, and model/effort remain Host-inherited when omitted. Do not add model fallback, permission fallback, preset matrices, or compatibility wrappers without a current consumer.

When changing an English developer document, update its Simplified Chinese companion with the same explicit anchor IDs, section order, and fenced command blocks. Codex-facing AGENTS, Skill, Rules, Cases, role TOML, `LICENSE`, and `CODE_OF_CONDUCT.md` remain English.

<a id="validate"></a>
## Validate

Linux or macOS:

```bash
./scripts/validate.sh
```

Windows native PowerShell:

```powershell
.\scripts\validate.ps1
```

Inspect rendered Markdown when navigation, tables, badges, Mermaid, or assets change. Use a trusted new Codex session for discovery changes; old sessions are not guaranteed to hot-load.

For Pages changes, build and test locally before deployment, then verify the deployed English root and Chinese `zh-CN/` URLs:

```bash
python3 -m pip install -r requirements-site.txt
python3 -m unittest tests.test_build_site
python3 scripts/build_site.py --output _site
```

Keep README language links pointed at verified Pages URLs; do not replace them with unverified deployment targets.

<a id="stop-boundary"></a>
## Stop Boundary

Stop after the ambiguity is resolved with the smallest clear addition. Do not add adjacent governance, telemetry, scoring, release machinery, or speculative compatibility. New setup behavior needs a current installation consumer and must preserve explicit scope, collision safety, and reversible ownership.
