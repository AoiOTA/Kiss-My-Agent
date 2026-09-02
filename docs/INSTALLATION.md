# Installation and coexistence

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.md) · [Configuration](CONFIGURATION.md) · [Testing](TESTING.md) · [FAQ](FAQ.md)

<a id="release-status"></a>
## Release status

The current Git-backed marketplace entry pins the Plugin source to `v0.2.0`. A successful remote install is publication evidence for that tag; source inspection and static validation alone are not remote-install or live-discovery evidence. Existing `v0.1.0` tags and project files remain untouched.

<a id="requirements"></a>
## User requirements

Installing and updating KISS My Agent from its Git-backed marketplace requires a plugin-capable Codex client, a usable `git` executable on `PATH`, and network access to GitHub. Project setup, checks, removal, and Agent configuration use Codex's own file tools. Users do not need Python, Node.js, Docker, or a package manager.

Python 3.11 or newer is a contributor-only requirement for repository tests and the documentation site. It is not a Plugin runtime dependency.

<a id="install-plugin"></a>
## Install the Plugin

Use the public Git marketplace:

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

Start a new authenticated Codex session after installation. A session that was already running is not guaranteed to discover a newly installed Plugin or Skill.

<a id="first-use"></a>
## First use

For a simple one-off task, use an ordinary single conversation and skip project setup. For a complex research-engineering project that needs a persistent executive workflow, open a new session at the project and run:

```text
$kiss-my-agent-setup set up this project
```

Trust the project through the Host interface when prompted, then start one more new session and run:

```text
$kiss-my-agent-setup check this project
```

After setup, use Codex normally. The master coordinates the persistent workflow and delegates routine work; `$kiss-my-agent` remains reserved for a consequential engineering ambiguity. If delegation is disabled or unavailable, or no suitable role exists, the master reports a staffing issue and asks you to repair or enable staffing or explicitly switch this task to ordinary single-conversation execution. It does not silently take over delegated work.

When you need live discovery evidence, run `/skills` in that fresh session and confirm both Plugin-owned Skills before using the narrow Smokes in [Testing](TESTING.md).

<a id="project-setup"></a>
## What project setup changes

Project setup manages only the selected target:

- `.codex/config.toml`: owns four paths—the paired first-setup master defaults `model = "gpt-5.6-sol"` and `model_reasoning_effort = "max"`, plus the two public enablement switches. It adds the master pair only when both keys are absent during first setup or exact v0.1 migration; if either key exists, setup preserves it and leaves the missing companion absent. Each missing feature switch is added independently.
- `.codex/agents/`: installs standalone seeds with `gpt-5.6-sol` / `high` for `kiss_explorer` and `kiss_coder`, and `gpt-5.6-sol` / `xhigh` for `kiss_reviewer`; a later setup may replace only an exact, unmodified bundled v0.1 seed with its v0.2 seed.
- `AGENTS.md`: appends one bounded KISS managed block while preserving existing instructions.

These are initial defaults, not locks. The Host and account must support the selected model and effort. Existing target values are preserved, and later setup or Plugin updates do not reset them. Master settings live in `config.toml`; role settings live in standalone role TOML files. The managed instructions keep the master on strategy, architecture and acceptance decisions, orchestration, conflict resolution, evidence interpretation, and synthesis, with investigation, implementation, and review assigned to roles.

Coordination is flat by default: the master directly fans out to current roles, including multiple instances of the same role, while every shared file or slow resource keeps one writer/operator. Only a large independent subsystem whose direct aggregation would pollute master context may receive one temporary bounded department lead. Its workers cannot delegate again, and the assignment ends with the task; no deeper or permanent hierarchy is created.

The Skill itself remains Plugin-owned and is never copied into the project. Setup does not install software, establish trust, start Codex, or alter global configuration.

<a id="configure-agents"></a>
## Configure the Master or existing Agents

The bundled model/effort values are editable defaults. Change the master only by directly editing `model` and `model_reasoning_effort` in the selected project or Codex-home `config.toml`; the role wizard cannot modify the master. If an unsupported persistent value prevents the master from starting, use this temporary highest-precedence override for one launch, repair the persistent config, and then start another new session:

```bash
codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'
```

To change an existing role's model, reasoning effort, or sandbox default through the conversational wizard, run:

```text
$kiss-my-agent-setup configure agents for this project
```

The wizard edits only existing role TOML files and previews the exact changes before writing. It does not modify master config, create, delete, or rename roles. You can also edit `.codex/agents/*.toml` directly; see [Configuration](CONFIGURATION.md).

<a id="global-setup"></a>
## Optional global setup

Global setup is never inferred from a project request. It must be explicit:

