# Configuration

[README](../README.md) · [简体中文](../README.zh-CN.md) · [Installation](INSTALLATION.md) · [Extending](EXTENDING.md) · [FAQ](FAQ.md)

KISS My Agent separates durable guidance from host runtime configuration. The repository defaults are examples, not requirements. Choose settings that your Codex host and selected model actually support.

This repository intentionally does not contain an active `.codex/config.toml`. The annotated [`config.example.toml`](../examples/config.example.toml) is inert at its tracked path. Copy only the settings you need into an existing configuration layer after reviewing them.

## Configuration layers

| Scope | Location or command | Typical use |
| --- | --- | --- |
| User | `~/.codex/config.toml` | Defaults for the primary thread and all projects |
| Trusted project | `<repo>/.codex/config.toml` | Overrides shared by one trusted project |
| Profile | `$CODEX_HOME/<name>.config.toml` with `--profile <name>` | Switchable personal modes such as fast or deep review |
| One run | `--model` or `--config key=value` | Temporary experiments without editing files |
| Personal role | `~/.codex/agents/<role>.toml` | A custom agent available across projects |
| Project role | `<repo>/.codex/agents/<role>.toml` | A custom agent available in one project |

Project config is loaded only for trusted projects. Provider, authentication, notification, profile-selection, and telemetry settings have user-level restrictions; consult the official reference before moving them into a project.

## Primary thread and custom roles

There is no `master.toml`. The primary or master thread uses the effective session configuration selected by the app, CLI, user config, trusted project config, Profile, and one-off overrides.

The supplied custom roles are editable examples:

| Role | Supplied model | Supplied reasoning | Supplied sandbox |
| --- | --- | --- | --- |
| `kiss_explorer` | `gpt-5.6-sol` | `medium` | `read-only` |
| `kiss_coder` | `gpt-5.6-sol` | `high` | `workspace-write` |
| `kiss_reviewer` | `gpt-5.6-sol` | `xhigh` | `read-only` |

Change `model`, `model_reasoning_effort`, or `sandbox_mode` in the role TOML when another choice better fits the host, workload, latency, cost, or authority boundary. The effort must be supported by the selected model. Codex custom agents can inherit optional settings that are omitted, but the supplied KISS role templates keep these three choices explicit and the repository validator checks their structure. Parent live permissions and administrator policy can still constrain a subagent.

The role TOML is the role's configuration layer, not a guarantee that a Host registered the role name. The annotated example contains optional `[agents.kiss_explorer]`, `[agents.kiss_coder]`, and `[agents.kiss_reviewer]` tables whose `config_file` values point at the matching TOML files. Merge only these prefixed tables into the intended user or trusted-project config when explicit registration is required. A trusted project layer must load before its registrations can take effect.

`review_model` is different from `.codex/agents/kiss_reviewer.toml`: the former selects the model used by the `/review` command, while the latter defines the optional `kiss_reviewer` custom subagent.

The KISS prefix is intentional. Existing built-in and personal `explorer`, `coder`, `review`, or similarly named roles remain untouched. If a destination already contains the same `kiss_*` name, stop and diff instead of overwriting it.

## High-value settings map

| Area | Settings | Guidance |
| --- | --- | --- |
| Primary model | `model`, `model_reasoning_effort`, `model_verbosity`, `service_tier` | Start with a host-supported model and increase effort only when it produces useful quality gains. |
| Review command | `review_model` | Optional override for `/review`; otherwise the current session model is used. |
| Subagent defaults | `agents.default_subagent_model`, `agents.default_subagent_reasoning_effort` | Defaults for spawned agents that do not select their own values. |
| Multi-Agent | `agents.enabled`, `agents.max_concurrent_threads_per_session`, `agents.interrupt_message` | The maximum is a capacity cap, not a fan-out target. Leave it unset to use the host default. |
| Context | `model_context_window`, `model_auto_compact_token_limit`, `model_auto_compact_token_limit_scope` | Prefer model defaults unless the real model/provider limits are known. |
| Permissions | `sandbox_mode`, `default_permissions`, `approval_policy` | Choose one sandbox configuration style and review its authority deliberately. |
| Workspace write | `sandbox_workspace_write.network_access`, `writable_roots`, temporary-directory exclusions | Applies only to workspace-write behavior. Add access only for a current task requirement. |
| Instructions | `project_doc_max_bytes`, `project_doc_fallback_filenames`, `project_root_markers`, project trust | Controls instruction discovery and whether project-local Codex layers load. |

