![KISS My Agent 主视觉：复杂的 Agent 路径汇聚为一个清晰结果](assets/kiss-my-agent-hero.png)

<div class="readme-intro" align="center" markdown="1">

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

KISS My Agent 帮助 Codex 把人的关键决策留给人，让改动规模与当前任务相称，让失败保持可见，让多 Agent 的职责明确、冲突可见，并让结论不超过证据。它面向的是“看起来合理”还不够的复杂科研工程任务。

[English](https://aoiota.github.io/Kiss-My-Agent/) | [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)

[![许可证：MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml/badge.svg)](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml)
![版本：v0.2.0](https://img.shields.io/badge/release-v0.2.0-blue.svg)
![宿主：Codex 优先](https://img.shields.io/badge/host-Codex--first-blue.svg)

</div>

<a id="why-this-exists"></a>
## KISS My Agent 是什么

KISS My Agent 是一个面向复杂科研工程项目、有版本管理的 Codex Plugin。它把一组协作规则、三个可编辑的初始角色和两个 Skills 打包在一起：一个 Skill 帮助处理少数重要而不显然的决策，另一个负责 setup、检查和配置。

它通过更清楚的工作边界来改善 Codex 的判断，不是凌驾于 Codex 之上的自主管理器或正确性检查器，也不会替人决定产品目标和科研结论。

<a id="failure-patterns"></a>
<a id="overengineering-and-overdefense"></a>
## 它解决的两个核心问题

| 核心问题 | 定义 | 常见表现 | 代价 |
| --- | --- | --- | --- |
| **过度设计** | 为当前没人需要的未来可能性增加框架、抽象、配置、迁移或流程，让改动超出当前目标 | 一个局部 bug 变成新平台；小任务也建立固定多 Agent 流程 | 代码、维护和审查成本上升，人的架构与范围决定被方案悄悄替代 |
| **过度防御** | 面对不确定性时，不先查事实和失败边界，就不断增加校验、重试、回退、审批、兼容层或门禁 | 真 bug 被空结果或过期“成功”隐藏；没有确认实际运行版本就反复测试；超出真实权限边界拒绝工作 | 原因更难查清，结论更不可信，维护成本继续增加 |

这两种倾向还会表现为：未经用户同意就扩大任务或改变验收标准；修改显眼的文件却没有修复实际运行的代码；把测试通过当成最终目标；或者让多个 Agent 重复工作、覆盖同一共享内容。它们不是六种互不相关的产品功能，而是同一类失控的不同后果。

必要安全不是过度防御。认证、授权、最小权限、真实边界上的验证、安全清理，以及对已知可选服务故障的明确处理，都应该保留。没有哪类任务或关键词必然触发这些问题，KISS 也不是安全绕过工具。

<a id="why-agents-drift"></a>
## 为什么 Codex 容易产生这些问题

用户的要求常常只写“全面”“稳健”或“生产级”，却没有同时说清目标、验收标准、非目标和停止条件。Codex 只能从不完整信息中推断，而更复杂的方案在文字上往往显得更完整、更安全；它也无法凭空知道哪些风险对这个项目真正重要。

科研工程还常有多个源码版本、构建结果、配置、数据和评分方法，多个 Agent 又各自看到不同信息。这样一来，修错对象、重复工作、共享内容冲突，以及拿局部检查代替真实结果都会更容易发生。

<a id="how-kiss-helps"></a>
<a id="before-and-after"></a>
## KISS 怎样减轻这些问题

- **关键决定由人保留：** 人决定目标、架构、怎样才算完成、哪些事不做以及何时停止；Codex 在这些边界内执行，需要明显扩大任务时先询问。
- **先找到真实需求：** 先查事实，找到真正受影响的人或代码，不因为“未来也许需要”就建立新系统。
- **优先最小正确改动：** 在真正负责问题的地方修复，并验证受影响的部分；没有必要时不扩展成通用框架，当前实现已经满足目标时也可以不修改。
- **让失败和证据保持真实：** 内部错误保留原始原因；只有明确的可选故障才降级并说明原因；测试通过只说明测试通过，不自动等于产品或科研目标已经实现。
- **按需要分工：** 只有分工确实有收益时才使用多个 Agent；同一共享文件、设备或输出始终由一个明确负责人操作，主对话负责汇总和决定。

<a id="is-it-for-you"></a>
## 它适合你吗？

| 比较适合 | 不适合 |
| --- | --- |
| 长期或复杂的科研工程项目，需要持续约束任务范围、失败处理和证据结论 | 简单、隔离、验收明确的一次性任务；普通 Codex 对话已经足够 |
| 你经常要删除 Agent 提出的多余框架、宽泛回退或流程机制 | 你希望 Agent 替你决定产品目标、架构、风险容忍度或验收标准 |
| 多 Agent、实验、共享文件或设备确实有帮助，但需要明确分工 | 你需要确定性安全强制、形式化验证、通用编排平台或非 Codex Host 支持 |

KISS 改善 Codex 工作时的规则和角色边界，不会让系统自动正确，也不会绕过认证、权限、管理员策略、项目 trust 或必要安全控制。

<a id="quick-start"></a>
## 快速开始

已在完成认证且支持 Plugin 的 Codex CLI 0.152.1 上测试。还需要 `git`、GitHub 网络访问，以及账号能够使用 `gpt-5.6-sol`；更早 Codex 版本未验证。普通用户不需要 Python、Node.js、Docker 或其他语言运行时。

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

此时只是安装了 Plugin；新的 Codex 会话可以发现它提供的两个 Skills，但项目规则和角色还没有配置。

在复杂项目中打开一个新的 Codex 会话，然后运行：

```text
$kiss-my-agent-setup set up this project with the default team
```

Project setup 会写入持久项目规则和角色配置。通过 Codex 界面信任该项目，再打开一个新会话；只有这个可信的新会话才会加载项目规则和角色。之后像平常一样提任务：

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

Plugin 没有后台服务；真正加载配置和启动 Agents 的是 Codex Host。

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
