# 配置

[English](CONFIGURATION.md) | [简体中文](CONFIGURATION.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="repository-default"></a>
## 仓库默认配置

仓库跟踪的 `.codex/config.toml` 刻意保持很小：设置 `agents.enabled = true`，并通过 `.codex/agents/` 下的文件注册 `kiss_explorer`、`kiss_coder` 和 `kiss_reviewer`。它不设置模型、reasoning effort、权限模式、上下文上限、并发上限、信任策略、provider、认证或 telemetry。

Host 只会在项目可信时考虑项目 config。修改项目 config、instructions、Skills 或角色后启动新会话；当前旧会话不保证热加载。

无需修改仓库即可为单次启动禁用自定义 Agent：

```bash
codex --config agents.enabled=false
```

```powershell
codex --config agents.enabled=false
```

<a id="configuration-layers"></a>
## 配置层

| Scope | 典型位置 | 用途 |
| --- | --- | --- |
| 用户 | `~/.codex/config.toml` | 跨项目个人默认值。 |
| 可信项目 | `<repo>/.codex/config.toml` | 项目注册与审核过的项目 override。 |
| Profile | Host 支持的 Profile config | 可切换的个人模式。 |
| 单次启动 | CLI `--config key=value` | 不编辑文件的临时 override。 |
| 个人角色 | `~/.codex/agents/<role>.toml` | 跨项目角色定义。 |
| 项目角色 | `<repo>/.codex/agents/<role>.toml` | 项目角色定义。 |

后生效的层可能覆盖先前取值。Provider、认证、telemetry 与管理员策略可能另有限制。把设置移到不同 scope 前，应查阅当前官方 Codex reference。

<a id="primary-thread-and-roles"></a>
## 主线程与角色

项目没有 `master.toml`。主线程使用 Host、CLI、用户、Profile 与可信项目共同决定的实际配置。

三个角色 TOML 包含可编辑的角色专用示例：

| 角色 | 职责 | 提供的 sandbox |
| --- | --- | --- |
| `kiss_explorer` | 只读调查 | `read-only` |
| `kiss_coder` | 实现与状态变更执行 | `workspace-write` |
| `kiss_reviewer` | 独立只读审查 | `read-only` |

模型与 effort 必须受已安装 Host 支持。角色 instructions 不是安全边界；实际 parent 权限与管理员策略仍可约束 subagent。`review_model` 选择 `/review` 的模型，与 `kiss_reviewer` 自定义角色不同。

<a id="registration"></a>
## 注册

每个 `[agents.<name>]` table 将稳定角色名映射到相对角色文件。相对 `config_file` 从该 config layer 解析。只复制角色文件不能证明 Host 已暴露该角色。已有同名注册必须 diff 并人工合并，绝不覆盖。

KISS 前缀避免与通用 `explorer`、`coder` 和 `review` 角色冲突；这些通用角色保持不变。

<a id="runtime-settings"></a>
## 运行设置

| 区域 | 代表性设置 | 指导 |
| --- | --- | --- |
| 模型 | `model`, `model_reasoning_effort`, `model_verbosity`, `review_model` | 使用 Host 支持值；不要增加静默 fallback。 |
| Multi-agent | `agents.enabled`, `agents.max_concurrent_threads_per_session` | 容量不等于 fan-out 目标。 |
| 上下文 | `model_context_window`, `model_auto_compact_token_limit` | 除非知道真实限制与需求，否则优先模型默认值。 |
| 权限 | `sandbox_mode`, `default_permissions`, `approval_policy` | 审核真实权限；不要混用不兼容的权限风格。 |
| Instructions | `project_doc_max_bytes`, `project_doc_fallback_filenames`, `project_root_markers` | 这些影响发现，不是产品行为。 |

`model_context_window` 不能增加模型真实容量；错误取值可能导致失败。自定义 `model_auto_compact_token_limit` 必须适配真实模型，并为输出、工具结果和后续 turns 留出空间。

`agents.max_concurrent_threads_per_session` 是容量上限，不是要求填满所有 slots。只有独立性、信息增益、风险隔离或延迟收益大于协调成本时才使用多个 Agent。

<a id="permissions-and-sandbox"></a>
## 权限与 Sandbox

- `read-only` 适合调查和独立审查。
- `workspace-write` 适合在预期 writable roots 内实现。
- `danger-full-access` 会实质扩大权限，验证本仓库不需要它。

静态验证作为普通原生脚本运行，不需要 Codex sandbox package；这不绕过 OS 或 Host 权限。文件系统访问、网络访问、approvals、外部 app 权限、认证与行为 instructions 彼此不同。

<a id="safe-customization"></a>
## 安全自定义

1. 找到影响当前工作负载的一个设置。
2. 确认已安装 Host 和所选模型支持它。
3. 只修改一个审核过的 layer，不替换无关内容。
4. Startup/discovery 改变后启动可信新会话。
5. 确认实际模型、权限、`/skills` 与已注册角色。
6. 只有真实任务改善时才保留修改。

以下命令只演示 launch 语法：

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

这些取值是示例，不是建议。项目不提供自动模型或权限 fallback。

<a id="official-references"></a>
## 官方参考

- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
