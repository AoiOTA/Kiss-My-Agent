# 测试

[English](TESTING.md) | [简体中文](TESTING.zh-CN.md)

[README](../README.zh-CN.md) · [安装](INSTALLATION.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="test-surfaces"></a>
## 测试表面

KISS My Agent 有几个彼此不同的证据表面：

1. 仓库验证和确定性的贡献者测试。
2. 隔离文件系统 scope 中 Agent 原生 setup/check/remove/configure 行为。
3. 新 Codex 会话中的 Plugin 安装或升级与 Skill 发现。
4. 每个 standalone role 的窄范围观察行为。
5. 新用户对首页的理解。
6. 精确 commit 的原生 CI 与已部署 Pages 响应。

不要把这些结果合并成更强声明。源码检查不是真实发现，CI 不是行为保证，一次角色运行不是通用可靠性，文档构建也不能证明新用户看懂了产品。

<a id="user-verification"></a>
## 用户验证不需要 Python

安装或更新 Plugin 后启动新会话，并使用 Plugin-owned interfaces：

```text
$kiss-my-agent-setup set up this project
$kiss-my-agent-setup check this project
$kiss-my-agent-setup configure agents for this project
```

这些操作使用 Codex 文件工具，不需要 Python、Node.js、Docker 或包管理器。`check` 只证明检查到的文件状态。需要真实 discovery 证据时再使用 `/skills` 和窄范围 role Smoke。

<a id="contributor-suite"></a>
## 贡献者测试套件

只修改 Plugin/Skill 的贡献者需要 Python 3.11 或更高版本，但不需要第三方包。运行本地核心检查：

```bash
python scripts/validate.py
python -m unittest tests.test_setup -v
```

这些改动不要求本地构建站点。Pull request CI 会安装 `requirements-site.txt` 并运行 `python scripts/test_all.py`，执行静态验证、全部单元测试和临时目录中的文档构建。它不得留下 tracked 文件改动。Linux/macOS 与原生 Windows CI 使用同一个完整入口；shell wrappers 只检查各自平台的原生启动行为。

测试套件验证仓库拥有的契约。CI 若没有真实已认证 Codex 会话，就无法执行模型驱动的 setup workflow，因此这些场景必须标记为明确的 engineering runs，不能用伪单测代替。

<a id="setup-scenarios"></a>
## Agent 原生 Setup 场景

Setup 场景只能在一次性项目和明确隔离的 Codex home 中运行。保留 before/after 文件用于审查，但不要提交日志或临时用户数据。

必测场景包括：

- 空项目 setup、重复 setup、check 与 remove；
- 无关 config、comments、换行风格、AGENTS 内容和已有角色；
- 有意设置的 `false` 与有意删除的 seed roles；
- 损坏 TOML、不安全路径类型、`AGENTS.override.md`、重复名称、文件名/identity 不匹配和 project/global 冲突；
- remove 能作为 cross-scope seed-name 冲突的解除出口；
- remove 保留已修改角色；
- 只配置一个选中角色，其他字段和文件保持不变；
- 恢复继承时只删除选中的可选 key；
- 未单独确认时拒绝写入 `danger-full-access`；
- 与 v0.1.0 markers 创建的项目兼容。

模型驱动文件编辑期间的进程或机器崩溃不在事务证明范围内。应直接报告，而不能声称原子恢复。

<a id="local-plugin"></a>
## 测试修改后的 Plugin，而不是旧缓存

开发时使用隔离的本地 marketplace，让它预先指向被编辑 Plugin 的临时副本。使用当前 Plugin Creator helper 对该副本加入一个 Codex cachebuster，从该本地 marketplace 重新安装，然后启动新会话。

不得给 canonical release manifest 添加 cachebuster、手工编辑已配置 marketplace，也不得把 Git-backed v0.1.0 cache 当作工作树改动的证据。记录实际加载的 Plugin 版本和候选版本独有行为。

<a id="fresh-session"></a>
## 可信新会话

安装、升级、setup、remove 以及 config、instructions、Skills 或 roles 的改变都会影响启动与发现。应在目标项目中新开已认证会话，并在 Host 提示时通过界面建立 trust。

记录 OS、原生 shell、Codex 版本、Plugin 版本、source identity、scope、trust state，以及会话是否为新会话。旧会话不能证明新配置已加载或没有加载。

<a id="skill-smoke"></a>
## Skill 发现 Smoke

在新会话中运行 `/skills`，确认 Plugin-owned `kiss-my-agent` 和 `kiss-my-agent-setup` entries。然后：

- 只有真实存在非显然机制、scope、runtime/evaluator 或证据决策时才使用 `$kiss-my-agent`；
- 只有显式 setup/check/configure/remove 工作才使用 `$kiss-my-agent-setup`。

普通实现、测试、构建、Git、查询和格式化不应路由到 `$kiss-my-agent`。发现只证明该会话可见，不能保证未来遵循 instructions。

<a id="role-smoke"></a>
## 三角色 Smoke

使用 Host 自定义 Agent 界面，或明确要求主线程把一个有界任务委派给每个已发现角色：

1. `kiss_explorer`：读取 fixture 并报告准确 anchors，不编辑文件。
2. `kiss_coder`：只拥有一个隔离的一次性文件，仅在不存在时创建，验证后只删除该文件。
3. `kiss_reviewer`：检查给定 diff，报告带准确位置的实质 findings，不编辑文件。

前后都检查工作树和选定 fixtures。一次成功调用只支持角色发现和观察到的窄行为。

<a id="upgrade-smoke"></a>
## 升级 Smoke

使用隔离安装证明支持的迁移：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

从已安装 v0.1.0 开始，在真实 v0.2.0 tag 存在后刷新 marketplace，确认 installed cache 报告 0.2.0，然后打开新会话。验证 `configure agents` 等 v0.2.0 独有接口，再检查一个 v0.1-managed 一次性项目。同时执行文档中的固定 tag 回退。如果任一步失败，保留第一个决定性错误。

<a id="dogfooding"></a>
## 开发过程中的 Dogfooding

开发下一版本时，使用当前 KISS 项目 instructions 和适合的真实角色。记录它们在哪里减少了 scope、暴露了失败或改善了证据，也记录可复现的错误停止或不必要机制。

保持产品 runtime 与 evaluator owner 分离：被测 Plugin 不能定义自己的验收标准，也不能批准自己的 release。人类维护者拥有目标与验收；确定性测试、独立审查和新会话 replay 判断观察结果。Dogfooding 是 engineering evidence，不是自主自证。

<a id="readme-pilot"></a>
## README 新用户 Pilot

只把渲染后的首页交给一名没有参与改动的人，不额外解释，并要求其在五分钟内找出：

- 过度设计和过度防御这两种失败模式；
- Agent 为什么以及什么时候容易出现这些问题；
- KISS My Agent 怎样提供帮助、不能保证什么；
- 它是否适合自己的工作；
- 安装、第一次使用、Agent 配置和更新入口。

条件允许时，让对方在一次性项目中完成 setup，且不安装 Python。只记录匿名的通过/失败观察和阻塞性困惑。修订后复用同一清单，不得移动标准。

<a id="evidence-boundaries"></a>
## 证据边界

| 证据 | 支持 | 不支持 |
| --- | --- | --- |
| 源码检查 | 跟踪文件写了什么 | 实际加载的 runtime identity 或行为 |
| 静态/单元测试 PASS | 被测试的仓库 invariants | Agent 原生 workflow 行为 |
| Setup engineering run | 该 scope 和 prompt 下观察到的文件 | 未来模型一致性或崩溃原子性 |
| 精确 SHA 原生 CI | 该 job、平台、Python 和 commit | 所有 OS/client 版本或未来兼容性 |
| `/skills` 发现 | 该新会话中的 Skill 可见性 | 通用 instructions 遵循或权限 |
| Role Smoke | 观察到的窄角色任务 | 通用角色可靠性 |
| 新用户 Pilot | 该参与者的理解 | 通用可用性 |
| HTTP 200 加内容检查 | 已部署页面可访问及检查到的内容 | Plugin 安装或行为 |

直接报告失败和未测试表面。前置条件失败造成的 invalid run 不能变成产品负面证据。

<a id="stop-boundary"></a>
## 停止边界

既定问题得到相称证据后停止。不要重复模型 Smoke 来制造信心，不要为一次 release 检查建立永久 evaluation platform，也不要把窄结果提升为兼容性、行为、研究、认证、权限或安全保证。
