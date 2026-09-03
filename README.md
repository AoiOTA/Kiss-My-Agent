![KISS My Agent hero showing complex agent paths converging into one clear result](assets/kiss-my-agent-hero.png)

<div class="readme-intro" align="center" markdown="1">

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

Reduce Codex overengineering and overdefense. Build a runnable, verifiable research MVP first, expose errors early, then iterate quickly from real results.

[English](https://aoiota.github.io/Kiss-My-Agent/) | [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml/badge.svg)](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml)
![Release: v0.2.3](https://img.shields.io/badge/release-v0.2.3-blue.svg)
![Host: Codex-first](https://img.shields.io/badge/host-Codex--first-blue.svg)

</div>

<a id="why-this-exists"></a>
## What KISS My Agent Is

KISS My Agent is an open-source Codex Plugin for research and exploratory engineering. It gives Codex a simple set of working principles: start from the current goal or hypothesis, build the smallest version that can run and be validated, then use real results to decide whether to continue, change, or stop.

It is outcome-driven, not process- or workload-driven: the number of files changed, Agents used, checks run, or steps completed cannot replace the question “did this answer the current problem?”

<a id="failure-patterns"></a>
<a id="overengineering-and-overdefense"></a>
## The Two Core Problems It Solves

| Problem | What it means | Common result |
| --- | --- | --- |
| **Overengineering** | Productizing before the current hypothesis is tested: adding abstractions, configuration, migrations, or platforms for future possibilities that nobody uses today | One experiment becomes a large system, feedback slows down, and both scope and new bugs grow |
| **Overdefense** | Preventing errors from surfacing naturally by layering validation, retries, fallbacks, exception handling, or gates—and sometimes presenting failure as success | The real cause disappears, a wrong result looks “normal,” and the next iteration starts from unreliable information |

Growing the scope, fixing something other than the code actually in use, treating a passing test as the goal, or letting several Agents conflict over the same work are common consequences of these two tendencies.

<a id="why-agents-drift"></a>
## Why Codex Can Fall Into Them

Codex tends to produce answers that look complete, robust, and successful. Prompts often ask for “comprehensive,” “robust,” or “production-ready” work without stating the current hypothesis, minimum goal, and stop condition. Adding frameworks, validation, retries, or fallbacks is easy to generate and easy to present as progress. Codex also tends to avoid an obvious failure, so an error may be caught, routed around, or packaged as a usable result. Mature products can genuinely need complete architecture and safeguards when real requirements and risks justify them. Added too early in research, however, they slow the feedback loop and obscure its most valuable signal: why this real run succeeded or failed.

<a id="how-kiss-helps"></a>
<a id="before-and-after"></a>
## How KISS Drives a Research Loop

`Goal or hypothesis → smallest runnable, verifiable version → real run → visible success or failure → next iteration or stop`

- Define the question and the minimum success condition for this round so implementation does not quietly rewrite the goal.
- Build only what is needed to run and test the hypothesis. Get a research MVP first; decide whether to productize it after the result.
- Run the real path early. Allow low-cost, recoverable mistakes to expose their original cause instead of covering them with a fallback or empty result.
- Act on the real result: fix the first revealed problem and start the next round, or stop when the hypothesis is answered or the goal is met. More process and changes do not prove more progress.

Multi-Agent work is only an optional accelerator: use it when the task truly splits into independent parts, and keep one clear person or Agent responsible for each shared file, device, or output. “Do not fear mistakes” means only low-cost, recoverable experimentation; never remove or bypass authentication, permissions, irreversible-operation safeguards, or other high-risk safety boundaries.

<a id="is-it-for-you"></a>
## Is It for You?

| Good fit | Not the problem it solves |
| --- | --- |
| Research prototypes, algorithm validation, experimental tools, and other work that needs an MVP quickly | Mature product work with stable requirements and a real need for complete compatibility, migration, audit, or safety systems |
| The solution is uncertain and real runs should guide rapid exploration | High-risk work where failure is irreversible and strict safety analysis must come first |
| Debugging hidden errors, or stopping Codex from productizing an imagined future | Deterministic security enforcement, formal verification, a general orchestration platform, or verified non-Codex support |

KISS does not promise to get the first attempt right. It aims to produce trustworthy feedback sooner so the next step can be right.

<a id="quick-start"></a>
## Quick Start

Tested with authenticated, Plugin-capable Codex CLI 0.152.1. You need `git`, GitHub network access, and account access to `gpt-5.6-sol`; earlier Codex versions are not verified. Normal users do not need Python, Node.js, Docker, or another language runtime.

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

At this point only the Plugin is installed. A new Codex session can discover its two Skills, but no persistent project rules or roles have been configured yet.

Open a new Codex session in the complex project. On the tested Codex CLI 0.152.1 baseline, type `$` and select `kiss-my-agent-setup (kiss-my-agent)` in the Skill picker. The picker inserts a structured Skill reference; add the setup request and submit the prompt to invoke it. If you paste raw text instead, use the fully qualified command shown here:

```text
$kiss-my-agent:kiss-my-agent-setup set up this project with the default team
```

Project setup writes the persistent project rules and role configuration. Trust the project through the Codex interface, then open another new session; only that trusted fresh session loads the project rules and roles. Then ask for work normally:

```text
Find the cause of this failing parser test, make the smallest correct fix, and run the affected tests.
```

Setup check is optional. It inspects the configured files; it does not prove live Agent behavior:

```text
$kiss-my-agent:kiss-my-agent-setup check this project
```

Default setup manages three project locations:

- `.codex/config.toml`: Master defaults and multi-Agent switches
- `.codex/agents/`: editable employee-role files
- `AGENTS.md`: the marked KISS instructions block

It preserves existing user configuration and needs no choices by default. On a fresh setup it creates each missing starter role, while every role that already exists is user-owned and is never overwritten. A role removed after setup stays absent. Setup asks only when the target or a conflict is unclear. If setup stops, follow its reported reason and exact path instead of overwriting files; see [Installation](docs/INSTALLATION.md).

The Plugin has no background service; the Codex Host loads the configuration and starts the requested Agents.

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
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
```

The role wizard changes only an existing role's model, reasoning effort, and permission mode; it does not modify the Master. See [Configuration](docs/CONFIGURATION.md) for global roles, precedence, permissions, and recovery details.

<a id="updates"></a>
## Update Now

The first command updates immediately. The second only verifies the installed result:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

Look for `kiss-my-agent@kiss-my-agent`, status `installed, enabled`, and a version matching the current release badge at the top of this README. Start a new session after an update. Host refresh updates only the Plugin package; it does not change project or global configuration, instructions, or role files.

KISS My Agent has no updater of its own. Codex may refresh an unpinned Git marketplace at startup. Existing roles are never automatically updated or version-classified; use the role wizard or edit their TOML manually when you want newer model or effort choices. Pinning and rollback details are in [Installation](docs/INSTALLATION.md#update).

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
