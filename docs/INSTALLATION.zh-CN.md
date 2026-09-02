# 安装与共存

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="release-status"></a>
## 发布状态

当前 Git-backed marketplace 条目把 Plugin source 固定到 `v0.2.0`。成功的远程安装是该 tag 的发布证据；源码检查和静态验证本身不是远程安装或真实发现证据。已有 `v0.1.0` tag 与项目文件保持不变。

<a id="requirements"></a>
## 用户环境要求

通过 Git-backed marketplace 安装或更新 KISS My Agent，需要支持 Plugin 的 Codex 客户端、`PATH` 中可用的 `git` executable，以及 GitHub 网络访问。项目 setup、检查、移除和 Agent 配置使用 Codex 自带的文件工具。用户不需要 Python、Node.js、Docker 或包管理器。

Python 3.11 或更高版本只供贡献者运行仓库测试和文档站点使用，不是 Plugin 运行时依赖。

<a id="install-plugin"></a>
## 安装 Plugin

使用公开 Git marketplace：

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

安装后启动新的已认证 Codex 会话。已经运行的会话不保证发现刚安装的 Plugin 或 Skill。

<a id="first-use"></a>
## 第一次使用

简单一次性任务直接使用普通单对话，跳过 project setup。复杂科研工程项目若需要持久 executive workflow，请在目标项目中新开会话并运行：

```text
$kiss-my-agent-setup set up this project
```

Host 提示时通过界面信任项目，再启动一个新会话并运行：

```text
$kiss-my-agent-setup check this project
```

Setup 完成后直接正常使用 Codex。Master 负责持久 workflow 的调度，并委派日常执行工作；只有遇到重大工程歧义时才使用 `$kiss-my-agent`。如果 delegation 被禁用、不可用或没有合适角色，Master 会报告 staffing issue，让你选择修复或启用 staffing，或者明确把本任务切换为普通单对话；不会静默接手 delegated work。

需要真实 discovery 证据时，在该新会话中运行 `/skills`，确认两个 Plugin-owned Skills，再执行[测试](TESTING.zh-CN.md)中的窄范围 Smokes。

<a id="project-setup"></a>
## 项目 setup 会修改什么

项目 setup 只管理明确选择的目标：

- `.codex/config.toml`：拥有四个 paths——成对的首次 setup Master defaults `model = "gpt-5.6-sol"` 与 `model_reasoning_effort = "max"`，以及两个公开启用开关。只有首次 setup 或精确 v0.1 migration 且两个 Master keys 都缺失时，才添加这一对；任一 key 已存在时，setup 会保留它并让缺失 companion 继续缺失。两个 feature switches 各自在缺失时添加。
- `.codex/agents/`：安装 standalone seeds：`kiss_explorer` 与 `kiss_coder` 使用 `gpt-5.6-sol` / `high`，`kiss_reviewer` 使用 `gpt-5.6-sol` / `xhigh`；后续 setup 只可把仍与 bundled v0.1 seed 完全一致且未修改的文件替换成 v0.2 seed。
- `AGENTS.md`：追加一个有界的 KISS managed block，并保留原有 instructions。

这些只是首次默认值，不是锁定。Host 与账号必须支持所选 model/effort。目标中已有的值会保留，后续 setup 或 Plugin update 不会重置。Master settings 位于 `config.toml`；role settings 位于 standalone role TOML。Managed instructions 让 Master 只负责战略、架构与验收决策、调度、冲突解决、证据判断和汇总，把调查、实现和审查交给相应角色。

组织默认扁平：Master 直接 fan-out 到当前角色，同一角色可以有多个实例；每个共享文件或慢资源仍只有一个 writer/operator。只有大型独立子系统的直接汇总会污染 Master context 时，才可临时指定一个有界 department lead。其 workers 不得继续委派，assignment 随任务结束而消失，不建立更深或永久层级。

Skill 始终归 Plugin 所有，不会复制进项目。Setup 不安装软件、不建立 trust、不启动 Codex，也不修改全局配置。

<a id="configure-agents"></a>
## 配置 Master 或现有 Agents

Bundled model/effort 是可编辑默认值。Master 只能通过直接编辑所选项目或 Codex-home `config.toml` 中的 `model` 与 `model_reasoning_effort` 修改；role wizard 不能修改 Master。若不支持的持久值导致 Master 无法启动，请用最高优先级临时 override 启动一次，修复持久 config 后再开新会话：

```bash
codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'
```

若要通过对话向导修改已有 role 的 model、reasoning effort 或 sandbox default，运行：

```text
$kiss-my-agent-setup configure agents for this project
```

向导只编辑已有 role TOML，并在写入前预览准确改动。它不会修改 Master config，也不会创建、删除或重命名角色。也可以直接编辑 `.codex/agents/*.toml`；详见[配置](CONFIGURATION.zh-CN.md)。

<a id="global-setup"></a>
## 可选的全局 setup

全局 setup 绝不会从项目请求推断，必须明确运行：

```text
$kiss-my-agent-setup set up globally
$kiss-my-agent-setup check global setup
$kiss-my-agent-setup configure global agents
```

