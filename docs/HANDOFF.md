# KISS My Agent 当前状态 Handoff

这是本仓库唯一的 canonical handoff。详细过程由 Git history、Issue 和 PR 保存，不创建 dated、attempt 或 campaign 副本。

## PawWeaver 持续 dogfooding · 当前交接（2026-09-10）

- **共同目标未完成**：推进PawWeaver研究MVP，同时让master与child无需用户提醒，持续应用KMA减少过度设计、冗余取证和阻塞。以实际决策、科研闭环及用户成果判断收益；读取、安装、测试或agent数量不算成功，不新增遥测、归档或流程系统。
- **当前观察到的缺陷**：旧指导未阻止root缩窄完整全身控制；随后又把用户示例数值和候选方法当成规定，纠偏时反向要求恢复整份参考plan。用户仍多次提醒目标，首先是root混淆明确要求与参考手段、未应用已有边界；此前重复取证和过多review也不能用新提示宣称已解决。
- **当前修正与安装**：最新 `e695db2` 仅修改 [Skill入口](../skills/kiss-my-agent/SKILL.md)：锚定明确目标／约束，例子、参考plan与暂定手段不自动成为要求或参数依据；按已有结果调整手段，纠偏保留有效进展。ONLY SKILL已同步 `/home/lyb/plugins/kiss-my-agent`，经现有helper默认cachebuster及plugin add安装 `0.2.7+codex.20260910024255`，dogfood源码、personal源与安装缓存三地SKILL逐字节一致。Plugin校验首次因root误用已知缺PyYAML的runtime失败；改用现有train环境后退出0，未安装依赖，不能称首次通过。未改roles／setup或发布。
- **真实采用证据有限**：fresh `umi_recipe_implementation` 与 `mujoco_contact_trace` 无额外KMA提醒，自行处理旧catalog路径并读取前一版 `03856`。仅支持旧版这两次读取，不是 `024255` 自动加载或有效行为的证据；旧thread宿主快照问题未解决。新措辞的效果待下一项实际自主决策验证，不能从安装、checks或当前任务输入推断模块收益。
- **Paw当前结果**：`be0246d` 已将当前能力目标与reference方法分开，不再把M0–M4全量模块当作固定必做项。256条train／64条test数据已实际生成并通过CPU检查；fresh PhysX baseline的64条均完成60s且无fall，但位置误差0.749939m、朝向误差2.038435rad，无task success。数据可生成、无跌倒与既有UMI局部精度均不等于任务成功或完整全身控制。
- **下一项已选、未完成**：新2000轮训练于2026-09-10 02:34:52 UTC实际启动，PID `2202283`，当前运行中。已授权12项执行：baseline、train、4 suites各双引擎、static16各双引擎；尚无新训练完成或完整后测结果。继续按真实证据推进广EE工作空间，以及原地全身够不到时移动支撑的能力；保持世界系完整EE pose、单18关节Actor、无外部底盘命令及原验收。CPU几何可达性仍非动态证据，临时硬件参数不支持硬件有效性或正式里程碑。
- **继续工作时复用**：以下Paw路径均相对 `artifacts/runs/diagnostic_pose_learning/`：`leg_mean_bound_comparison/next_learning_proposal/` 的reward读出已区分pose精度项近零与progress非零；`progress_weight_comparison/continuation_failure_analysis/early_training_signal_capture_preparation/readout/README.md` 已揭示早期失败回合中progress收益覆盖原终止惩罚，不能只因新policy身份就重做机制取证。此前整包metadata equality gate的真实误阻断已在既有 [product-contract案例](../skills/kiss-my-agent/references/cases/product-contract-provenance-vs-agent-proof.md) 局部修复并重验；有限收益不替代持续有效指导目标。详细旧过程留在Git，不再逐轮复制。

## 未发布候选：v0.2.7 Astra 增量升级（基于 v0.2.6）

