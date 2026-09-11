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

简单一次性任务直接使用普通单对话，不需要 setup 证据。若要在安装或更新 Plugin 后验证持久 KMA instructions，请启动新会话并使用 Plugin-owned interfaces：

```text
$kiss-my-agent:kiss-my-agent-setup set up this project
$kiss-my-agent:kiss-my-agent-setup check this project
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
```

这些操作使用 Codex 文件工具，不需要 Python、Node.js、Docker 或包管理器。Git-backed Plugin 的安装或刷新另行要求可用的 `git` executable 和 GitHub 网络访问。`check` 只证明检查到的文件状态。需要真实 discovery 证据时再使用 `/skills` 和窄范围 role Smoke。如果明确要求的 role Smoke 无法运行，应报告缺少 discovery 证据；直接执行不能证明角色加载。其他已授权且能力范围内的工作可以继续。

<a id="contributor-suite"></a>
## 贡献者测试套件

只修改 Plugin/Skill 的贡献者需要 Python 3.11 或更高版本，但不需要第三方包。运行本地核心检查：

```bash
python3 scripts/validate.py
python3 -m unittest tests.test_setup -v
```

这些改动不要求本地构建站点。Pull request CI 会安装 `requirements-site.txt` 并运行 `python scripts/test_all.py`，执行静态验证、全部单元测试和临时目录中的文档构建。它不得留下 tracked 文件改动。Linux/macOS 与原生 Windows CI 使用同一个完整入口；shell wrappers 只检查各自平台的原生启动行为。

