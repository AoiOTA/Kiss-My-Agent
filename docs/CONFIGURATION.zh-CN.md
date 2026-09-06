# 配置

[English](CONFIGURATION.md) | [简体中文](CONFIGURATION.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="default-configuration"></a>
## 默认配置

仓库跟踪的项目 config 只包含两个公开开关：

```toml
[features]
multi_agent = true

[agents]
enabled = true
```

当这个可信 project layer 生效且没有更高优先级层覆盖时，两个开关会启用 Host multi-agent 能力和自定义 Agent 发现。它们不选择 Master model 或 effort、权限、上下文、并发、trust、provider、认证或 telemetry。KISS 把 Master model 与 effort 留给 Host、对话和其他 Codex 配置层。

每个缺失开关都会独立获得带 marker 的 `true` 默认值；setup 会保留所有 marked 或 unmarked 的已有值，其中包括显式 `false`。为保持兼容，只有两个顶层旧 Master keys 都准确出现一次、值分别为 `gpt-5.6-sol` 与 `max`，且每行都有准确的 `# KISS My Agent managed` marker 时，setup 才成对删除它们。未标记、已修改、缺少 companion 或用户自选 custom pair 都继续归用户所有；duplicate assignment、无效 TOML 或 ownership 歧义属于 conflict，不是迁移候选。Static check 不再用 Master model 或 effort 判断 setup 是否 structurally valid；KISS 也不会为选择 Master 而修改用户的全局配置。

<a id="zero-configuration"></a>
## 默认角色没有 KISS model pin，并设置思考强度

首次 setup 会安装三个可编辑 seeds：

| 角色 | 职责 | 模型 | 思考强度 | Seed sandbox 默认值 |
| --- | --- | --- | --- | --- |
| `kiss_explorer` | 只读调查 | 无 KISS 角色级 model pin | `medium` | `read-only` |
| `kiss_coder` | 有界实现与状态修改 | 无 KISS 角色级 model pin | `medium` | `workspace-write` |
| `kiss_reviewer` | 独立只读审查 | 无 KISS 角色级 model pin | `medium` | `read-only` |

Current seeds 省略 `model`，只显式设置上表中的 effort。它们是可编辑的 fresh-setup 默认值。Fresh setup 只创建缺失 starter；任何已经存在的角色都归用户所有，setup 或 Plugin update 永不覆盖、迁移或判定其版本。Setup 已存在后，缺失 starter 会保持 intentionally absent。Plugin cache seeds 只是 package resources，不会自动成为 Host 可发现角色。

<a id="three-owners"></a>
## 三个 Owner

| Owner | 表面 | 职责 |
| --- | --- | --- |
| 启用 | `.codex/config.toml` | 两个公开开关；Master model 与 effort 由 Host/对话选择。 |
| 发现 | `.codex/agents/*.toml` | Host 发现的 standalone role definitions。 |
| 委派 | `AGENTS.md` | 判断 delegation 是否值得，并让 master 专注协调与决策的动态指导。 |

三个层次不能互相替代。角色文件不会启用 multi-agent tools，启用开关不会创建角色 catalog，instructions 也不会授予 runtime 权限。Catalog 保持开放，master 只从实际存在的角色中动态选择；KISS My Agent 不要求固定团队人数或 workflow。每种 explorer、coder 或 reviewer 角色都可有多个实例。组织默认扁平，由 master 直接 fan-out 到当前角色。只有独立子系统需要大量并行、且直接汇总会污染 master context 时，master 才可临时把一个现有 Agent 指定为有界的部门主管。主管可在自身 scope 内调度同类或相关角色实例并向 master 汇总，但其 workers 不再继续委派。Assignment 随任务结束而消失，因此最多一层中间管理，不允许深层嵌套、固定部门、新 seed、固定人数或 organization schema。每个共享文件或资源仍只有一个 writer/operator。可委派的批量探索、实现、验证与审查交给子代理，master 专注调度、架构与验收决策、冲突解决、证据解释和最终汇总。

简单任务不应仅为组建团队而执行 setup 或触发 KISS My Agent Skill；直接用用户选择的模型与 effort 进行普通单对话。复杂科研工程项目可显式 setup executive-only master workflow。若已配置的 workflow 中 delegation 被禁用、不可用或没有合适角色，master 不会静默接手 delegated work，而是报告 staffing issue。随后由用户选择修复或启用合适角色，或者明确把本次任务切换为普通单对话；只有后者的明确选择才授权 master 直接执行。

<a id="configuration-layers"></a>
## 配置层

| Scope | 典型位置 | 用途 |
| --- | --- | --- |
| 用户/全局 | `$CODEX_HOME/config.toml` | 跨项目个人默认值。 |
| 可信项目 | `<repo>/.codex/config.toml` | 审核过的项目级设置。 |
| 全局角色 | `$CODEX_HOME/agents/<file>.toml` | 跨项目个人 standalone roles。 |
| 项目角色 | `<repo>/.codex/agents/<file>.toml` | 项目专有 standalone roles。 |
| 单次启动 | CLI `--config key=value` | 不编辑文件的临时 override。 |

Codex 配置优先级从高到低为：CLI flags 与 `--config` overrides；可信项目中的 `.codex/config.toml`（越接近当前工作目录优先级越高）；`--profile` 选择的 profile；用户 config；系统 config；内置 defaults。因此，project 中的 `true` 可以覆盖更低层的 user `false`，CLI `false` 也可以覆盖 project。管理员 requirements 还可能单独约束最终设置。

项目与全局 setup 始终分开。对于 role definitions，Host 应用 project-over-global precedence 并负责更广泛的 catalog warnings；KISS setup 不会拒绝或协调这两个 scope 中的 roles。修改 config、instructions、Skills、Plugins 或角色 TOML 后启动新会话；已有会话不保证热加载。

<a id="configure-wizard"></a>
## 对话式 Agent 配置向导

没有真实工作负载需要不同模型、effort 或 sandbox 时，应保留继承默认值。要在一个明确 scope 中配置现有角色，运行：

```text
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
$kiss-my-agent:kiss-my-agent-setup configure global agents
```

要移除三个已有 KISS roles 中的 KISS 角色级 model pin 并设置 `medium` effort，请使用下面准确的项目限定 prompt：

```text
$kiss-my-agent:kiss-my-agent-setup configure agents in this project: for kiss_explorer, kiss_coder, and kiss_reviewer, set model to inherit and model_reasoning_effort to medium
```

请求已经点名一个或多个角色时，向导只解析这些 targets；没有点名时，先只列出 direct role paths 而不解析内容，等待用户选择一个或多个角色后，再只解析选中的文件。向导为 `model`、`model_reasoning_effort` 与 `sandbox_mode` 提供 `keep`、`inherit` 或显式值，写入前展示准确 diff；设置 `danger-full-access` 时必须单独确认。无效的未选角色不会阻塞操作，其 catalog warnings 由 Host 负责。

Project scope 解析到 `<unique Host project or active workspace root>/.codex/agents`；存在多个 roots 或没有唯一 root 时，向导会先要求选择绝对 project target，选择前不写入。Global scope 优先使用非空 `CODEX_HOME`，否则使用当前用户的 `~/.codex`，并定位到其 `agents/` 目录。向导会在检查前展示解析后的绝对 role-directory path。

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

Codex 会先为每个 model 或 effort 字段依次解析显式 spawn 值、`agents.default_subagent_model` 或 `agents.default_subagent_reasoning_effort`，最后是 parent。若显式 spawn 或 `[agents]` 默认值选择了模型，但这两个来源都没有指定 effort，Codex 会使用该模型的默认 effort。随后，自定义 Agent role 文件中显式的 `model` 或 `model_reasoning_effort` 成为最终 role override。Role 文件只 override `model` 时，会保留此前已解析的 effort，不会根据该角色模型自动重新计算。

其他省略的 session 设置继承 parent。子代理继承 parent 当前的 sandbox policy；Codex 在 spawn 时还会重新应用 parent turn 的实时 sandbox 与 approval overrides，即使 role 文件写了不同默认值。管理员要求还可进一步限制权限；角色文件不是权限授权。应在新会话中验证实际行为。

KISS setup 与 static check 无法证明 Host 各配置层最终生效的 model 或 effort。Master 应在 Host 或对话中选择；对于复杂 KISS 任务，如果账号与 Host 提供该选项，可以从 **GPT-6 Astra / High** 开始。这是建议，不是 bundled default 或强制要求。若另行配置的 Master 值导致无法启动，可用最高优先级 CLI override 启动一次恢复会话：

```bash
codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'
```

随后修改持久 config 或 role TOML，并再次启动新会话。KISS My Agent 不会静默替换 fallback model 或 effort。

<a id="setup-scopes"></a>
## Setup Scopes

Plugin-owned Skill 使用 Agent 原生文件操作，不需要 Python、Node.js 或包管理器：

```text
$kiss-my-agent:kiss-my-agent-setup set up this project
$kiss-my-agent:kiss-my-agent-setup check this project
$kiss-my-agent:kiss-my-agent-setup remove from this project

$kiss-my-agent:kiss-my-agent-setup set up globally
$kiss-my-agent:kiss-my-agent-setup check global setup
$kiss-my-agent:kiss-my-agent-setup remove global setup
```

项目 scope 管理 `<target>/.codex/config.toml`、准确的 `<target>/.codex/agents/{kiss_explorer,kiss_coder,kiss_reviewer}.toml` targets，以及 `<target>/AGENTS.md` 中的一个 managed block。全局 scope 管理 `$CODEX_HOME` 下的对应 paths。Skill 始终留在已安装 Plugin 中。

“This project” 表示 Host 当前唯一的 project 或 active workspace root，而不是 shell 恰好所在的某个子目录。Skill 会显示解析后的绝对目标；存在多个 workspace roots、目标不唯一时先让用户选择。

<a id="conflicts-and-ownership"></a>
## 冲突与 Ownership

- 保留无关 config、角色、instructions、comments 和显式 `false`。
- Setup、check 与 remove 只检查所选 scope 中由 KISS 管理的 config、AGENTS paths 和三个准确 bundled role targets；不解析其他 role files 或 opposite scope 中的 roles。
- 所选 managed path 的类型不安全、所选 config 或准确 bundled target 的 TOML 无效、准确 bundled target 缺少 identity fields 或 `name` 与文件名不同、managed ownership 不明确，或存在适用的 `AGENTS.override.md` 时，在写入前停止。
- 其他文件中的 duplicate identities 与 project/global duplicate role names 不会阻塞 KISS setup 或 check。Catalog warnings 和 project-over-global precedence 由 Host 负责；KISS 不会协调这些冲突。
- 每个已有角色都归用户所有并逐字节保留。Setup 永不拿它与历史 seeds 比较、判定版本或迁移它。后续 setup 不会恢复用户有意删除的 starter。
- 显式 remove 会删除当前带 marker 的 switches 与任何准确的旧 marked Master pair、managed AGENTS block，以及字节完全匹配 current、known v0.2.5 或 known v0.1 seed 的 bundled roles；其他角色文件仍归用户所有。

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
- [Basic configuration and precedence](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [GPT-6 Astra](https://openai.com/index/gpt-6-astra/)
