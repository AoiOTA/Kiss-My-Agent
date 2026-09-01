# Contributing

Thank you for helping KISS My Agent stay small, useful, and evidence-honest.

## Before proposing a change

Read [`AGENTS.md`](AGENTS.md) and, for skill content, [`docs/EXTENDING.md`](docs/EXTENDING.md). Open an issue when the change would alter the public installation layout, role schema, skill trigger boundary, or permanent rules. Small corrections can go directly to a pull request.

Use the issue templates for reproducible bugs and rule-or-case proposals. Security issues follow [`SECURITY.md`](SECURITY.md); conduct concerns follow [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Local checks

The repository uses local, dependency-light checks rather than hosted CI:

```bash
./scripts/validate.sh
./scripts/stage-sandbox.sh
./scripts/validate.sh
```

The staging command rebuilds only `.sandbox/` and does not launch Codex. Review its printed command before any optional manual session.

## Change boundaries

- Preserve the permanent human/agent boundary in `AGENTS.md`.
- Keep `$kiss-my-agent` precisely routed; routine edits, tests, builds, Git work, lookups, and formatting do not belong in the skill.
- Add a rule only for a recurring decision method. Add a case only when one concrete contrast materially clarifies an existing rule.
- Keep the Rent Test, twelve mechanism semantics, evidence methods, and four case boundaries coherent.
- Do not add an installer, hosted workflow, release system, compatibility alias, plugin manifest, telemetry, scoring harness, or evaluation platform without a present approved consumer.
- Keep English and Chinese README structure and installation commands synchronized.
- Never add private paths, project-specific terminology, credentials, logs, sessions, or generated sandbox content.

## Pull requests

Describe the user-visible outcome, current consumer, smallest mechanism retained, validation performed, and limitations. A no-change investigation can be valuable, but a pull request should contain an actual scoped improvement. Keep unrelated formatting and refactors out of the diff.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
