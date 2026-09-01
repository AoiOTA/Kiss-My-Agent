# 安装与共存

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="release-status"></a>
## 发布状态

Git-backed marketplace 已为 `v0.1.0` 做好准备，但 Git tag 存在之前 Codex 无法远程安装该版本。当前证据是源码检查与静态验证，不是发布、远程安装或真实发现。不要把下列命令理解为该 tag 已经可用的声明。

<a id="install-plugin"></a>
## 安装 Plugin

带 tag 的 marketplace 版本可用后，使用公开安装接口：

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

安装后启动新的已认证 Codex 会话。已在运行的会话不保证发现新安装的 plugin 或 Skill。

<a id="project-setup"></a>
## 设置一个项目

在目标项目中新开的会话里运行：

```text
$kiss-my-agent-setup set up this project
```

项目 setup 只管理所选项目：

- `.codex/config.toml`：合并两个公开开关，不替换无关设置。
- `.codex/agents/`：三个 standalone seed role 文件。
- `AGENTS.md`：有界 KISS managed block，保留无关 instructions。

Skill 仍归 plugin 所有；setup 不会把 Skill tree 复制进项目。它也不会建立 Host trust 或重启 Codex。

通过 Host 信任项目，另开一个新会话，然后运行：

```text
$kiss-my-agent-setup check this project
```

只有需要真实发现证据时，才继续使用 `/skills` 和[测试](TESTING.zh-CN.md)中的无害检查。

<a id="global-setup"></a>
## 全局设置

全局 setup 是可选操作，绝不会从项目请求推断。必须明确请求：

```text
$kiss-my-agent-setup set up globally
```

它管理 `$CODEX_HOME` 下对应的 `config.toml`、`agents/` 与 AGENTS managed block。启动新会话，然后显式检查该 scope：

```text
$kiss-my-agent-setup check global setup
```

行为只属于特定项目时优先使用项目 scope。全局 scope 会影响加载用户配置的每个项目，但仍受实际 Host、管理员、用户与项目设置约束。

<a id="collision-policy"></a>
## 冲突与 Override 策略

| 已有状态 | 必须采取的行为 |
| --- | --- |
| 无关 config keys 或 AGENTS 内容 | 保留。 |
| 任一公开开关被有意设为 `false` | 保留并报告 `disabled`；不静默重新启用。 |
| 具有预期 `name` 的已有 seed 文件，包括用户编辑 | 保留。 |
| 文件名/identity 不匹配、重复 identity 或 project/global seed-name 冲突 | 停止并审核；不要覆盖。 |
| 已有有效 KISS managed content | 精确 setup 按幂等处理。 |
| 损坏或重复的 managed block | 停止且不得声称成功。 |
| 所选 scope 存在 `AGENTS.override.md` | 停止。不得写入 override，也不得把内容藏在低优先级 base 文件。 |

Setup 操作只做最小 scope-owned 改动。它不替换已有 config、不发明 compatibility alias，也不会把项目 setup 转换为全局 setup。

<a id="role-lifecycle"></a>
## 角色生命周期

提供的 `kiss_explorer`、`kiss_coder` 与 `kiss_reviewer` definitions 是 seeds，不是封闭 catalog。Standalone role TOML 会被自动发现；`name` 字段是身份，文件名只是约定。Model 与 effort 在省略时继承 Host 取值，并且可编辑。

用户可以新增、编辑、重命名或删除角色。首次 setup 后，普通会话、setup 与 `check` 会保留当前 catalog，绝不会重新创建已删除文件。

<a id="check-and-remove"></a>
## 检查或移除

使用匹配的显式 scope：

```text
$kiss-my-agent-setup check this project
$kiss-my-agent-setup remove from this project

$kiss-my-agent-setup check global setup
$kiss-my-agent-setup remove global setup
```

`check` 检查 managed filesystem state；它不证明 trust、活动会话加载、plugin 发布或角色行为。`remove` 只针对所选 scope 与 KISS-managed content。它必须保留无关设置、instructions 与角色；owner 不清或有冲突编辑时应停止，而不是删除。

移除后启动新会话再判断 discovery。移除 setup 输出不会卸载 plugin 本身；plugin 生命周期仍由 Codex plugin 操作管理。

<a id="source-tools"></a>
## Source Checkout 工具

贡献者无需安装 plugin 即可验证 checkout：

```bash
python3 scripts/validate.py
```

底层 setup utility 可用于隔离测试与开发：

```bash
python3 skills/kiss-my-agent-setup/scripts/setup.py setup --scope project --target /absolute/path/to/project
python3 skills/kiss-my-agent-setup/scripts/setup.py check --scope project --target /absolute/path/to/project
python3 skills/kiss-my-agent-setup/scripts/setup.py remove --scope project --target /absolute/path/to/project
```

全局操作使用 `--scope global`；显式隔离目标可使用 `--codex-home`。直接 source-tool 成功属于静态文件系统证据，不是 marketplace 安装成功或真实 Codex 会话。

<a id="fresh-session"></a>
## 新会话边界

Plugin 安装与 setup 都属于 startup/discovery 改变。安装 plugin 后使用一个新会话；setup、remove 或角色/config 改变后再使用一个新会话。当前会话不保证热加载。汇报真实结果时记录 Host 版本、scope、trust state 与 session freshness。
