# Extending KISS My Agent

[README](../README.md) · [Installation](INSTALLATION.md) · [FAQ](FAQ.md) · [Contributing](../CONTRIBUTING.md)

Extend the repository only when a current recurring ambiguity is not already covered. The objective is better decisions with less mechanism, not a larger handbook.

## Choose the owner

- Change [`AGENTS.md`](../AGENTS.md) only for a short, permanent, broadly applicable boundary.
- Change a Rule when a recurring decision needs a reusable method across several concrete situations.
- Add or change a Case when one contrast makes an existing Rule materially easier to apply.
- Change role TOML only when role ownership, model availability, or sandbox behavior actually changes.
- Change installation or FAQ documentation when user-facing adoption facts change.

Do not duplicate the same rule across these owners. Rules extend `AGENTS.md`; Cases illustrate Rules without redefining them.

## Preserve precise routing

[`SKILL.md`](../.agents/skills/kiss-my-agent/SKILL.md) must remain non-catch-all. Its description should trigger only for:

- non-obvious persistent or shared mechanisms;
- local repair versus a new system;
- experiment validity or evidence strength;
- runtime versus evaluator ambiguity; or
- material scope or acceptance expansion.

Routine implementation, small fixes, mechanical edits, tests, builds, Git operations, lookups, and formatting remain outside the skill.

The entrypoint routes one ambiguity to exactly one Rule and, only if useful, one matching Case. Do not require reading every reference.

## Add a Rule

Before adding a Rule, identify at least two current situations that need the same decision method and show why `AGENTS.md` is too compact an owner. Keep it incremental: do not restate permanent rules, role instructions, or another Rule. Link it from `SKILL.md` only when the trigger can select it precisely.

The engineering Rule owns the silent Rent Test, twelve mechanism semantics, local-versus-system reasoning, failure ownership, review questions, goal boundaries, and stopping. The evidence Rule owns experiment design, valid versus invalid outcomes, stale-artifact discrimination, runtime/evaluator comparisons, replay versus recollection, evidence ownership, and artifact placement.

## Add a Case

A Case has exactly these sections:

1. Goal
2. Consumer
3. Minimum mechanism to retain
4. Mechanism to reject
5. Deletion counterfactual
6. Legitimate exception

It must illustrate an existing Rule without creating new requirements. Prefer revising an existing Case when the semantic contrast is already represented.

## Update roles or model settings

Keep each role file limited to its role-specific increment. If a configured model or reasoning effort is unavailable, change the TOML and the matching `expected_roles` value in [`scripts/validate.sh`](../scripts/validate.sh). Do not add `config.toml`, automatic model fallback, or compatibility wrappers.

## Validate

```bash
./scripts/validate.sh
./scripts/stage-sandbox.sh
./scripts/validate.sh
```

Also inspect the rendered READMEs when navigation, badges, Mermaid, or the hero changes. Static checks cannot establish agent behavior or research validity.

## Stop boundary

Stop after the new ambiguity is resolved with the smallest clear instruction. Do not add adjacent governance, installation automation, telemetry, scoring, release machinery, or speculative compatibility.
