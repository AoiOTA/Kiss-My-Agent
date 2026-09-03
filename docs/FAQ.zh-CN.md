# 常见问题

[English](FAQ.md) | [简体中文](FAQ.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md)

<a id="what-is-kiss"></a>
## 这里的 KISS 是什么？

“Keep It Simple, Scientist”：先做能运行、能验证的最小版本，用真实成功或失败决定下一步；只有结果证明需要时，才增加复杂度。

<a id="problem"></a>
## KISS My Agent 解决什么问题？

它主要减少两种会拖慢科研闭环的倾向：

- **过度设计：** 当前假设还没有验证，就先按成熟产品去建设，为未来可能性增加现在没人使用的抽象、配置、迁移、兼容层或平台。
- **过度防御：** 不让错误自然暴露，而是叠加校验、重试、回退、异常捕获、审批或门禁，甚至把失败包装成成功。

多 Agent 流程、handoff 和检查变成产出，以及把测试通过夸大成产品或科研目标成功，都是这两种问题的常见表现或后果，不是另外两类核心功能。

必要的认证、授权、边界验证、清理，以及对已知可选故障的明确处理，不属于过度防御。KISS 允许的是低成本、可恢复试错，不会移除不可逆操作或其他高风险安全边界。

<a id="why-agents-drift"></a>
## 编码 Agent 为什么容易偏离，KISS 又怎样应对？

Codex 倾向产出“看起来完整、稳健、成功”的答案。用户又常只说“全面”“稳健”或“生产级”，没有说明当前假设、最小目标和停止条件。框架、防御代码、校验、重试和回退既容易生成，也容易表现为工作有进展；模型还倾向避免明显失败，于是错误可能被捕获、绕开或包装成可用结果。

成熟产品在有真实需求和风险时当然可能需要完整架构与防护；科研早期过早加入它们，则会拖慢反馈并隐藏真实错误。KISS 推动一个更短的闭环：`目标或假设 → 最小可运行验证 → 真实运行 → 显式成功或失败 → 迭代或停止`。测试和流程服务这个目标，不能替代真实结果。

<a id="fit"></a>
## 它适合我吗？

