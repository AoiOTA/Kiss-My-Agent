# 贡献

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

<a id="before-you-start"></a>
## 开始之前

先阅读 [`AGENTS.md`](AGENTS.md)。修改 Skill、Rule 或 Case 时还要阅读[扩展](docs/EXTENDING.zh-CN.md)。Runtime 和测试行为分别由[配置](docs/CONFIGURATION.zh-CN.md)与[测试](docs/TESTING.zh-CN.md)说明。

提案会改变 plugin/marketplace 布局、setup scope、角色 schema、Skill trigger 边界、Pages 发布或永久规则时先开 issue。小型、有界修正可以直接提交 pull request。安全报告遵循[安全说明](SECURITY.zh-CN.md)；行为规范问题遵循仅英文的 [Code of Conduct](CODE_OF_CONDUCT.md)。

<a id="change-boundaries"></a>
## 修改边界

- 保持人对目标、架构、验收、非目标和停止边界的所有权。
- 保持 `$kiss-my-agent` 精确路由且 non-catch-all。
- 只有反复出现的方法才新增 Rule，只有有用的具体对照才新增 Case。
- 没有当前已批准 consumer 时，不扩张 setup、workflow、release、compatibility、telemetry、scoring 或 evaluation machinery。
- 保持三个 owner：config 中的两个公开开关、standalone role TOML discovery，以及 AGENTS 中的动态调度。Config 不得枚举角色文件。
- 把三个提供的角色视为可编辑 seeds，而不是封闭 catalog；角色 `name` 是身份，文件名只是约定。
- 保留用户和其他 Agent 的无关改动；范围外重构与格式化不得进入 diff。
- 每份英文开发者文档与简体中文配套文件必须同步：语言切换、显式 anchor IDs、章节顺序和 fenced command blocks。
- 面向 Codex 的 AGENTS、Skill、Rules、Cases、角色 TOML、`LICENSE` 与 `CODE_OF_CONDUCT.md` 只保留英文。
- 绝不加入凭证、私有路径、私有数据、日志、sessions 或生成的测试内容。

<a id="local-validation"></a>
## 本地验证

Linux 或 macOS：

```bash
./scripts/validate.sh
```

Windows 原生 PowerShell：

```powershell
.\scripts\validate.ps1
```

修改文档站点时：

```bash
python3 -m unittest tests.test_build_site
python3 scripts/build_site.py --output _site
```

`_site/` 是已忽略的本地产物。首次部署 Pages 响应返回 HTTP 200 前保持 README 语言链接为相对路径。WSL 属于 Linux 证据。不能仅凭配置声称 macOS 或 Windows 已验证；必须有精确 commit 上的原生绿色 CI job。Discovery 改变时使用可信新 Codex 会话；当前旧会话不保证热加载。

<a id="pull-requests"></a>
## Pull Requests

说明用户可见结果、当前 consumer、保留的最小机制、已执行验证、证据层级和局限。静态检查通过不证明模型行为或产品验收。Pull request 保持聚焦并使用仓库模板。

参与本项目即表示同意遵守 [Code of Conduct](CODE_OF_CONDUCT.md)。
