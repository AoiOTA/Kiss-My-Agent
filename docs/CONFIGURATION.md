# Configuration

[English](CONFIGURATION.md) | [简体中文](CONFIGURATION.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Testing](TESTING.md) · [FAQ](FAQ.md)

<a id="default-configuration"></a>
## Default configuration

The default configuration is:

```toml
model = "gpt-6-astra" # KISS My Agent managed
model_reasoning_effort = "high" # KISS My Agent managed

[features]
multi_agent = true # KISS My Agent managed

[features.context_management]
experimental_mode = true # KISS My Agent managed

[agents]
enabled = true # KISS My Agent managed
```

These defaults select Astra/high, multi-agent capability, custom-Agent discovery and experimental context management when the selected trusted layer is active and no higher-priority layer overrides it. They do not change permissions, concurrency, trust, providers, authentication or telemetry.

Setup independently fills each missing master field with `gpt-6-astra` / `high` and each missing feature with marked `true`, including `features.context_management.experimental_mode`. Existing explicit values, including `false`, are preserved. Only a complete top-level `gpt-5.6-sol` / `max` pair, with each key occurring exactly once and each line carrying the exact `# KISS My Agent managed` marker, is updated together to Astra/high. Modified, unmarked or incomplete pairs remain user-owned; only truly missing fields are filled. Duplicate assignments, invalid TOML and ambiguous ownership are conflicts. Setup changes only the selected project or global scope.

<a id="zero-configuration"></a>
## Default roles use Astra / medium

First setup installs three editable seeds:

| Role | Responsibility | Model | Reasoning effort | Seed sandbox default |
| --- | --- | --- | --- | --- |
| `kiss_explorer` | Read-only investigation | `gpt-6-astra` | `medium` | `read-only` |
| `kiss_coder` | Bounded implementation and state changes | `gpt-6-astra` | `medium` | `workspace-write` |
| `kiss_reviewer` | Independent read-only review | `gpt-6-astra` | `medium` | `read-only` |

The current seeds explicitly set `model = "gpt-6-astra"` and the effort shown above. They are editable fresh-setup defaults. A fresh setup creates only missing starters; every role that already exists is user-owned and setup or a Plugin update never overwrites, migrates, or version-classifies it. Once setup exists, a missing starter remains intentionally absent. Plugin cache seeds are package resources and do not automatically become Host-discoverable roles.

<a id="three-owners"></a>
## Three owners

| Owner | Surface | Responsibility |
| --- | --- | --- |
| Enablement | `.codex/config.toml` | Multi-agent switches and missing Astra/high and experimental-context defaults. |
| Discovery | `.codex/agents/*.toml` | Standalone role definitions discovered by the Host. |
| Delegation | `AGENTS.md` | Direct small work and beneficial delegation, chosen dynamically while the master owns architecture, acceptance, and evidence. |

The layers do not replace one another. A role file does not enable multi-agent tools, an enablement switch does not create a role catalog, and instructions do not grant runtime permissions. The catalog remains open and the master chooses dynamically from roles that actually exist; KISS My Agent does not require a fixed team size or workflow. The master may directly complete clear small or local work, and should actively delegate substantial bulk, independent parallel work, or work needing another perspective when the benefit outweighs coordination cost. Choose by workload, parallel opportunity, coupling, risk, and coordination cost; optional roles do not mean the master should do everything. Each available role may have zero, one, or multiple instances, with no fixed team, sequence, or required subagent launch. Coordination is flat by default, with the master directly fanning out to current roles. Only when an independent subsystem needs substantial parallel work and direct aggregation would pollute the master's context may it temporarily give one existing Agent a bounded department-lead assignment. That lead may delegate within its scope to same-role or related-role instances and synthesize results for the master, but its workers do not delegate again. The assignment ends with the task, so there is at most one intermediate management layer and no deep nesting, fixed department, additional seed, headcount, or organization schema. Every shared file or resource still has one writer or operator. The master retains architecture and acceptance decisions, conflict resolution, evidence interpretation, and final synthesis in either mode.

