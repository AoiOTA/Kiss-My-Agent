# Configuration

[English](CONFIGURATION.md) | [简体中文](CONFIGURATION.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Testing](TESTING.md) · [FAQ](FAQ.md)

<a id="repository-default"></a>
## Repository Default

The tracked `.codex/config.toml` has exactly two public switches:

```toml
[features]
multi_agent = true

[agents]
enabled = true
```

They enable the Host multi-agent capability and custom agents for this trusted project. They do not enumerate roles or set a model, reasoning effort, permission mode, context limit, concurrency limit, trust policy, provider, authentication, or telemetry.

An explicit `false` in an effective user or administrative layer, or a one-launch override, remains authoritative. Setup must not silently turn an intentional disablement back on.

<a id="three-layers"></a>
## Three Responsibilities

| Owner | Surface | Responsibility |
| --- | --- | --- |
| Enablement | `.codex/config.toml` | Two public switches only. |
| Discovery | `.codex/agents/*.toml` | Standalone role definitions auto-discovered by the Host. |
| Dispatch | `AGENTS.md` | Dynamic guidance for whether and how the primary thread delegates. |

These layers are not substitutes for one another. A role file does not turn on multi-agent support; the switches do not create a role catalog; AGENTS guidance does not grant runtime authority.

<a id="configuration-layers"></a>
## Configuration Layers

| Scope | Typical location | Purpose |
| --- | --- | --- |
| User/global | `$CODEX_HOME/config.toml` | Personal defaults across projects. |
| Trusted project | `<repo>/.codex/config.toml` | Reviewed project-local switches and settings. |
| Profile | Host-supported Profile config | Switchable personal modes. |
| One launch | CLI `--config key=value` | Temporary override without editing files. |
| Global role | `$CODEX_HOME/agents/<file>.toml` | Cross-project standalone role definition. |
| Project role | `<repo>/.codex/agents/<file>.toml` | Project standalone role definition. |

Project and global scope are always selected explicitly. Provider, authentication, telemetry, and administrative policy may add restrictions. Start a new session after changing config, instructions, Skills, plugins, or role files; an old session is not guaranteed to hot-load them.

<a id="standalone-roles"></a>
## Standalone Roles

Every standalone role TOML owns its identity through the required `name` field. The filename is a readability convention, not the source of truth. A mismatch is valid only if the Host accepts it and operators understand it; duplicate `name` values are a conflict that must be resolved rather than hidden.

KISS My Agent supplies three seed files:

| Seed name | Responsibility | Default authority intent |
| --- | --- | --- |
| `kiss_explorer` | Read-only investigation | Read-only |
| `kiss_coder` | Implementation and state-changing execution | Writable only within its assignment |
| `kiss_reviewer` | Independent read-only review | Read-only |

The seeds are not a closed catalog. Add, rename, edit, or remove standalone files deliberately. After initial setup, later setup operations preserve the current catalog; normal sessions, setup, and `check` do not restore a removed role.

Model and reasoning effort inherit effective Host settings when omitted. Optional role fields such as `model`, `model_reasoning_effort`, and `sandbox_mode` may be edited to Host-supported, intentionally authorized values. KISS My Agent intentionally does not fix role model, effort, context, concurrency, or a default subagent model.

<a id="disable"></a>
## Disable Without Editing

Disable both public surfaces for one launch:

```bash
codex --config features.multi_agent=false --config agents.enabled=false
```

To keep the capability available but disable custom agents, set only `agents.enabled=false`. A user or administrator can also persist an explicit `false`; project setup must report that effective disablement instead of treating file presence as live enablement.

<a id="setup-scopes"></a>
## Setup Scopes

After the plugin is installed and a new session discovers the setup Skill, use exactly one intended scope:

```text
$kiss-my-agent-setup set up this project
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup set up globally
$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

Project scope manages `<target>/.codex/config.toml`, `<target>/.codex/agents/`, and a KISS managed block in `<target>/AGENTS.md`. Global scope manages the corresponding files under `$CODEX_HOME`. The Skill itself remains plugin-owned and is not copied into either target.

The underlying source tool is `skills/kiss-my-agent-setup/scripts/setup.py {setup,check,remove} --scope project|global`. Project scope can use `--target`; tests and explicit isolated use can supply `--codex-home`. Most users should use the Skill interface so scope is stated in plain language.

<a id="conflicts-and-precedence"></a>
## Conflicts and Precedence

- Setup preserves unrelated config, role files, and AGENTS content; it does not replace a whole file for convenience.
- If the selected scope contains `AGENTS.override.md`, setup stops. It does not write into the override, write a hidden lower-precedence base, or report success.
- An existing seed file with the expected `name` is preserved, including user edits. A filename collision with another identity, duplicate identity, or project/global seed-name collision stops the operation.
- An existing `false` is preserved and reported as `disabled`; it is not silently replaced with `true`.
- Setup does not establish project trust, start Codex, or prove live discovery.
- Project setup never silently becomes global setup. Global setup requires the explicit global command.
- Remove acts only on the selected scope and KISS-managed content. Preserve user-edited or ambiguously owned material and report the conflict.

<a id="safe-customization"></a>
## Safe Customization

1. Identify the one effective setting or role affecting the current workload.
2. Confirm support in the installed Host and selected model.
3. Change only the owning layer without replacing unrelated content.
4. Keep `name` unique when editing or adding a standalone role.
5. Start a trusted new session after startup or discovery changes.
6. Run setup `check`, then use `/skills` and a narrow role Smoke only when live evidence is required.

No automatic model, permission, or compatibility fallback is provided.

<a id="official-references"></a>
## Official References

- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
