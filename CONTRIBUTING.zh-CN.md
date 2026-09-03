# 贡献

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

<a id="before-you-start"></a>
## 开始之前

KISS My Agent 是一个科研工程插件，用于让 Agent 工作与问题规模相称、让失败保持可见，并让结论与证据相称。修改仓库前先阅读 [`AGENTS.md`](AGENTS.md)。修改 Skill、Rule 或 Case 时还要阅读[扩展](docs/EXTENDING.zh-CN.md)。Runtime 和测试行为分别由[配置](docs/CONFIGURATION.zh-CN.md)与[测试](docs/TESTING.zh-CN.md)说明。

通过 Git-backed marketplace 安装或更新正式发布的 Plugin，需要可用的 Git executable 和 GitHub 网络访问，但不需要 Python、Node.js、Docker 或其他语言运行时。贡献者工具链与用户路径分开：Git 与 Python 3.11 或更高版本足以运行标准库 validator 和 Setup contract tests。只修改 Plugin 或 Skill 的贡献者不需要安装 Markdown，也不需要在本地构建站点；pull-request CI 会验证站点。只有真实 discovery 和 dogfooding 检查才需要 Codex。

v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` 已在 v0.2 移除，这是 breaking contributor-interface change。Setup、check、remove 与 role configuration 应迁移到对话式 `kiss-my-agent-setup` Skill；粘贴 raw text 时使用 `$kiss-my-agent:kiss-my-agent-setup` 调用，并把 Agent 原生 engineering evidence 与 deterministic repository-test evidence 分开。

参与本项目即表示同意遵守 [Code of Conduct](CODE_OF_CONDUCT.md)。

<a id="where-to-participate"></a>
## 在哪里参与

- 当前文档契约存在可复现缺陷时，使用 [bug report](https://github.com/AoiOTA/Kiss-My-Agent/issues/new?template=bug-report.md)。
- 说明缺失、矛盾或难以执行时，使用 [documentation report](https://github.com/AoiOTA/Kiss-My-Agent/issues/new?template=documentation.md)。
- 有当前 consumer 且结果范围明确时，使用 [feature request](https://github.com/AoiOTA/Kiss-My-Agent/issues/new?template=feature-request.md)。改变 plugin/marketplace 布局、setup scope、角色 schema、Skill trigger 边界、Pages 发布或永久规则前必须先建 issue。
- 对反复出现的决策方法或具体对照，使用专门的 Rule or Case proposal 模板。小型、有界修正可以直接提交 pull request。
- 使用 [Q&A Discussions](https://github.com/AoiOTA/Kiss-My-Agent/discussions/categories/q-a)寻求使用帮助；尚未收敛为有界改动的开放想法放入 [Ideas Discussions](https://github.com/AoiOTA/Kiss-My-Agent/discussions/categories/ideas)。
- 按[安全说明](SECURITY.zh-CN.md)私下报告漏洞。绝不在 issue 或 Discussion 中放入凭证、exploit 细节、私有数据或敏感日志。

<a id="contributor-bootstrap"></a>
## 贡献者环境准备

在 GitHub 上 fork 仓库，clone 自己的 fork，并把 canonical repository 添加为 `upstream`：

```bash
git clone https://github.com/YOUR_ACCOUNT/Kiss-My-Agent.git
cd Kiss-My-Agent
git remote add upstream https://github.com/AoiOTA/Kiss-My-Agent.git
git fetch upstream
```

确认贡献者解释器。修改 Plugin、Skill、配置或 Setup contract 不需要虚拟环境或安装 package。

Linux 或 macOS：

```bash
python3 --version
```

Windows 原生 PowerShell：

```powershell
py -3 --version
```

显示的 Python 版本必须是 3.11 或更高。WSL 使用 Linux 步骤，产生的是 Linux 证据，而不是 Windows 证据。文档贡献者可以选择创建[本地验证](#local-validation)中说明的隔离环境。

<a id="change-boundaries"></a>
## 修改边界

- 保持人对目标、架构、验收标准、非目标和停止边界的所有权。
- 保持 `kiss-my-agent` 精确路由且 non-catch-all。只有反复出现的方法才新增 Rule，只有有用的具体对照才新增 Case。
- 没有已批准的当前 consumer 时，不扩张 setup、workflow、release、compatibility、telemetry、scoring 或 evaluation machinery。
- 保持三个 owner：`config.toml` 中四个 config paths（成对的 Master model/effort defaults 加两个独立补默认的公开开关）、standalone role TOML discovery，以及 AGENTS 中的动态调度。Marker 只控制 remove ownership，不授权重置已有值。Config 不得枚举角色文件。
- 把提供的角色视为可编辑的 fresh-setup seeds，而不是封闭 catalog；角色 `name` 是身份，文件名只是约定。角色一旦存在即归用户所有，setup 或 Plugin update 永不覆盖、迁移或判定其版本。
- 让 Master 只负责调度、决策与汇总。默认扁平 direct fan-out，允许同一角色多个实例，并为每个共享资源保留一个 writer/operator。合格的大型独立子系统可使用一个临时有界 lead，其 workers 不再委派；绝不增加更深或永久层级。
- 区分 Master settings 与 role settings。可编辑的 bundled defaults 为：Master 在 scope config 中使用 `gpt-5.6-sol` / `max`，explorer/coder roles 使用 `gpt-5.6-sol` / `high`，reviewer 使用 `gpt-5.6-sol` / `xhigh`。保留已有选择；后续 setup 和 update 不得重置，role wizard 也不得编辑 Master config。
- 保留用户和其他 Agent 的无关改动。范围外 refactor、生成产物和格式化不得进入 diff。
- 每份英文开发者文档与简体中文配套文件必须同步：语言切换、显式 anchor IDs、章节顺序和 fenced command blocks。
- 面向 Codex 的 AGENTS、Skills、Rules、Cases、角色 TOML、`LICENSE` 与 `CODE_OF_CONDUCT.md` 只保留英文。
- 绝不加入凭证、私有路径、私有数据、日志、sessions、本地 plugin cache、虚拟环境或生成的测试内容。

<a id="development-workflow"></a>
## 开发流程

从 canonical `main` 的最新状态创建聚焦分支。使用简短、描述性的分支名；下面只是示例，不是强制命名规则。

```bash
git fetch upstream
git switch -c docs/clear-onboarding upstream/main
```

编辑前先追踪实际 producer-consumer 路径。用最小有效输入复现缺陷，只修改 owning module，加入一条修复前失败的 regression check，并在迭代时运行聚焦检查。如果证据表明不需要代码或文档变更，有依据的 no-change 结论也是有效结果。

创建 pull request 前，检查完整 diff，确认没有无关工作，运行下文适用的必需本地检查，只提交预期文件，再把分支推到自己的 fork：

```bash
git status --short
git diff upstream/main
git add path/to/intended-file path/to/another-intended-file
git diff --cached --check
git commit -m "docs: clarify onboarding"
git diff --stat upstream/main...HEAD
git push -u origin docs/clear-onboarding
```

把示例 paths 和 commit message 换成实际的有界改动；不要使用 `git add .`。不要重写其他贡献者的分支、force-push 共享工作，或把 release 准备与无关修复混在一起。

<a id="local-validation"></a>
## 本地验证

只修改 Plugin、Skill、配置或 Setup 的贡献不需要第三方 Python 依赖。本地运行下面两项标准库检查。

Linux 或 macOS：

```bash
python3 scripts/validate.py
python3 -m unittest tests.test_setup -v
```

Windows 原生 PowerShell：

```powershell
py -3 scripts/validate.py
py -3 -m unittest tests.test_setup -v
```

这些检查验证 source 与 Setup contracts；它们不会执行真实 Codex setup，也不能证明 Host 行为。

它们还验证 v0.1 `skills/kiss-my-agent-setup/scripts/setup.py` interface 已被移除。不得恢复它，也不得用另一个仓库 staging/setup script 取代；受支持的 setup interface 是对话式 Skill。

修改文档或站点时，CI 是必需的站点构建证据。贡献者可以选择在 checkout 外创建隔离环境进行本地预览。

Linux 或 macOS：

```bash
python3 -m venv ../kiss-my-agent-docs-venv
. ../kiss-my-agent-docs-venv/bin/activate
python -m pip install -r requirements-site.txt
python -m unittest tests.test_build_site -v
python scripts/build_site.py --output _site
```

Windows 原生 PowerShell：

```powershell
py -3 -m venv ..\kiss-my-agent-docs-venv
..\kiss-my-agent-docs-venv\Scripts\Activate.ps1
python -m pip install -r requirements-site.txt
python -m unittest tests.test_build_site -v
python scripts/build_site.py --output _site
```

`_site/` 是已忽略的本地预览，不得提交。贡献者不需要只为在本地运行完整套件而安装 Markdown。

CI 与 release maintainer 在安装 `requirements-site.txt` 后负责完整的 deterministic 入口：

```bash
python scripts/test_all.py
```

它会运行仓库验证、所有单元测试、临时文档站构建、Git whitespace validation 和运行前后 working-tree 检查。失败本身就是结果的一部分：保留第一个决定性错误，并修复真实 owner。配置了 workflow 不代表它已通过：pull request 需要其当前 commit 的原生绿色 jobs。macOS 或 Windows 支持必须由对应 platform 的精确绿色 job 证明；WSL 仍然只是 Linux 证据。

<a id="dogfooding"></a>
## 用 KISS My Agent 开发 KISS My Agent

开发 KISS My Agent 时使用 KISS My Agent，但反馈循环必须受 issue 中由人确定的目标和验收标准约束。Dogfooding 可以暴露歧义或缺陷；它不授权插件重新定义自身架构、扩大自身范围，或把自己的判断当作验收证据。

真实检查前记录 source 和 Host 基线：

```bash
git rev-parse HEAD
git status --short
codex --version
```

真实检查分为两个不同层面：

1. **项目 instructions 与 roles。** 从当前 checkout 启动可信的新 Codex 会话，给它一项真实且有界的贡献任务。让 Master 只负责调度、决策与汇总：默认扁平 direct fan-out 到 `kiss_explorer`、`kiss_coder` 与 `kiss_reviewer`，合理时使用同角色多个实例，并为每个共享资源指定一个 owner。只有合格的大型独立子系统才使用临时 lead，绝不形成更深层级。确认无关 dirty-tree 改动仍被保留，subprocess failures 仍然可见。
2. **已编辑的 plugin package。** 不要为了让本地 cache 失效而修改 tracked release manifest 或 Git-backed marketplace。使用 Codex 的 Plugin Creator local-update workflow，在独立 local marketplace 中暂存一次性副本，让该 marketplace 指向暂存副本，并且只给暂存 manifest 添加一个 `+codex.<cachebuster>` 后缀。把它从该 local marketplace 安装进隔离 Codex home，然后启动新 thread，让 Host 加载暂存的 Skills。

外部贡献者可复制下面的 Codex prompt 调用该 workflow：

```text
$plugin-creator update this existing KISS My Agent plugin for local development. Stage a disposable candidate copy outside the checkout in a separate local marketplace, point that marketplace only at the candidate copy, add exactly one +codex.<cachebuster> suffix to the copy's manifest version, reinstall it from that marketplace into an isolated Codex home, and tell me to start a new thread. Do not modify tracked release files or the Git-backed marketplace.
```

参见 OpenAI 官方的 [Plugin Creator 与 local marketplace 指南](https://developers.openai.com/plugins/build/plugins#package-with-plugin-creator)和[marketplace add/upgrade 命令](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli)。不要为此 workflow 新增仓库 staging script。

在新 thread 中确认 `/skills` 显示 canonical Plugin Skills `kiss-my-agent:kiss-my-agent` 与 `kiss-my-agent:kiss-my-agent-setup`。只对匹配的非显然决策调用 `$kiss-my-agent:kiss-my-agent`。只在一次性 project scope 中使用 `$kiss-my-agent:kiss-my-agent-setup` 检查 setup、check、Agent 配置和 remove；开发测试不得使用真实 global scope。保留首次 failed precondition，不要通过重试隐藏它。

分别报告每种证据层级：

| 证据 | 能支持 | 不能支持 |
| --- | --- | --- |
| Source inspection | 被检查文件写了什么 | 已加载的 runtime 行为 |
| `test_all.py` PASS | 该精确 source 实际实现的检查 | 发布、Host 加载或 Agent 服从 |
| 原生 CI PASS | 该 platform、job 与精确 commit | 所有 OS 版本或未来兼容性 |
| Fresh-session discovery | 该 session 中可见的 Skills 或 roles | 未来行为或权限安全性 |
| 一次有界 Smoke | 观察到的任务与环境 | 普遍可靠性或产品验收 |
| 新用户 Pilot | 该参与者无需帮助完成了指定场景 | 普遍可用性 |
| Release verification | 已测试的公开 tag、archive、install 或 upgrade 路径 | 未发布改动或未来 release |

记录 platform、原生 shell、精确 source state、Codex 版本、trust state、session 是否为新建、marketplace source/version、prompt、预期结果、实际结果和未测试表面。回答了既定问题后立即停止；不要为了制造信心而重复运行。

Coordinator wait window 在没有新消息时返回，不代表子 Agent 超时或失败。有界且不冲突的任务应继续；只有 assignment 已失效、越界、争用共享资源，或用户明确要求停止时才中断。

如果 delegation 被禁用、不可用或没有合适角色，应报告 staffing issue，让用户选择修复或启用 staffing，或者明确把本任务切换为普通单对话。只有用户选择后者，Master 才能直接执行；不得静默接手。

<a id="pull-requests"></a>
## Pull Requests

向 canonical `main` 创建 pull request，并完整填写仓库模板。说明用户可见结果、当前 consumer、修改的 owner、显式非目标、精确验证命令、证据层级与局限。需要先建 issue 时必须关联它。

Pull request 要聚焦且便于审查。解决重大 review findings 时不要顺带做宽泛清理。绿色 checks 必须属于当前 pull-request commit。Maintainer 使用 **Squash and merge** 合并已接受的改动，并可删除已合并分支；贡献者不需要只为制造一个 commit 而重写原本清晰的本地 commit history。

测试通过不能证明模型行为、可用性、发布或 release 成功。直接说明所有未测试表面。

<a id="release-process"></a>
## v0.2.3 发布流程

本节仅供 maintainer 使用。`v0.1.0`、`v0.2.0`、`v0.2.1` 与 `v0.2.2` tags 不可变，绝不能移动或重建。`v0.2.0`、`v0.2.1` 与 `v0.2.2` tags 都没有 GitHub Release。v0.2.2 post-tag 的 public fresh install 与 marketplace upgrade 已通过，但 public legacy-role transition 因无法解析 Plugin resource workdir/path 而在写入前停止，因此没有创建 v0.2.2 Release。v0.2.3 采用 user-owned roles：fresh setup 创建缺失的 current starters，所有已有角色直接保持不变。

1. 使用 [Issue #8](https://github.com/AoiOTA/Kiss-My-Agent/issues/8) 跟踪 v0.2.3，并写明验收标准、兼容性约束和非目标。
2. 创建 release pull request 前，运行适用且不需要第三方依赖的本地 core checks。要求该精确 candidate commit 的完整测试套件以及 Ubuntu、macOS、Windows 原生 pull-request CI 全绿。这些只属于 candidate 结果；公开 tag 存在前，不得声称 public install 或真实 Host 证据。
3. 通过聚焦 pull request 合入实现。将 Plugin manifest version 与 marketplace ref 对齐为 `0.2.3` / `v0.2.3`，并同步中英文文档。
4. Pull request squash-merge 后，验证精确的 `origin/main` commit，创建不可变的 annotated tag 并推送。此时还不能创建 GitHub Release：

```bash
git fetch origin
git switch main
git pull --ff-only origin main
python3 scripts/test_all.py
git tag -a v0.2.3 -m "KISS My Agent v0.2.3"
git push origin v0.2.3
```

5. 针对已推送的公开 tag，只运行有界的 public release 顺序：完成 fresh install 并确认 installed cache 报告并加载 `0.2.3`；在空的一次性项目中运行 fresh setup 并确认三份 current starter role files 全部创建，再启动一个可信新会话，让一个已发现的 KISS role 实际执行窄范围无害任务，随后删除一份 starter，在同一项目中重跑 setup 与 check，并确认它保持 intentionally absent；在一次性 v0.1-managed fixture 中保留每个角色文件的 before bytes，运行 current setup，要求 managed block 变为 current，并在两个 Master keys 原本都缺失时成对补齐，再通过 direct byte comparison 确认每个角色文件都与 before bytes 一致；随后执行文档中的 pinned rollback，确认普通 upgrade 仍保持 pinned，再用文档中的 marketplace remove 加 unpinned-add 顺序恢复 current channel。不要求角色迁移、角色 hash、诱导失败或重复矩阵。

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

6. 只有完整 public 顺序通过后，才能创建 GitHub Release：

```bash
gh release create v0.2.3 --verify-tag --title "KISS My Agent v0.2.3" --generate-notes
```

7. 验证公开 Release 页面与 archives，并通过后续 pull request 在 canonical handoff 中记录精确 commit、CI runs、有界 public 顺序和剩余限制。

如果 post-tag public check 失败，保留该 tag，不创建误导性的 v0.2.3 Release，并以新的 patch version 发布修复。如果已经发布的 Release 后来发现缺陷，同样保留 tag 并发布新的 patch version。绝不 force-push `main`、移动任何已推送 tag、压掉失败检查，或把 invalid run 重新标记为成功。
