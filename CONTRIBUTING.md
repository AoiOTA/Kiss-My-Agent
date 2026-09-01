# Contributing

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

<a id="before-you-start"></a>
## Before You Start

Read [`AGENTS.md`](AGENTS.md). For Skill, Rule, or Case changes, also read [Extending](docs/EXTENDING.md). Runtime and test behavior belong in [Configuration](docs/CONFIGURATION.md) and [Testing](docs/TESTING.md).

Open an issue when a proposal changes public installation layout, role schema, Skill trigger boundaries, or permanent rules. Small, scoped corrections can go directly to a pull request. Security reports follow [Security](SECURITY.md); conduct concerns follow the English-only [Code of Conduct](CODE_OF_CONDUCT.md).

<a id="change-boundaries"></a>
## Change Boundaries

- Preserve human ownership of the goal, architecture, acceptance, non-goals, and stop boundary.
- Keep `$kiss-my-agent` precisely routed and non-catch-all.
- Add a Rule only for a recurring method and a Case only for a useful concrete contrast.
- Do not add workflow, installer, release, compatibility, telemetry, scoring, or evaluation machinery without a current approved consumer.
- Preserve unrelated user and agent changes; keep refactors and formatting outside the scoped diff.
- Keep every English developer document synchronized with its Simplified Chinese companion: language switch, explicit anchor IDs, section order, and fenced command blocks.
- Keep Codex-facing AGENTS, Skill, Rules, Cases, role TOML, `LICENSE`, and `CODE_OF_CONDUCT.md` English-only.
- Never add credentials, private paths, private data, logs, sessions, or generated test content.

<a id="local-validation"></a>
## Local Validation

Linux or macOS:

```bash
./scripts/validate.sh
```

Windows native PowerShell:

```powershell
.\scripts\validate.ps1
```

WSL is Linux evidence. Do not claim macOS or Windows verification from configuration alone; require the exact commit's green native CI job. For discovery changes, use a trusted new Codex session. Current old sessions are not guaranteed to hot-load.

<a id="pull-requests"></a>
## Pull Requests

Describe the user-visible outcome, current consumer, smallest mechanism retained, validation performed, evidence level, and limitations. A passing static check does not prove model behavior or product acceptance. Keep the pull request focused and use the repository template.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
