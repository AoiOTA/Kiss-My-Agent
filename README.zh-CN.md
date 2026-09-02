![KISS My Agent 主视觉：复杂的 Agent 路径汇聚为一个清晰结果](assets/kiss-my-agent-hero.png)

<div class="readme-intro" align="center" markdown="1">

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

KISS My Agent 帮助 Codex 完成复杂科研工程任务，避免把每个不确定点都变成更多系统。你决定目标和怎样才算完成；Agents 负责让改动保持精简、失败保持可见、结论不超过证据。

[English](https://aoiota.github.io/Kiss-My-Agent/) | [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)

[![许可证：MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml/badge.svg)](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml)
![版本：v0.2.0](https://img.shields.io/badge/release-v0.2.0-blue.svg)
![宿主：Codex 优先](https://img.shields.io/badge/host-Codex--first-blue.svg)

</div>

<a id="why-this-exists"></a>
## 它针对的两个问题

**1. 一个小 bug 变成一套新平台。**

之前：一个 parser 出错，Agent 却提出 framework、registry、新配置格式、迁移计划和大型测试系统。之后：KISS 要求只修 parser，补最小的有效回归检查，然后停止。

**2. 真实失败被隐藏成成功。**

之前：内部错误被捕获后，以空结果或过期结果伪装成“成功”。之后：KISS 要求清楚报告预期的可选服务故障，让真正的 bug 带着原因失败。

<a id="is-it-for-you"></a>
## 它适合你吗？

- **简单、明确、一次性任务：** 不需要 project setup，直接使用普通 Codex 对话。
- **复杂科研或工程项目：** 当多个 Agents、重要决策、共享文件、实验或强证据结论需要明确分工时使用 KISS。

KISS 是指导，不是权限绕过工具，也不能保证模型永远不犯错。

<a id="quick-start"></a>
## 快速开始

已在完成认证且支持 Plugin 的 Codex CLI 0.152.1 上测试。还需要 `git`、GitHub 网络访问，以及账号能够使用 `gpt-5.6-sol`；更早 Codex 版本未验证。

确认当前 Codex build 支持 Plugins：

```bash
codex --version
codex plugin --help
```

安装 Plugin：

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

在复杂项目中打开一个新的 Codex 会话，然后运行：

```text
$kiss-my-agent-setup set up this project with the default team
```

再打开一个新会话，然后像平常一样提任务：

```text
Find the cause of this failing parser test, make the smallest correct fix, and run the affected tests.
```

Setup check 是可选的。它只检查配置文件，不能证明 Agents 的真实行为：

```text
$kiss-my-agent-setup check this project
```

默认 setup 管理项目中的三个位置：

- `.codex/config.toml`：Master 默认值和多 Agent 开关
- `.codex/agents/`：可编辑的员工角色文件
- `AGENTS.md`：带标记的 KISS instructions 区块

它会保留已有用户配置，默认不需要选择。只有目标位置或冲突不明确时才会询问。如果 setup 停止，请按报告中的原因和准确路径处理，不要覆盖文件；详见[安装](docs/INSTALLATION.zh-CN.md)。

Plugin 没有后台服务。它安装 instructions 和角色配置；真正启动 Agents 的是 Codex Host。

<a id="how-to-use"></a>
## 默认公司班底

**Master** 就是你现在正在对话的主 Codex Agent，也就是主会话，不是另一个员工角色。

| 成员 | 职责 | 默认配置 |
| --- | --- | --- |
| 你 / Owner | 决定目标、架构、验收标准、非目标和停止点 | 人来决策 |
| Master | 规划、分配工作、解决冲突、判断证据并汇总 | `gpt-5.6-sol` / `max` |
| `kiss_explorer` | 调查并报告事实，不编辑文件 | `gpt-5.6-sol` / `high` |
| `kiss_coder` | 实现分配的改动并运行相关检查 | `gpt-5.6-sol` / `high` |
| `kiss_reviewer` | 独立检查结果，不编辑文件 | `gpt-5.6-sol` / `xhigh` |

这些是可编辑的默认值，不是锁定。Master 通常直接分配任务，可以启动同一角色的多个实例，每个共享事项由一个 Agent 负责，大型独立子系统可以临时设一个 lead。

这些 instructions 还要求：如果无法委派，Master 应报告人员配置问题，而不是静默代替员工执行。然后由你选择修复团队配置，或者明确让本次任务改为普通单对话。

公司类比只用于解释职责，不是固定流程或游戏系统。

<a id="configure-agents"></a>
## 只有想修改默认值时才看这里

Master 在所选配置文件中修改：

- 项目：`<project>/.codex/config.toml`
- 全局：`$CODEX_HOME/config.toml`；未设置 `CODEX_HOME` 时是 `~/.codex/config.toml`

如果 bundled default 不受支持，请使用 Host 模型选择器显示的值临时启动一次：

```bash
codex --model YOUR_SUPPORTED_MODEL --config 'model_reasoning_effort="YOUR_SUPPORTED_EFFORT"'
```

Codex 会报告不支持的设置；KISS 不会静默选择 fallback。临时启动后，编辑上面的 Master config，再用下面的 role wizard 修改员工角色。

通过 Codex 配置已有员工角色：

```text
$kiss-my-agent-setup configure agents for this project
```

Role wizard 只修改已有角色的 model、reasoning effort 和 permission mode，不修改 Master。全局角色、优先级、权限和恢复细节见[配置](docs/CONFIGURATION.zh-CN.md)。

<a id="updates"></a>
## 立即更新

第一条命令立即更新，第二条只核验安装结果：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

应看到 `kiss-my-agent@kiss-my-agent`、状态 `installed, enabled`，版本与本 README 顶部的当前 release badge 一致。更新后启动新会话。v0.1-managed 项目还要再运行一次 project setup，才能更新未修改的 KISS 文件。

KISS My Agent 自身没有 updater。Codex 可能在启动时刷新未固定版本的 Git marketplace。固定版本、回退和 v0.1 迁移细节见[安装](docs/INSTALLATION.zh-CN.md#update)。

<a id="limitations"></a>
## 局限

- 已在 Codex CLI 0.152.1 上测试；更早版本和其他 Host 未验证。
- Instructions 可以改善工作上下文，但不能保证模型服从、结果正确或通过验收。
- 成功委派或测试通过，不能证明用户的产品目标或科研目标已经实现。
- 当前 release 没有 MCP 服务、独立 UI、遥测、评测平台或 LTS 承诺。
- 它不能替代认证、权限、管理员策略、项目安全规则或专业领域判断。

<a id="documentation"></a>
## 详细文档

- [Installation and recovery](docs/INSTALLATION.md) / [安装与恢复](docs/INSTALLATION.zh-CN.md)
- [Configuration](docs/CONFIGURATION.md) / [配置](docs/CONFIGURATION.zh-CN.md)
- [Testing and evidence](docs/TESTING.md) / [测试与证据](docs/TESTING.zh-CN.md)
- [FAQ](docs/FAQ.md) / [常见问题](docs/FAQ.zh-CN.md)
- [Contributing](CONTRIBUTING.md) / [贡献](CONTRIBUTING.zh-CN.md)
- [Security](SECURITY.md) / [安全](SECURITY.zh-CN.md)

完整文档站点提供[英文版](https://aoiota.github.io/Kiss-My-Agent/)与[简体中文版](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)。

<a id="license"></a>
## License

[MIT](LICENSE)
