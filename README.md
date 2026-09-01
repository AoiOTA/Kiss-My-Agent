![KISS My Agent hero showing complex agent paths converging into one clear result](assets/kiss-my-agent-hero.png)

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

[English](README.md) | [简体中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Status: early stage](https://img.shields.io/badge/status-early_stage-orange.svg)
![Host: Codex-first](https://img.shields.io/badge/host-Codex--first-blue.svg)

<a id="overview"></a>
## Overview

KISS My Agent is a compact instruction layer for research-oriented coding agents. People retain the research goal, architecture, acceptance criteria, non-goals, and stop boundary. Agents make bounded implementation decisions, prefer the smallest sufficient change, keep failures visible, and report evidence at the level it actually supports.

This Codex-first repository ships project instructions, one narrowly routed Skill, three prefixed custom roles, a project configuration that enables and registers those roles, static validation, and developer documentation. It is not an installer, workflow platform, permission system, or behavioral guarantee.

<a id="quick-start"></a>
## Quick Start

Run the native validator for your operating system. Python 3.11 or newer is required: use `python3` on Linux or macOS; on Windows the wrapper accepts the `py -3` launcher or `python`.

Linux or macOS (POSIX shell):

```bash
cd /absolute/path/to/kiss-my-agent
./scripts/validate.sh
```

Windows (native PowerShell; WSL is not the Windows path):

```powershell
Set-Location C:\absolute\path\to\kiss-my-agent
.\scripts\validate.ps1
```

For live discovery, trust this project and start a new authenticated session:

```bash
cd /absolute/path/to/kiss-my-agent
codex
```

```powershell
Set-Location C:\absolute\path\to\kiss-my-agent
codex
```

In that new session, run `/skills`, confirm `kiss-my-agent`, and smoke the registered `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` roles as described in [Testing](docs/TESTING.md).

The tracked [`.codex/config.toml`](.codex/config.toml) enables multi-agent support and registers only those three roles. It does not select a model, permission mode, context limit, concurrency limit, trust policy, or credential. Project configuration requires project trust and a new session. An already-running session is not guaranteed to hot-load configuration, Skills, instructions, or roles.

<a id="components"></a>
## Components

- [`AGENTS.md`](AGENTS.md): permanent human/agent boundaries.
- [`.agents/skills/kiss-my-agent/`](.agents/skills/kiss-my-agent/): one precise Skill entrypoint with two Rules and four Cases.
- [`.codex/config.toml`](.codex/config.toml): project-local enablement and registration for three prefixed roles.
- [`.codex/agents/`](.codex/agents/): `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` definitions.
- [`scripts/validate.sh`](scripts/validate.sh) and [`scripts/validate.ps1`](scripts/validate.ps1): native static-validation entrypoints.
- [`tests/`](tests/): layered-instruction fixtures and manual scenarios.
- English-first documentation with synchronized Simplified Chinese companions.

Adoption into another project is explicit and collision-safe. Documented copy commands never overwrite existing configuration, instructions, Skills, or roles. See [Installation](docs/INSTALLATION.md).

<a id="platform-support"></a>
## Platform Support

| Platform | Native command | Evidence status |
| --- | --- | --- |
| Linux | `./scripts/validate.sh` | Locally exercised on the current checkout; the exact result is reported by the command. |
| macOS | `./scripts/validate.sh` | CI target. Do not describe it as verified until the exact commit has a green macOS job. |
| Windows | `.\scripts\validate.ps1` in native PowerShell | CI target. Do not describe it as verified until the exact commit has a green Windows job. WSL counts as Linux evidence. |

The [`Validate` workflow](.github/workflows/validate.yml) runs native wrappers. A workflow definition is not proof of a passing platform; green jobs for the exact commit are the authority.

Static validation needs no Codex sandbox package, copied `CODEX_HOME`, container, VM, or extra test project. “No sandbox required” means the validators run as ordinary local scripts. It does not mean `danger-full-access` is required or Host permission controls are bypassed. Live Codex checks may update normal Host-owned state such as trust, history, or caches.

<a id="runtime-configuration"></a>
## Runtime Configuration

The primary thread uses the effective Host, CLI, user, Profile, and trusted-project settings. There is no `master.toml`. Role files contain editable role-specific model, reasoning, and sandbox examples; project config only enables and registers them.

Disable all custom-agent support for one launch without editing the repository:

```bash
codex --config agents.enabled=false
```

```powershell
codex --config agents.enabled=false
```

See [Configuration](docs/CONFIGURATION.md) before changing models, permissions, context, concurrency, or registrations.

<a id="core-principles"></a>
## Core Principles

- People own the question, architecture, acceptance, non-goals, and stop boundary.
- A supported no-change result is valid.
- Keep single-consumer needs local unless a real boundary or second consumer justifies sharing.
- Persistent mechanisms must serve a current consumer or concrete high-consequence risk.
- Internal bugs remain visible; optional degradation is narrow and explicit.
- Source inspection, tests, builds, Smoke, Pilot, and Final support different claims.
- Use multiple agents only when the benefit exceeds coordination cost.
- Stop when proportionate evidence answers the goal.

<a id="project-structure"></a>
## Project Structure

```text
.
├── AGENTS.md
├── .agents/skills/kiss-my-agent/
├── .codex/{config.toml,agents/}
├── docs/{INSTALLATION,CONFIGURATION,TESTING,EXTENDING,FAQ}{,.zh-CN}.md
├── scripts/{validate.py,validate.sh,validate.ps1}
├── tests/
├── CONTRIBUTING{,.zh-CN}.md
├── SECURITY{,.zh-CN}.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

Codex-facing instructions, Skill content, Rules, Cases, role TOML, `LICENSE`, and `CODE_OF_CONDUCT.md` remain English so the runtime surface has one authoritative language.

<a id="validation-boundaries"></a>
## Validation Boundaries

Static validation can check repository structure, TOML syntax and registrations, Skill routing, bilingual-document parity, relative links, instruction fixtures, shell syntax, and assets. It does not prove model compliance, research validity, authentication, network access, filesystem authority, external integrations, or future Host compatibility.

A live `/skills` check proves discovery in that session. A role Smoke proves only that the role can be invoked for the harmless task used. Neither proves future behavior or grants authority. See [Testing](docs/TESTING.md).

<a id="documentation"></a>
## Documentation

- [Installation](docs/INSTALLATION.md) / [安装](docs/INSTALLATION.zh-CN.md)
- [Configuration](docs/CONFIGURATION.md) / [配置](docs/CONFIGURATION.zh-CN.md)
- [Testing](docs/TESTING.md) / [测试](docs/TESTING.zh-CN.md)
- [Extending](docs/EXTENDING.md) / [扩展](docs/EXTENDING.zh-CN.md)
- [FAQ](docs/FAQ.md) / [常见问题](docs/FAQ.zh-CN.md)
- [Contributing](CONTRIBUTING.md) / [贡献](CONTRIBUTING.zh-CN.md)
- [Security](SECURITY.md) / [安全](SECURITY.zh-CN.md)

<a id="limitations"></a>
## Limitations

- Early-stage source distribution; compatibility and release guarantees are not claimed.
- Codex-first; other hosts have not been verified.
- Instructions do not grant filesystem, network, account, or authentication authority.
- Model and reasoning availability varies by Host.
- Manual scenarios and Smoke checks are not behavioral qualification or research evidence.
- Project-specific safety, compliance, and domain rules remain the adopter's responsibility.

<a id="license"></a>
## License

[MIT](LICENSE)
