![KISS My Agent 主视觉：复杂的 Agent 路径汇聚为一个清晰结果](assets/kiss-my-agent-hero.png)

# KISS My Agent

**Keep It Simple, Scientist. Less ceremony. More science.**

[English](README.md) | [简体中文](README.zh-CN.md)

[![许可证：MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![状态：早期阶段](https://img.shields.io/badge/status-early_stage-orange.svg)
![宿主：Codex 优先](https://img.shields.io/badge/host-Codex--first-blue.svg)

<a id="overview"></a>
## 概览

KISS My Agent 是面向科研型编码 Agent 的紧凑指令层。人掌握研究目标、架构、验收标准、非目标和停止边界；Agent 在边界内作实现决策，优先选择最小充分改动，让失败保持可见，并且只按证据实际支持的层级汇报结果。

本仓库以 Codex 为首要宿主，提供项目指令、一个窄路由 Skill、三个带前缀的自定义角色、默认启用并注册这些角色的项目配置、静态验证和开发者文档。它不是 installer、工作流平台、权限系统或行为保证。

<a id="quick-start"></a>
## 快速开始

运行操作系统对应的原生 validator。前置条件为 Python 3.11 或更高版本：Linux 或 macOS 使用 `python3`；Windows wrapper 可使用 `py -3` launcher 或 `python`。

Linux 或 macOS（POSIX shell）：

```bash
cd /absolute/path/to/kiss-my-agent
./scripts/validate.sh
```

Windows（原生 PowerShell；WSL 不属于 Windows 路径）：

```powershell
Set-Location C:\absolute\path\to\kiss-my-agent
.\scripts\validate.ps1
```

要检查真实发现行为，请信任该项目并启动新的已认证会话：

```bash
cd /absolute/path/to/kiss-my-agent
codex
```

```powershell
Set-Location C:\absolute\path\to\kiss-my-agent
codex
```

在新会话中运行 `/skills`、确认 `kiss-my-agent`，并按[测试](docs/TESTING.zh-CN.md)对已注册的 `kiss_explorer`、`kiss_coder` 和 `kiss_reviewer` 角色做 Smoke。

仓库跟踪的 [`.codex/config.toml`](.codex/config.toml) 只启用 multi-agent 并注册这三个角色。它不选择模型、权限模式、上下文上限、并发上限、信任策略或凭证。项目配置需要项目可信并启动新会话；已在运行的旧会话不保证热加载配置、Skills、instructions 或角色。

<a id="components"></a>
## 组件

- [`AGENTS.md`](AGENTS.md)：永久的人与 Agent 边界。
- [`.agents/skills/kiss-my-agent/`](.agents/skills/kiss-my-agent/)：含两个 Rules 和四个 Cases 的精确 Skill 入口。
- [`.codex/config.toml`](.codex/config.toml)：项目级 multi-agent 启用与三个前缀角色注册。
- [`.codex/agents/`](.codex/agents/)：`kiss_explorer`、`kiss_coder` 和 `kiss_reviewer` 定义。
- [`scripts/validate.sh`](scripts/validate.sh) 与 [`scripts/validate.ps1`](scripts/validate.ps1)：原生静态验证入口。
- [`tests/`](tests/)：分层 instruction fixtures 和人工 scenarios。
- 英文优先、结构同步的简体中文配套文档。

采用到其他项目时始终显式操作并避免冲突。文档中的复制命令绝不覆盖已有配置、instructions、Skills 或角色。详见[安装](docs/INSTALLATION.zh-CN.md)。

<a id="platform-support"></a>
## 平台支持

| 平台 | 原生命令 | 证据状态 |
| --- | --- | --- |
| Linux | `./scripts/validate.sh` | 已在当前 checkout 本地执行；精确结果以命令输出为准。 |
| macOS | `./scripts/validate.sh` | CI 目标。精确 commit 的 macOS job 变绿前，不描述为已验证。 |
| Windows | 在原生 PowerShell 中运行 `.\scripts\validate.ps1` | CI 目标。精确 commit 的 Windows job 变绿前，不描述为已验证。WSL 只算 Linux 证据。 |

[`Validate` workflow](.github/workflows/validate.yml) 运行原生 wrappers。存在 workflow 定义不等于平台已经通过；精确 commit 上的绿色 jobs 才是权威证据。

静态验证不需要 Codex sandbox package、复制的 `CODEX_HOME`、容器、虚拟机或额外测试项目。“无需 sandbox”表示 validator 作为普通本地脚本运行；它不表示需要 `danger-full-access`，也不表示绕过 Host 权限控制。真实 Codex 检查可能更新 trust、历史或缓存等正常 Host 状态。

<a id="runtime-configuration"></a>
## 运行配置

主线程使用 Host、CLI、用户配置、Profile 与可信项目配置共同决定的实际设置。项目没有 `master.toml`。角色文件包含可编辑的角色专用模型、reasoning 与 sandbox 示例；项目配置只负责启用和注册。

无需修改仓库，即可为单次启动禁用所有自定义 Agent：

```bash
codex --config agents.enabled=false
```

```powershell
codex --config agents.enabled=false
```

修改模型、权限、上下文、并发或注册前，请阅读[配置](docs/CONFIGURATION.zh-CN.md)。

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
├── .agents/skills/kiss-my-agent/
├── .codex/{config.toml,agents/}
├── docs/{INSTALLATION,CONFIGURATION,TESTING,EXTENDING,FAQ}{,.zh-CN}.md
├── scripts/{validate.py,validate.sh,validate.ps1}
├── tests/
├── CONTRIBUTING{,.zh-CN}.md
├── SECURITY{,.zh-CN}.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

面向 Codex 的 instructions、Skill 内容、Rules、Cases、角色 TOML、`LICENSE` 和 `CODE_OF_CONDUCT.md` 保持英文，使运行时表面只有一个权威语言版本。

<a id="validation-boundaries"></a>
## 验证边界

静态验证可以检查仓库结构、TOML 语法与注册、Skill 路由、双语文档一致性、相对链接、instruction fixtures、shell 语法和资产。它不能证明模型服从性、研究有效性、认证、网络访问、文件系统权限、外部集成或未来 Host 兼容性。

真实 `/skills` 检查只证明该会话完成发现。角色 Smoke 只证明该角色能执行所用的无害任务；两者都不证明未来行为，也不授予权限。详见[测试](docs/TESTING.zh-CN.md)。

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
- 模型与 reasoning 可用性取决于 Host。
- 人工 scenarios 与 Smoke 检查不是行为资格认定或研究证据。
- 项目专有的安全、合规和领域规则仍由采用者负责。

<a id="license"></a>
## 许可证

[MIT](LICENSE)
