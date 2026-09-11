# Installation and coexistence

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.md) · [Configuration](CONFIGURATION.md) · [Testing](TESTING.md) · [FAQ](FAQ.md)

<a id="release-status"></a>
## Release status

The [latest GitHub Release](https://github.com/AoiOTA/Kiss-My-Agent/releases/latest) is the current supported release. Use it for current installation artifacts and [HANDOFF](HANDOFF.md) for release evidence and history.

<a id="requirements"></a>
## User requirements

The tested baselines are authenticated, Plugin-capable Codex CLI 0.152.1 and 0.153.0. Installation and updates also require a usable `git` executable on `PATH` and GitHub network access. Other Codex versions are not verified. Project setup, checks, removal, and Agent configuration use Codex's own file tools. Users do not need Python, Node.js, Docker, or a package manager.

Python 3.11 or newer is a contributor-only requirement for repository tests and the documentation site. It is not a Plugin runtime dependency.

<a id="install-plugin"></a>
## Install the Plugin

Use the public Git marketplace:

```bash
codex --version
codex plugin --help
```

If `codex plugin --help` is unavailable, update to a Plugin-capable client. If authentication or marketplace access fails, check the client login state, `git`, and GitHub network access before retrying.

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
codex plugin list --marketplace kiss-my-agent
```

Expect Plugin ID `kiss-my-agent@kiss-my-agent`, status `installed, enabled`, and a version matching the current supported release. Cache paths may differ. Start a new authenticated Codex session after installation. A session that was already running is not guaranteed to discover a newly installed Plugin or Skill.

<a id="first-use"></a>
## First use

For a simple one-off task, use an ordinary single conversation and skip project setup. For a complex research-engineering project that needs persistent coordination instructions, open a new session at the project. On the tested Codex CLI 0.152.1 baseline, type `$` and select `kiss-my-agent-setup (kiss-my-agent)` in the Skill picker. The picker inserts a structured Skill reference; add the setup request and submit the prompt to invoke it. If you paste raw text instead, use the fully qualified command shown here:

```text
$kiss-my-agent:kiss-my-agent-setup set up this project
```

Trust the project through the Host interface when prompted, then start one more new session and run:

```text
$kiss-my-agent:kiss-my-agent-setup check this project
```

After setup, use Codex normally. Each agent reads `kiss-my-agent` once per assignment and reuses its guidance at decisions without a user reminder. The master may directly complete clear small or local work, and should actively delegate substantial bulk, independent parallel work, or work needing another perspective when the benefit outweighs coordination cost. Choose by workload, parallel opportunity, coupling, risk, and coordination cost; optional roles do not mean the master should do everything. Each available role may have zero, one, or multiple instances, with no fixed team, sequence, or required subagent launch. If delegation is disabled or unavailable, or no suitable role exists, the master may continue within its capabilities and existing authorization without a staffing approval step. Report unmet explicit requirements for independent checking or a specific role, and real capability gaps; direct execution must not be presented as satisfying them.

When you need live discovery evidence, run `/skills` in that fresh session and confirm both Plugin-owned Skills before using the narrow Smokes in [Testing](TESTING.md).

<a id="project-setup"></a>
## What project setup changes

Project setup manages only the selected target:

- `.codex/config.toml`: fills missing Astra/high, multi-agent and experimental-context defaults; preserves user values and updates only the exact legacy pair described below.
- `.codex/agents/`: during fresh setup, installs any missing editable starter role with `model = "gpt-6-astra"` and `model_reasoning_effort = "medium"`. Setup inspects only these three exact target paths, not the complete role directory or another scope. Every role that already exists is user-owned and remains byte-for-byte unchanged. After setup, an absent starter is a valid intentionally absent catalog entry and is not recreated.
- `AGENTS.md`: appends one bounded KISS managed block while preserving existing instructions.

Setup fills missing master fields with `gpt-6-astra` / `high`; current seed roles explicitly use `gpt-6-astra` / `medium`. Existing explicit user choices are preserved. The role wizard changes selected roles only. Static checks do not prove effective Host settings; verify them in a new task. Plugin cache role files are package resources; they do not automatically enter the Host role catalog, so fresh setup is still required. Role settings live in standalone role TOML files. The managed instructions retain the master's architecture, acceptance, orchestration, conflict resolution, evidence interpretation, and synthesis responsibilities while allowing direct small work and beneficial delegation; roles are not mandatory stages.

The managed instructions call for flat coordination by default: direct assignment to current roles, including multiple instances of the same role, while every shared file or slow resource keeps one writer/operator. Only a large independent subsystem whose direct aggregation would pollute master context may receive one temporary bounded department lead. Its workers cannot delegate again, and the assignment ends with the task; no deeper or permanent hierarchy is created.

The Skill itself remains Plugin-owned and is never copied into the project. Setup does not install software, establish trust, start Codex, or alter global configuration.

On Ubuntu 24.04 with the ChatGPT Pro client, no API key or separate API runtime is required. Upgrade: update the Plugin → run setup in the original scope → explicitly configure selected existing roles → start a new trusted Astra task and verify loading. Experimental context defaults to enabled; existing false is preserved, and enabling it requires a new task. Static check proves files, not client loading.

<a id="configure-agents"></a>
## Choose the Master and configure existing Agents

Setup fills missing master fields with `gpt-6-astra` / `high`; current seed roles explicitly use `gpt-6-astra` / `medium`. Existing explicit user choices are preserved. The role wizard changes selected roles only. Static checks do not prove effective Host settings; verify them in a new task.

To change an existing role's model, reasoning effort, or sandbox default through the conversational wizard, run:

```text
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
```

Plugin updates and setup preserve every existing role. To explicitly set `gpt-6-astra` and `medium` effort in all three existing KISS roles, use this exact qualified prompt:

```text
$kiss-my-agent:kiss-my-agent-setup configure agents in this project: for kiss_explorer, kiss_coder, and kiss_reviewer, set model to gpt-6-astra and model_reasoning_effort to medium
```

The wizard edits only existing role TOML files and previews the exact changes before writing. If the request names roles, it resolves and parses only those files. Otherwise it first lists direct role paths without parsing them, waits for your selection, and then parses only the selected files. An invalid unselected role does not block configuration; broader catalog warnings and precedence remain the Host's responsibility. The wizard does not modify master config, create, delete, or rename roles. You can also edit `.codex/agents/*.toml` directly; see [Configuration](CONFIGURATION.md).

<a id="global-setup"></a>
## Optional global setup

Global setup is never inferred from a project request. It must be explicit:

```text
$kiss-my-agent:kiss-my-agent-setup set up globally
$kiss-my-agent:kiss-my-agent-setup check global setup
$kiss-my-agent:kiss-my-agent-setup configure global agents
```

It manages the model, effort and feature defaults in `config.toml`, starter roles under `agents/`, and the KISS block in `AGENTS.md` under `$CODEX_HOME`. When `CODEX_HOME` is unset, the global config is `~/.codex/config.toml`. Global state can affect every project that loads that Codex home, so prefer project scope for project-specific behavior.

<a id="collision-policy"></a>
## Collision and override policy

| Existing state | Required behavior |
| --- | --- |
| Both legacy top-level master keys occur exactly once, equal `gpt-5.6-sol` / `max`, and each line has the exact KISS marker | Update the pair together to Astra/high during setup. |
| A legacy master assignment is unmarked, modified, missing its companion, or is a user-chosen custom pair | Preserve every existing field as user-owned; fill only truly missing fields and report retained values. |
| A master assignment is duplicated, TOML is invalid, or ownership is ambiguous | Stop as a conflict; do not migrate or repair by guesswork. |
| Either public switch absent | Add only that missing marked `true` assignment. |
| Existing public switch, marked or unmarked | Preserve its complete assignment, including `false`. |
| Unrelated config keys or AGENTS content | Preserve them. |
| Starter role missing during fresh setup | Create it from the current bundled seed. |
| Any exact bundled target already exists | Treat it as user-owned and preserve it byte-for-byte; do not infer or migrate a role version. |
| An exact bundled target has an unsafe type, invalid TOML, missing identity fields, or a `name` different from its filename | Stop before writing. |
| An unrelated role or a role in another scope is malformed or declares the same identity | Leave it untouched. The Host owns broader catalog warnings and project-over-global precedence. |
| Valid existing managed block | Update only that block; report missing starters as intentionally absent and do not restore them. |
| Malformed markers, invalid TOML, unsafe path type, or applicable `AGENTS.override.md` | Stop without claiming success. |

Setup, check, and remove inspect only their selected KISS config and AGENTS paths plus the three exact bundled role targets in the selected scope. They do not validate the full role catalog or reconcile project and global roles. Setup prepares all changes before the first write, verifies files afterward, and rolls back only its own unchanged after-content when a failure permits safe rollback. Agent-native file operations cannot promise recovery from a process or machine crash, so ambiguity in a managed target fails closed.

When setup stops, use its reported reason and exact path to resolve the conflict without overwriting user work, then rerun the same command. An observed `false` delegation switch is reported as `disabled`. Context `false` is reported separately and does not disable KISS. If delegation is disabled or unavailable, or no suitable role exists, the master may continue within its capabilities and existing authorization without a staffing approval step. Report unmet explicit requirements for independent checking or a specific role, and real capability gaps; direct execution must not be presented as satisfying them.

<a id="update"></a>
## Update now

The first command immediately requests a marketplace and installed-Plugin update. The second command only verifies the result:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list --marketplace kiss-my-agent
```

KISS My Agent has no updater of its own. On the verified Codex 0.152.1 baseline, the Host can refresh an unpinned Git marketplace at startup and reinstall an enabled non-curated Plugin; other versions may differ. After the commands above complete, verify that `kiss-my-agent@kiss-my-agent` is `installed, enabled` at the current supported release. Start a new session after an update changes the installed Plugin.

Host refresh updates only the Plugin package. It does not modify project or global config, AGENTS instructions, or role files. For a previously managed project, you may run `$kiss-my-agent:kiss-my-agent-setup set up this project` after upgrading to refresh the managed instruction block, add missing model, effort and feature defaults, and update only the exact legacy marked master pair to Astra/high described above; every existing role file remains directly unchanged. Setup never compares existing roles with bundled historical seeds, assigns them a version, or migrates them. To explicitly set existing roles to `gpt-6-astra` and `medium` effort, use the exact qualified wizard prompt above or edit the role TOML manually.

If you require marketplace movement to happen only after an explicit action, replace the unpinned Git marketplace with a tag-pinned source:

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent@vX.Y.Z
codex plugin add kiss-my-agent@kiss-my-agent
```

Replace `vX.Y.Z` with the release you need, as listed on the [Releases page](https://github.com/AoiOTA/Kiss-My-Agent/releases). This trades automatic marketplace following for reproducibility: `marketplace upgrade` cannot follow a future release until you replace the pinned source. To return to the previous immutable release, reinstall from its pinned marketplace tag:

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent@v0.1.0
codex plugin add kiss-my-agent@kiss-my-agent
```

An ordinary `marketplace upgrade` after this rollback remains on the pinned v0.1.0 channel. To return to the current unpinned channel, replace the marketplace source explicitly:

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

Start a new session after rollback or channel restoration. Existing project and global files remain user-owned and are not automatically upgraded, downgraded, or reset.

<a id="check-and-remove"></a>
## Check or remove setup

Use the command that matches the explicit scope:

```text
$kiss-my-agent:kiss-my-agent-setup check this project
$kiss-my-agent:kiss-my-agent-setup remove from this project

$kiss-my-agent:kiss-my-agent-setup check global setup
$kiss-my-agent:kiss-my-agent-setup remove global setup
```

`check` inspects managed filesystem state only. It checks required master fields and feature types; experimental context is reported separately as true, false or missing. An existing role is reported as user-owned; a starter missing after setup is reported as intentionally absent, not outdated or incomplete. Explicit `remove` deletes exact current defaults with their KISS markers and any exact legacy marked master pair, the managed AGENTS block, and bundled roles whose bytes exactly match a current, known v0.2.6, known v0.2.5, or known v0.1 seed in the chosen scope. Other role files remain user-owned. Removing setup does not uninstall the Plugin. Remove preserves the context table and other user fields; a current config field is removed only when both its exact default value and marker match.

<a id="contributor-tools"></a>
## Contributor tools

Plugin/Skill-only contributors can run the dependency-free local core checks with Python 3.11+:

```bash
python3 scripts/validate.py
python3 -m unittest tests.test_setup -v
```

They do not need to install the Markdown package or build the site locally. That dependency exists only to render the documentation site; pull-request CI installs its pinned version and runs `python scripts/test_all.py` in its activated environment, including the isolated site build. See [Contributing](../CONTRIBUTING.md) for platform-specific details. None of these tools are used by Plugin consumers.

The v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` was removed in v0.2. This is a breaking contributor-interface change, not a missing user runtime dependency. Migrate setup, check, remove, and Agent configuration to the conversational `kiss-my-agent-setup` Skill, invoking it as `$kiss-my-agent:kiss-my-agent-setup` when you paste raw text. Its Agent-native engineering run demonstrates observed file-tool behavior; repository validation demonstrates deterministic source contracts, so neither is a substitute for the other.

<a id="fresh-session"></a>
## New-session boundary

Plugin install/update and project config, instructions, Skill, or role changes affect startup and discovery. Use a new authenticated session at the intended trusted project before interpreting results. Record the Codex version, release, scope, trust state, and session freshness when reporting live behavior.