它管理 `$CODEX_HOME` 下的 `config.toml`、`agents/` 和 `AGENTS.md` 中的 KISS block。全局状态可能影响加载该 Codex home 的所有项目，因此项目专有行为应优先使用项目 scope。

<a id="collision-policy"></a>
## 冲突与 Override 策略

| 已有状态 | 必须采取的行为 |
| --- | --- |
| 首次 setup 或精确 v0.1 migration 时两个 Master keys 都缺失 | 成对添加带 marker 的 model/effort。 |
| 任一 Master key 已存在，或 current setup 后缺少任一 key | 保留已有 assignment，让缺失 companion 继续缺失；绝不逐 key 补齐该 pair。 |
| 任一公开开关缺失 | 只添加该项带 marker 的 `true` assignment。 |
| 公开开关已有值，无论带不带 marker | 完整保留，包括 `false`。 |
| 无关 config keys 或 AGENTS 内容 | 保留。 |
| `name` 正确，且与 bundled v0.1 seed 完全一致、从未修改 | 升级到当前 bundled seed。 |
| 已有 seed 包含用户修改或 owner 不清 | 保留并报告；不得以升级为由覆盖。 |
| 文件名/identity 不匹配、重复 identity 或 project/global seed-name 冲突 | 写入前停止。 |
| 已有有效 managed block | 只更新该 block；不恢复用户有意删除的角色。 |
| markers 损坏、TOML 无效、路径类型不安全或存在适用的 `AGENTS.override.md` | 停止且不得声称成功。 |

Setup 在首次写入前准备全部改动，写入后验证文件；失败时只在安全的情况下回滚仍与本次 after-content 完全一致的自有修改。Agent 原生文件操作不能保证从进程或机器崩溃中恢复，因此所有歧义状态都会 fail closed。

观察到 `false` 开关时报告 `disabled`。如果真实新会话无法委派或没有合适角色，Master 会报告 staffing issue 并等待用户选择；不能把持久 executive workflow 重新解释成 Master 可直接执行。

<a id="update"></a>
## 更新已安装的 Plugin

请求立即手动刷新 Git marketplace 和已安装 Plugin cache，然后确认选择的版本：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

KISS My Agent 自身没有 updater。当前 Codex Host 可能会在启动时自动刷新未固定 tag 的 Git marketplace，并强制重新安装已启用的 non-curated Plugin；这种启动行为归 Host 所有，也可能随 Codex 版本变化。上面的显式命令会立即请求刷新。只要刷新改变了已安装 Plugin，就应启动新会话。

v0.2.0 managed block 加入了 dogfooding 发现的 coordinator-wait 与 Master ownership 说明。v0.1-managed 项目会被识别为结构完整但 `outdated`；升级后运行一次 `$kiss-my-agent-setup set up this project`。Setup 会替换 managed block，并且只升级仍与 bundled v0.1 seeds 完全一致、未经修改的角色文件。已有 config values 以及修改过或 owner 不清的角色都会保留。

如果要求 marketplace 只能在显式操作后移动，请把未固定的 Git marketplace 换成固定 tag 的 source：

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent@v0.2.0
codex plugin add kiss-my-agent@kiss-my-agent
```

代价是不再自动跟随 marketplace：在替换固定 source 之前，`marketplace upgrade` 无法跟随未来 release。若要返回上一个不可变 release，可从固定的 marketplace tag 重新安装：

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

Rollback 或 channel 恢复后都要启动新会话。已有项目文件仍归用户所有，不会自动降级或重置。

<a id="check-and-remove"></a>
## 检查或移除 setup

使用与显式 scope 匹配的命令：

```text
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

`check` 只检查 managed filesystem state。`remove` 只删除所选 scope 中带 KISS marker 的 Master model/effort 与两个公开开关 assignments、managed AGENTS block，以及与 current 或 known v0.1 bundled seed 完全一致的角色文件。不带 marker 的 config、已修改角色和 owner 不清的角色都会保留并报告。移除 setup 不会卸载 Plugin。

<a id="contributor-tools"></a>
## 贡献者工具

只修改 Plugin/Skill 的贡献者可以使用 Python 3.11+ 运行不需要第三方依赖的本地核心检查：

```bash
python scripts/validate.py
python -m unittest tests.test_setup -v
```

他们无需安装 Markdown 包或在本地构建站点。该依赖只用于渲染文档站点；Pull request CI 会安装其固定版本并运行 `python scripts/test_all.py`，其中包括隔离站点构建。各平台细节见[贡献指南](../CONTRIBUTING.zh-CN.md)。这些工具都不会被 Plugin 用户执行。

v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` 已在 v0.2 移除。这是 breaking contributor-interface change，不是缺少用户 runtime dependency。Setup、check、remove 与 Agent configuration 应迁移到对话式 `$kiss-my-agent-setup` Skill。Agent 原生 engineering run 证明观察到的文件工具行为；仓库 validation 证明 deterministic source contracts，两者不能互相替代。

<a id="fresh-session"></a>
## 新会话边界

Plugin 安装/更新以及项目 config、instructions、Skill 或角色改动都会影响启动与发现。解释结果前，应在预期的可信项目中新开已认证会话。报告真实行为时记录 Codex 版本、release、scope、trust state 和 session freshness。
