# Configuration

[English](CONFIGURATION.md) | [简体中文](CONFIGURATION.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Testing](TESTING.md) · [FAQ](FAQ.md)

<a id="default-configuration"></a>
## Default configuration

The tracked project config contains only two public switches:

```toml
[features]
multi_agent = true

[agents]
enabled = true
```

They enable the Host's multi-agent capability and custom-Agent discovery for a trusted project. They do not select roles, models, reasoning effort, permissions, context, concurrency, trust, providers, authentication, or telemetry. Explicit user, administrator, or one-launch `false` values remain authoritative.

<a id="zero-configuration"></a>
## Default roles need no model setup

First setup installs three editable seeds:

| Role | Responsibility | Seed sandbox default |
| --- | --- | --- |
| `kiss_explorer` | Read-only investigation | `read-only` |
| `kiss_coder` | Bounded implementation and state changes | `workspace-write` |
| `kiss_reviewer` | Independent read-only review | `read-only` |

The seeds omit `model` and `model_reasoning_effort`, so they inherit the effective Host settings. This is the recommended cross-version default: users can start immediately without knowing model identifiers or maintaining a version-specific preset.

<a id="three-owners"></a>
## Three owners

| Owner | Surface | Responsibility |
| --- | --- | --- |
| Enablement | `.codex/config.toml` | The two public switches only. |
| Discovery | `.codex/agents/*.toml` | Standalone role definitions discovered by the Host. |
| Delegation | `AGENTS.md` | Dynamic guidance for deciding whether delegation is worthwhile. |

The layers do not replace one another. A role file does not enable multi-agent tools, an enablement switch does not create a role catalog, and instructions do not grant runtime permissions.

<a id="configuration-layers"></a>
## Configuration layers

| Scope | Typical location | Use |
| --- | --- | --- |
| User/global | `$CODEX_HOME/config.toml` | Personal defaults across projects. |
| Trusted project | `<repo>/.codex/config.toml` | Reviewed project-level settings. |
| Global roles | `$CODEX_HOME/agents/<file>.toml` | Personal standalone roles across projects. |
| Project roles | `<repo>/.codex/agents/<file>.toml` | Project-specific standalone roles. |
| One launch | CLI `--config key=value` | Temporary override without editing a file. |

Project and global setup are always distinct. Start a new session after changing config, instructions, Skills, Plugins, or role TOML; an existing session is not guaranteed to hot-load them.

<a id="configure-wizard"></a>
## Conversational Agent configuration wizard

Keep the inherited defaults unless a real workload needs a different model, effort, or sandbox. To configure existing roles in one explicit scope, run:

```text
$kiss-my-agent-setup configure agents for this project
$kiss-my-agent-setup configure global agents
```

The wizard lists the current role catalog, lets you select one or more roles, and offers `keep`, `inherit`, or an explicit value for `model`, `model_reasoning_effort`, and `sandbox_mode`. It shows the exact diff before writing and requires a separate confirmation for `danger-full-access`.

It does not create, delete, rename, or restore roles. Model availability is Host- and account-specific, so the wizard does not ship a hard-coded model catalog. Use the exact identifier exposed by the current Host or retain inheritance.

If an existing role uses `default_permissions` or a `sandbox_workspace_write` table, the wizard will not create a conflicting `sandbox_mode` edit. Make that related multi-key change manually after checking the current Host schema.

<a id="manual-role-editing"></a>
## Manual role editing

You can make the same change directly in an existing standalone role file:

```toml
name = "my_role"
description = "Explain when Codex should use this role."
model = "HOST_SUPPORTED_MODEL_ID"
model_reasoning_effort = "HOST_SUPPORTED_EFFORT"
sandbox_mode = "read-only"

developer_instructions = """
Give this role one narrow responsibility and preserve the parent task boundary.
"""
```

Required fields are `name`, `description`, and `developer_instructions`. The `name` field is the identity; matching the filename is the simplest convention. Keep names unique in the effective catalog.

<a id="precedence"></a>
## Model and permission precedence

When a custom-Agent file sets `model` or `model_reasoning_effort`, that file is applied as the role override. When a field is omitted, Codex resolves it from an explicit spawn value, then the corresponding `[agents]` default, then the parent. A role file that overrides only `model` preserves the effort resolved before that role override; it does not automatically recompute effort from the role model.

Other omitted session settings inherit from the parent. Parent-turn live permission choices and administrator requirements can still constrain or override a role file's `sandbox_mode`; a role file is not a permission grant. Validate effective behavior in a new session.

<a id="setup-scopes"></a>
## Setup scopes

The Plugin-owned Skill performs Agent-native file operations without Python, Node.js, or a package manager:

```text
$kiss-my-agent-setup set up this project
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup set up globally
$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

Project scope manages `<target>/.codex/config.toml`, `<target>/.codex/agents/`, and one managed block in `<target>/AGENTS.md`. Global scope manages the corresponding files under `$CODEX_HOME`. The Skill itself stays in the installed Plugin.

“This project” means the Host's current unique project or active workspace root, not whichever child directory a shell happens to use. The Skill displays the resolved absolute target and asks the user to choose when multiple workspace roots make it ambiguous.

<a id="conflicts-and-ownership"></a>
## Conflicts and ownership

- Preserve unrelated config, roles, instructions, comments, and explicit `false` values.
- Stop before writing on malformed TOML, unsafe path types, duplicate identities, filename/identity conflicts, or an applicable `AGENTS.override.md`.
- Project/global duplicate seed names prevent setup and check. They do not prevent an explicit remove from one selected scope, because remove is the recovery path.
- Existing correctly identified roles are user-owned and preserved. A later setup does not restore a deliberately deleted seed.
- Remove deletes only marked config assignments, the managed AGENTS block, and bundled roles whose bytes still match the current seeds.

<a id="disable"></a>
## Disable for one launch

To disable both public multi-agent surfaces without editing files:

```bash
codex --config features.multi_agent=false --config agents.enabled=false
```

To remove KISS project guidance and seed setup persistently, use the explicit project remove command instead. Disabling the multi-agent switches alone does not delete an existing AGENTS block.

<a id="official-references"></a>
## Official references

- [Subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
