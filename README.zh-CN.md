![KISS My Agent 主视觉：复杂的 Agent 路径汇聚为一个清晰结果](assets/kiss-my-agent-hero.png)

<div class="readme-intro" align="center" markdown="1">

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

减少 Codex 的过度设计和过度防御。先做出能运行、能验证的科研 MVP，让错误尽早暴露，再根据真实结果快速迭代。

[English](https://aoiota.github.io/Kiss-My-Agent/) | [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)

[![许可证：MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml/badge.svg)](https://github.com/AoiOTA/Kiss-My-Agent/actions/workflows/validate.yml)
![版本：v0.2.2](https://img.shields.io/badge/release-v0.2.2-blue.svg)
![宿主：Codex 优先](https://img.shields.io/badge/host-Codex--first-blue.svg)

</div>

<a id="why-this-exists"></a>
## KISS My Agent 是什么

KISS My Agent 是一个面向科研和探索性工程的开源 Codex 插件。它给 Codex 一套简单的工作原则：围绕当前目标或假设，先做出能运行、能验证的最小版本，再根据真实结果决定继续、修改还是停止。

它以目标为导向，不以过程或工作量为导向：改了多少文件、调用多少 Agent、跑了多少检查、流程走到哪一步，都不能替代“当前问题是否真正得到回答”。

<a id="failure-patterns"></a>
<a id="overengineering-and-overdefense"></a>
## 它解决的两个核心问题

| 问题 | 是什么 | 常见结果 |
| --- | --- | --- |
| **过度设计** | 当前假设还没有验证，就先按成熟产品去建设，为未来可能性增加现在没人使用的抽象、配置、迁移或平台 | 一个实验变成大型系统，反馈变慢，改动范围和新 bug 一起增加 |
| **过度防御** | 不让错误自然暴露，而是叠加校验、重试、回退、异常捕获或门禁，甚至把失败包装成成功 | 真正原因被隐藏，错误结果看起来“正常”，下一轮迭代失去可靠起点 |

范围越做越大、没有修到实际生效的代码、把测试通过当成目标，或让多个 Agent 在同一件事上相互冲突，通常都是这两种倾向带来的后果。

<a id="why-agents-drift"></a>
## 为什么 Codex 容易产生这些问题

Codex 倾向产出“看起来完整、稳健、成功”的答案。用户又常只要求“全面”“稳健”或“生产级”，没有把当前假设、最小目标和停止条件说清；于是增加框架、校验、重试或回退既容易生成，也容易表现为工作有进展。同时，Codex 往往会尽量避免给出明显失败，错误就可能被捕获、绕开或包装成可用结果。成熟产品在有真实需求和风险时当然可能需要完整架构与防护，但科研早期过早加入这些东西，会延长反馈周期，也会遮住最有价值的信号：这次真实运行为什么成功或失败。

<a id="how-kiss-helps"></a>
<a id="before-and-after"></a>
## KISS 怎样推动科研闭环

`目标或假设 → 最小可运行、可验证版本 → 真实运行 → 暴露成功或失败 → 下一轮迭代或停止`

- 先把这一轮要回答的问题和最小成功条件说清，不让实现过程悄悄改写目标。
- 只做让假设能够运行和验证的必要部分；先得到科研 MVP，再决定是否值得产品化。
- 尽快在真实路径上运行。允许低成本、可恢复的试错，让错误带着原始原因尽早出现，而不是用回退或空结果遮住它。
- 根据真实结果行动：修复最先暴露的问题进入下一轮；假设已回答或目标已满足时就停止，不用更多流程和改动证明“做过很多工作”。

多 Agent 只是可选的加速手段：任务确实能独立拆分时才使用，共享文件、设备或输出仍由一个明确负责人操作。这里的“不怕犯错”只指低成本、可恢复的试错；认证、权限、不可逆操作和其他高风险安全边界不能删除或绕过。

<a id="is-it-for-you"></a>
## 它适合你吗？

| 比较适合 | 不是它要解决的场景 |
| --- | --- |
| 科研原型、算法验证、实验工具和其他需要尽快完成 MVP 的工作 | 已经有稳定需求、且确实需要完整兼容、迁移、审计或安全体系的成熟产品环节 |
| 方案还不确定，需要用真实运行结果快速探索 | 失败代价不可恢复，必须先完成严格安全论证的高风险操作 |
| 调试隐藏错误，或让 Codex 停止为假想未来提前产品化 | 需要确定性安全强制、形式化验证、通用编排平台或非 Codex Host 支持 |

KISS 不保证第一次就做对；它追求的是更快得到可信结果，再据此做对下一步。

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

在复杂项目中打开一个新的 Codex 会话。在已测试的 Codex CLI 0.152.1 baseline 上，先输入 `$`，再在 Skill picker 中选择 `kiss-my-agent-setup (kiss-my-agent)`。Picker 会插入一个结构化 Skill reference；继续补充 setup 请求并提交 prompt 后，才会调用该 Skill。如果直接粘贴文字，请使用下面完整限定的命令：

```text
$kiss-my-agent:kiss-my-agent-setup set up this project with the default team
```

Project setup 会写入持久项目规则和角色配置。通过 Codex 界面信任该项目，再打开一个新会话；只有这个可信的新会话才会加载项目规则和角色。之后像平常一样提任务：

```text
Find the cause of this failing parser test, make the smallest correct fix, and run the affected tests.
```

Setup check 是可选的。它只检查配置文件，不能证明 Agents 的真实行为：

```text
$kiss-my-agent:kiss-my-agent-setup check this project
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
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
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
