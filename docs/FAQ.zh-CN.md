# 常见问题

[English](FAQ.md) | [简体中文](FAQ.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md)

<a id="what-is-kiss"></a>
## 这里的 KISS 是什么？

“Keep It Simple, Scientist”：为当前问题选择最小充分实现和证据，同时保持真实契约、安全与失败可见性。

<a id="install"></a>
## 主安装路径是什么？

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

启动新会话，运行 `$kiss-my-agent-setup set up this project`，再启动一个新会话并运行 `$kiss-my-agent-setup check this project`。Git-backed marketplace 远程安装之前必须存在 `v0.1.0` Git tag；当前 source/static 证据不是发布证据。

<a id="global"></a>
## 项目 setup 会全局安装吗？

不会。全局 setup 必须使用显式 `$kiss-my-agent-setup set up globally` 命令。项目与全局 check/remove 命令也彼此独立。

<a id="when-skill"></a>
## 何时调用 `$kiss-my-agent`？

用于非显然持久机制、局部修复与新系统、实验有效性、证据强度、runtime/evaluator 歧义或重大范围扩张。普通实现、测试、构建、Git、查询和格式化不需要它。`$kiss-my-agent-setup` 是另一个用于显式 setup/check/remove 请求的操作型 Skill。

<a id="fixed-workflow"></a>
## 它会运行固定工作流吗？

不会。`.codex/config.toml` 启用能力，standalone role TOML 文件被自动发现，AGENTS 指导让主线程动态调度。有界工作可以保持单线程；只有委派收益大于协调成本时才使用 delegation。

<a id="no-change"></a>
## 无需修改也能成功吗？

可以。证据可能说明当前行为已满足目标、故障不成立，或根因位于授权范围外。

<a id="project-config"></a>
## 跟踪的项目 config 做什么？

它显式设置 `features.multi_agent = true` 与 `agents.enabled = true`，不枚举角色，也不设置模型、effort、trust、权限、上下文、并发、provider、认证或 telemetry。

<a id="roles"></a>
## 三个角色是固定的吗？

不是。它们是 seed standalone TOML files，不是封闭 catalog。`name` 字段是身份；文件名只是约定。Models 与 efforts 在省略时继承 Host 取值，并且可编辑。移除角色会让它离开 discovery；普通会话与 `check` 不会重新创建它。

<a id="disable-agents"></a>
## 如何为单次启动禁用？

```bash
codex --config features.multi_agent=false --config agents.enabled=false
```

实际生效的显式 `false` 仍是权威取值。Setup 不得静默撤销用户或管理员的禁用。

<a id="existing-files"></a>
## 已经有 config、AGENTS 或角色怎么办？

保留无关内容。Setup 只合并 KISS-managed content，并在 identity、ownership 或 managed-block 冲突时停止。所选 scope 中存在 `AGENTS.override.md` 时，setup 会停止，而不是写入 override 或把 base 文件藏在它下方。

<a id="remove"></a>
## Remove 会删除什么？

只删除明确选择的项目或全局 scope 中 KISS-managed content。Owner 不清或用户编辑过的内容会被保留并报告为冲突。移除 setup 输出不会卸载 plugin。

<a id="sandbox"></a>
## 测试需要 sandbox 吗？

静态验证不需要 Codex sandbox package。这不要求 `danger-full-access`，也不绕过 OS 与 Host 权限。真实 discovery 可能更新正常 Host-owned trust、历史或缓存状态。

<a id="confirm-installation"></a>
## 如何确认安装？

应分开证据：source/static validation、setup `check`、可信新会话中的 `/skills` 与无害角色 Smoke 各自只证明自己的表面。详见[测试](TESTING.zh-CN.md)。

<a id="pages"></a>
## Pages 站点在哪里？

Stage 1 本地构建支持已经准备好，但 README 有意保持相对语言链接。只有首次部署响应返回 HTTP 200 后才能发布 Pages URL；不要传播部署前返回 404 的 URL。

<a id="windows-wsl"></a>
## WSL 是 Windows 测试路径吗？

不是。WSL 使用 Linux wrapper，只产生 Linux 证据。Windows 支持使用原生 PowerShell 中的 `scripts\validate.ps1`。

<a id="other-hosts"></a>
## 其他 Host 可以使用吗？

内容可能可以适配，但仓库以 Codex 为首要 Host；其他 Host 尚未验证。
