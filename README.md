![KISS My Agent hero showing complex agent paths converging into one clear result](assets/kiss-my-agent-hero.png)

<div class="readme-intro" align="center" markdown="1">

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

A Codex plugin that helps research-engineering agents solve the task you asked for without turning uncertainty into extra systems, hidden fallbacks, or process theater.

[English](https://aoiota.github.io/Kiss-My-Agent/) | [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml/badge.svg)](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml)
![Release: v0.2.0](https://img.shields.io/badge/release-v0.2.0-blue.svg)
![Host: Codex-first](https://img.shields.io/badge/host-Codex--first-blue.svg)

</div>

<a id="why-this-exists"></a>
## Why This Exists

Coding agents are often asked to be thorough, safe, reusable, and future-proof while working from incomplete context. Those are reasonable goals, but when the actual acceptance boundary is unclear, an agent can make the task larger instead of making the result better.

You may recognize the symptoms:

- one parser bug becomes a framework, registry, configuration layer, and migration plan;
- an internal error is caught and returned as an empty or stale “successful” result;
- speculative checks, gates, state machines, or telemetry appear without a current consumer;
- several agents and handoff artifacts are created for work one thread could finish clearly;
- tests pass, so the agent claims the product or research goal is proven;
- the agent keeps polishing after the requested outcome is already met.

KISS My Agent gives Codex a small set of persistent boundaries for these decisions. It keeps the human in control of the goal and asks the agent to prefer the smallest sufficient change, visible failures, proportionate evidence, and a real stop point.

<a id="overengineering-and-overdefense"></a>
## Overengineering and Overdefense

**Overengineering** means adding abstractions, infrastructure, configuration, compatibility layers, workflows, or persistent state that the current task and its real consumers do not need.

**Overdefense** means reacting to uncertainty with behavior that obscures the truth: broad catch-and-continue logic, stale-data fallback, duplicate safety layers, invented approval gates, or refusal beyond the actual safety and permission boundary.

Necessary safety is not overdefense. Authentication, least privilege, input validation at a real boundary, safe cleanup, and explicit handling of a known optional outage can all be essential. The problem is defensive machinery that hides an internal bug, changes the requested acceptance criteria, or adds cost without protecting a concrete risk.

There is no task or keyword that inevitably triggers these problems, and KISS My Agent is not a bypass for Codex safety. It reduces the tendency by making ownership, failure semantics, evidence, and stopping rules explicit.

<a id="when-it-happens"></a>
## When Agents Are Most Likely to Drift

The risk rises when a prompt asks for “complete,” “robust,” “production-ready,” or “future-proof” work without concrete acceptance criteria; when a failure path or optional dependency is ambiguous; when runtime behavior disagrees with tests or evaluators; when a research claim is stronger than the experiment; or when multi-agent coordination itself starts becoming the product.

This is not unique to Codex, and it does not happen in every session. Language-model coding agents infer intent from the available instructions and context. When several plausible solutions exist, an elaborate solution can look safer or more complete even when it is worse for the current goal.

<a id="how-kiss-helps"></a>
## How KISS My Agent Helps

| Drift | KISS boundary | Intended result |
| --- | --- | --- |
| The agent expands an underspecified goal | People own the goal, architecture, acceptance criteria, non-goals, and stop boundary | Material scope changes return to the user |
| A local need becomes a shared system | Keep a single-consumer need in its owning module unless a real boundary or second consumer justifies extraction | Smaller, easier-to-review changes |
| Defensive code hides a defect | Propagate internal bugs; degrade only for a specific expected optional failure and make the reason visible | Failures remain diagnosable |
| Checks become stronger claims | Separate source inspection, tests, build, Smoke, Pilot, and Final evidence | Reports say only what was actually proven |
| Multi-agent work becomes a fixed ceremony | Keep simple one-off work in an ordinary single conversation; use dynamic delegation only in a configured complex project | Flat direct fan-out by default; at most one temporary lead for a qualifying large subsystem |
| Work continues to manufacture confidence | Treat supported no-change as valid and stop when proportionate evidence answers the goal | Less churn and process theater |

These are guidance constraints, not a formal verifier or a behavioral guarantee. They improve the decision context in which Codex works; they cannot guarantee that every model, prompt, or future Host version behaves identically.

<a id="is-it-for-you"></a>
## Is It for You?

KISS My Agent is a good fit if you:

- use Codex for research software, experiments, infrastructure, debugging, or substantial engineering work;
- want the agent to distinguish a local fix from a justified shared mechanism;
- care about visible failures and claims that match the evidence;
- want optional multi-agent help without a fixed pipeline or mandatory team size;
- prefer project-owned boundaries that contributors can inspect and change.

It is probably not the right tool if you want:

- a generic autonomous orchestrator, approval platform, telemetry service, or evaluation system;
- a way around Codex permissions, administrator policy, project trust, or security controls;
- deterministic enforcement that guarantees a model will never overengineer;
- verified support for non-Codex hosts;
- extra process for simple one-off work that already has a clear boundary.

<a id="quick-start"></a>
## Three-Minute Start

**Normal users need Codex, a usable `git` executable, and network access to GitHub. Setup and Agent configuration do not require Python, Node.js, Docker, a package manager, or a separate KISS executable.**

Choose the mode that matches the work:

- **Simple one-off task:** install the Plugin if you want its decision Skill, but skip project setup and use an ordinary single conversation with your chosen model and effort.
- **Complex research-engineering project:** use the steps below to install a persistent executive workflow in which the master coordinates and delegates routine work.

1. Install the plugin from its Git-backed marketplace:

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

2. Only for the persistent complex-project mode, start a new authenticated Codex session in the project you want to configure, then run:

```text
$kiss-my-agent-setup set up this project
```

3. Trust the project through the Codex Host when prompted. Start another new session so the project instructions and roles can be discovered, then run:

```text
$kiss-my-agent-setup check this project
```

That completes the persistent project mode. You do not need to invoke a Skill before every task. Ask Codex for normal work as usual:

```text
Find the cause of this failing parser test, make the smallest correct fix, and run the affected tests.
```

Setup owns four config paths: the paired master model/effort defaults and two public multi-agent switches. It adds the master pair only when both are absent in a first setup or exact v0.1 migration; one existing master key preserves the other as absent. Feature defaults are added independently when missing. It also seeds `kiss_explorer`, `kiss_coder`, and `kiss_reviewer`. Existing values and user changes are preserved. If configured delegation is disabled or unavailable, or no suitable role exists, the master reports the staffing issue and asks the user to repair staffing or explicitly switch this task to ordinary single-conversation execution; it does not silently take over. See [Installation](docs/INSTALLATION.md) for the exact boundary, Host-support caveat, and fresh-session requirements.

<a id="how-to-use"></a>
## What Do I Invoke?

| Need | What to do |
| --- | --- |
| Simple one-off implementation, debugging, tests, review, or Git work | Use an ordinary single conversation; project setup is not required. |
| Persistent executive workflow for a complex project | Run project setup, then ask Codex normally; the master coordinates and delegates routine work under the project `AGENTS.md`. |
| One consequential ambiguity about a shared mechanism, local fix versus new system, hidden failure, experiment validity, evidence strength, runtime/evaluator mismatch, or scope expansion | Explicitly invoke `$kiss-my-agent` for that decision, then return to the task. It is not a general workflow. |
| Set up, check, remove, or configure KISS files and existing roles | Invoke `$kiss-my-agent-setup` with an explicit project or global scope. |

The three bundled roles are editable seeds, not a mandatory workflow or closed catalog:

- `kiss_explorer` performs bounded read-only investigation with `gpt-5.6-sol` / `high`.
- `kiss_coder` owns a bounded implementation and its checks with `gpt-5.6-sol` / `high`.
- `kiss_reviewer` performs an independent read-only review with `gpt-5.6-sol` / `xhigh`.

The bundled master default is `gpt-5.6-sol` / `max`. The Host and account must support those model/effort values; setup preserves existing target choices. The master dynamically chooses available roles, and may use multiple instances of the same role. Coordination is flat by default: the master directly fans out to current roles while keeping one writer or operator for every shared file or resource.

Only when a large independent subsystem needs substantial parallel work and direct aggregation would pollute the master's context may one existing Agent temporarily act as a bounded department lead. That lead may delegate within its scope and summarize to the master, but its workers do not delegate again. The assignment ends with the task: there is at most one intermediate layer, never a permanent department, new role, fixed headcount, or deep hierarchy.

A useful company analogy is: the user or Owner sets the destination; the master acts like the CEO and owns strategy, architecture and acceptance decisions, orchestration, conflict resolution, evidence interpretation, and final synthesis; explorer supplies intelligence, coder does the engineering, and reviewer performs an independent audit. This explains ownership only—it is not a fixed pipeline, required team, or game mechanic.

<a id="before-and-after"></a>
## Two Concrete Contrasts

### A parser defect

**Before:** A parser fails on one valid input. The proposed repair adds a generic validation framework, adapter registry, new configuration schema, compatibility mode, and broad test harness “for future parsers.”

**With KISS:** Trace the active parser and its consumer, fix the defect in the owning module, add the smallest regression case that fails before the repair, run the affected closure, and stop. Extract shared behavior only when another current consumer or a real interface boundary requires it.

### An optional service is unavailable

**Before:** A broad exception handler returns an empty success or stale enrichment, so internal computation bugs look like an expected outage.

**With KISS:** Catch only the known availability failure at the owner boundary, keep the primary behavior correct, expose the degraded reason, and let internal defects fail with their cause. This preserves real safety without hiding failure.

<a id="configure-agents"></a>
## Configure the Master and Roles

The bundled defaults are `gpt-5.6-sol` / `high` for `kiss_explorer` and `kiss_coder`, and `gpt-5.6-sol` / `xhigh` for `kiss_reviewer`; the master default is `gpt-5.6-sol` / `max`. These values require Host/account support and are not locks.

The master settings belong to the selected scope's `config.toml`, not to a role. Edit `model` and `model_reasoning_effort` there directly. If an unsupported persistent setting prevents the master from starting, use a one-launch CLI override, then repair the persistent config and start another new session:

```bash
codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'
```

The conversational wizard configures only existing role TOML files:

```text
$kiss-my-agent-setup configure agents for this project
$kiss-my-agent-setup configure global agents
```

The wizard can change only `model`, `model_reasoning_effort`, and `sandbox_mode` on roles that already exist. It cannot modify the master. It previews the diff, preserves every unrelated field, and requires separate confirmation for `danger-full-access`. It does not maintain a model catalog or create, delete, or rename roles.

For manual configuration, edit the relevant standalone role files under `<project>/.codex/agents/` or `$CODEX_HOME/agents/`; see [Configuration](docs/CONFIGURATION.md). An explicit `model` or `model_reasoning_effort` in a role file is a role override; when either field is omitted, resolution follows explicit spawn settings, then `[agents]` defaults, then the parent's resolved setting. The parent session's live sandbox/approval state and administrator requirements can still constrain permissions. Start a new session after any role change.

<a id="updates"></a>
## One-Command Manual Refresh

Update the installed plugin, confirm the resolved version, and then start a new Codex session:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

The explicit `marketplace upgrade` command requests an immediate manual refresh. KISS My Agent contains no updater of its own; whether an unpinned Git marketplace is also refreshed automatically at startup is behavior owned by the current Codex Host. The v0.2.0 marketplace entry pins the Plugin source to the immutable `v0.2.0` tag. A refresh can update Plugin-owned Skills and resources, but project role handling remains setup-owned.

After upgrading a v0.1-managed project, run project setup once in a new session. It refreshes the KISS managed AGENTS block and upgrades only role files that still exactly match bundled v0.1 seeds; customized or ambiguously owned roles and existing explicit config values remain preserved.

If explicit-only marketplace movement matters more than one-command upgrades, add the marketplace at the pinned `@v0.2.0` tag. That prevents the marketplace source from following later releases. A rollback pin such as `@v0.1.0` likewise stays on that channel during ordinary upgrades; returning to the current unpinned channel requires removing and re-adding the marketplace without a tag. See [Installation](docs/INSTALLATION.md) for exact pinning, rollback, and channel-restoration commands and [Testing](docs/TESTING.md) for the evidence boundary.

<a id="project-and-global-scope"></a>
## Project and Global Scope

Project setup is the recommended persistent mode for a complex project, not a prerequisite for a simple one-off task. It manages only the selected repository's `.codex/config.toml`, `.codex/agents/`, and a marked block in `AGENTS.md`. It does not copy the Plugin Skills, establish project trust, restart Codex, or modify `$CODEX_HOME`.

Global setup is optional and must be requested explicitly:

```text
$kiss-my-agent-setup set up globally
$kiss-my-agent-setup check global setup
```

Global setup manages the corresponding config, roles, and instructions under `$CODEX_HOME`, so it may affect every project using that Codex home. Project/global role collisions, malformed TOML, symlinks, ambiguous managed content, or an effective `AGENTS.override.md` make setup stop for review instead of overwriting. `check` proves inspected file structure only; it does not prove trust, live discovery, permissions, publication, or model behavior.

<a id="architecture"></a>
## What the Plugin Contains

- `$kiss-my-agent`: narrowly routed decision guidance for research-engineering ambiguity.
- `$kiss-my-agent-setup`: file-tool-native setup, check, remove, and existing-role configuration guidance.
- `AGENTS.md`: persistent human/agent ownership, scope, failure, evidence, and stop boundaries.
- [`.codex/agents/*.toml`](.codex/agents/): three editable seed roles discovered by Codex.
- `.codex/config.toml`: the paired first-setup master defaults `model = "gpt-5.6-sol"` and `model_reasoning_effort = "max"`, plus `features.multi_agent = true` and `agents.enabled = true`; it does not set context, concurrency, providers, authentication, or telemetry.

Codex-facing instructions remain English so runtime behavior has one authoritative language. The user documentation is maintained in synchronized English and Simplified Chinese.

<a id="contributor-runtime"></a>
## Users and Contributors Have Different Requirements

Plugin users do not need a language runtime for installation, setup, role configuration, normal use, or updates. Contributors use Python 3.11 or newer for repository validation and documentation-site builds; this is a development toolchain, not a user runtime dependency. The v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` was removed in v0.2, which is a breaking contributor-interface change: migrate setup/check/remove/configure work to the conversational `$kiss-my-agent-setup` Skill. Its Agent-native engineering evidence is not the same as deterministic CLI or unit-test evidence.

Start with [Contributing](CONTRIBUTING.md), then follow the native platform commands and evidence rules in [Testing](docs/TESTING.md). Windows validation runs in native PowerShell; WSL is Linux evidence. The repository is designed for fork, branch, test, and pull-request collaboration without requiring contributors to share one local Codex model or permission configuration.

<a id="evidence-boundaries"></a>
## Evidence Boundaries

KISS My Agent does not turn a check into a stronger claim than it supports:

- source inspection says what files contain;
- static tests say which repository invariants passed;
- setup `check` says what managed files were inspected;
- `/skills` in a new session demonstrates discovery in that session;
- a harmless role Smoke demonstrates only the observed narrow behavior;
- a Pilot or Final result needs its own acceptance criteria and real environment.

Passing tests does not prove the user's research or product goal. Instructions also do not grant filesystem, network, account, or authentication authority, and they do not replace project-specific safety, security, compliance, or domain rules.

<a id="documentation"></a>
## Documentation

- [Installation](docs/INSTALLATION.md) / [安装](docs/INSTALLATION.zh-CN.md)
- [Configuration](docs/CONFIGURATION.md) / [配置](docs/CONFIGURATION.zh-CN.md)
- [Testing](docs/TESTING.md) / [测试](docs/TESTING.zh-CN.md)
- [Extending](docs/EXTENDING.md) / [扩展](docs/EXTENDING.zh-CN.md)
- [FAQ](docs/FAQ.md) / [常见问题](docs/FAQ.zh-CN.md)
- [Contributing](CONTRIBUTING.md) / [贡献](CONTRIBUTING.zh-CN.md)
- [Security](SECURITY.md) / [安全](SECURITY.zh-CN.md)

The documentation site is published in [English](https://aoiota.github.io/Kiss-My-Agent/) and [Simplified Chinese](https://aoiota.github.io/Kiss-My-Agent/zh-CN/).

<a id="limitations"></a>
## Limitations

- Codex-first; other hosts are not verified.
- Guidance reduces a tendency; it cannot guarantee model compliance or identical future behavior.
- The seed roles do not form a required team, and successful delegation is not product acceptance.
- KISS My Agent does not contain its own updater; the Codex Host may automatically refresh an unpinned Git marketplace. The current release does not provide an MCP service, standalone UI, telemetry, or evaluation platform.
- The latest release is supported without an LTS compatibility promise; check release notes before upgrading customized environments.

<a id="license"></a>
## License

[MIT](LICENSE)
