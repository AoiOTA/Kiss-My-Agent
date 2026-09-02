![KISS My Agent hero showing complex agent paths converging into one clear result](assets/kiss-my-agent-hero.png)

<div class="readme-intro" align="center" markdown="1">

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

KISS My Agent helps Codex keep key human decisions human, match the size of a change to the current task, keep failures visible, make multi-Agent responsibilities and conflicts explicit, and keep conclusions within the evidence. It is built for complex research-engineering work where a plausible-looking result is not enough.

[English](https://aoiota.github.io/Kiss-My-Agent/) | [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml/badge.svg)](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml)
![Release: v0.2.0](https://img.shields.io/badge/release-v0.2.0-blue.svg)
![Host: Codex-first](https://img.shields.io/badge/host-Codex--first-blue.svg)

</div>

<a id="why-this-exists"></a>
## What KISS My Agent Is

KISS My Agent is a versioned Codex Plugin for complex research and engineering projects. It packages a small set of working rules, three editable starter roles, and two Skills: one helps with the few important decisions that are not obvious, and the other handles setup, checks, and configuration.

It improves Codex's decisions through clearer working boundaries. It is not an autonomous manager above Codex or a correctness checker, and it does not replace human product or scientific judgment.

<a id="failure-patterns"></a>
<a id="overengineering-and-overdefense"></a>
## The Two Core Problems It Solves

| Core problem | Definition | Common signs | Cost |
| --- | --- | --- | --- |
| **Overengineering** | Adding frameworks, abstractions, configuration, migrations, or process for future possibilities that nobody needs now, so the change grows beyond the current goal | One local bug becomes a new platform; a small task gets a fixed multi-Agent workflow | Code, maintenance, and review costs rise while the solution quietly replaces human architecture and scope decisions |
| **Overdefense** | Facing uncertainty without first checking facts and the failure boundary, then accumulating validation, retries, fallbacks, approvals, compatibility layers, or gates | A real bug becomes an empty or stale “success”; tests repeat without confirming what is actually running; work is refused beyond the real permission boundary | Causes become harder to find, conclusions become less trustworthy, and maintenance cost keeps growing |

These tendencies also appear as changing scope or acceptance without the user, editing a visible file instead of fixing the code that actually runs, treating a passing test as the final goal, or letting several Agents duplicate work and overwrite shared state. These are consequences of the two core problems, not six unrelated product features.

Necessary safety is not overdefense. Authentication, authorization, least privilege, validation at a real boundary, safe cleanup, and explicit handling of a known optional outage should remain. No task or keyword inevitably triggers these problems, and KISS is not a safety bypass.

<a id="why-agents-drift"></a>
## Why Codex Can Fall Into Them

Prompts often say “complete,” “robust,” or “production-ready” without also stating the goal, acceptance criteria, non-goals, and stop condition. Codex must infer the missing decisions, and a more complex answer can look more complete and safer in text. It also cannot know from those adjectives alone which risks truly matter to this project.

Research projects often have several source versions, builds, configurations, datasets, and scoring methods, while multiple Agents see different slices of the work. That makes it easier to fix the wrong thing, duplicate effort, collide on shared state, or mistake a local check for the real result.

<a id="how-kiss-helps"></a>
<a id="before-and-after"></a>
## How KISS Reduces These Problems

- **People keep the key decisions:** people decide the goal, architecture, what counts as done, what is out of scope, and when to stop. Codex works inside those boundaries and asks before materially expanding them.
- **Start from the real need:** check the facts and find the person or code actually affected instead of building a new system because it may be useful someday.
- **Prefer the smallest correct change:** repair the part truly responsible for the problem and test what it affects. Do not turn it into a general framework without a present need, and allow no change when the current result already meets the goal.
- **Keep failures and evidence truthful:** preserve the cause of internal errors; degrade only for a clear optional failure and explain why; a passing test proves the test passed, not automatically that the product or research goal succeeded.
- **Divide work only when it helps:** use multiple Agents only when the split adds value. Give every shared file, device, or output one clearly responsible Agent, while the main conversation combines results and decisions.

<a id="is-it-for-you"></a>
## Is It for You?

| Good fit | Not designed for |
| --- | --- |
| Long-running or complex research-engineering projects that need persistent boundaries for scope, failure handling, and evidence claims | Simple, isolated work with an obvious acceptance check; a normal Codex conversation is enough |
| You often remove speculative frameworks, broad fallbacks, or process machinery from Agent proposals | You want the Agent to choose the product goal, architecture, risk tolerance, or acceptance criteria for you |
| Multiple Agents, experiments, shared files, or devices are useful but need clear responsibility | You need deterministic security enforcement, formal verification, a general orchestration platform, or verified non-Codex support |

KISS improves the rules and role boundaries under which Codex works. It does not make the system automatically correct or bypass authentication, permissions, administrator policy, project trust, or necessary safety controls.

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

Open a new Codex session in the complex project and run:

```text
$kiss-my-agent-setup set up this project with the default team
```

Project setup writes the persistent project rules and role configuration. Trust the project through the Codex interface, then open another new session; only that trusted fresh session loads the project rules and roles. Then ask for work normally:

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
