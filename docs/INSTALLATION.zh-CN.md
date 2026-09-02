# 安装与共存

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="release-status"></a>
## 发布状态

Git-backed marketplace 将当前 release 固定到 `v0.2.0`。成功的远程安装是该 tag 的发布证据；源码检查和静态验证本身不是远程安装或真实发现证据。已有 `v0.1.0` tag 与项目文件保持不变。

<a id="requirements"></a>
## 用户环境要求

安装和使用 KISS My Agent 只需要支持 Plugin 的 Codex 客户端以及访问 GitHub 仓库的能力。项目 setup、检查、移除和 Agent 配置使用 Codex 自带的文件工具。用户不需要 Python、Node.js、Docker 或包管理器。

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

在需要配置的项目中新开会话，然后运行：

```text
$kiss-my-agent-setup set up this project
```

Host 提示时通过界面信任项目，再启动一个新会话并运行：

```text
$kiss-my-agent-setup check this project
```

Setup 完成后直接正常使用 Codex。普通实现、测试、构建、Git 操作或格式化不需要调用 KISS 命令；项目 instructions 会指导日常工作，只有遇到重大工程歧义时才使用 `$kiss-my-agent`。

需要真实 discovery 证据时，在该新会话中运行 `/skills`，确认两个 Plugin-owned Skills，再执行[测试](TESTING.zh-CN.md)中的窄范围 Smokes。

<a id="project-setup"></a>
## 项目 setup 会修改什么

项目 setup 只管理明确选择的目标：

- `.codex/config.toml`：最小合并两个公开启用开关。
- `.codex/agents/`：首次 setup 时安装 `kiss_explorer`、`kiss_coder` 和 `kiss_reviewer` 三个 standalone seed roles。
- `AGENTS.md`：追加一个有界的 KISS managed block，并保留原有 instructions。

Skill 始终归 Plugin 所有，不会复制进项目。Setup 不安装软件、不建立 trust、不启动 Codex，也不修改全局配置。

<a id="configure-agents"></a>
## 配置现有 Agents

默认角色无需设置模型即可使用。若要通过对话向导修改现有项目角色的模型、思考强度或 sandbox 默认值，运行：

```text
$kiss-my-agent-setup configure agents for this project
```

向导会在写入前预览准确的 TOML 改动，不会创建、删除或重命名角色。也可以直接编辑 `.codex/agents/*.toml`；详见[配置](CONFIGURATION.zh-CN.md)。

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
| 无关 config keys 或 AGENTS 内容 | 保留。 |
| 任一公开开关被有意设为 `false` | 保留并报告 `disabled`。 |
| 已有 seed 文件名及 `name` 正确 | 保留，包括用户编辑。 |
| 文件名/identity 不匹配、重复 identity 或 project/global seed-name 冲突 | 写入前停止。 |
| 已有有效 managed block | 只更新该 block；不恢复用户有意删除的角色。 |
| markers 损坏、TOML 无效、路径类型不安全或存在适用的 `AGENTS.override.md` | 停止且不得声称成功。 |

Setup 在首次写入前准备全部改动，写入后验证文件；失败时只在安全的情况下回滚仍与本次 after-content 完全一致的自有修改。Agent 原生文件操作不能保证从进程或机器崩溃中恢复，因此所有歧义状态都会 fail closed。

<a id="update"></a>
## 更新已安装的 Plugin

用一条显式命令刷新 Git marketplace 和已安装 Plugin cache，然后确认选择的版本：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

升级后启动新会话。Plugin 升级不会静默改写项目拥有的角色文件；只有需要检查或修改项目时，才运行对应 `check` 或可选配置向导。

KISS My Agent 不实现静默后台更新。若要返回上一个不可变 release，可从固定的 marketplace tag 重新安装：

```bash
codex plugin remove kiss-my-agent@kiss-my-agent
codex plugin marketplace remove kiss-my-agent
codex plugin marketplace add AoiOTA/Kiss-My-Agent@v0.1.0
codex plugin add kiss-my-agent@kiss-my-agent
```

回退后启动新会话。已有项目文件仍归用户所有，不会自动降级。

<a id="check-and-remove"></a>
## 检查或移除 setup

使用与显式 scope 匹配的命令：

```text
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

`check` 只检查 managed filesystem state。`remove` 只删除所选 scope 中带 marker 的 config 行、managed AGENTS block 和未修改的 bundled roles。已修改或 owner 不清的角色会被保留并报告。移除 setup 不会卸载 Plugin。

<a id="contributor-tools"></a>
## 贡献者工具

只修改 Plugin/Skill 的贡献者可以使用 Python 3.11+ 运行不需要第三方依赖的本地核心检查：

```bash
python scripts/validate.py
python -m unittest tests.test_setup -v
```

他们无需安装 Markdown 包或在本地构建站点。Pull request CI 会安装固定版本的文档依赖并运行 `python scripts/test_all.py`，其中包括隔离站点构建。各平台细节见[贡献指南](../CONTRIBUTING.zh-CN.md)。这些工具都不会被 Plugin 用户执行。

<a id="fresh-session"></a>
## 新会话边界

Plugin 安装/更新以及项目 config、instructions、Skill 或角色改动都会影响启动与发现。解释结果前，应在预期的可信项目中新开已认证会话。报告真实行为时记录 Codex 版本、release、scope、trust state 和 session freshness。
