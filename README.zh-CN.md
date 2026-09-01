![KISS My Agent 主视觉：复杂的 Agent 路径汇聚为一个清晰结果](assets/kiss-my-agent-hero.png)

<div class="readme-intro" align="center" markdown="1">

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

[English](https://aoiota.github.io/Kiss-My-Agent/) | [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)

[![许可证：MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![状态：早期阶段](https://img.shields.io/badge/status-early_stage-orange.svg)
![宿主：Codex 优先](https://img.shields.io/badge/host-Codex--first-blue.svg)

</div>

<a id="overview"></a>
## 概览

KISS My Agent 是面向科研型编码 Agent 的紧凑 Codex plugin。人掌握研究目标、架构、验收标准、非目标和停止边界；Agent 在边界内作实现决策，优先选择最小充分改动，让失败保持可见，并且只按证据实际支持的层级汇报结果。

Plugin 提供两个窄路由 Skills、三个 seed 自定义角色、setup/check/remove 支持、项目指导、静态验证和双语开发者文档。它不是固定工作流、权限系统、行为保证或封闭角色 catalog。

<a id="quick-start"></a>
## 快速开始

公开安装接口为：

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

启动新的已认证 Codex 会话，让新安装的 plugin 被发现。在该会话中运行：

```text
$kiss-my-agent-setup set up this project
```

Setup Skill 只修改当前项目；它不会信任项目或重启 Codex。通过 Host 信任项目，另开一个新会话，然后运行：

```text
$kiss-my-agent-setup check this project
```

需要真实发现证据时，还应按[测试](docs/TESTING.zh-CN.md)使用 `/skills` 和无害角色 Smoke。

全局安装绝不隐式发生。必须明确请求 `$kiss-my-agent-setup set up globally`；选择该 scope 前请阅读[安装](docs/INSTALLATION.zh-CN.md)。

Git-backed marketplace 将本次 release 固定到 `v0.1.0`。成功的远程安装是该 tag 的发布证据；源码检查与静态验证本身不是远程安装或真实发现证据。

<a id="components"></a>
## 组件

- [`AGENTS.md`](AGENTS.md)：永久的人与 Agent 边界，以及动态调度指导。
- Plugin Skills：用于所列窄决策场景的 `$kiss-my-agent`，以及用于显式 setup/check/remove 的 `$kiss-my-agent-setup`。
- [`.codex/config.toml`](.codex/config.toml)：两个公开 multi-agent 启用开关，本项目都显式设为 `true`。
- [`.codex/agents/`](.codex/agents/)：从独立 TOML 文件自动发现的三个 seed 角色。
- [`scripts/validate.sh`](scripts/validate.sh) 与 [`scripts/validate.ps1`](scripts/validate.ps1)：原生静态验证入口。
- [`tests/`](tests/)：分层 instruction fixtures 和人工 scenarios。
- 英文优先、结构同步的简体中文配套文档。

<a id="three-layers"></a>
## 三层职责

Runtime 表面有三个不同 owner：

1. `.codex/config.toml` 通过 `features.multi_agent = true` 启用 Host multi-agent 能力，通过 `agents.enabled = true` 启用自定义 Agent。
2. 每个 standalone role TOML 会被自动发现。其 `name` 字段是角色身份；文件名只是约定。
3. `AGENTS.md` 告诉主线程何时委派值得，不强制流水线或固定 fan-out。

提供的 `kiss_explorer`、`kiss_coder` 与 `kiss_reviewer` 文件是可编辑 seeds，不是封闭 catalog。应有意地增加或删除 standalone roles。首次 setup 后，后续 setup 与 check 会保留 catalog，不会重新创建已删除角色。

角色 model 与 reasoning effort 在省略时继承 Host 设置，也可修改为 Host 支持的值。KISS My Agent 不固定模型、effort、context window 或并发上限。

<a id="platform-support"></a>
## 平台支持

| 平台 | 原生命令 | 证据状态 |
| --- | --- | --- |
| Linux | `./scripts/validate.sh` | 只有针对精确 checkout 报告时才算本地已执行。 |
| macOS | `./scripts/validate.sh` | CI 目标；精确 commit 需要绿色原生 job。 |
| Windows | 在原生 PowerShell 中运行 `.\scripts\validate.ps1` | CI 目标；精确 commit 需要绿色原生 job。WSL 属于 Linux 证据。 |

静态验证需要 Python 3.11 或更高版本，不需要 Codex sandbox package、复制的 `CODEX_HOME`、容器、虚拟机或额外测试项目。存在 workflow 定义不等于平台已经通过；精确 commit 上的绿色 jobs 才是权威证据。

<a id="runtime-configuration"></a>
## 运行配置

主线程与角色文件使用 Host 实际生效的设置。有效用户层或管理员层中的显式 `false`，或者单次启动 CLI override，优先于 KISS 默认值。为单次启动关闭两个公开开关：

```bash
codex --config features.multi_agent=false --config agents.enabled=false
```

项目 setup 与全局 setup 是两个独立显式操作。已有设置和 instructions 会被保留；发生冲突时 setup 会停止以供审核。详见[配置](docs/CONFIGURATION.zh-CN.md)。

<a id="core-principles"></a>
## 核心原则

- 人拥有问题、架构、验收、非目标和停止边界。
- 有证据支持的“无需修改”是合法结果。
- 单 consumer 需求保持局部，除非真实边界或第二个 consumer 证明共享合理。
- 持久机制必须服务当前 consumer 或具体高后果风险。
- 内部 bug 保持可见；可选降级必须狭窄且显式。
- 源码检查、测试、构建、Smoke、Pilot 与 Final 支持不同声明。
- 只有收益大于协调成本时才使用多个 Agent。
- 相称证据回答目标后立即停止。

<a id="project-structure"></a>
## 项目结构

```text
.
├── AGENTS.md
├── .codex/{config.toml,agents/}
├── plugin and marketplace metadata
├── skills/kiss-my-agent/
├── skills/kiss-my-agent-setup/{SKILL.md,scripts/setup.py}
├── docs/{INSTALLATION,CONFIGURATION,TESTING,EXTENDING,FAQ}{,.zh-CN}.md
├── scripts/{validate.py,validate.sh,validate.ps1,build_site.py}
├── tests/
├── CONTRIBUTING{,.zh-CN}.md
├── SECURITY{,.zh-CN}.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

面向 Codex 的 instructions、Skill 内容、Rules、Cases、角色 TOML、`LICENSE` 和 `CODE_OF_CONDUCT.md` 保持英文，使 runtime 表面只有一个权威语言版本。

<a id="pages-status"></a>
## 文档站点状态

文档站点已发布[英文版](https://aoiota.github.io/Kiss-My-Agent/)与[简体中文版](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)。使用以下命令在本地构建并验证：

```bash
python3 -m pip install -r requirements-site.txt
python3 -m unittest tests.test_build_site
python3 scripts/build_site.py --output _site
```

`_site/` 是已忽略的本地产物。Pages workflow 通过 GitHub Actions 从 `main` 发布。绿色 workflow 与真实 HTTP 响应是不同证据；部署后应验证两个语言 URL。

<a id="validation-boundaries"></a>
## 验证边界

静态验证可以检查仓库结构、TOML 语法、standalone role identity、Skill 路由、双语文档一致性、相对链接、instruction fixtures、shell 语法和资产。它不能证明 plugin 发布、marketplace 安装、模型服从性、研究有效性、认证、网络访问、文件系统权限或未来 Host 兼容性。

Setup `check` 只证明它检查的文件与 managed content。真实 `/skills` 结果只证明该会话完成发现。角色 Smoke 只证明观察到的无害任务。详见[测试](docs/TESTING.zh-CN.md)。

<a id="documentation"></a>
## 文档

- [Installation](docs/INSTALLATION.md) / [安装](docs/INSTALLATION.zh-CN.md)
- [Configuration](docs/CONFIGURATION.md) / [配置](docs/CONFIGURATION.zh-CN.md)
- [Testing](docs/TESTING.md) / [测试](docs/TESTING.zh-CN.md)
- [Extending](docs/EXTENDING.md) / [扩展](docs/EXTENDING.zh-CN.md)
- [FAQ](docs/FAQ.md) / [常见问题](docs/FAQ.zh-CN.md)
- [Contributing](CONTRIBUTING.md) / [贡献](CONTRIBUTING.zh-CN.md)
- [Security](SECURITY.md) / [安全](SECURITY.zh-CN.md)

<a id="limitations"></a>
## 局限

- 早期源码分发；不声明兼容性与 release 保证。
- Codex 优先；其他 Host 尚未验证。
- Instructions 不授予文件系统、网络、账户或认证权限。
- 人工 scenarios 与 Smoke 检查不是行为资格认定或研究证据。
- 项目专有的安全、合规和领域规则仍由采用者负责。

<a id="license"></a>
## 许可证

[MIT](LICENSE)