Do not run setup solely to create a team. KMA-managed work can use direct execution for clear small tasks without switching workflows. If delegation is disabled or unavailable, or no suitable role exists, the master may continue within its capabilities and existing authorization without a staffing approval step. Report unmet explicit requirements for independent checking or a specific role, and real capability gaps; direct execution must not be presented as satisfying them.

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

Project and global setup are always distinct. For role definitions, the Host applies project-over-global precedence and owns broader catalog warnings; KISS setup does not reject or reconcile roles across those scopes. Start a new session after changing config, instructions, Skills, Plugins, or role TOML; an existing session is not guaranteed to hot-load them.

<a id="configure-wizard"></a>
## Conversational Agent configuration wizard

Keep the current role settings unless a real workload needs a different model, effort, or sandbox. To configure existing roles in one explicit scope, run:

```text
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
$kiss-my-agent:kiss-my-agent-setup configure global agents
```

To explicitly set `gpt-6-astra` and `medium` effort in the three existing KISS roles, use this exact qualified project prompt:

```text
$kiss-my-agent:kiss-my-agent-setup configure agents in this project: for kiss_explorer, kiss_coder, and kiss_reviewer, set model to gpt-6-astra and model_reasoning_effort to medium
```

If the request names one or more roles, the wizard resolves and parses only those targets. Otherwise it lists direct role paths without parsing their contents, waits for the user to select one or more, and then parses only the selected files. It offers `keep`, `inherit`, or an explicit value for `model`, `model_reasoning_effort`, and `sandbox_mode`, shows the exact diff before writing, and requires a separate confirmation for `danger-full-access`. Invalid unselected roles do not block the operation; their catalog warnings remain the Host's responsibility.

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

Setup fills missing master fields with `gpt-6-astra` / `high`; current seed roles explicitly use `gpt-6-astra` / `medium`. Existing explicit user choices are preserved. The role wizard changes selected roles only. Static checks do not prove effective Host settings; verify them in a new task. If the configured model prevents startup, use a Host-supported model override for one recovery session:

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

Project scope manages `<target>/.codex/config.toml`, the exact `<target>/.codex/agents/{kiss_explorer,kiss_coder,kiss_reviewer}.toml` targets, and one managed block in `<target>/AGENTS.md`. Global scope manages the corresponding paths under `$CODEX_HOME`. The Skill itself stays in the installed Plugin.

“This project” means the Host's current unique project or active workspace root, not whichever child directory a shell happens to use. The Skill displays the resolved absolute target and asks the user to choose when multiple workspace roots make it ambiguous.

<a id="conflicts-and-ownership"></a>
## Conflicts and ownership

- Preserve unrelated config, roles, instructions, comments, and explicit `false` values.
- Setup, check, and remove inspect only their selected KISS config and AGENTS paths plus the three exact bundled role targets in that scope. They do not parse other role files or roles in the opposite scope.
- Stop before writing when a selected managed path has an unsafe type, the selected config or an exact bundled target has invalid TOML, an exact bundled target has missing identity fields or a `name` different from its filename, managed ownership is ambiguous, or an applicable `AGENTS.override.md` exists.
- Duplicate identities in other files and project/global duplicate role names do not block KISS setup or check. The Host owns catalog warnings and project-over-global precedence; KISS does not reconcile them.
- Every existing role is user-owned and preserved byte-for-byte. Setup never compares it with historical seeds, assigns it a version, or migrates it. A later setup does not restore a deliberately deleted starter.
- Explicit remove deletes exact current defaults with their KISS markers and any exact legacy marked master pair, the managed AGENTS block, and bundled roles whose bytes exactly match a current, known v0.2.6, known v0.2.5, or known v0.1 seed. Other role files remain user-owned. Remove preserves the context table and other user fields; a current config field is removed only when both its exact default value and marker match.

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
- [GPT-6 Astra](https://openai.com/index/gpt-6-astra/)
