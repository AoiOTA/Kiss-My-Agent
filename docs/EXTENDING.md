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
- Change role TOML only when role ownership or real runtime needs change.
- Change developer docs when installation, configuration, testing, security, or contribution facts change.

Do not duplicate one fact across owners. Rules extend `AGENTS.md`; Cases illustrate Rules without redefining them.

<a id="preserve-routing"></a>
## Preserve Precise Routing

[`SKILL.md`](../.agents/skills/kiss-my-agent/SKILL.md) must remain non-catch-all. Routine implementation, mechanical edits, tests, builds, Git operations, lookups, and formatting stay outside the Skill. One ambiguity routes to one Rule and, only when useful, one Case.

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

When changing registrations or role settings, keep `.codex/config.toml`, `.codex/agents/`, Configuration, Testing, both READMEs, and the annotated example consistent. Do not add model fallback, permission fallback, preset matrices, or compatibility wrappers without a current consumer.

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

<a id="stop-boundary"></a>
## Stop Boundary

Stop after the ambiguity is resolved with the smallest clear addition. Do not add adjacent governance, installation automation, telemetry, scoring, release machinery, or speculative compatibility.
