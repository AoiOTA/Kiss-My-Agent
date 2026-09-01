![KISS My Agent hero showing complex agent paths converging into one clear result](assets/kiss-my-agent-hero.png)

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

[English](https://aoiota.github.io/Kiss-My-Agent/) | [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Status: early stage](https://img.shields.io/badge/status-early_stage-orange.svg)
![Host: Codex-first](https://img.shields.io/badge/host-Codex--first-blue.svg)

<a id="overview"></a>
## Overview

KISS My Agent is a compact Codex plugin for research-oriented coding agents. People retain the research goal, architecture, acceptance criteria, non-goals, and stop boundary. Agents make bounded implementation decisions, prefer the smallest sufficient change, keep failures visible, and report evidence at the level it actually supports.

The plugin supplies two narrowly routed Skills, three seed custom roles, setup/check/remove support, project guidance, static validation, and bilingual developer documentation. It is not a fixed workflow, permission system, behavioral guarantee, or closed role catalog.

<a id="quick-start"></a>
## Quick Start

The public installation interface is:

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

Start a new authenticated Codex session so the newly installed plugin can be discovered. In that session, run:

```text
$kiss-my-agent-setup set up this project
```

The setup Skill changes the current project only. It does not trust the project or restart Codex. Trust the project through the Host, start another new session, then run:

```text
$kiss-my-agent-setup check this project
```

Also use `/skills` and a harmless role Smoke from [Testing](docs/TESTING.md) when live discovery evidence is required.

Global installation is never implicit. Request it explicitly with `$kiss-my-agent-setup set up globally`; see [Installation](docs/INSTALLATION.md) before choosing that scope.

The Git-backed marketplace pins this release to `v0.1.0`. A successful remote install is publication evidence for that tag; source inspection and static validation alone are not remote-install or live-discovery evidence.

<a id="components"></a>
## Components

- [`AGENTS.md`](AGENTS.md): permanent human/agent boundaries and dynamic-dispatch guidance.
- Plugin Skills: `$kiss-my-agent` for the narrow decision cases it names, and `$kiss-my-agent-setup` for explicit setup/check/remove operations.
- [`.codex/config.toml`](.codex/config.toml): the two public multi-agent enablement switches, both explicitly `true` for this project.
- [`.codex/agents/`](.codex/agents/): three standalone seed roles discovered from TOML files.
- [`scripts/validate.sh`](scripts/validate.sh) and [`scripts/validate.ps1`](scripts/validate.ps1): native static-validation entrypoints.
- [`tests/`](tests/): layered-instruction fixtures and manual scenarios.
- English-first documentation with synchronized Simplified Chinese companions.

<a id="three-layers"></a>
## Three Responsibilities

The runtime surface has three separate owners:

1. `.codex/config.toml` enables the Host multi-agent capability with `features.multi_agent = true` and custom agents with `agents.enabled = true`.
2. Each standalone role TOML is auto-discovered. Its `name` field is the role identity; the filename is only a convention.
3. `AGENTS.md` tells the primary thread when delegation is worthwhile. It does not force a pipeline or fixed fan-out.

The supplied `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` files are editable seeds, not a closed catalog. Add or remove standalone roles deliberately. After initial setup, later setup and check operations preserve the catalog and do not recreate a deleted role.

Role model and reasoning effort inherit Host settings when omitted and may be edited to supported values. KISS My Agent does not pin a model, effort, context window, or concurrency limit.

<a id="platform-support"></a>
## Platform Support

| Platform | Native command | Evidence status |
| --- | --- | --- |
| Linux | `./scripts/validate.sh` | Locally exercised only when reported for the exact checkout. |
| macOS | `./scripts/validate.sh` | CI target; the exact commit needs a green native job. |
| Windows | `.\scripts\validate.ps1` in native PowerShell | CI target; the exact commit needs a green native job. WSL is Linux evidence. |

Static validation needs Python 3.11 or newer and no Codex sandbox package, copied `CODEX_HOME`, container, VM, or extra test project. A workflow definition is not proof of a passing platform; green jobs for the exact commit are the authority.

<a id="runtime-configuration"></a>
## Runtime Configuration

The primary thread and role files use the effective Host settings. An explicit `false` in an effective user or administrative layer, or a one-launch CLI override, takes precedence over KISS defaults. To disable both public switches for one launch:

```bash
codex --config features.multi_agent=false --config agents.enabled=false
```

Project and global setup are separate explicit operations. Existing settings and instructions are preserved; conflicts stop setup for review. See [Configuration](docs/CONFIGURATION.md).

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
├── .codex/{config.toml,agents/}
├── plugin and marketplace metadata
├── skills/kiss-my-agent/
├── skills/kiss-my-agent-setup/{SKILL.md,scripts/setup.py}
├── docs/{INSTALLATION,CONFIGURATION,TESTING,EXTENDING,FAQ}{,.zh-CN}.md
├── scripts/{validate.py,validate.sh,validate.ps1,build_site.py}
├── tests/
├── CONTRIBUTING{,.zh-CN}.md
├── SECURITY{,.zh-CN}.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

Codex-facing instructions, Skill content, Rules, Cases, role TOML, `LICENSE`, and `CODE_OF_CONDUCT.md` remain English so the runtime surface has one authoritative language.

<a id="pages-status"></a>
## Documentation Site Status

The documentation site is published in [English](https://aoiota.github.io/Kiss-My-Agent/) and [Simplified Chinese](https://aoiota.github.io/Kiss-My-Agent/zh-CN/). Build and verify it locally with:

```bash
python3 -m pip install -r requirements-site.txt
python3 -m unittest tests.test_build_site
python3 scripts/build_site.py --output _site
```

`_site/` is a local ignored artifact. The Pages workflow publishes from `main` through GitHub Actions. A green workflow and live HTTP responses are separate evidence; verify both language URLs after deployment.

<a id="validation-boundaries"></a>
## Validation Boundaries

Static validation can check repository structure, TOML syntax, standalone role identity, Skill routing, bilingual-document parity, relative links, instruction fixtures, shell syntax, and assets. It does not prove plugin publication, marketplace installation, model compliance, research validity, authentication, network access, filesystem authority, or future Host compatibility.

A setup `check` proves only the files and managed content it inspects. A live `/skills` result proves discovery in that session. A role Smoke proves only the harmless task observed. See [Testing](docs/TESTING.md).

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
- Manual scenarios and Smoke checks are not behavioral qualification or research evidence.
- Project-specific safety, compliance, and domain rules remain the adopter's responsibility.

<a id="license"></a>
## License

[MIT](LICENSE)