The complete Codex surface also includes model providers, authentication, shell environment policy, web search, MCP servers, hooks, apps, and telemetry. KISS My Agent does not duplicate that evolving reference or prescribe values without a current consumer.

## Context and automatic compaction

`model_context_window` describes the token capacity available to Codex for the active model. Increasing the number does not increase the model's real capability. An incorrect value can cause requests or compaction behavior to fail.

`model_auto_compact_token_limit` is the threshold that triggers automatic history compaction. Leave it unset to use the model default unless you know the active context limit and why a custom threshold improves the workload. If set, leave enough space for output, tool results, and subsequent turns.

`model_auto_compact_token_limit_scope` controls whether the threshold counts the total active context or only growth after the carried compaction prefix. Do not copy one context or compaction number across different models or providers as a universal recommendation.

## Multi-Agent capacity

The `[agents]` table controls availability and defaults. `agents.max_concurrent_threads_per_session` limits concurrently open spawned-agent threads and excludes the primary thread. It does not instruct the master to use that many agents.

KISS My Agent still routes by independence and information gain:

- keep coherent small work in one thread;
- parallelize only genuinely independent work;
- give one operator control of shared mutable resources;
- stop spawning when coordination costs more than it returns.

Use `agents.max_concurrent_threads_per_session`; `agents.max_threads` is a legacy alias.

## Permissions and approvals

The supplied role defaults express the intended responsibility, but behavioral instructions are not a security boundary.

- `read-only` is suitable for investigation and independent review.
- `workspace-write` is suitable for implementation inside writable roots.
- `danger-full-access` materially broadens authority and should be selected only when the user and environment intend it.

At a config layer, use either the legacy-style `sandbox_mode` plus optional `sandbox_workspace_write.*` settings, or `default_permissions` with a permission profile. Do not combine those approaches in the same layer. `approval_policy` separately controls when Codex asks before executing commands.

Filesystem access, network access, approvals, MCP/app permissions, authentication, and role instructions are distinct. A writable filesystem setting does not automatically grant network or external-account authority.

KISS My Agent does not disable Web access. Web availability follows the Host, selected tools, `web_search`, network policy, sandbox, and approval configuration. A focused local-discovery test may temporarily forbid Web so an Agent cannot hide a broken local Skill or reference path by searching for a similarly named public file; that test constraint is not a product default.

## Profiles and one-off overrides

Profiles are useful when the same user needs several recurring runtime combinations without changing the base config. A Profile file uses ordinary top-level config keys and is selected with `--profile`.

For a one-time comparison, prefer a CLI override:

```bash
codex --model gpt-5.6-sol
codex --config model_reasoning_effort='"medium"'
codex --config agents.max_concurrent_threads_per_session=4
```

The model and concurrency number above demonstrate syntax only, not a universal recommendation. Replace the model with one supported by your Host.

## Safe customization workflow

1. Identify the narrow setting that affects the current workload.
2. Confirm the model, effort, and setting are supported by the installed host.
3. Change one user, project, Profile, role, or CLI layer deliberately.
4. Start a new session when discovery or startup configuration changed.
5. Confirm the actual model, permissions, agents, and `/skills` result.
6. Keep the change only if it improves the real task.

KISS My Agent does not silently switch models, efforts, permissions, or providers when a selection fails. Visible configuration errors are easier to diagnose than hidden fallback behavior.

## Official references

- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