```text
$kiss-my-agent-setup set up globally
$kiss-my-agent-setup check global setup
$kiss-my-agent-setup configure global agents
```

It manages `config.toml`, `agents/`, and the KISS block in `AGENTS.md` under `$CODEX_HOME`. Global state can affect every project that loads that Codex home, so prefer project scope for project-specific behavior.

<a id="collision-policy"></a>
## Collision and override policy

| Existing state | Required behavior |
| --- | --- |
| Both master keys absent during first setup or exact v0.1 migration | Add the marked model/effort pair together. |
| Either master key already exists, or either is absent after current setup | Preserve existing assignments and leave any missing companion absent; never fill the pair one key at a time. |
| Either public switch absent | Add only that missing marked `true` assignment. |
| Existing public switch, marked or unmarked | Preserve its complete assignment, including `false`. |
| Unrelated config keys or AGENTS content | Preserve them. |
| Exact, unmodified bundled v0.1 seed with the expected `name` | Upgrade it to the current bundled seed. |
| Existing seed with user edits or ambiguous ownership | Preserve it and report it; do not overwrite it as an upgrade. |
| Filename/identity mismatch, duplicate identity, or project/global seed-name conflict | Stop before writing. |
| Valid existing managed block | Update only that block; do not restore deliberately deleted roles. |
| Malformed markers, invalid TOML, unsafe path type, or applicable `AGENTS.override.md` | Stop without claiming success. |

Setup prepares all changes before the first write, verifies files afterward, and rolls back only its own unchanged after-content when a failure permits safe rollback. Agent-native file operations cannot promise recovery from a process or machine crash, so all ambiguous states fail closed.

An observed `false` switch is reported as `disabled`. If a real new session cannot delegate or has no suitable role, the master reports the staffing issue and waits for the user's choice; it does not reinterpret the persistent executive workflow as permission to work directly.

<a id="update"></a>
## Update an installed Plugin

Request an immediate manual refresh of the Git marketplace and installed Plugin cache, then verify the selected version:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

KISS My Agent has no updater of its own. The current Codex Host may refresh an unpinned Git marketplace at startup and force-reinstall an enabled non-curated Plugin; that startup behavior belongs to the Host and may change between Codex versions. The explicit command above requests the refresh immediately. Start a new session after any refresh that changes the installed Plugin.

The v0.2.0 managed block adds the coordinator-wait and master-ownership clarifications discovered while dogfooding. A v0.1-managed project is recognized as well-formed but `outdated`; run `$kiss-my-agent-setup set up this project` once after upgrading. Setup replaces the managed block and upgrades only exact, unmodified bundled v0.1 role seeds. Existing config values and modified or ambiguously owned roles remain preserved.

If you require marketplace movement to happen only after an explicit action, replace the unpinned Git marketplace with a tag-pinned source:

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent@v0.2.0
codex plugin add kiss-my-agent@kiss-my-agent
```

This trades automatic marketplace following for reproducibility: `marketplace upgrade` cannot follow a future release until you replace the pinned source. To return to the previous immutable release, reinstall from its pinned marketplace tag:

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

Start a new session after rollback or channel restoration. Existing project files remain user-owned and are not automatically downgraded or reset.

<a id="check-and-remove"></a>
## Check or remove setup

Use the command that matches the explicit scope:

```text
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

`check` inspects managed filesystem state only. `remove` removes only KISS-marked assignments for the master model/effort and two public switches, the managed AGENTS block, and role files that exactly match either a current or known v0.1 bundled seed in the chosen scope. Unmarked config, modified roles, and ambiguously owned roles are preserved and reported. Removing setup does not uninstall the Plugin.

<a id="contributor-tools"></a>
## Contributor tools

Plugin/Skill-only contributors can run the dependency-free local core checks with Python 3.11+:

```bash
python scripts/validate.py
python -m unittest tests.test_setup -v
```

They do not need to install the Markdown package or build the site locally. That dependency exists only to render the documentation site; pull-request CI installs its pinned version and runs `python scripts/test_all.py`, including the isolated site build. See [Contributing](../CONTRIBUTING.md) for platform-specific details. None of these tools are used by Plugin consumers.

The v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` was removed in v0.2. This is a breaking contributor-interface change, not a missing user runtime dependency. Migrate setup, check, remove, and Agent configuration to the conversational `$kiss-my-agent-setup` Skill. Its Agent-native engineering run demonstrates observed file-tool behavior; repository validation demonstrates deterministic source contracts, so neither is a substitute for the other.

<a id="fresh-session"></a>
## New-session boundary

Plugin install/update and project config, instructions, Skill, or role changes affect startup and discovery. Use a new authenticated session at the intended trusted project before interpreting results. Record the Codex version, release, scope, trust state, and session freshness when reporting live behavior.