- 基线：`v0.2.6` / `38f29be1a224a0687e5a6fdba3b1c18fff0a2bb8`。保留原有规则、案例和保护机制，只修委派矛盾与默认配置。
- 缺失 Master 配置默认 Astra/high，新角色 Astra/medium，实验上下文默认 true；已有显式值与已有角色保留。准确完整的受管 Sol/max pair 更新为 Astra/high。
- 升级路径：更新插件 → 原 scope setup → 显式 configure 选定角色 → 新建可信客户端任务。静态配置与实际加载分别验收。
- 候选 manifest 为 `0.2.7`、marketplace ref 为 `v0.2.7`；tag 和 Release 尚未创建。本段不是已发布声明。以下当前 Release、行为和证据仍指已公开的 v0.2.6，不代表本候选已获远程 CI、Pages 或分发证据。Tracking issue：[#22](https://github.com/AoiOTA/Kiss-My-Agent/issues/22)。
- 本轮静态证据：完整 `scripts/test_all.py` 通过，42 tests、16 页隔离站点构建、whitespace 与 repository-state 检查通过；两个 Skill 的 `quick_validate` 和 Plugin validation 通过。独立审查发现的两处安装文档矛盾已修复并复核关闭；原有角色正文与历史 snapshots 的保留已核验。
- 隔离 CLI 运行：Codex `0.153.2`、ChatGPT 登录、临时 Codex home 和本地 marketplace，使用临时 cachebuster 的隔离候选缓存（临时后缀不用于发布元数据）。Fresh setup 经独立断言确认 Master Astra/high、三个 seeds Astra/medium、context true，并保留 AGENTS 外部前缀。CLI features 报告 context/multi_agent true；这属于配置加载证据，不是历史检索行为证明。
- 一次有界三角色 Smoke 通过：宿主 rollout turn context 确认 Master Astra/high 与三个不同子代理 Astra/medium；explorer 读取 fixture，coder 独占创建、验证并删除临时文件，reviewer 识别 add→subtract 回归。Fixture、config 与 AGENTS 无遗留修改。
- 升级首轮经独立断言确认：完整标记 Sol/max 更新为 Astra/high，显式 context false 保留，自定义 explorer 与原 v0.2.6 coder 字节不变，已删除 reviewer 未恢复，AGENTS 外部前缀保留且受管块刷新。同一升级 fixture 的后续生命周期经独立断言确认：check 为 `structurally-valid`，context false 单独报告且不判为 disabled；重复 setup 前后文件映射逐字节相同；remove 删除精确 v0.2.6 coder，保留自定义 explorer，reviewer 仍缺失，AGENTS 恢复为原外部文本，剩余 TOML 保留用户注释、原表（包括 context 子表）与显式 context false。本轮运行覆盖不扩展为 global、configure、fresh-remove 或完整失败矩阵。
- 运行限制：首次 workspace-write 因 `.codex` 只读保护被阻止，属于 invalid harness，零产品修改；随后仅对隔离 fixture 使用 danger-full-access，因此没有 sandbox enforcement 证据。Smoke 中 `python` 不存在并返回 127，保留原失败后改用 `python3` 成功。
- 实际桌面新任务仍未验证：当前工具未暴露隔离 home 或候选安装源。用户全局配置未改，原工作区哈希复核相同；上述 CLI 证据不替代桌面加载、公开 CI、Pages 或发布证据。

## 当前 Release

- Canonical repository：[`AoiOTA/Kiss-My-Agent`](https://github.com/AoiOTA/Kiss-My-Agent)，公开 branch 为 `main`。
- 当前 supported release：[`v0.2.6`](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.2.6)；Plugin manifest 为 `0.2.6`，Git-backed marketplace ref 为 `v0.2.6`。
- v0.2.6 tag 与 Release commit 为 [`38f29be1a224a0687e5a6fdba3b1c18fff0a2bb8`](https://github.com/AoiOTA/Kiss-My-Agent/commit/38f29be1a224a0687e5a6fdba3b1c18fff0a2bb8)。实现 PR [#19](https://github.com/AoiOTA/Kiss-My-Agent/pull/19) 与 tracking issue [#18](https://github.com/AoiOTA/Kiss-My-Agent/issues/18) 均已关闭。
- Pages：[English](https://aoiota.github.io/Kiss-My-Agent/) · [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)。

## 当前行为

- KISS 不再固定 Master 的 model 或 reasoning effort；两者由 Host、对话选择或更高优先级配置决定。若账号可用，复杂 KISS 任务可从 Astra High 开始，但这不是强制默认。
- 当前 `kiss_explorer`、`kiss_coder` 与 `kiss_reviewer` seeds 均无 KISS role-level model pin，并将 `model_reasoning_effort` 设为 `medium`。显式 spawn 或 Host 的 `[agents]` 默认仍可能覆盖 Parent。
- Fresh setup 只创建缺失 starters。角色一旦存在即由用户所有；setup 与 Plugin update 不覆盖、自动迁移或判定其版本，用户后来删除的 starter 也不会被重建。
- Setup 只在两个旧 Master assignments 均为顶层唯一键、值精确为 `gpt-5.6-sol` / `max`、且各自带精确 managed marker 时成对删除。部分、无标记、修改过或冲突的状态保留，并提示用户手工恢复继承。
- 显式 remove 可按字节识别当前、v0.2.5 与 v0.1 role seeds；这些历史 snapshots 仅供 remove 比较，setup、check 与 configure 不读取它们来判版本或迁移角色。
- Setup、check 与 remove 只检查当前 scope 中会读取、创建、修改或删除的 KISS targets，不验证无关自定义角色。Plugin 暴露 `kiss-my-agent` 与 `kiss-my-agent-setup` 两个 Skills。

## 当前证据

- v0.2.6 tag 的 [Validate run](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34011252597) 在六个 OS/Python jobs 上全部通过；该 release commit 的 [Pages build/deploy](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34011174208) 通过。
- Candidate fresh-session 验证通过 setup、check 与再次 setup no-op。精确带标记的旧 Sol/max pair 被清理；已有 v0.2.5 roles保持不变；单角色 configure 与 remove-only compatibility 均通过。
- Desktop candidate 验证中，对话切换后连续两轮保持 Astra/high；Master 只委派一个 `kiss_explorer`，该 child 使用 Astra/medium。
- Public marketplace upgrade 后，Plugin 为 installed/enabled v0.2.6，fresh public CLI 成功发现两个 v0.2.6 Skills。Public parent thread `01a074f9-7cd8-7f21-8ccd-e281d2e3d045` 使用 Astra/high；其唯一 `kiss_explorer` child `01a074f9-ae2e-70d3-8d2e-f8f8bc888716` 使用 Astra/medium。

## 已知限制

- Plugin 用户不需要 Python、Node.js 或 Docker；Git-backed marketplace 安装和更新仍需要可用的 Git 与 GitHub 网络访问。
- Setup 的静态 `check` 只证明被检查文件的状态；加载、discovery 或模型切换仍需可信的新会话验证。
- 本次观察到一个长时间运行的 Desktop process：CLI 已升级且旧 cache 已不存在后，它创建的新任务仍持有旧 v0.2.5 Skill catalog；fresh public CLI 能正确加载 v0.2.6。若 fresh Desktop 验证出现旧 cache path，应先完全退出并重新打开 Codex。这是 Host lifecycle 证据，不是 KISS 产品失败。
- 当前证据不外推到未运行的 Host/version matrix、所有角色组合或人工 failure matrix。Source inspection、tests、CI、fresh-session behavior 与 public distribution 是不同证据层级。

## Release 历史

| Tag | GitHub Release | 一行结果 |
| --- | --- | --- |
| `v0.1.0` | 有 | 首个正式公开版本；公开安装、discovery、project setup/check、三个 starter roles 的各一次窄任务与 remove 在 Codex CLI 0.152.0 上观察通过。 |
| `v0.2.0` | 无 | 公开验证暴露非 canonical Skill invocation 与 harness quoting 问题，停止发布。 |
| `v0.2.1` | 无 | Legacy-role transition 出现产品写入失败；rollback 恢复 before-state，停止发布。 |
| `v0.2.2` | 无 | Public transition 在写入前遇到 Plugin resource path 解析问题，项目零修改，停止发布。 |
| `v0.2.3` | 无 | Public setup 暴露 outdated/current 分类歧义，保留 tag，由下一 patch 修正。 |
| `v0.2.4` | 有 | 分类修正、公开分发与有界升级证据通过。 |
| `v0.2.5` | 有 | Setup 缩小到精确 KISS targets，candidate、CI、公开升级与 fresh check 通过。 |
| `v0.2.6` | 有 | 解除 Master 与 starter roles 的 Sol 锁定；Astra/high Master 与 Astra/medium Explorer 的 candidate 和 public fresh-session 路径通过。 |

所有已推送 tags 都保留且不可移动、删除或重建。没有 GitHub Release 的 tag 不描述为正式发布版本。

## 停止线

- 不移动、删除、重建任何已推送 tag，也不 force-push `main`。Candidate 阶段解决产品行为问题；tag 后只补 public-only evidence，不重复未受影响的 candidate checks。
- Tagged source 中的产品缺陷阻止创建 Release，并由下一 patch 修复；harness、command、environment 或 evaluator failure 修复其 owner 后针对同一 tag 补证据，不自动触发 patch。
- 后续只根据真实用户缺陷、Host 变化或明确的新目标重新立项；满足有界验收或得到受支持的 no-change 结论后停止。