测试套件验证仓库拥有的契约。CI 若没有真实已认证 Codex 会话，就无法执行模型驱动的 setup workflow，因此这些场景必须标记为明确的 engineering runs，不能用伪单测代替。v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` 已在 v0.2 移除；validation 应证明这个 breaking interface 已不存在，并确认文档路由到对话式 Skill，不能把 Agent 原生行为伪装成 deterministic CLI coverage。

<a id="setup-scenarios"></a>
## Agent 原生 Setup 场景

Setup 场景只能在一次性项目和明确隔离的 Codex home 中运行。保留 before/after 文件用于审查，但不要提交日志或临时用户数据。

必测场景包括：

- 空项目 setup、重复 setup、check 与 remove；
- 缺失 Master 字段分别补入 Astra/high，已有显式字段保留，缺失实验上下文补 true；`check` 验证字段存在与类型；
- 两个 feature switches 各自在缺失时添加，同时保留两个 switch paths 的 marked/unmarked values、无关 config、comments、换行风格、AGENTS 内容和已有角色；
- 只有两个旧顶层 `gpt-5.6-sol` / `max` lines 都准确出现一次并带准确 KISS marker 时才成对迁移，随后重复 setup 必须 no-op；
- 四类 near miss 都保留已有字段，仅补真正缺失字段：缺少 companion、pair 未标记、值已修改，以及用户自选 custom pair；duplicate 或 invalid assignments 仍属于 conflicts；
- 有意设置的 `false` 与有意删除的 seed roles；
- 损坏的 managed config 或准确 bundled-role TOML、不安全的 managed path type、`AGENTS.override.md`，以及准确 bundled filename/identity mismatch；无效的未选 custom role 不属于 KISS ownership，不会阻塞 setup、check、remove，也不会阻塞已经选择其他角色的配置请求；
- project 与 global scope 中同一个 bundled role filename 使用不同的可观察定义：project setup/check 只检查 project target 并保持 global role 不变；fresh project session 证明 Host 使用 project-over-global precedence，KISS 不拒绝也不协调这个 duplicate；
- remove 只删除带准确 marker 且值匹配的当前默认配置、任何准确的旧 marked Master pair，以及 current/v0.2.6/v0.2.5/v0.1 exact role seeds，并保留 unmarked config 与已修改角色；
- 只配置一个选中角色，其他字段和文件保持不变；
- 恢复继承时只删除选中的可选 key；
- fresh setup 创建缺失 roles 时设置 `model = "gpt-6-astra"` 与 `model_reasoning_effort = "medium"`，同时保留所有已有角色；
- 未单独确认时拒绝写入 `danger-full-access`；
- 把 v0.1.0 markers 创建的项目识别为 `outdated`，随后通过 setup 刷新可能更新的 managed block 与 config，同时所有角色文件直接保持不变；
- current 或 outdated managed block 下缺失的 starter 报告为 intentionally absent，而不是重建、outdated 或 incomplete。

模型驱动文件编辑期间的进程或机器崩溃不在事务证明范围内。应直接报告，而不能声称原子恢复。

<a id="local-plugin"></a>
## 测试修改后的 Plugin，而不是旧缓存

开发时使用隔离的本地 marketplace，让它预先指向被编辑 Plugin 的临时副本。使用当前 Plugin Creator helper 对该副本加入一个 Codex cachebuster，从该本地 marketplace 重新安装，然后启动新会话。

使用下面可直接复制的 Codex prompt：

```text
$plugin-creator update this existing KISS My Agent plugin for local development. Stage a disposable candidate copy outside the checkout in a separate local marketplace, point that marketplace only at the candidate copy, add exactly one +codex.<cachebuster> suffix to the copy's manifest version, reinstall it from that marketplace into an isolated Codex home, and tell me to start a new thread. Do not modify tracked release files or the Git-backed marketplace.
```

参见 OpenAI 官方的 [Plugin Creator 与 local marketplace 指南](https://developers.openai.com/plugins/build/plugins#package-with-plugin-creator)和[marketplace add/upgrade 命令](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli)。

不得给 canonical release manifest 添加 cachebuster、手工编辑已配置 marketplace，也不得把 Git-backed release cache 当作工作树改动的证据。记录实际加载的 Plugin 版本和候选版本独有行为。

<a id="fresh-session"></a>
## 可信新会话

安装、升级、setup、remove 以及 config、instructions、Skills 或 roles 的改变都会影响启动与发现。应在目标项目中新开已认证会话，并在 Host 提示时通过界面建立 trust。

记录 OS、原生 shell、Codex 版本、Plugin 版本、source identity、scope、trust state，以及会话是否为新会话。旧会话不能证明新配置已加载或没有加载。

测试真实 delegation 时使用普通新会话；使用 `codex exec` 时省略 `--ephemeral`。在一次 PawWeaver dogfood 对照中，同一可信项目使用 Codex CLI 0.153.4 与 KISS My Agent v0.2.7，`--ephemeral --json --sandbox read-only` 暴露了三个 KISS 角色与两个 Skill，但原生 `kiss_explorer` 创建两次均报 `no thread with id`。随后，不带 `--ephemeral` 的普通 `codex exec` 会话成功创建了一个原生 `kiss_explorer`，该子 Agent 完成只读调查并返回 findings。

将失败结果保留为 Host/会话测试失败：发现可见角色并未证明 delegation 可用，当时也没有子 Agent 结果。检查恢复时，应确认原生子 Agent 完成有界任务并返回结果；仅发现可见角色或成功创建子 Agent 都不够。这项观察不能确定根因，也不能证明 `--ephemeral` 普遍不兼容、CLI 0.153.4 全面兼容或 KISS 的有效性。

如果项目迁移或启动路径变化后命名角色消失，应对照当前启动路径、解析后的项目目录与 Host 持久保存的项目信任条目。Role TOML 文件存在，不代表该项目 scope 已加载。在另一项 CLI 0.153.4 的 PawWeaver 观察中，旧符号链接路径受信任，但规范启动目录未列入持久项目信任。临时 CLI trust override 未恢复发现；仅补入用户授权的规范项目路径信任条目后，普通新会话恢复了原生角色 catalog。随后三个原生 KISS 角色均完成有界只读任务，spawn 参数与子会话记录确认了角色身份及 Astra/medium 执行。这是项目信任与发现恢复，不是 KISS 代码缺陷，也不能证明更广泛的任务有效性。

在用户授权范围内，通过 Host 修复实际观察到的当前项目信任不匹配，保留已有条目，再检查新会话中的原生角色执行。Role 文件保持在原定项目 scope；这项观察不构成把角色移到 global scope、重装 Plugin 或修改无关 feature flags 的理由。文件存在、发现可见与原生子任务完成仍是不同层级的证据。

<a id="skill-smoke"></a>
## Skill 发现 Smoke

在新会话中运行 `/skills`，确认 canonical Plugin Skills `kiss-my-agent:kiss-my-agent` 与 `kiss-my-agent:kiss-my-agent-setup`；在已测试的 Codex 0.152.1 baseline 上，picker labels 可能显示为 `kiss-my-agent (kiss-my-agent)` 与 `kiss-my-agent-setup (kiss-my-agent)`。然后：

- 只有真实存在非显然机制、scope、runtime/evaluator 或证据决策时才使用 `$kiss-my-agent:kiss-my-agent`；
- 只有显式 setup/check/configure/remove 工作才使用 `$kiss-my-agent:kiss-my-agent-setup`。

普通实现、测试、构建、Git、查询和格式化不应路由到 `kiss-my-agent`。发现只证明该会话可见，不能保证未来遵循 instructions。

<a id="role-smoke"></a>
## 三角色 Smoke

此项显式 role Smoke 测试三个 seed roles，不代表普通任务必须组成三角色团队。Master 使用 Host 自定义 Agent 界面，或明确要求把一个有界的一次性任务委派给每个已发现角色：

1. `kiss_explorer`：读取 fixture 并报告准确 anchors，不编辑文件。
2. `kiss_coder`：只拥有一个隔离的一次性文件，仅在不存在时创建，验证后只删除该文件。
3. `kiss_reviewer`：检查给定 diff，报告带准确位置的实质 findings，不编辑文件。

在新的可信客户端任务中确认 Master 实际采用 Astra/high、三个当前角色采用 Astra/medium，实验上下文管理已加载。依据可观察的 Host 配置或诊断，不只依赖 Agent 自述；无法取得的证据明确报告。运行一次上面的有界三角色 Smoke，前后检查工作树与选定 fixtures。静态配置、实际加载和观察到的行为支持不同结论；不增加长上下文或模型性能基准。

只有大型独立的一次性子系统的直接汇总会污染 Master context 时，才测试 department lead。确认最多一层临时中间管理、workers 不继续委派、assignment 随任务结束而消失，并且每个共享资源保持一个 operator。不要为了测试而制造层级。

<a id="upgrade-smoke"></a>
## 公开 Release Smoke

创建 tag 前，运行不需要第三方依赖的本地 core checks，并要求该精确 candidate commit 的完整原生 pull-request CI 通过。这些只属于 candidate 证据，不是公开 install 或真实 Host 证据。

Pull request 合并且精确 commit 已创建并推送 `vX.Y.Z` tag 后，只使用隔离的公开安装执行必须经过公开分发表面的有界检查。把每条命令中的 `vX.Y.Z` 替换为本次 release 唯一选定的版本：

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list --marketplace kiss-my-agent
```

