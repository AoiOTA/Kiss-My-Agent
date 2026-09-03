# 安装与共存

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="release-status"></a>
## 发布状态

[GitHub 最新 Release](https://github.com/AoiOTA/Kiss-My-Agent/releases/latest) 是当前支持的 release。当前安装产物以它为准，发布证据与历史见 [HANDOFF](HANDOFF.md)。

<a id="requirements"></a>
## 用户环境要求

已测试基线是已认证且支持 Plugin 的 Codex CLI 0.152.1 和 0.153.0。安装和更新还需要 `PATH` 中可用的 `git` executable、GitHub 网络访问，以及账号支持 bundled default model `gpt-5.6-sol`。其他 Codex 版本未验证。项目 setup、检查、移除和 Agent 配置使用 Codex 自带的文件工具。用户不需要 Python、Node.js、Docker 或包管理器。

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

Setup 完成后直接正常使用 Codex。项目 instructions 要求 Master 调度持久 workflow，并委派日常执行工作；只有遇到重要工程疑问时才使用 `kiss-my-agent`。如果 delegation 被禁用、不可用或没有合适角色，这些 instructions 要求 Master 报告 staffing issue，让你选择修复或启用 staffing，或者明确把本任务切换为普通单对话，而不是静默接手 delegated work。

需要真实 discovery 证据时，在该新会话中运行 `/skills`，确认两个 Plugin-owned Skills，再执行[测试](TESTING.zh-CN.md)中的窄范围 Smokes。

<a id="project-setup"></a>
## 项目 setup 会修改什么

项目 setup 只管理明确选择的目标：

- `.codex/config.toml`：管理四项 settings——成对的初始 Master defaults `model = "gpt-5.6-sol"` 与 `model_reasoning_effort = "max"`，以及两个公开启用开关。Managed block 分类互斥：current block 绝不补缺失的 Master keys；block 缺失或被识别为 outdated 时，只有两个 keys 都缺失才补入这一对；其他情况都保留已有 assignments，并让每个缺失 key 继续缺失和继承。两个 feature switches 各自在缺失时添加。
- `.codex/agents/`：fresh setup 会创建每个缺失的可编辑 starter role；`kiss_explorer` 与 `kiss_coder` 使用 `gpt-5.6-sol` / `high`，`kiss_reviewer` 使用 `gpt-5.6-sol` / `xhigh`。任何已经存在的角色都归用户所有并逐字节保持不变。Setup 后缺失的 starter 是合法且有意缺失的 catalog entry，不会重建。
- `AGENTS.md`：追加一个有界的 KISS managed block，并保留原有 instructions。

这些只是首次默认值，不是锁定。Host 与账号必须支持所选 model/effort。目标中已有的值会保留，后续 setup 或 Plugin update 不会重置。Plugin cache 中的角色文件只是 package resources，不会自动进入 Host role catalog，因此仍需 fresh setup。Master settings 位于 `config.toml`；role settings 位于 standalone role TOML。Managed instructions 让 Master 只负责战略、架构与验收决策、调度、冲突解决、证据判断和汇总，把调查、实现和审查交给相应角色。

Managed instructions 要求默认扁平协调：直接向当前角色分配任务，同一角色可以有多个实例；每个共享文件或慢资源仍只有一个 writer/operator。只有大型独立子系统的直接汇总会污染 Master context 时，才可临时指定一个有界 department lead。其 workers 不得继续委派，assignment 随任务结束而消失，不建立更深或永久层级。

Skill 始终归 Plugin 所有，不会复制进项目。Setup 不安装软件、不建立 trust、不启动 Codex，也不修改全局配置。

<a id="configure-agents"></a>
## 配置 Master 或现有 Agents

Bundled model/effort 是可编辑默认值。Project setup 的 Master 在 `<project>/.codex/config.toml` 中修改；global setup 使用 `$CODEX_HOME/config.toml`，未设置 `CODEX_HOME` 时使用 `~/.codex/config.toml`。Role wizard 不能修改 Master。若不支持的持久值导致 Master 无法启动，请用最高优先级临时 override 启动一次，修复持久 config 后再开新会话：

```bash
codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'
```

若要通过对话向导修改已有 role 的 model、reasoning effort 或 sandbox default，运行：

```text
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
```

向导只编辑已有 role TOML，并在写入前预览准确改动。它不会修改 Master config，也不会创建、删除或重命名角色。也可以直接编辑 `.codex/agents/*.toml`；详见[配置](CONFIGURATION.zh-CN.md)。

<a id="global-setup"></a>
## 可选的全局 setup

全局 setup 绝不会从项目请求推断，必须明确运行：

```text
$kiss-my-agent:kiss-my-agent-setup set up globally
$kiss-my-agent:kiss-my-agent-setup check global setup
$kiss-my-agent:kiss-my-agent-setup configure global agents
```

它管理 `$CODEX_HOME` 下的 `config.toml`、`agents/` 和 `AGENTS.md` 中的 KISS block。未设置 `CODEX_HOME` 时，全局 Master config 是 `~/.codex/config.toml`。全局状态可能影响加载该 Codex home 的所有项目，因此项目专有行为应优先使用项目 scope。

<a id="collision-policy"></a>
## 冲突与 Override 策略

| 已有状态 | 必须采取的行为 |
| --- | --- |
| Managed block 为 current，无论哪些 Master keys 存在 | 保留已有 assignments，让每个缺失 key 继续缺失和继承。 |
| Managed block 缺失或被识别为 outdated，且两个 Master keys 都缺失 | 成对添加带 marker 的 model/effort。 |
| Managed block 缺失或被识别为 outdated，且任一 Master key 已存在 | 保留已有 assignments，让缺失 companion 继续缺失和继承；绝不逐 key 补齐该 pair。 |
| 任一公开开关缺失 | 只添加该项带 marker 的 `true` assignment。 |
| 公开开关已有值，无论带不带 marker | 完整保留，包括 `false`。 |
| 无关 config keys 或 AGENTS 内容 | 保留。 |
| Fresh setup 时 starter role 缺失 | 从当前 bundled seed 创建。 |
| 任何 role file 已存在 | 视为 user-owned 并逐字节保留；不得推断或迁移角色版本。 |
| 文件名/identity 不匹配、重复 identity 或 project/global seed-name 冲突 | 写入前停止。 |
| 已有有效 managed block | 只更新该 block；把缺失 starter 报告为 intentionally absent，不恢复它们。 |
| markers 损坏、TOML 无效、路径类型不安全或存在适用的 `AGENTS.override.md` | 停止且不得声称成功。 |

Setup 在首次写入前准备全部改动，写入后验证文件；失败时只在安全的情况下回滚仍与本次 after-content 完全一致的自有修改。Agent 原生文件操作不能保证从进程或机器崩溃中恢复，因此所有歧义状态都会 fail closed。

Setup 停止时，请按报告中的原因和准确路径解决冲突，不覆盖用户工作，然后重跑同一命令。观察到 `false` 开关时报告 `disabled`。如果真实新会话无法委派或没有合适角色，项目 instructions 要求 Master 报告 staffing issue 并等待用户选择，而不是把持久 workflow 解释成 Master 可直接执行。

<a id="update"></a>
## 立即更新

第一条命令立即请求更新 marketplace 与已安装 Plugin；第二条只核验结果：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list --marketplace kiss-my-agent
```

KISS My Agent 自身没有 updater。在已验证的 Codex 0.152.1 baseline 上，Host 可在启动时刷新 unpinned Git marketplace，并重新安装已启用的 non-curated Plugin；其他版本可能不同。上面命令完成后，应确认 `kiss-my-agent@kiss-my-agent` 为 `installed, enabled`，且版本与当前支持的 release 一致。更新改变已安装 Plugin 后，应启动新会话。

Host refresh 只更新 Plugin 包，不会修改 project/global config、AGENTS instructions 或角色文件。v0.1-managed 项目升级后，可以运行 `$kiss-my-agent:kiss-my-agent-setup set up this project` 来刷新 managed instruction block 并补充缺失的公开开关，但所有已有角色文件都直接保持不变。Setup 永不拿已有角色与历史 bundled seeds 比较、判定其版本或迁移它。若要采用新版 model 或 effort，请使用 existing-role wizard 或手工编辑角色 TOML。

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

`check` 只检查 managed filesystem state。已有角色会报告为 user-owned；setup 后缺失的 starter 会报告为 intentionally absent，而不是 outdated 或 incomplete。显式 `remove` 只删除所选 scope 中带 KISS marker 的 Master model/effort 与两个公开开关 assignments、managed AGENTS block，以及字节完全匹配 current 或 known v0.1 seed 的 bundled roles；其他角色文件仍归用户所有。移除 setup 不会卸载 Plugin。

<a id="contributor-tools"></a>
## 贡献者工具

只修改 Plugin/Skill 的贡献者可以使用 Python 3.11+ 运行不需要第三方依赖的本地核心检查：

```bash
python scripts/validate.py
python -m unittest tests.test_setup -v
```

他们无需安装 Markdown 包或在本地构建站点。该依赖只用于渲染文档站点；Pull request CI 会安装其固定版本并运行 `python scripts/test_all.py`，其中包括隔离站点构建。各平台细节见[贡献指南](../CONTRIBUTING.zh-CN.md)。这些工具都不会被 Plugin 用户执行。

v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` 已在 v0.2 移除。这是 breaking contributor-interface change，不是缺少用户 runtime dependency。Setup、check、remove 与 Agent configuration 应迁移到对话式 `kiss-my-agent-setup` Skill；粘贴 raw text 时使用 `$kiss-my-agent:kiss-my-agent-setup` 调用。Agent 原生 engineering run 证明观察到的文件工具行为；仓库 validation 证明 deterministic source contracts，两者不能互相替代。

<a id="fresh-session"></a>
## 新会话边界

Plugin 安装/更新以及项目 config、instructions、Skill 或角色改动都会影响启动与发现。解释结果前，应在预期的可信项目中新开已认证会话。报告真实行为时记录 Codex 版本、release、scope、trust state 和 session freshness。
