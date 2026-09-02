# 常见问题

[English](FAQ.md) | [简体中文](FAQ.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md)

<a id="what-is-kiss"></a>
## 这里的 KISS 是什么？

“Keep It Simple, Scientist”：为当前问题选择最小充分实现和证据，同时保留真实契约、必要安全与可见失败。

<a id="problem"></a>
## KISS My Agent 解决什么问题？

它用于减少科研工程中常见的 Agent 偏离：

- **过度设计：** 一个局部缺陷或单 consumer 需求扩张为不必要的抽象、配置、兼容层、工作流或持久系统。
- **过度防御：** 不确定性导致宽泛 catch-and-continue、过期 fallback、重复 gates，或超出真实边界的拒绝，从而隐藏真正失败。
- **流程表演：** 多 Agent 协调、handoff、检查或状态机制变成了产出，而不是服务用户要求的结果。
- **证据膨胀：** 把源码检查或测试通过，报告为它们没有测量的产品或科研目标已经得到证明。

必要的认证、授权、边界验证、清理，以及对已知可选故障的窄处理，不属于过度防御。KISS 要移除的是没有依据的机制，而不是真实安全。

<a id="why-agents-drift"></a>
## 编码 Agent 为什么以及什么时候容易偏离？

模型会从不完整 instructions 中推断意图。当用户要求“全面”“稳健”“生产就绪”或“面向未来”却没有明确验收；失败 owner 不清；runtime 与 evaluator 输出不一致；声明超过实验依据；或者多个 Agent 共享可变工作时，风险会上升。

对模型而言，复杂方案可能看起来更安全、更完整，即使它对当前 consumer 更差。KISS 通过划分人与 Agent 的 owner、要求机制服务当前 consumer、让失败可见、区分证据层级并定义停止边界，改善决策上下文。它能降低倾向，但无法保证所有模型和 prompt 表现一致。

<a id="fit"></a>
## 它适合我吗？

它主要面向使用 Codex 开发科研软件、实验、调试、基础设施或实质性工程任务，并希望获得有界自主能力而非固定 multi-agent pipeline 的用户。它不是通用编排器、权限绕过、策略引擎、形式化 evaluator，也不能保证模型永不犯错。详见首页的[适用性判断](../README.zh-CN.md#is-it-for-you)。

<a id="install"></a>
## 如何安装？

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

启动新会话，运行 `$kiss-my-agent-setup set up this project`；Host 提示时信任项目；再启动一个新会话并运行 `$kiss-my-agent-setup check this project`。

<a id="after-setup"></a>
## Setup 后该怎么用？

直接正常使用 Codex，不需要每次任务前先调用 KISS。项目 `AGENTS.md` 指导已经生效；主线程会判断是否需要任何角色。只有下面列出的特定接口才需要调用 Skill。

<a id="plugin-vs-skills"></a>
## 这是 Plugin 还是只有一个 Skill？

它是一个带版本的 Codex Plugin。Plugin 负责安装、分发与更新，目前打包两个 Skills：

- `$kiss-my-agent` 提供窄范围决策指导。
- `$kiss-my-agent-setup` 管理显式 project/global setup、检查、移除和现有角色配置。

配置后的项目拥有自己的 `.codex/config.toml`、standalone role TOML 和 managed AGENTS block。这些文件工具工作流仍可由 Skill 完成，不需要 MCP 服务或独立程序。

<a id="when-skill"></a>
## 何时调用 `$kiss-my-agent`？

用于一个重要且不显然的持久/共享机制、局部修复还是新系统、实验有效性、证据强度、runtime/evaluator 歧义或重大 scope 扩张决策。不要把它套在普通实现、测试、构建、Git、查询或格式化外面。`$kiss-my-agent-setup` 是另一个操作型 Skill。

<a id="configure"></a>
## 如何配置初始 Agents？

三个 seeds 默认继承 Host model 与 reasoning effort，可以直接使用。若要通过对话向导修改已有角色的模型、effort 或 sandbox 默认值，运行：

```text
$kiss-my-agent-setup configure agents for this project
$kiss-my-agent-setup configure global agents
```

也可以直接编辑 `.codex/agents/*.toml` 或 `$CODEX_HOME/agents/*.toml`。向导不会创建、删除或重命名角色，也不会硬编码会变化的 model catalog。

<a id="python"></a>
## 用户需要 Python 吗？

不需要。Plugin 安装、setup、check、remove、Agent 配置、正常使用和更新都不需要 Python、Node.js、Docker 或包管理器。Python 3.11+ 与固定版本 Markdown 包只供贡献者运行仓库测试或构建文档站点。

<a id="update"></a>
## 已安装用户如何更新？会自动更新吗？

用一条显式 marketplace refresh，然后确认解析到的版本：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

之后启动新会话。更新不会静默或自动进行，因为未经用户审核就更改 Agent 指导会损害可复现性。Plugin 更新也不会覆盖项目拥有的角色文件。

<a id="global"></a>
## 项目 setup 会配置所有项目吗？

不会。Project scope 只修改所选项目。全局 setup 必须明确运行 `$kiss-my-agent-setup set up globally`，并可能影响加载该 Codex home 的所有项目。项目和全局 check/configure/remove 命令始终分开。

<a id="roles"></a>
## 三个角色是固定的吗？

不是。它们是可编辑的 standalone seed files，不是封闭 catalog 或强制团队。`name` 字段是身份，文件名只是约定。用户可以有意地新增、编辑、重命名或删除角色。后续 setup 与 check 不会重建有意删除的 seed。

<a id="existing-files"></a>
## 已经有 config、AGENTS 或角色文件怎么办？

Setup 会保留无关内容和显式 `false`。遇到无效 TOML、不安全路径类型、重复 identity、ownership 冲突、project/global seed-name 冲突或适用的 `AGENTS.override.md` 时，会在写入前停止。显式 remove 仍可用于解除 cross-scope 冲突。

<a id="remove"></a>
## Remove 会删除什么？

只删除明确 scope 中 KISS-marked config assignments、delimited managed AGENTS block 和未修改的 bundled roles。已修改或 owner 不清的角色会保留。移除 setup 不会卸载 Plugin。

<a id="verification"></a>
## 怎样确认它有效？

应分开证据：仓库测试、setup `check`、可信新会话中的 `/skills` 发现、窄 role Smoke、升级测试和真实项目 Pilot 分别支持不同结论。详见[测试](TESTING.zh-CN.md)。静态 PASS 不能证明模型行为或用户科研目标。

<a id="windows-wsl"></a>
## WSL 是 Windows 测试路径吗？

不是。WSL 只产生 Linux 证据。原生 Windows 兼容性需要 Windows runner 或原生 PowerShell 检查。Agent 原生用户 setup 避免依赖某种 shell 语言，但真实 Host 行为仍需要对应平台证据。

<a id="other-hosts"></a>
## 其他 Agent Host 可以使用吗？

这些思想可以适配，但打包后的 Plugin、config、roles 和测试以 Codex 为首要 Host。其他 Host 未被本 release 验证。

<a id="pages"></a>
## 文档站点在哪里？

站点提供[英文版](https://aoiota.github.io/Kiss-My-Agent/)与[简体中文版](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)。部署成功与真实 HTTP/content 检查是不同证据。
