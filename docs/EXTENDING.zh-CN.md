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
- 只有角色 owner 或真实 runtime 需求改变时才修改 standalone role TOML。其 `name` 字段是身份；文件名只是约定。
- 只有显式 project/global managed scope 或冲突策略改变时才修改 setup 逻辑。
- 安装、配置、测试、安全或贡献事实改变时修改开发者文档。

不要在多个 owner 复制同一事实。Rules 扩展 `AGENTS.md`；Cases 只说明 Rules，不重新定义它们。

<a id="preserve-routing"></a>
## 保持精确路由

Plugin-owned `kiss-my-agent` Skill 必须保持 non-catch-all。常规实现、机械编辑、测试、构建、Git 操作、查询和格式化都不进入 Skill。一个歧义路由到一个 Rule，并且只在有用时读取一个 Case。`kiss-my-agent-setup` 保持独立，并且只处理显式 setup/check/configure/remove 操作。

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

修改公开开关、standalone role discovery 或 setup scope 时，保持 `.codex/config.toml`、`.codex/agents/`、plugin metadata、Agent 原生 setup references、Configuration、Installation、Testing、两份 README 与带注释示例一致。`.codex/config.toml` 拥有四个 paths：成对的初始 Master defaults `gpt-5.6-sol` / `max` 与两个公开启用开关；它绝不枚举角色文件。可编辑的 fresh-setup seeds 显式默认使用 `gpt-5.6-sol`：explorer 和 coder 为 `high`，reviewer 为 `xhigh`。Plugin cache seeds 不会自动进入 Host catalog。它们不是封闭 catalog：fresh setup 创建缺失 starters，任何已经存在的角色都归用户所有，因此 setup 与 Plugin updates 永不覆盖、迁移或判定其版本。新版 model 或 effort 应通过 existing-role wizard 或手工 TOML edits 采用。没有当前 consumer 时，不新增模型 fallback、权限 fallback、preset matrices 或 compatibility wrappers。

修改英文开发者文档时，同步更新简体中文配套文件，保持相同显式 anchor IDs、章节顺序和 fenced command blocks。面向 Codex 的 AGENTS、Skill、Rules、Cases、角色 TOML、`LICENSE` 和 `CODE_OF_CONDUCT.md` 保持英文。

<a id="validate"></a>
## 验证

只修改 Plugin/Skill 时可以运行不需要第三方包的本地核心检查。Pull request CI 负责完整跨平台和站点套件：

```bash
python3 scripts/validate.py
python3 -m unittest tests.test_setup -v
```

导航、tables、badges、Mermaid 或 assets 改变时检查渲染 Markdown。发现行为改变时使用可信新 Codex 会话；旧会话不保证热加载。

Pages 变更应在部署前检查测试套件生成的隔离构建，随后验证已部署的英文根 URL 与中文 `zh-CN/` URL。README 语言链接应指向已验证的 Pages URL；不要替换为未经验证的部署目标。

<a id="stop-boundary"></a>
## 停止边界

用最小清晰新增解决歧义后立即停止。不要附带增加 governance、telemetry、scoring、release machinery 或推测性兼容。新的 setup 行为必须有当前安装 consumer，并保持显式 scope、冲突安全与可逆 ownership。
