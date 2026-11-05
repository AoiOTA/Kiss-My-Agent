# 安装与共存

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="release-status"></a>
## 发布状态

[GitHub 最新 Release](https://github.com/AoiOTA/Kiss-My-Agent/releases/latest) 是当前支持的 release。当前安装产物以它为准，发布证据与历史见 [HANDOFF](HANDOFF.md)。

<a id="local-development-candidate"></a>
## 本地开发候选

此工作树包含 `0.2.10-dev.1`，插件名为 `kiss-my-agent`，独立本地 marketplace 为 `kiss-my-agent-dev`。进入解压后的候选根目录，再安装：

```bash
codex plugin marketplace add .
codex plugin add kiss-my-agent@kiss-my-agent-dev
codex plugin list --marketplace kiss-my-agent-dev --json
```

保留解压后的来源目录，确认 installed 条目报告 `0.2.10-dev.1`。新建会话前停用旧的已启用 KMA 条目，避免同名 Skill 选到旧包；旧安装可保留用于回退。安装插件本身不修改项目角色。新项目使用 setup，已有角色使用下文显式 follow-master prompt。本候选有 CLI `0.159.2` 的有限本地证据，尚不证明公开分发、所有客户端兼容或长期提效。

<a id="requirements"></a>
## 用户环境要求

已测试基线是已认证且支持 Plugin 的 Codex CLI 0.152.1 和 0.153.0。安装和更新还需要 `PATH` 中可用的 `git` executable与 GitHub 网络访问。其他 Codex 版本未验证。项目 setup、检查、移除和 Agent 配置使用 Codex 自带的文件工具。用户不需要 Python、Node.js、Docker 或包管理器。

Python 3.11 或更高版本只供贡献者运行仓库测试和文档站点使用，不是 Plugin 运行时依赖。

<a id="install-plugin"></a>
## 安装 Plugin

使用公开 Git marketplace：

```bash
codex --version
codex plugin --help
```

如果 `codex plugin --help` 不可用，请更新到支持 Plugin 的客户端。认证或 marketplace 访问失败时，先检查客户端 login 状态、`git` 与 GitHub 网络，再重试。

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
codex plugin list --marketplace kiss-my-agent
```

列表中应看到 Plugin ID `kiss-my-agent@kiss-my-agent`、状态 `installed, enabled`，且版本与当前支持的 release 一致；cache path 可以不同。安装后启动新的已认证 Codex 会话。已经运行的会话不保证发现刚安装的 Plugin 或 Skill。

<a id="first-use"></a>
## 第一次使用

简单一次性任务直接使用普通单对话，跳过 project setup。复杂科研工程项目若需要持久协调 instructions，请在目标项目中新开会话。在已测试的 Codex CLI 0.152.1 baseline 上，先输入 `$`，再在 Skill picker 中选择 `kiss-my-agent-setup (kiss-my-agent)`。Picker 会插入一个结构化 Skill reference；继续补充 setup 请求并提交 prompt 后，才会调用该 Skill。如果直接粘贴文字，请使用下面完整限定的命令：

```text
$kiss-my-agent:kiss-my-agent-setup set up this project
```

Host 提示时通过界面信任项目，再启动一个新会话并运行：

```text
$kiss-my-agent:kiss-my-agent-setup check this project
```

Setup 完成后直接正常使用 Codex。每个 Agent 首次承担 KMA 工作时读取一次 `kiss-my-agent`，在后续 assignment 和 follow-up 中主动复用已加载指导，无需用户提醒；仅在指导更新或缺少相关细节时重读。Master 可以直接完成明确的小任务或局部工作；对实质批量工作、可独立并行或需要不同视角的工作，在收益超过协调成本时应积极委派。按工作量、并行机会、耦合、风险与协调成本选择，角色可选不等于 Master 包办全部。每种可用角色都可有零个、一个或多个实例，不要求固定组合、顺序或每次启动子代理。如果 delegation 被禁用、不可用或没有合适角色，Master 可在已有授权和自身能力内继续工作，无需为 staffing 另设审批。用户明确要求的独立检查、特定角色或真实能力缺口仍须报告，不能把直接执行冒充为满足这些要求。

需要真实 discovery 证据时，在该新会话中运行 `/skills`，确认两个 Plugin-owned Skills，再执行[测试](TESTING.zh-CN.md)中的窄范围 Smokes。

<a id="project-setup"></a>
## 项目 setup 会修改什么

项目 setup 只管理明确选择的目标：

- `.codex/config.toml`：只补齐缺失的多代理及实验上下文默认值；保留全部模型与 effort 设置。
- `.codex/agents/`：fresh setup 会创建每个缺失的可编辑 starter role；它们省略 model 与 effort 覆盖。Setup 只检查这三个准确目标路径，不检查完整角色目录或另一 scope。任何已经存在的角色都归用户所有并逐字节保持不变。Setup 后缺失的 starter 是合法且有意缺失的 catalog entry，不会重建。
- `AGENTS.md`：追加一个有界的 KISS managed block，并保留原有 instructions。

Master 使用当前 Host／会话选择的模型与推理强度。新 seeds 省略两项覆盖并跟随 Master，默认委派也省略 model 和 effort 参数。Setup 保留已有模型选择与角色；显式 follow-master 配置移除选定角色和所选 scope 的 `[agents]` 覆盖，旧 KMA Master 固定值需要单独明确选中。有效设置须在新任务中验证。 Plugin cache 中的角色文件只是 package resources，不会自动进入 Host role catalog，因此仍需 fresh setup。Role settings 位于 standalone role TOML。Managed instructions 保留 Master 的架构、验收、调度、冲突解决、证据判断和汇总责任，同时允许直接完成小任务并积极进行有收益的委派；角色不是必经阶段。

Managed instructions 要求默认扁平协调：直接向当前角色分配任务，同一角色可以有多个实例；每个共享文件或慢资源仍只有一个 writer/operator。只有大型独立子系统的直接汇总会污染 Master context 时，才可临时指定一个有界 department lead。其 workers 不得继续委派，assignment 随任务结束而消失，不建立更深或永久层级。

Skill 始终归 Plugin 所有，不会复制进项目。Setup 不安装软件、不建立 trust、不启动 Codex，也不修改全局配置。

Ubuntu 24.04 的 ChatGPT Pro 客户端无需 API key 或独立 API 运行时。升级路径：更新 Plugin → 在原 scope 运行 setup → 通过现有 configure 显式迁移选定角色 → 新建可信任务并验证加载。实验上下文默认开启；已有 false 保留，启用后须新建任务。静态 check 只证明文件状态，不能证明客户端加载。

<a id="configure-agents"></a>
## 选择 Master 并配置现有 Agents

Master 使用当前 Host／会话选择的模型与推理强度。新 seeds 省略两项覆盖并跟随 Master，默认委派也省略 model 和 effort 参数。Setup 保留已有模型选择与角色；显式 follow-master 配置移除选定角色和所选 scope 的 `[agents]` 覆盖，旧 KMA Master 固定值需要单独明确选中。有效设置须在新任务中验证。

若要通过对话向导修改已有 role 的 model、reasoning effort 或 sandbox default，运行：

```text
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
```

Plugin update 和 setup 保留每个已有角色。要让三个已有角色跟随 Master，请使用下面限定的项目 prompt：

```text
$kiss-my-agent:kiss-my-agent-setup configure agents in this project: make kiss_explorer, kiss_coder, and kiss_reviewer follow master
```

普通向导只编辑已有 role TOML，并在写入前预览准确改动。请求已经点名角色时，只解析这些文件；没有点名时，先只列出 direct role paths 而不解析，等待用户选择后再只解析选中的文件。未选角色无效不会阻塞配置；更广泛的 catalog warning 和 precedence 由 Host 负责。Follow-master 模式额外预览所选 scope 的 `[agents]` 默认覆盖及单独选中的精确 marked legacy KMA Master 固定值移除，不创建、删除或重命名角色。也可以直接编辑 `.codex/agents/*.toml`；详见[配置](CONFIGURATION.zh-CN.md)。

<a id="global-setup"></a>
## 可选的全局 setup

全局 setup 绝不会从项目请求推断，必须明确运行：

```text
$kiss-my-agent:kiss-my-agent-setup set up globally
$kiss-my-agent:kiss-my-agent-setup check global setup
$kiss-my-agent:kiss-my-agent-setup configure global agents
```

它管理 `$CODEX_HOME` 下 `config.toml` 中的功能默认值、`agents/` 中的 starter roles 和 `AGENTS.md` 中的 KISS block。未设置 `CODEX_HOME` 时，全局 config 是 `~/.codex/config.toml`。全局状态可能影响加载该 Codex home 的所有项目，因此项目专有行为应优先使用项目 scope。

<a id="collision-policy"></a>
## 冲突与 Override 策略

| 已有状态 | 必须采取的行为 |
| --- | --- |
| 旧 marked Master model／effort pair | Setup 保留；只在明确选中的迁移或兼容 remove 中移除。 |
| 已有 Master assignment，包括部分或用户自选设置 | 逐字节保留；缺失字段继续继承。 |
| Master assignment 重复、TOML 无效或 ownership 有歧义 | 作为 conflict 停止；不得猜测迁移或修复。 |
| 任一公开开关缺失 | 只添加该项带 marker 的 `true` assignment。 |
| 公开开关已有值，无论带不带 marker | 完整保留，包括 `false`。 |
| 无关 config keys 或 AGENTS 内容 | 保留。 |
| Fresh setup 时 starter role 缺失 | 从当前 bundled seed 创建。 |
| 任何准确 bundled target 已存在 | 视为 user-owned 并逐字节保留；不得推断或迁移角色版本。 |
| 准确 bundled target 的类型不安全、TOML 无效、缺失 identity fields 或 `name` 与文件名不同 | 写入前停止。 |
| 无关角色或另一 scope 的角色损坏或声明同一 identity | 保持不变；更广泛的 catalog warning 和 project-over-global precedence 由 Host 负责。 |
| 已有有效 managed block | 只更新该 block；把缺失 starter 报告为 intentionally absent，不恢复它们。 |
| markers 损坏、TOML 无效、路径类型不安全或存在适用的 `AGENTS.override.md` | 停止且不得声称成功。 |

Setup、check 与 remove 只检查所选 scope 中由 KISS 管理的 config、AGENTS paths 和三个准确 bundled role targets；不验证完整 role catalog，也不协调 project/global roles。Setup 在首次写入前准备全部改动，写入后验证文件；失败时只在安全的情况下回滚仍与本次 after-content 完全一致的自有修改。Agent 原生文件操作不能保证从进程或机器崩溃中恢复，因此 managed target 中的歧义状态都会 fail closed。

Setup 停止时，请按报告中的原因和准确路径解决冲突，不覆盖用户工作，然后重跑同一命令。观察到委派开关为 `false` 时报告 `disabled`；上下文 `false` 单独报告，不禁用 KISS。如果 delegation 被禁用、不可用或没有合适角色，Master 可在已有授权和自身能力内继续工作，无需为 staffing 另设审批。用户明确要求的独立检查、特定角色或真实能力缺口仍须报告，不能把直接执行冒充为满足这些要求。

<a id="update"></a>
## 立即更新

第一条命令立即请求更新 marketplace 与已安装 Plugin；第二条只核验结果：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list --marketplace kiss-my-agent
```

KISS My Agent 自身没有 updater。在已验证的 Codex 0.152.1 baseline 上，Host 可在启动时刷新 unpinned Git marketplace，并重新安装已启用的 non-curated Plugin；其他版本可能不同。上面命令完成后，应确认 `kiss-my-agent@kiss-my-agent` 为 `installed, enabled`，且版本与当前支持的 release 一致。更新改变已安装 Plugin 后，应启动新会话。

Host refresh 与 marketplace upgrade 只更新 Plugin 包，不改变 project/global config、instructions 或角色文件。Setup 可刷新 managed instruction block、补齐缺失功能开关，永不添加或迁移 model／effort 字段或已有角色。需要迁移时使用上面的 follow-master prompt 明确选择，或手工编辑 TOML。

如果要求 marketplace 只能在显式操作后移动，请把未固定的 Git marketplace 换成固定 tag 的 source：

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent@vX.Y.Z
codex plugin add kiss-my-agent@kiss-my-agent
```

把 `vX.Y.Z` 替换为 [Releases 页面](https://github.com/AoiOTA/Kiss-My-Agent/releases)中需要的 release。代价是不再自动跟随 marketplace：在替换固定 source 之前，`marketplace upgrade` 无法跟随未来 release。若要返回上一个不可变 release，可从固定的 marketplace tag 重新安装：

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent@v0.1.0
codex plugin add kiss-my-agent@kiss-my-agent
```

这样 rollback 后，普通 `marketplace upgrade` 仍会停留在固定的 v0.1.0 channel。若要返回 current/unpinned channel，请显式替换 marketplace source：

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

Rollback 或 channel 恢复后都要启动新会话。已有 project/global 文件仍归用户所有，不会自动升级、降级或重置。

<a id="check-and-remove"></a>
## 检查或移除 setup

使用与显式 scope 匹配的命令：

```text
$kiss-my-agent:kiss-my-agent-setup check this project
$kiss-my-agent:kiss-my-agent-setup remove from this project

$kiss-my-agent:kiss-my-agent-setup check global setup
$kiss-my-agent:kiss-my-agent-setup remove global setup
```

`check` 只检查 managed filesystem state，报告已有 Master 设置并检查必需功能字段类型，单独报告实验上下文 true、false 或缺失。已有角色会报告为 user-owned；setup 后缺失的 starter 会报告为 intentionally absent，而不是 outdated 或 incomplete。显式 `remove` 只删除带准确 KISS marker 且值精确匹配的当前默认配置 与任何准确的旧 marked Master pair、managed AGENTS block，以及字节完全匹配 current、exact v0.2.9/v0.2.9-active-guidance/v0.2.7/v0.2.6/v0.2.5/v0.1 seed 的 bundled roles；其他角色文件仍归用户所有。移除 setup 不会卸载 Plugin。 Remove 保留上下文子表及其他用户字段；只删除精确默认值和准确 marker 同时匹配的配置。

<a id="contributor-tools"></a>
## 贡献者工具

只修改 Plugin/Skill 的贡献者可以使用 Python 3.11+ 运行不需要第三方依赖的本地核心检查：

```bash
python3 scripts/validate.py
python3 -m unittest tests.test_setup -v
```

他们无需安装 Markdown 包或在本地构建站点。该依赖只用于渲染文档站点；Pull request CI 会安装其固定版本，并在已激活环境中运行 `python scripts/test_all.py`，其中包括隔离站点构建。各平台细节见[贡献指南](../CONTRIBUTING.zh-CN.md)。这些工具都不会被 Plugin 用户执行。

v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` 已在 v0.2 移除。这是 breaking contributor-interface change，不是缺少用户 runtime dependency。Setup、check、remove 与 Agent configuration 应迁移到对话式 `kiss-my-agent-setup` Skill；粘贴 raw text 时使用 `$kiss-my-agent:kiss-my-agent-setup` 调用。Agent 原生 engineering run 证明观察到的文件工具行为；仓库 validation 证明 deterministic source contracts，两者不能互相替代。

<a id="fresh-session"></a>
## 新会话边界

Plugin 安装/更新以及项目 config、instructions、Skill 或角色改动都会影响启动与发现。解释结果前，应在预期的可信项目中新开已认证会话。报告真实行为时记录 Codex 版本、release、scope、trust state 和 session freshness。
