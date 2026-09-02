# 配置

[English](CONFIGURATION.md) | [简体中文](CONFIGURATION.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="default-configuration"></a>
## 默认配置

仓库跟踪的项目 config 只有两个公开开关：

```toml
[features]
multi_agent = true

[agents]
enabled = true
```

它们为可信项目启用 Host multi-agent 能力和自定义 Agent 发现。它们不选择角色、模型、思考强度、权限、上下文、并发、trust、provider、认证或 telemetry。用户层、管理员层或单次启动中的显式 `false` 仍是权威值。

<a id="zero-configuration"></a>
## 默认角色无需配置模型

首次 setup 会安装三个可编辑 seeds：

| 角色 | 职责 | Seed sandbox 默认值 |
| --- | --- | --- |
| `kiss_explorer` | 只读调查 | `read-only` |
| `kiss_coder` | 有界实现与状态修改 | `workspace-write` |
| `kiss_reviewer` | 独立只读审查 | `read-only` |

Seeds 省略 `model` 和 `model_reasoning_effort`，因此会继承实际 Host 设置。这是推荐的跨版本默认方式：用户无需先理解模型 ID 或维护特定版本 preset，即可直接开始使用。

<a id="three-owners"></a>
## 三个 Owner

| Owner | 表面 | 职责 |
| --- | --- | --- |
| 启用 | `.codex/config.toml` | 只拥有两个公开开关。 |
| 发现 | `.codex/agents/*.toml` | Host 发现的 standalone role definitions。 |
| 委派 | `AGENTS.md` | 判断 delegation 是否值得的动态指导。 |

三个层次不能互相替代。角色文件不会启用 multi-agent tools，启用开关不会创建角色 catalog，instructions 也不会授予 runtime 权限。

<a id="configuration-layers"></a>
## 配置层

| Scope | 典型位置 | 用途 |
| --- | --- | --- |
| 用户/全局 | `$CODEX_HOME/config.toml` | 跨项目个人默认值。 |
| 可信项目 | `<repo>/.codex/config.toml` | 审核过的项目级设置。 |
| 全局角色 | `$CODEX_HOME/agents/<file>.toml` | 跨项目个人 standalone roles。 |
| 项目角色 | `<repo>/.codex/agents/<file>.toml` | 项目专有 standalone roles。 |
| 单次启动 | CLI `--config key=value` | 不编辑文件的临时 override。 |

项目与全局 setup 始终分开。修改 config、instructions、Skills、Plugins 或角色 TOML 后启动新会话；已有会话不保证热加载。

<a id="configure-wizard"></a>
## 对话式 Agent 配置向导

没有真实工作负载需要不同模型、effort 或 sandbox 时，应保留继承默认值。要在一个明确 scope 中配置现有角色，运行：

```text
$kiss-my-agent-setup configure agents for this project
$kiss-my-agent-setup configure global agents
```

向导会列出当前 role catalog，让用户选择一个或多个角色，并为 `model`、`model_reasoning_effort` 与 `sandbox_mode` 提供 `keep`、`inherit` 或显式值。写入前会展示准确 diff；设置 `danger-full-access` 时必须单独确认。

向导不会创建、删除、重命名或恢复角色。模型可用性取决于 Host 与账户，因此向导不附带硬编码 model catalog。请使用当前 Host 展示的准确 ID，或者保留继承。

若已有角色使用 `default_permissions` 或 `sandbox_workspace_write` table，向导不会再写入冲突的 `sandbox_mode`。这类相关多字段修改应在核对当前 Host schema 后手工完成。

<a id="manual-role-editing"></a>
## 手工编辑角色

也可以直接在已有 standalone role 文件中完成相同修改：

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

必需字段为 `name`、`description` 与 `developer_instructions`。`name` 字段才是身份；让文件名与它一致是最简单的约定。有效 catalog 中的名称必须唯一。

<a id="precedence"></a>
## 模型与权限优先级

自定义 Agent 文件设置 `model` 或 `model_reasoning_effort` 时，该文件会作为角色 override 应用。字段省略时，Codex 依次从显式 spawn 值、对应的 `[agents]` 默认值和 parent 中解析。角色文件只 override `model` 时，会保留此前已经解析的 effort，不会根据该角色模型自动重新计算 effort。

其他省略的 session 设置继承 parent。Parent turn 的实时权限选择和管理员要求仍可能限制或覆盖角色文件中的 `sandbox_mode`；角色文件不是权限授权。应在新会话中验证实际行为。

<a id="setup-scopes"></a>
## Setup Scopes

Plugin-owned Skill 使用 Agent 原生文件操作，不需要 Python、Node.js 或包管理器：

```text
$kiss-my-agent-setup set up this project
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup set up globally
$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

项目 scope 管理 `<target>/.codex/config.toml`、`<target>/.codex/agents/` 和 `<target>/AGENTS.md` 中的一个 managed block。全局 scope 管理 `$CODEX_HOME` 下的对应文件。Skill 始终留在已安装 Plugin 中。

“This project” 表示 Host 当前唯一的 project 或 active workspace root，而不是 shell 恰好所在的某个子目录。Skill 会显示解析后的绝对目标；存在多个 workspace roots、目标不唯一时先让用户选择。

<a id="conflicts-and-ownership"></a>
## 冲突与 Ownership

- 保留无关 config、角色、instructions、comments 和显式 `false`。
- TOML 损坏、路径类型不安全、identity 重复、文件名/identity 冲突或存在适用的 `AGENTS.override.md` 时，在写入前停止。
- project/global seed 名称重复会阻止 setup 和 check，但不会阻止从一个明确 scope 执行 remove，因为 remove 是解除该冲突的出口。
- 已有且 identity 正确的角色归用户所有并会被保留。后续 setup 不会恢复用户有意删除的 seed。
- Remove 只删除带 marker 的 config assignments、managed AGENTS block，以及字节仍与当前 seeds 一致的 bundled roles。

<a id="disable"></a>
## 单次启动禁用

不编辑文件并关闭两个公开 multi-agent 表面：

```bash
codex --config features.multi_agent=false --config agents.enabled=false
```

如需持久移除 KISS 项目指导与 seeds，应使用明确的 project remove 命令。只禁用 multi-agent 开关不会删除已有 AGENTS block。

<a id="official-references"></a>
## 官方参考

- [Subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
