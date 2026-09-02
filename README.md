![KISS My Agent hero showing complex agent paths converging into one clear result](assets/kiss-my-agent-hero.png)

<div class="readme-intro" align="center" markdown="1">

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

KISS My Agent helps Codex finish complex research-engineering work without turning every uncertainty into more machinery. You set the goal and decide what counts as done; the Agents keep changes small, failures visible, and conclusions honest.

[English](https://aoiota.github.io/Kiss-My-Agent/) | [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml/badge.svg)](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml)
![Release: v0.2.0](https://img.shields.io/badge/release-v0.2.0-blue.svg)
![Host: Codex-first](https://img.shields.io/badge/host-Codex--first-blue.svg)

</div>

<a id="why-this-exists"></a>
## Two Problems It Targets

**1. A small bug becomes a new platform.**

Before: one parser fails, so the Agent proposes a framework, registry, configuration format, migration plan, and large test system. After: KISS directs it to fix the parser, add the smallest useful regression check, and stop.

**2. A real failure is hidden as success.**

Before: an internal error is caught and returned as an empty or stale “successful” result. After: KISS directs expected optional outages to be reported clearly and lets real bugs fail with their cause.

<a id="is-it-for-you"></a>
## Is It for You?

- **Simple, clear, one-off task:** you do not need project setup. Use a normal Codex conversation.
- **Complex research or engineering project:** use KISS when several Agents, important decisions, shared files, experiments, or strong evidence claims need clear ownership.

KISS is guidance, not a permission bypass or a guarantee that a model will never make a mistake.

<a id="quick-start"></a>
## Quick Start

Tested with authenticated, Plugin-capable Codex CLI 0.152.1. You need `git`, GitHub network access, and account access to `gpt-5.6-sol`; earlier Codex versions are not verified.

Confirm that this Codex build supports Plugins:

```bash
codex --version
codex plugin --help
```

Install the Plugin:

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

Open a new Codex session in the complex project and run:

```text
$kiss-my-agent-setup set up this project with the default team
```

Open another new session. Then ask for work normally:

```text
Find the cause of this failing parser test, make the smallest correct fix, and run the affected tests.
```

Setup check is optional. It inspects the configured files; it does not prove live Agent behavior:

```text
$kiss-my-agent-setup check this project
```

Default setup manages three project locations:

- `.codex/config.toml`: Master defaults and multi-Agent switches
- `.codex/agents/`: editable employee-role files
- `AGENTS.md`: the marked KISS instructions block

It preserves existing user configuration and needs no choices by default. It asks only when the target or a conflict is unclear. If setup stops, follow its reported reason and exact path instead of overwriting files; see [Installation](docs/INSTALLATION.md).

The Plugin has no background service. It installs instructions and role configuration; the Codex Host starts the requested Agents.

<a id="how-to-use"></a>
## The Default Team

The **Master** is the main Codex Agent in the conversation you are using now—the primary session—not another employee role.

| Who | Job | Default |
| --- | --- | --- |
| You / Owner | Set the goal, architecture, acceptance criteria, non-goals, and stop point | Human decision |
| Master | Plan, assign work, resolve conflicts, judge evidence, and summarize | `gpt-5.6-sol` / `max` |
| `kiss_explorer` | Investigate and report facts without editing | `gpt-5.6-sol` / `high` |
| `kiss_coder` | Implement the assigned change and run its checks | `gpt-5.6-sol` / `high` |
| `kiss_reviewer` | Independently inspect the result without editing | `gpt-5.6-sol` / `xhigh` |

These are editable defaults, not locks. The Master normally assigns directly, may use multiple instances of a role, keeps one Agent responsible for each shared item, and may give one temporary lead to a large independent subsystem.

The same instructions require the Master to report when delegation is unavailable instead of silently doing the employees' work. You then choose whether to repair the team or explicitly continue this task as a normal single conversation.

The company comparison only explains responsibilities; it is not a fixed workflow or game system.

<a id="configure-agents"></a>
## Only Read This If You Want Different Defaults

Change the Master in the selected configuration file:

- project: `<project>/.codex/config.toml`
- global: `$CODEX_HOME/config.toml`, or `~/.codex/config.toml` when `CODEX_HOME` is unset

If the bundled default is unsupported, use values shown by the Host's model selector for one temporary launch:

```bash
codex --model YOUR_SUPPORTED_MODEL --config 'model_reasoning_effort="YOUR_SUPPORTED_EFFORT"'
```

Codex reports the unsupported setting; KISS does not silently choose a fallback. After the temporary launch, edit the Master config above and use the role wizard below for employees.

Configure existing employee roles through Codex:

```text
$kiss-my-agent-setup configure agents for this project
```

The role wizard changes only an existing role's model, reasoning effort, and permission mode; it does not modify the Master. See [Configuration](docs/CONFIGURATION.md) for global roles, precedence, permissions, and recovery details.

<a id="updates"></a>
## Update Now

The first command updates immediately. The second only verifies the installed result:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

Look for `kiss-my-agent@kiss-my-agent`, status `installed, enabled`, and a version matching the current release badge at the top of this README. Start a new session after an update. A v0.1-managed project also needs the project setup command once more to update its unchanged KISS files.

KISS My Agent has no updater of its own. Codex may refresh an unpinned Git marketplace at startup. Pinning, rollback, and v0.1 migration details are in [Installation](docs/INSTALLATION.md#update).

<a id="limitations"></a>
## Limitations

- Tested on Codex CLI 0.152.1; earlier versions and non-Codex hosts are not verified.
- Instructions improve the working context but cannot guarantee model compliance, correctness, or acceptance.
- Successful delegation or passing tests do not prove the user's product or research goal.
- The current release has no MCP service, standalone UI, telemetry, evaluation platform, or LTS promise.
- It does not replace authentication, permissions, administrator policy, project safety rules, or domain expertise.

<a id="documentation"></a>
## Detailed Documentation

- [Installation and recovery](docs/INSTALLATION.md) / [安装与恢复](docs/INSTALLATION.zh-CN.md)
- [Configuration](docs/CONFIGURATION.md) / [配置](docs/CONFIGURATION.zh-CN.md)
- [Testing and evidence](docs/TESTING.md) / [测试与证据](docs/TESTING.zh-CN.md)
- [FAQ](docs/FAQ.md) / [常见问题](docs/FAQ.zh-CN.md)
- [Contributing](CONTRIBUTING.md) / [贡献](CONTRIBUTING.zh-CN.md)
- [Security](SECURITY.md) / [安全](SECURITY.zh-CN.md)

The full documentation site is published in [English](https://aoiota.github.io/Kiss-My-Agent/) and [Simplified Chinese](https://aoiota.github.io/Kiss-My-Agent/zh-CN/).

<a id="license"></a>
## License

[MIT](LICENSE)