只有覆盖的 source 与行为没有变化时才能复用旧证据，并明确说明这是复用而不是重跑。创建 tag 后不要重复 candidate checks；只验证 release 验收标准要求的公开 archive、marketplace install 或 upgrade、fresh-session discovery 或其他 public-only 行为。除非改动行为确实需要，否则不要增加角色迁移、hash、诱导失败或重复矩阵。

行动前先分类第一个决定性的 post-tag failure：

- Tagged 产品源码中的缺陷：保留 tag，不为它创建 GitHub Release；修复 source 后使用下一个 patch version。
- Harness、command construction 或 environment failure：修复该 owner，并针对同一个 tag 只补取缺失证据。
- Evaluator error 或其他 invalid run：修正 evaluation，只重跑无效观察；它不是产品负面证据，也不触发 patch version。
- GitHub Release 发布后才发现的产品缺陷：保留已发布 tag，以新的 patch version 发布修复。

只有必需的公开检查通过后，maintainer 才能创建 GitHub Release。保留所有已推送 tag 与第一个决定性错误。

<a id="dogfooding"></a>
## 开发过程中的 Dogfooding

开发下一版本时使用当前 KISS 项目 instructions。Master 可以直接完成明确的小任务或局部工作；对实质批量工作、可独立并行或需要不同视角的工作，在收益超过协调成本时应积极委派。按工作量、并行机会、耦合、风险与协调成本选择，角色可选不等于 Master 包办全部。每种可用角色都可有零个、一个或多个实例，不要求固定组合、顺序或每次启动子代理。委派默认保持扁平。观察分工是否减少 scope、暴露失败或改善证据，以及是否造成可复现的错误停止或不必要机制。

保持产品 runtime 与 evaluator owner 分离：被测 Plugin 不能定义自己的验收标准，也不能批准自己的 release。人类维护者拥有目标与验收；按适用范围使用确定性测试、新会话 replay，以及有决策价值或用户明确要求的独立审查来判断观察结果。Dogfooding 是 engineering evidence，不是自主自证。

Coordinator wait 调用在没有新消息时返回，不能证明子 Agent 超时或失败。有界且不冲突的工作应继续；只有任务已经失效、scope 或资源冲突，或者用户明确要求停止时才中断。

如果 delegation 被禁用、不可用或没有合适角色，Master 可在已有授权和自身能力内继续工作，无需为 staffing 另设审批。用户明确要求的独立检查、特定角色或真实能力缺口仍须报告，不能把直接执行冒充为满足这些要求。

<a id="readme-pilot"></a>
## README 新用户 Pilot

只把最终渲染后的首页交给一名此前未接触本项目、未看过任何早期 README 草稿且没有参与改动的新用户，不额外解释，并要求其在五分钟内找出：

- 过度设计和过度防御这两种失败模式；
- Agent 为什么以及什么时候容易出现这些问题；
- KISS My Agent 怎样提供帮助、不能保证什么；
- 用白话复述 `目标/假设 → 最小可运行验证 → 真实结果 → 迭代或停止`，并区分低成本、可恢复的试错与绕过认证或权限、跨越不可逆高风险边界；
- 它是否适合自己的工作；
- company model：Owner 保留目标、架构、验收标准和停止点；Master / CEO 负责调度、决策与汇总；`kiss_explorer`、`kiss_coder`、`kiss_reviewer` 分别负责只读调查、有界实现和独立只读审查；
- KISS 为缺失 Master 配置提供 Astra/high 默认值，starter roles 使用 Astra/medium，而且 Master 通常使用扁平直接委派，而不是固定 workflow 或深层组织；
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
