# 扩展 KISS My Agent

[English](EXTENDING.md) | [简体中文](EXTENDING.zh-CN.md)

[README](../README.zh-CN.md) · [测试](TESTING.zh-CN.md) · [贡献](../CONTRIBUTING.zh-CN.md)

<a id="scope"></a>
## 范围

只有当前反复出现的歧义尚未被覆盖时才扩展仓库。目标是用更少机制做出更好决策，而不是扩大 handbook。

<a id="choose-owner"></a>
## 选择 Owner

- 只有简短、永久且广泛适用的边界才修改 [`AGENTS.md`](../AGENTS.md)。
- 多个当前场景需要同一种可复用决策方法时修改 Rule。
- 一个具体对照能让现有 Rule 更容易应用时新增或修改 Case。
- 只有角色 owner 或真实 runtime 需求改变时才修改角色 TOML。
- 安装、配置、测试、安全或贡献事实改变时修改开发者文档。

不要在多个 owner 复制同一事实。Rules 扩展 `AGENTS.md`；Cases 只说明 Rules，不重新定义它们。

<a id="preserve-routing"></a>
## 保持精确路由

[`SKILL.md`](../.agents/skills/kiss-my-agent/SKILL.md) 必须保持 non-catch-all。常规实现、机械编辑、测试、构建、Git 操作、查询和格式化都不进入 Skill。一个歧义路由到一个 Rule，并且只在有用时读取一个 Case。

<a id="add-rule"></a>
## 新增 Rule

先找出至少两个需要同一种方法的当前场景，并说明永久 AGENTS 边界为何不足。新增内容保持增量；只有 trigger 能精确选择时才从 Skill 链接；避免重复现有失败、证据或 owner 指导。

<a id="add-case"></a>
## 新增 Case

Case 保持以下精确章节顺序：

1. Goal
2. Consumer
3. Minimum mechanism to retain
4. Mechanism to reject
5. Deletion counterfactual
6. Legitimate exception

它只说明现有 Rule，不创建新要求。相同语义对照已经存在时，应修改现有 Case。

<a id="update-runtime-docs"></a>
## 更新 Runtime 与文档

修改注册或角色设置时，保持 `.codex/config.toml`、`.codex/agents/`、Configuration、Testing、两份 README 和带注释示例一致。没有当前 consumer 时，不新增模型 fallback、权限 fallback、preset matrices 或 compatibility wrappers。

修改英文开发者文档时，同步更新简体中文配套文件，保持相同显式 anchor IDs、章节顺序和 fenced command blocks。面向 Codex 的 AGENTS、Skill、Rules、Cases、角色 TOML、`LICENSE` 和 `CODE_OF_CONDUCT.md` 保持英文。

<a id="validate"></a>
## 验证

Linux 或 macOS：

```bash
./scripts/validate.sh
```

Windows 原生 PowerShell：

```powershell
.\scripts\validate.ps1
```

导航、tables、badges、Mermaid 或 assets 改变时检查渲染 Markdown。发现行为改变时使用可信新 Codex 会话；旧会话不保证热加载。

<a id="stop-boundary"></a>
## 停止边界

用最小清晰新增解决歧义后立即停止。不要附带增加 governance、安装自动化、telemetry、scoring、release machinery 或推测性兼容。
