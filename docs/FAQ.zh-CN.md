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

Git-backed marketplace 要求 `PATH` 中有可用的 `git` executable，并且网络可以访问 GitHub。简单一次性任务安装后直接使用普通单对话。复杂项目若需要持久 executive workflow，再启动新会话，运行 `$kiss-my-agent-setup set up this project`；Host 提示时信任项目；随后另开新会话并运行 `$kiss-my-agent-setup check this project`。

<a id="after-setup"></a>
## Setup 后该怎么用？

直接正常使用 Codex，不需要每次任务前先调用 KISS。项目 `AGENTS.md` 指导已经生效；Master 负责调度、决策和汇总，被委派的角色分别拥有调查、实现与审查。默认由 Master 直接 fan-out，同一角色可有多个实例，每个共享资源保持一个 writer/operator。合格的大型独立子系统可有一个临时 department lead，但不建立更深或永久层级。

如果 delegation 被禁用、不可用或没有合适角色，Master 会报告 staffing issue，让你选择修复 staffing 或明确把本任务切换为普通单对话。只有后者才授权 Master 直接执行。

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
## 如何配置 Master 或初始 Agents？

Bundled defaults 使用 `gpt-5.6-sol`：Master 为 `max`，`kiss_explorer` 与 `kiss_coder` 为 `high`，`kiss_reviewer` 为 `xhigh`。Host 与账号必须支持这些值。只有首次 setup 或精确 v0.1 migration 且两个 Master keys 都缺失时，才成对添加 Master defaults。已有 keys 会保留，缺失 companion 继续缺失，后续 setup 或 Plugin update 不会重置选择。

Master 不是 role，role wizard 不能修改它。请编辑所选 scope 的 `config.toml` 中的 `model` 与 `model_reasoning_effort`。如果这些值不受支持导致 Master 无法启动，请用临时 CLI override 启动一次，修复持久 config 后另开新会话：

```bash
codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'
```

对话向导只用于已有 role TOML：

```text
$kiss-my-agent-setup configure agents for this project
$kiss-my-agent-setup configure global agents
```

也可以直接编辑 `.codex/agents/*.toml` 或 `$CODEX_HOME/agents/*.toml`。向导不会修改 Master config，不会创建、删除或重命名角色，也不会硬编码会变化的 model catalog。

<a id="legacy-setup-cli"></a>
## v0.1 setup CLI 去哪里了？

Contributor interface `skills/kiss-my-agent-setup/scripts/setup.py` 已在 v0.2 移除。这是有意的 breaking contributor-interface change。Setup、check、remove 和 role configuration 应迁移到对话式 `$kiss-my-agent-setup` Skill。其 Agent 原生 engineering evidence 与 deterministic CLI 或 repository-test evidence 不同，必须分别报告。

<a id="python"></a>
## 用户需要 Python 吗？

不需要。Plugin 安装、setup、check、remove、Agent 配置、正常使用和更新都不需要 Python、Node.js、Docker 或包管理器。但 Git-backed 安装或更新要求可用的 `git` executable 和 GitHub 网络访问。Python 3.11+ 只供贡献者使用；固定版本 Markdown 包只用于渲染和测试文档站点，只修改 Plugin/Skill 的贡献者可以把站点构建交给 pull-request CI。

<a id="update"></a>
## 已安装用户如何更新？会自动更新吗？

用一条显式 marketplace refresh，然后确认解析到的版本：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

在已验证的 Codex 0.152.1 baseline 上，Host 会在启动时自动刷新默认的 unpinned Git marketplace，并强制重新安装已启用的 non-curated Plugin。KISS My Agent 自身没有 updater，其他 Codex 版本的行为可能不同。上面的显式命令会立即请求一次手动刷新。只要刷新改变了已安装 Plugin，就启动新会话。

对于 v0.1-managed 项目，升级后再运行一次 project setup。它会刷新带版本差异的 managed AGENTS block，并且只升级仍与 bundled v0.1 seeds 完全一致、未经修改的角色文件；修改过或 owner 不清的角色以及已有 config values 都会保留。

若要求 marketplace 只在显式操作后移动，可把 marketplace source 固定到 `AoiOTA/Kiss-My-Agent@v0.2.0`。代价是它不能通过一键刷新跟随未来 release，必须手动替换 pin。回退到 `@v0.1.0` 后，普通 upgrade 同样会继续留在 v0.1.0 channel。恢复 current channel 所需的 marketplace remove 加 unpinned add 准确命令见[安装](INSTALLATION.zh-CN.md#update)。

<a id="global"></a>
## 项目 setup 会配置所有项目吗？

不会。Project scope 只修改所选项目。全局 setup 必须明确运行 `$kiss-my-agent-setup set up globally`，并可能影响加载该 Codex home 的所有项目。项目和全局 check/configure/remove 命令始终分开。

<a id="roles"></a>
## 三个角色是固定的吗？

不是。它们是可编辑的 standalone seed files，不是封闭 catalog 或强制团队。`name` 字段是身份，文件名只是约定，同一角色可以运行多个实例。默认 topology 是 Master 扁平 fan-out；只有合格的大型独立子系统可临时增加一层 lead。用户可以有意地新增、编辑、重命名或删除角色。后续 setup 与 check 不会重建有意删除的 seed。只有角色仍与 bundled v0.1 seed 完全一致、未经修改时，setup 才可升级它；用户修改过的角色保持不变。

<a id="existing-files"></a>
## 已经有 config、AGENTS 或角色文件怎么办？

Setup 拥有四个 config paths，但不会逐项独立补齐。只有首次 setup 或精确 v0.1 migration 且两个 Master keys 都缺失时，才成对添加 model/effort；任一 key 已存在时，已有状态与缺失 companion 都会保留。两个公开开关各自在缺失时添加。已有带 marker 或不带 marker 的 assignments、无关内容和显式 `false` 都逐字节保留。遇到无效 TOML、不安全路径类型、重复 identity、ownership 冲突、project/global seed-name 冲突或适用的 `AGENTS.override.md` 时，会在写入前停止。显式 remove 仍可用于解除 cross-scope 冲突。

<a id="remove"></a>
## Remove 会删除什么？

只删除明确 scope 中四个 KISS-marked config assignments、delimited managed AGENTS block，以及与 current 或 known v0.1 bundled seed 完全一致的角色文件。不带 marker 的 config、已修改角色和 owner 不清的角色都会保留。移除 setup 不会卸载 Plugin。

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
