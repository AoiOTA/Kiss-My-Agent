# 测试

[English](TESTING.md) | [简体中文](TESTING.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="test-surfaces"></a>
## 测试表面

KISS My Agent 有四个彼此不同的测试表面：

1. 仓库文件的原生静态验证。
2. 对一个显式文件系统 scope 的 setup `check`。
3. 可信新 Codex 会话中 plugin Skills 与 standalone roles 的真实发现。
4. 每个角色只验证一项窄职责的无害 Smoke。

不要把这些结果合并成更强声明。静态 PASS 不等于 setup 或发布证据；setup `check` 不等于真实发现；发现不等于行为资格认定；Smoke 也不是研究或产品证据。

<a id="static-validation"></a>
## 静态验证

前置条件为 Python 3.11 或更高版本。Linux 或 macOS 的 POSIX wrapper 使用 `python3`；Windows wrapper 可使用 `py -3` launcher 或 `python`。

Linux 或 macOS：

```bash
cd /absolute/path/to/kiss-my-agent
./scripts/validate.sh
```

Windows 原生 PowerShell：

```powershell
Set-Location C:\absolute\path\to\kiss-my-agent
.\scripts\validate.ps1
```

WSL 使用 Linux 命令，只产生 Linux 证据，不产生 Windows 证据。[`Validate` workflow](../.github/workflows/validate.yml) 执行原生 wrappers。配置了 CI job 不等于测试通过；必须引用精确 commit 上的绿色 job。

Validator 不需要 Codex sandbox package、复制的 `CODEX_HOME`、容器、虚拟机或额外测试项目。它只检查输出和源码明确列出的属性。

<a id="project-defaults"></a>
## 项目默认值

跟踪的 `.codex/config.toml` 显式设置 `features.multi_agent = true` 与 `agents.enabled = true`，且不枚举角色。Host 自动发现 standalone role TOML；每个文件的 `name` 字段是身份，文件名只是约定。

提供的三个角色是可编辑 seeds，不是封闭 catalog。配置不选择 trust、模型、权限、上下文、并发、provider 或凭证。角色 model 与 effort 在省略时继承 Host 设置。Host 必须先信任项目，项目 config 才能加载；实际生效的显式 `false` 仍表示禁用。

<a id="setup-check"></a>
## Setup 检查

Setup 后启动新会话，并检查同一显式 scope：

```text
$kiss-my-agent-setup check this project
$kiss-my-agent-setup check global setup
```

只使用与已修改 scope 匹配的命令。Setup `check` 支持关于其检查的 managed config、standalone seed files 与 AGENTS block 的声明。它不建立项目 trust、不证明活动会话 discovery、不恢复已删除角色，也不会把 source/static 证据提升为远程安装证据。

<a id="fresh-session"></a>
## 可信新会话

安装 plugin 或修改 config、instructions、Skills、角色 TOML 后，关闭或离开旧会话，再从仓库根目录启动新的已认证会话。

Linux 或 macOS：

```bash
cd /absolute/path/to/kiss-my-agent
codex
```

Windows 原生 PowerShell：

```powershell
Set-Location C:\absolute\path\to\kiss-my-agent
codex
```

Host 提示时通过其界面建立项目 trust。当前已在运行的会话不保证热加载以上任何表面，因此旧会话的结果不能证明新项目 config 已经或没有加载。

<a id="skill-smoke"></a>
## Skill 发现 Smoke

在可信新会话中运行 `/skills`，确认 plugin-owned `kiss-my-agent` 与 `kiss-my-agent-setup` entries。然后只针对匹配的非显然机制或证据决策调用 `$kiss-my-agent`。Setup Skill 只用于显式 project/global setup、check 与 remove 操作。

这只证明该会话与该 prompt 的发现和路由，不证明未来 prompt 的服从性。

<a id="role-smoke"></a>
## 三角色 Smoke

使用 Host 自定义 Agent 界面，或明确要求主线程委派给指定已发现角色。逐个运行并保持任务无害：

1. `kiss_explorer`：要求它只读 `README.md`、列出显式 HTML anchor IDs，且不作修改。
2. `kiss_coder`：要求它仅在 `tests/.kiss-coder-smoke.txt` 不存在时创建该文件、写入一行、报告后只删除这个自有文件；路径已存在时必须停止且不覆盖。
3. `kiss_reviewer`：把当前文档 diff 交给它，要求只读报告带精确位置的实质 findings，不编辑文件。

Smoke 前后都检查 working tree，并保留无关改动。Coder Smoke 若在创建后中断，可能遗留该命名文件；确认它确属 Smoke 产物后才能移除。

预期 owner 分别是只读 explorer、在分配内改变状态的 coder，以及独立只读 reviewer。成功调用只支持角色发现和已观察的窄行为。

<a id="manual-scenarios"></a>
## 人工 Scenarios

[`tests/scenarios.md`](../tests/scenarios.md) 是用于讨论永久规则与 Skill 路由的 fixtures。它们不是自动评分、release gates，也不保证所有模型行为一致。

<a id="evidence-boundaries"></a>
## 证据边界

| 证据 | 支持 | 不支持 |
| --- | --- | --- |
| 源码检查 | 跟踪文件写了什么 | 实际加载的 runtime identity 或行为 |
| 静态 validator PASS | 被检查的仓库 invariants | Plugin 发布、Agent 服从、Host 支持、研究有效性 |
| Setup `check` PASS | 对应显式 scope 的 managed files | Trust、活动加载、远程安装、角色行为 |
| CI 绿色 job | 对应 job、平台和 commit 上原生 wrapper PASS | 所有 OS 版本或未来兼容性 |
| `/skills` 发现 | Plugin Skills 在该新会话可见 | 未来服从性或权限 |
| 单次角色 Smoke | 已发现角色完成该窄任务 | 通用角色可靠性或产品验收 |
| 人工 scenario 讨论 | 人对该 Case 的解释 | 自动评估或资格认定 |

始终记录平台、原生 shell；归因需要时记录精确 commit；真实检查还应记录 Host 版本、项目是否可信以及会话是否为新会话。直接报告失败和未测试表面。

<a id="stop-boundary"></a>
## 停止边界

测试回答其既定问题后停止。不要为了制造信心重复 Smoke、创建持久测试安装，或把窄结果提升为兼容性或行为保证。
