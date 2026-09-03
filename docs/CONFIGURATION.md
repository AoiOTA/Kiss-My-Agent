# Configuration

[English](CONFIGURATION.md) | [简体中文](CONFIGURATION.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Testing](TESTING.md) · [FAQ](FAQ.md)

<a id="default-configuration"></a>
## Default configuration

The tracked project config contains two master defaults and two public switches:

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "max"

[features]
multi_agent = true

[agents]
enabled = true
```

The first two values select `gpt-5.6-sol` with `max` effort for the master. The switches enable the Host's multi-agent capability and custom-Agent discovery when this trusted project layer is active and no higher-priority layer overrides them. They do not select permissions, context, concurrency, trust, providers, authentication, or telemetry.

These are initial defaults, not enforcement. The managed-block classifications are mutually exclusive: a current block never receives missing master keys; when the block is absent or recognized as outdated, setup adds the master model and effort together only if both keys are absent; in every other case, existing assignments are preserved and each missing key remains absent for inheritance. Deleting one or both keys after current setup is also an intentional user change, so later setup or Plugin updates do not restore them. Existing feature values are likewise preserved whether marked or unmarked, including an explicit `false`. Local file preservation is not a claim about the final runtime value, and static check reports each master setting as explicit or `inherit`; it does not resolve all configuration layers or prove that the Host/account supports a model or effort. Start a new session so unsupported settings surface as real load or spawn failures.

<a id="zero-configuration"></a>
## Default roles set model and effort

First setup installs three editable seeds:

| Role | Responsibility | Model | Reasoning effort | Seed sandbox default |
| --- | --- | --- | --- | --- |
| `kiss_explorer` | Read-only investigation | `gpt-5.6-sol` | `high` | `read-only` |
| `kiss_coder` | Bounded implementation and state changes | `gpt-5.6-sol` | `high` | `workspace-write` |
| `kiss_reviewer` | Independent read-only review | `gpt-5.6-sol` | `xhigh` | `read-only` |

The current seeds explicitly set the model and effort shown above. They are editable fresh-setup defaults. A fresh setup creates only missing starters; every role that already exists is user-owned and setup never overwrites, migrates, or version-classifies it. Once setup exists, a missing starter remains intentionally absent. Plugin cache seeds are package resources and do not automatically become Host-discoverable roles.

<a id="three-owners"></a>
## Three owners

| Owner | Surface | Responsibility |
| --- | --- | --- |
| Master and enablement | `.codex/config.toml` | First-setup master model/effort defaults and the two public switches. |
| Discovery | `.codex/agents/*.toml` | Standalone role definitions discovered by the Host. |
| Delegation | `AGENTS.md` | Dynamic guidance for deciding whether delegation is worthwhile and keeping the master on coordination and decisions. |

The layers do not replace one another. A role file does not enable multi-agent tools, an enablement switch does not create a role catalog, and instructions do not grant runtime permissions. The catalog remains open and the master chooses dynamically from roles that actually exist; KISS My Agent does not require a fixed team size or workflow. Multiple instances of each explorer, coder, or reviewer role may run. Coordination is flat by default, with the master directly fanning out to current roles. Only when an independent subsystem needs substantial parallel work and direct aggregation would pollute the master's context may it temporarily give one existing Agent a bounded department-lead assignment. That lead may delegate within its scope to same-role or related-role instances and synthesize results for the master, but its workers do not delegate again. The assignment ends with the task, so there is at most one intermediate management layer and no deep nesting, fixed department, additional seed, headcount, or organization schema. Every shared file or resource still has one writer or operator. Delegable bulk exploration, implementation, validation, and review stay with subagents so the master can coordinate, resolve architecture and acceptance questions or conflicts, interpret evidence, and synthesize the final result.

For a simple task, do not run setup or trigger the KISS My Agent Skill solely to create a team; use the user's selected model and effort in an ordinary single conversation. For a complex research-engineering project, setup may explicitly enable the executive-only master workflow. If that configured workflow has delegation disabled or unavailable, or no suitable role exists, the master reports the staffing issue instead of silently doing delegated work. The user then chooses either to repair or enable a suitable role, or to explicitly switch this task to ordinary single-conversation execution; only that explicit switch authorizes the master to execute it directly.

<a id="configuration-layers"></a>
## Configuration layers

| Scope | Typical location | Use |
| --- | --- | --- |
| User/global | `$CODEX_HOME/config.toml` | Personal defaults across projects. |
| Trusted project | `<repo>/.codex/config.toml` | Reviewed project-level settings. |
| Global roles | `$CODEX_HOME/agents/<file>.toml` | Personal standalone roles across projects. |
| Project roles | `<repo>/.codex/agents/<file>.toml` | Project-specific standalone roles. |
| One launch | CLI `--config key=value` | Temporary override without editing a file. |

Codex resolves configuration from highest to lowest precedence: CLI flags and `--config` overrides; trusted project `.codex/config.toml` files, with the file nearest the current working directory winning; the profile selected by `--profile`; user config; system config; then built-in defaults. Therefore a project `true` can override a lower user `false`, while a CLI `false` can override the project. Administrator requirements may constrain the resulting settings separately.

Project and global setup are always distinct. Start a new session after changing config, instructions, Skills, Plugins, or role TOML; an existing session is not guaranteed to hot-load them.

<a id="configure-wizard"></a>
## Conversational Agent configuration wizard

Keep the inherited defaults unless a real workload needs a different model, effort, or sandbox. To configure existing roles in one explicit scope, run:

```text
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
$kiss-my-agent:kiss-my-agent-setup configure global agents
```

The wizard lists the current role catalog, lets you select one or more roles, and offers `keep`, `inherit`, or an explicit value for `model`, `model_reasoning_effort`, and `sandbox_mode`. It shows the exact diff before writing and requires a separate confirmation for `danger-full-access`.

Project scope resolves to `<unique Host project or active workspace root>/.codex/agents`; if multiple roots or no unique root are available, the wizard asks for an absolute project target before writing. Global scope resolves from a non-empty `CODEX_HOME`, otherwise from the current user's `~/.codex`, and uses its `agents/` directory. The wizard shows the resolved absolute role-directory path before inspection.

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

Codex first resolves each model or effort field from an explicit spawn value, then `agents.default_subagent_model` or `agents.default_subagent_reasoning_effort`, then the parent. If an explicit spawn or `[agents]` default selects a model but neither source specifies effort, Codex uses that model's default effort. An explicit `model` or `model_reasoning_effort` in the custom-Agent role file is then the final role override. A role file that overrides only `model` preserves the already-resolved effort; it does not automatically recompute effort from the role model.

Other omitted session settings inherit from the parent. A child inherits the parent's current sandbox policy, and Codex reapplies the parent turn's live sandbox and approval overrides when spawning it, even if the role file contains different defaults. Administrator requirements can constrain permissions further; a role file is not a permission grant. Validate effective behavior in a new session.

Setup and static check cannot prove that the Host/account supports the default model or efforts. Before restarting, edit the selected config or role TOML directly if a supported value is already known. If the configured master cannot start, use the highest-precedence CLI override for one recovery session:

```bash
codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'
```

Then edit the persistent config or role TOML and start another new session. KISS My Agent never silently substitutes a fallback model or effort.

<a id="setup-scopes"></a>
## Setup scopes

The Plugin-owned Skill performs Agent-native file operations without Python, Node.js, or a package manager:

```text
$kiss-my-agent:kiss-my-agent-setup set up this project
$kiss-my-agent:kiss-my-agent-setup check this project
$kiss-my-agent:kiss-my-agent-setup remove from this project

$kiss-my-agent:kiss-my-agent-setup set up globally
$kiss-my-agent:kiss-my-agent-setup check global setup
$kiss-my-agent:kiss-my-agent-setup remove global setup
```

Project scope manages `<target>/.codex/config.toml`, `<target>/.codex/agents/`, and one managed block in `<target>/AGENTS.md`. Global scope manages the corresponding files under `$CODEX_HOME`. The Skill itself stays in the installed Plugin.

“This project” means the Host's current unique project or active workspace root, not whichever child directory a shell happens to use. The Skill displays the resolved absolute target and asks the user to choose when multiple workspace roots make it ambiguous.

<a id="conflicts-and-ownership"></a>
## Conflicts and ownership

- Preserve unrelated config, roles, instructions, comments, and explicit `false` values.
- Stop before writing on malformed TOML, unsafe path types, duplicate identities, filename/identity conflicts, or an applicable `AGENTS.override.md`.
- Project/global duplicate seed names prevent setup and check. They do not prevent an explicit remove from one selected scope, because remove is the recovery path.
- Every existing role is user-owned and preserved byte-for-byte. Setup never compares it with historical seeds, assigns it a version, or migrates it. A later setup does not restore a deliberately deleted starter.
- Explicit remove deletes marked config assignments, the managed AGENTS block, and bundled roles whose bytes exactly match a current or known v0.1 seed. Other role files remain user-owned.

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
- [Basic configuration and precedence](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model)
