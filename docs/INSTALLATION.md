# Installation and Coexistence

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.md) · [Configuration](CONFIGURATION.md) · [Testing](TESTING.md) · [FAQ](FAQ.md)

<a id="release-status"></a>
## Release Status

The Git-backed marketplace is prepared for version `v0.1.0`, but Codex cannot install that version remotely until the Git tag exists. The current evidence is source inspection and static validation, not publication, remote installation, or live discovery. Do not interpret the commands below as a claim that the tag is already available.

<a id="install-plugin"></a>
## Install the Plugin

When the tagged marketplace version is available, use the public installation interface:

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

Start a new authenticated Codex session after installation. An already-running session is not guaranteed to discover a newly installed plugin or Skill.

<a id="project-setup"></a>
## Set Up One Project

From a new session opened in the intended project, run:

```text
$kiss-my-agent-setup set up this project
```

Project setup manages only the selected project:

- `.codex/config.toml`: the two public switches, merged without replacing unrelated settings.
- `.codex/agents/`: the three standalone seed role files.
- `AGENTS.md`: a bounded KISS managed block, preserving unrelated instructions.

The Skill remains plugin-owned; setup does not copy a Skill tree into the project. It also does not establish Host trust or restart Codex.

Trust the project through the Host, start another new session, and run:

```text
$kiss-my-agent-setup check this project
```

Use `/skills` and the harmless checks in [Testing](TESTING.md) only when live discovery evidence is needed.

<a id="global-setup"></a>
## Set Up Globally

Global setup is optional and never inferred from a project request. Ask for it explicitly:

```text
$kiss-my-agent-setup set up globally
```

It manages the corresponding `config.toml`, `agents/`, and AGENTS managed block under `$CODEX_HOME`. Start a new session, then check that scope explicitly:

```text
$kiss-my-agent-setup check global setup
```

Prefer project scope when the behavior is project-specific. Global scope affects every project that loads the user configuration, subject to effective Host, administrator, user, and project settings.

<a id="collision-policy"></a>
## Collision and Override Policy

| Existing state | Required behavior |
| --- | --- |
| Unrelated config keys or AGENTS content | Preserve them. |
| Intentional `false` for either public switch | Preserve it and report `disabled`; do not silently re-enable. |
| Existing seed file with its expected `name`, including edits | Preserve it. |
| Filename/identity mismatch, duplicate identity, or project/global seed-name collision | Stop and review; do not overwrite. |
| Valid KISS managed content already present | Treat exact setup as idempotent. |
| Malformed or duplicated managed block | Stop without claiming success. |
| `AGENTS.override.md` in the selected scope | Stop. Do not write to the override or hide content in a lower-precedence base file. |

The setup operation makes the smallest scope-owned change. It does not replace an existing config, invent a compatibility alias, or convert project setup into global setup.

<a id="role-lifecycle"></a>
## Role Lifecycle

The supplied `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` definitions are seeds, not a closed catalog. Standalone role TOML files are auto-discovered; the `name` field is identity and the filename is only a convention. Model and effort inherit Host values when omitted and remain editable.

Users may add, edit, rename, or delete roles. After initial setup, normal sessions, setup, and `check` preserve the current catalog and never recreate a deleted file.

<a id="check-and-remove"></a>
## Check or Remove

Use the matching explicit scope:

```text
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

`check` inspects managed filesystem state; it does not prove trust, active-session loading, plugin publication, or role behavior. `remove` targets only the selected scope and KISS-managed content. It must preserve unrelated settings, instructions, and roles, and stop on ambiguous ownership or conflicting edits rather than deleting them.

After removal, start a new session before judging discovery. Removing setup output does not uninstall the plugin itself; plugin lifecycle remains a Codex plugin operation.

<a id="source-tools"></a>
## Source Checkout Tools

Contributors can validate a checkout without installing the plugin:

```bash
python3 scripts/validate.py
```

The underlying setup utility is available for isolated testing and development:

```bash
python3 skills/kiss-my-agent-setup/scripts/setup.py setup --scope project --target /absolute/path/to/project
python3 skills/kiss-my-agent-setup/scripts/setup.py check --scope project --target /absolute/path/to/project
python3 skills/kiss-my-agent-setup/scripts/setup.py remove --scope project --target /absolute/path/to/project
```

Global operations use `--scope global`; `--codex-home` is available for explicit isolated targets. Direct source-tool success is static filesystem evidence, not a successful marketplace installation or live Codex session.

<a id="fresh-session"></a>
## Fresh-Session Boundary

Plugin installation and setup are startup/discovery changes. Use a new session after installing the plugin and another new session after setup, removal, or role/config changes. Current sessions are not guaranteed to hot-load. Record the Host version, scope, trust state, and session freshness when reporting live results.