它主要面向使用 Codex 做科研 MVP、算法验证、探索性开发和隐藏错误调试的用户，尤其适合需要用真实运行结果快速决定下一步的任务。它不是通用编排器、权限绕过、确定性执行器或形式化 evaluator，也不能保证第一次尝试就正确。详见首页的[适用性判断](../README.zh-CN.md#is-it-for-you)。

<a id="install"></a>
## 如何安装？

已测试基线是已认证且支持 Plugin 的 Codex CLI 0.152.1。还需要 `git`、GitHub 网络访问和账号支持 bundled default model `gpt-5.6-sol`。更早 Codex 版本未验证。请先检查客户端：

```bash
codex --version
codex plugin --help
```

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
codex plugin list
```

列表中应看到 `kiss-my-agent@kiss-my-agent` 的状态为 `installed, enabled`，版本为 `0.2.2`；cache path 可以不同。如果 Plugin 命令、认证或 marketplace 访问失败，请检查客户端支持、login 状态、`git` 与 GitHub 网络。简单一次性任务安装后直接使用普通单对话。复杂项目若需要持久 workflow，请启动新会话。在已测试的 Codex 0.152.1 baseline 上，输入 `$` 并在 picker 中选择 `kiss-my-agent-setup (kiss-my-agent)`。Picker 会插入一个结构化 Skill reference；继续补充 setup 请求并提交 prompt 后，才会调用该 Skill。如果直接粘贴文字，运行 `$kiss-my-agent:kiss-my-agent-setup set up this project`。Host 提示时信任项目；随后另开新会话并运行 `$kiss-my-agent:kiss-my-agent-setup check this project`。

<a id="after-setup"></a>
## Setup 后该怎么用？

直接正常使用 Codex，不需要每次任务前先调用 KISS。项目 `AGENTS.md` instructions 要求 Master 负责调度、决策和汇总，被委派的角色分别负责调查、实现与审查。默认由 Master 直接分配，同一角色可有多个实例，每个共享资源由一个人或 Agent 负责。合格的大型独立子系统可有一个临时 lead，但不建立更深或永久层级。

如果 delegation 被禁用、不可用或没有合适角色，instructions 要求 Master 报告 staffing issue，让你选择修复 staffing 或明确把本任务切换为普通单对话。只有后者才授权直接执行。

<a id="plugin-vs-skills"></a>
## 这是 Plugin 还是只有一个 Skill？

它是一个带版本的 Codex Plugin。Plugin 负责安装、分发与更新，目前打包两个 Skills：

- `kiss-my-agent` 提供窄范围决策指导。
- `kiss-my-agent-setup` 管理显式 project/global setup、检查、移除和现有角色配置。

配置后的项目拥有自己的 `.codex/config.toml`、standalone role TOML 和 managed AGENTS block。这些文件工具工作流仍可由 Skill 完成，不需要 MCP 服务或独立程序。

<a id="when-skill"></a>
## 何时调用 `$kiss-my-agent:kiss-my-agent`？

用于一个重要且不显然的决策，例如应继续规划或增加持久机制，还是先运行一个安全、低成本、可恢复的小型 probe；也可用于局部修复还是新系统、实验有效性、证据强度或重大 scope 扩张。不要把它套在普通实现、测试、构建、Git、查询或格式化外面。`kiss-my-agent-setup` 是另一个操作型 Skill。

<a id="configure"></a>
## 如何配置 Master 或初始 Agents？

Bundled defaults 使用 `gpt-5.6-sol`：Master 为 `max`，`kiss_explorer` 与 `kiss_coder` 为 `high`，`kiss_reviewer` 为 `xhigh`。Host 与账号必须支持这些值。只有首次 setup 或精确 v0.1 migration 且两个 Master keys 都缺失时，才成对添加 Master defaults。已有 keys 会保留，缺失 companion 继续缺失，后续 setup 或 Plugin update 不会重置选择。

Master 不是 role，role wizard 不能修改它。Project setup 编辑 `<project>/.codex/config.toml`；global setup 编辑 `$CODEX_HOME/config.toml`，未设置 `CODEX_HOME` 时编辑 `~/.codex/config.toml`。如果这些值不受支持导致 Master 无法启动，请用临时 CLI override 启动一次，修复持久 config 后另开新会话：

```bash
codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'
```

对话向导只用于已有 role TOML：

```text
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
$kiss-my-agent:kiss-my-agent-setup configure global agents
```

也可以直接编辑 `.codex/agents/*.toml` 或 `$CODEX_HOME/agents/*.toml`。向导不会修改 Master config，不会创建、删除或重命名角色，也不会硬编码会变化的 model catalog。

<a id="legacy-setup-cli"></a>
## v0.1 setup CLI 去哪里了？

Contributor interface `skills/kiss-my-agent-setup/scripts/setup.py` 已在 v0.2 移除。这是有意的 breaking contributor-interface change。Setup、check、remove 和 role configuration 应迁移到对话式 `kiss-my-agent-setup` Skill；粘贴 raw text 时使用 `$kiss-my-agent:kiss-my-agent-setup` 调用。其 Agent 原生 engineering evidence 与 deterministic CLI 或 repository-test evidence 不同，必须分别报告。

<a id="python"></a>
## 用户需要 Python 吗？

不需要。Plugin 安装、setup、check、remove、Agent 配置、正常使用和更新都不需要 Python、Node.js、Docker 或包管理器。但 Git-backed 安装或更新要求可用的 `git` executable 和 GitHub 网络访问。Python 3.11+ 只供贡献者使用；固定版本 Markdown 包只用于渲染和测试文档站点，只修改 Plugin/Skill 的贡献者可以把站点构建交给 pull-request CI。

<a id="update"></a>
## 已安装用户如何更新？会自动更新吗？

第一条命令立即更新，第二条只用于核验结果：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

在已验证的 Codex 0.152.1 baseline 上，Host 会在启动时自动刷新默认的 unpinned Git marketplace，并重新安装已启用的 non-curated Plugin。KISS My Agent 自身没有 updater，其他 Codex 版本的行为可能不同。执行上面命令后，应看到 `kiss-my-agent@kiss-my-agent` 为 `installed, enabled`，版本是 `0.2.2`。更新改变已安装 Plugin 后，请启动新会话。

只更新 Plugin 不会迁移项目文件。v0.1-managed 项目更新后，请启动新会话并再运行一次 project setup。它会刷新 KISS instruction block，并且只升级仍与 bundled v0.1 starter roles 完全一致、未经修改的角色文件；修改过或 owner 不清的角色以及已有 config values 都会保留。

显式 marketplace pin、rollback 与恢复 current unpinned channel 的命令见[安装](INSTALLATION.zh-CN.md#update)。

<a id="global"></a>
## 项目 setup 会配置所有项目吗？

不会。Project scope 只修改所选项目。全局 setup 必须明确运行 `$kiss-my-agent:kiss-my-agent-setup set up globally`，并可能影响加载该 Codex home 的所有项目。项目和全局 check/configure/remove 命令始终分开。

<a id="roles"></a>
## 三个角色是固定的吗？

不是。它们是可编辑的 standalone starter-role files，不是封闭列表或强制团队。`name` 字段是身份，文件名只是约定，同一角色可以运行多个实例。默认由 Master 直接分配；只有合格的大型独立子系统可临时增加一层 lead。用户可以有意地新增、编辑、重命名或删除角色。后续 setup 与 check 不会重建有意删除的 starter。只有角色仍与 bundled v0.1 starter 完全一致、未经修改时，setup 才可升级它；用户修改过的角色保持不变。

<a id="existing-files"></a>
## 已经有 config、AGENTS 或角色文件怎么办？

Setup 管理四项 settings，但不会逐项独立补齐。只有首次 setup 或精确 v0.1 migration 且两个 Master keys 都缺失时，才成对添加 model/effort；任一 key 已存在时，已有状态与缺失 companion 都会保留。两个公开开关各自在缺失时添加。已有带 marker 或不带 marker 的 assignments、无关内容和显式 `false` 都逐字节保留。遇到无效 TOML、不安全路径类型、重复 identity、ownership 冲突、project/global starter-role 冲突或适用的 `AGENTS.override.md` 时，会在写入前停止。

请按报告中的原因和准确路径解决冲突，不覆盖用户工作，然后重跑同一个 setup 命令。完整策略见[安装](INSTALLATION.zh-CN.md#collision-policy)。

<a id="remove"></a>
## Remove 会删除什么？

只删除明确 scope 中四个 KISS-marked config assignments、delimited managed AGENTS block，以及与 current 或 known v0.1 bundled seed 完全一致的角色文件。不带 marker 的 config、已修改角色和 owner 不清的角色都会保留。移除 setup 不会卸载 Plugin。

<a id="verification"></a>
## 怎样确认它有效？

应分开证据：仓库测试、setup `check`、可信新会话中的 `/skills` 发现、窄范围实时 **Smoke**、更新测试和小规模真实 **Pilot** 分别支持不同结论。**Final** 表示按用户标准完成完整验收。详见[测试](TESTING.zh-CN.md)。静态 PASS 不能证明模型行为或用户科研目标。

<a id="windows-wsl"></a>
## WSL 是 Windows 测试路径吗？

不是。WSL 只产生 Linux 证据。原生 Windows 兼容性需要 Windows runner 或原生 PowerShell 检查。Agent 原生用户 setup 避免依赖某种 shell 语言，但真实 Host 行为仍需要对应平台证据。

<a id="other-hosts"></a>
## 其他 Agent Host 可以使用吗？

这些思想可以适配，但打包后的 Plugin、config、roles 和测试以 Codex 为首要 Host。其他 Host 未被本 release 验证。

<a id="pages"></a>
## 文档站点在哪里？

站点提供[英文版](https://aoiota.github.io/Kiss-My-Agent/)与[简体中文版](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)。部署成功与真实 HTTP/content 检查是不同证据。
