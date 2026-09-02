# Installation and coexistence

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.md) · [Configuration](CONFIGURATION.md) · [Testing](TESTING.md) · [FAQ](FAQ.md)

<a id="release-status"></a>
## Release status

The Git-backed marketplace pins the current release to `v0.2.0`. A successful remote install is publication evidence for that tag; source inspection and static validation alone are not remote-install or live-discovery evidence. Existing `v0.1.0` tags and project files remain untouched.

<a id="requirements"></a>
## User requirements

Installing and using KISS My Agent requires a plugin-capable Codex client and access to the GitHub repository. Project setup, checks, removal, and Agent configuration use Codex's own file tools. Users do not need Python, Node.js, Docker, or a package manager.

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

In a new session opened at the project you want to configure, run:

```text
$kiss-my-agent-setup set up this project
```

Trust the project through the Host interface when prompted, then start one more new session and run:

```text
$kiss-my-agent-setup check this project
```

After setup, use Codex normally. You do not need to invoke a KISS command for ordinary implementation, tests, builds, Git work, or formatting. Project instructions guide normal work; `$kiss-my-agent` is reserved for a consequential engineering ambiguity.

When you need live discovery evidence, run `/skills` in that fresh session and confirm both Plugin-owned Skills before using the narrow Smokes in [Testing](TESTING.md).

<a id="project-setup"></a>
## What project setup changes

Project setup manages only the selected target:

- `.codex/config.toml`: minimally merges the two public enablement switches.
- `.codex/agents/`: installs `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` as standalone seed roles on first setup.
- `AGENTS.md`: appends one bounded KISS managed block while preserving existing instructions.

The Skill itself remains Plugin-owned and is never copied into the project. Setup does not install software, establish trust, start Codex, or alter global configuration.

<a id="configure-agents"></a>
## Configure existing Agents

The default roles work without model configuration. To change an existing project's role model, reasoning effort, or sandbox default through a conversational wizard, run:

```text
$kiss-my-agent-setup configure agents for this project
```

The wizard previews the exact TOML changes before writing. It does not create, delete, or rename roles. You can also edit `.codex/agents/*.toml` directly; see [Configuration](CONFIGURATION.md).

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
| Unrelated config keys or AGENTS content | Preserve them. |
| Either public switch intentionally set to `false` | Preserve it and report `disabled`. |
| Existing seed filename with the expected `name` | Preserve it, including user edits. |
| Filename/identity mismatch, duplicate identity, or project/global seed-name conflict | Stop before writing. |
| Valid existing managed block | Update only that block; do not restore deliberately deleted roles. |
| Malformed markers, invalid TOML, unsafe path type, or applicable `AGENTS.override.md` | Stop without claiming success. |

Setup prepares all changes before the first write, verifies files afterward, and rolls back only its own unchanged after-content when a failure permits safe rollback. Agent-native file operations cannot promise recovery from a process or machine crash, so all ambiguous states fail closed.

<a id="update"></a>
## Update an installed Plugin

Refresh the Git marketplace and installed Plugin cache with one explicit command, then verify the selected version:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

Start a new session after the upgrade. Plugin upgrades do not silently rewrite project-owned role files. Run the matching `check` or optional configuration wizard only when you want to inspect or change a project.

KISS My Agent does not implement silent background updates. To return to the previous immutable release, reinstall from its pinned marketplace tag:

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent@v0.1.0
codex plugin add kiss-my-agent@kiss-my-agent
```

Start a new session after rollback. Existing project files remain user-owned and are not automatically downgraded.

<a id="check-and-remove"></a>
## Check or remove setup

Use the command that matches the explicit scope:

```text
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

`check` inspects managed filesystem state only. `remove` removes marked config lines, the managed AGENTS block, and unchanged bundled roles in the chosen scope. Modified or ambiguously owned roles are preserved and reported. Removing setup does not uninstall the Plugin.

<a id="contributor-tools"></a>
## Contributor tools

Plugin/Skill-only contributors can run the dependency-free local core checks with Python 3.11+:

```bash
python scripts/validate.py
python -m unittest tests.test_setup -v
```

They do not need to install the Markdown package or build the site locally. Pull-request CI installs the pinned documentation dependency and runs `python scripts/test_all.py`, including the isolated site build. See [Contributing](../CONTRIBUTING.md) for platform-specific details. None of these tools are used by Plugin consumers.

<a id="fresh-session"></a>
## New-session boundary

Plugin install/update and project config, instructions, Skill, or role changes affect startup and discovery. Use a new authenticated session at the intended trusted project before interpreting results. Record the Codex version, release, scope, trust state, and session freshness when reporting live behavior.
