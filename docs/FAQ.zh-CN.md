# 常见问题

[English](FAQ.md) | [简体中文](FAQ.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md)

<a id="what-is-kiss"></a>
## 这里的 KISS 是什么？

“Keep It Simple, Scientist”：为当前问题选择最小充分实现和证据，同时保持真实契约、安全与失败可见性。

<a id="when-skill"></a>
## 何时调用 `$kiss-my-agent`？

用于非显然持久机制、局部修复与新系统、实验有效性、证据强度、runtime/evaluator 歧义或重大范围扩张。不要用于普通实现、测试、构建、Git、查询或格式化。

<a id="fixed-workflow"></a>
## 它会运行固定工作流吗？

不会。一个歧义路由到一个 Rule，并可选读取一个 Case。有界工作可以保持单线程；只有委派收益大于协调成本时才使用 delegation。

<a id="no-change"></a>
## 无需修改也能成功吗？

可以。证据可能说明当前行为已满足目标、故障不成立，或根因位于授权范围外。

<a id="project-config"></a>
## 跟踪的项目 config 做什么？

它启用自定义 Agent，并且只注册 `kiss_explorer`、`kiss_coder` 和 `kiss_reviewer`。它不设置 trust、模型、权限、上下文、并发、provider、认证或 telemetry。项目 config 需要 trust 和新会话；旧会话不保证热加载。

<a id="disable-agents"></a>
## 如何为单次启动禁用自定义 Agent？

```bash
codex --config agents.enabled=false
```

```powershell
codex --config agents.enabled=false
```

<a id="existing-files"></a>
## 已经有 config、AGENTS、Skills 或角色怎么办？

保留它们。只使用一个 Skill scope，人工合并 config 与 AGENTS，并且只有精确前缀名不存在时才增加角色。[安装说明](INSTALLATION.zh-CN.md)使用冲突检查和 exclusive 文件创建。

<a id="models-permissions"></a>
## 可以修改角色模型或权限吗？

可以，但取值必须受 Host 支持，而且权限改变必须符合意图。Instructions 不是安全边界。项目不提供自动模型或权限 fallback。

<a id="sandbox"></a>
## 测试需要 sandbox 吗？

静态验证不需要 Codex sandbox package，运行原生脚本即可。这不要求 `danger-full-access`，也不绕过普通 OS 和 Host 权限。真实发现可能写入正常 Host 管理的 trust、历史或缓存状态。

<a id="windows-wsl"></a>
## WSL 是 Windows 测试路径吗？

不是。WSL 使用 Linux wrapper，只产生 Linux 证据。Windows 支持使用原生 PowerShell 中的 `scripts\validate.ps1` 测试。

<a id="confirm-installation"></a>
## 如何确认发现？

信任项目，启动新的已认证会话，运行 `/skills`，并 Smoke 三个已注册角色。详见[测试](TESTING.zh-CN.md)。发现与 Smoke 都只是窄证据，不是行为保证。

<a id="validation-proof"></a>
## 验证证明什么？

只证明输出与源码明确检查的 invariants。绿色 CI job 只适用于对应平台、job 与精确 commit。静态验证不证明模型服从、权限、认证、研究有效性或未来兼容性。

<a id="other-hosts"></a>
## 其他 Host 可以使用吗？

内容可能可以适配，但仓库以 Codex 为首要 Host；其他 Host 尚未验证。

<a id="ci-status"></a>
## macOS 和 Windows 已验证吗？

它们是 CI 目标。精确 commit 的 [`Validate` workflow](../.github/workflows/validate.yml) 在对应平台变绿前，不得称为已验证。存在 workflow 定义不等于已有通过证据。
