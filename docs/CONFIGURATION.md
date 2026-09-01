# Configuration

[English](CONFIGURATION.md) | [简体中文](CONFIGURATION.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Testing](TESTING.md) · [FAQ](FAQ.md)

<a id="repository-default"></a>
## Repository Default

The tracked `.codex/config.toml` is intentionally small. It sets `agents.enabled = true` and registers `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` through their files under `.codex/agents/`. It does not set a model, reasoning effort, permission mode, context limit, concurrency limit, trust policy, provider, authentication, or telemetry.

Project config is considered only when the Host trusts the project. Start a new session after changing project config, instructions, Skills, or roles. Current old sessions are not guaranteed to hot-load them.

Disable custom agents for one launch without modifying the repository:

```bash
codex --config agents.enabled=false
```

```powershell
codex --config agents.enabled=false
```

<a id="configuration-layers"></a>
## Configuration Layers

| Scope | Typical location | Purpose |
| --- | --- | --- |
| User | `~/.codex/config.toml` | Personal defaults across projects. |
| Trusted project | `<repo>/.codex/config.toml` | Project registrations and reviewed project overrides. |
| Profile | Host-supported Profile config | Switchable personal modes. |
| One launch | CLI `--config key=value` | Temporary override without editing files. |
| Personal role | `~/.codex/agents/<role>.toml` | Cross-project role definition. |
| Project role | `<repo>/.codex/agents/<role>.toml` | Project role definition. |

Later effective layers may override earlier values. Provider, authentication, telemetry, and administrative policy can have additional restrictions. Consult the current official Codex reference before moving settings between scopes.

<a id="primary-thread-and-roles"></a>
## Primary Thread and Roles

There is no `master.toml`. The primary thread uses effective Host, CLI, user, Profile, and trusted-project settings.

The three role TOML files contain editable role-specific examples:

| Role | Responsibility | Supplied sandbox |
| --- | --- | --- |
| `kiss_explorer` | Read-only investigation | `read-only` |
| `kiss_coder` | Implementation and state-changing execution | `workspace-write` |
| `kiss_reviewer` | Independent read-only review | `read-only` |

Model and effort values must be supported by the installed Host. Role instructions are not a security boundary; live parent permissions and administrator policy can constrain a subagent. `review_model` selects the `/review` model and is separate from the `kiss_reviewer` custom role.

<a id="registration"></a>
## Registration

Each `[agents.<name>]` table maps a stable role name to a relative role file. Relative `config_file` paths resolve from the config layer. Copying a role file without a registration does not prove that the Host exposes it. Existing same-name registrations must be diffed and merged manually, never overwritten.

The KISS prefix avoids collision with generic `explorer`, `coder`, and `review` roles. Those generic roles remain untouched.

<a id="runtime-settings"></a>
## Runtime Settings

| Area | Representative settings | Guidance |
| --- | --- | --- |
| Model | `model`, `model_reasoning_effort`, `model_verbosity`, `review_model` | Use Host-supported values; do not add silent fallback. |
| Multi-agent | `agents.enabled`, `agents.max_concurrent_threads_per_session` | Capacity is not a fan-out target. |
| Context | `model_context_window`, `model_auto_compact_token_limit` | Prefer model defaults unless actual limits and need are known. |
| Permissions | `sandbox_mode`, `default_permissions`, `approval_policy` | Review real authority; do not mix incompatible permission styles. |
| Instructions | `project_doc_max_bytes`, `project_doc_fallback_filenames`, `project_root_markers` | These affect discovery, not product behavior. |

`model_context_window` cannot increase a model's real capacity. A wrong value can cause failures. A custom `model_auto_compact_token_limit` must fit the actual model and leave space for output, tool results, and later turns.

`agents.max_concurrent_threads_per_session` is a capacity cap, not an instruction to fill every slot. Use multiple agents only when independence, information gain, risk isolation, or latency outweighs coordination cost.

<a id="permissions-and-sandbox"></a>
## Permissions and Sandbox

- `read-only` fits investigation and independent review.
- `workspace-write` fits implementation inside intended writable roots.
- `danger-full-access` materially broadens authority and is not required to validate this repository.

Static validation runs as an ordinary native script and requires no Codex sandbox package. This does not bypass OS or Host permissions. Filesystem access, network access, approvals, external-app permissions, authentication, and behavioral instructions are distinct.

<a id="safe-customization"></a>
## Safe Customization

1. Identify the one setting affecting the current workload.
2. Confirm support in the installed Host and selected model.
3. Change one reviewed layer without replacing unrelated content.
4. Start a trusted new session for startup/discovery changes.
5. Confirm actual model, permissions, `/skills`, and registered roles.
6. Keep the change only when it improves the real task.

For syntax-only launch comparisons:

```bash
codex --model gpt-5.6-sol
codex --config model_reasoning_effort='"medium"'
codex --config agents.max_concurrent_threads_per_session=4
```

```powershell
codex --model gpt-5.6-sol
codex --config 'model_reasoning_effort="medium"'
codex --config agents.max_concurrent_threads_per_session=4
```

These values are examples, not recommendations. No automatic model or permission fallback is provided.

<a id="official-references"></a>
## Official References

- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
