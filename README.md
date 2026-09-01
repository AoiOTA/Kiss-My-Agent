# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

KISS My Agent is a small, reusable instruction layer for research-oriented coding agents. It addresses a common failure mode: agent workflow, defensive machinery, and proof artifacts growing faster than the scientific or product result they were meant to support.

## What is included

- `AGENTS.md`: permanent, general boundaries.
- `.codex/agents/`: focused explorer, coder, and review roles.
- `.agents/skills/research-mvp-engineering/`: an opt-in skill for genuinely ambiguous engineering and evidence decisions.
- `tests/fixtures/layered-project/`: a generic effective-instruction fixture.
- `tests/scenarios.md`: manual discussion scenarios, not an evaluation gate.
- `scripts/validate.sh`: dependency-light static checks.
- `scripts/stage-sandbox.sh`: a local staging helper that writes only under `.sandbox/`.

## Suitable for

Research prototypes, scientific software, small product experiments, and teams that want agents to prefer direct results, honest evidence, and minimal mechanisms.

It is not a complete development process, a policy engine, a scoring harness, an autonomous release system, or a substitute for project-specific safety and compliance rules.

## Local sandbox

```bash
./scripts/validate.sh
./scripts/stage-sandbox.sh
```

The staging script prepares `$REPO_ROOT/.sandbox/codex-home` and an isolated Git project at `$REPO_ROOT/.sandbox/project`, then prints a launch command. It does not start Codex or modify real user configuration.

## Future installation

This repository currently provides source material and a sandbox, not an installer. A future installer should copy selected files into the user's chosen Codex home and project only after showing the destination and preserving existing instructions. Until then, copy files manually and review the effective instruction chain before use.

## Maturity

Early-stage. The static validator checks structure and repository hygiene, but the scenarios are intentionally human-reviewed and do not establish behavioral qualification across models or environments.
