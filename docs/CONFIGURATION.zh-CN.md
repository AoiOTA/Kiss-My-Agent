# 配置

[English](CONFIGURATION.md) | [简体中文](CONFIGURATION.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="repository-default"></a>
## 仓库默认配置

仓库跟踪的 `.codex/config.toml` 只有两个公开开关：

```toml
[features]
multi_agent = true

[agents]
enabled = true
```

它们为该可信项目启用 Host multi-agent 能力和自定义 Agent。它们不枚举角色，也不设置模型、reasoning effort、权限模式、上下文上限、并发上限、信任策略、provider、认证或 telemetry。

有效用户层或管理员层中的显式 `false`，或者单次启动 override，仍是权威取值。Setup 不得静默重新打开有意禁用的功能。

<a id="three-layers"></a>
## 三层职责

| Owner | 表面 | 职责 |
| --- | --- | --- |
| 启用 | `.codex/config.toml` | 只有两个公开开关。 |
| 发现 | `.codex/agents/*.toml` | Host 自动发现 standalone role definitions。 |
| 调度 | `AGENTS.md` | 主线程是否以及如何委派的动态指导。 |

这三层不能互相替代。Role 文件不会打开 multi-agent 支持；开关不会创建角色 catalog；AGENTS 指导不会授予 runtime 权限。

<a id="configuration-layers"></a>
## 配置层

| Scope | 典型位置 | 用途 |
| --- | --- | --- |
| 用户/全局 | `$CODEX_HOME/config.toml` | 跨项目个人默认值。 |
| 可信项目 | `<repo>/.codex/config.toml` | 审核过的项目级开关与设置。 |
| Profile | Host 支持的 Profile config | 可切换的个人模式。 |
| 单次启动 | CLI `--config key=value` | 不编辑文件的临时 override。 |
| 全局角色 | `$CODEX_HOME/agents/<file>.toml` | 跨项目 standalone role definition。 |
| 项目角色 | `<repo>/.codex/agents/<file>.toml` | 项目 standalone role definition。 |

项目与全局 scope 始终显式选择。Provider、认证、telemetry 与管理员策略可能增加限制。修改 config、instructions、Skills、plugins 或角色文件后启动新会话；旧会话不保证热加载。

<a id="standalone-roles"></a>
## Standalone Roles

每个 standalone role TOML 通过必需的 `name` 字段拥有身份。文件名是可读性约定，不是真值来源。只有 Host 接受且 operator 理解时，文件名与 `name` 不同才是有效的；重复 `name` 属于必须解决而不能掩盖的冲突。

KISS My Agent 提供三个 seed 文件：

| Seed name | 职责 | 默认权限意图 |
| --- | --- | --- |
| `kiss_explorer` | 只读调查 | 只读 |
| `kiss_coder` | 实现与状态变更执行 | 只在分配范围内可写 |
| `kiss_reviewer` | 独立只读审查 | 只读 |

Seeds 不是封闭 catalog。应有意地增加、重命名、编辑或删除 standalone 文件。首次 setup 后，后续 setup 会保留当前 catalog；普通会话、setup 与 `check` 都不会恢复已移除角色。

Model 与 reasoning effort 在省略时继承实际 Host 设置。`model`、`model_reasoning_effort` 与 `sandbox_mode` 等可选角色字段可修改为 Host 支持且有意授权的值。KISS My Agent 有意不固定角色模型、effort、context、concurrency 或默认 subagent model。

<a id="disable"></a>
## 不编辑文件的禁用方式

为单次启动关闭两个公开表面：

```bash
codex --config features.multi_agent=false --config agents.enabled=false
```

若要保留能力但禁用自定义 Agent，只设置 `agents.enabled=false`。用户或管理员也可持久设置显式 `false`；项目 setup 必须报告该实际禁用状态，不能把文件存在误当成真实启用。

<a id="setup-scopes"></a>
## Setup Scopes

Plugin 安装后，先启动新会话让 setup Skill 被发现，再使用一个明确预期的 scope：

```text
$kiss-my-agent-setup set up this project
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup set up globally
$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

项目 scope 管理 `<target>/.codex/config.toml`、`<target>/.codex/agents/` 和 `<target>/AGENTS.md` 中的 KISS managed block。全局 scope 管理 `$CODEX_HOME` 下的对应文件。Skill 本身归 plugin 所有，不复制到任何目标。

底层源码工具为 `skills/kiss-my-agent-setup/scripts/setup.py {setup,check,remove} --scope project|global`。项目 scope 可使用 `--target`；测试与显式隔离使用可提供 `--codex-home`。多数用户应使用 Skill 接口，以自然语言明确 scope。

<a id="conflicts-and-precedence"></a>
## 冲突与优先级

- Setup 保留无关 config、角色文件和 AGENTS 内容；不会为方便而替换整个文件。
- 所选 scope 存在 `AGENTS.override.md` 时，setup 停止。它不会写入 override、写一个被隐藏的低优先级 base，也不会报告成功。
- 具有预期 `name` 的已有 seed 文件会被保留，包括用户编辑。文件名与其他 identity 冲突、重复 identity 或 project/global seed-name 冲突会使操作停止。
- 已有 `false` 会被保留并报告为 `disabled`，不会被静默替换为 `true`。
- Setup 不建立项目 trust、不启动 Codex，也不证明真实发现。
- 项目 setup 绝不会静默变成全局 setup。全局 setup 必须使用显式 global 命令。
- Remove 只作用于所选 scope 和 KISS managed content。保留用户编辑或 owner 不清的内容，并报告冲突。

<a id="safe-customization"></a>
## 安全自定义

1. 找到影响当前工作负载的一个实际设置或角色。
2. 确认已安装 Host 与所选模型支持它。
3. 只修改 owning layer，不替换无关内容。
4. 编辑或新增 standalone role 时保持 `name` 唯一。
5. Startup 或 discovery 改变后启动可信新会话。
6. 运行 setup `check`；只有需要真实证据时才继续使用 `/skills` 与窄角色 Smoke。

项目不提供自动模型、权限或兼容性 fallback。

<a id="official-references"></a>
## 官方参考

- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
