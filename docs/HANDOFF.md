# KISS My Agent 当前状态 Handoff

这是本仓库唯一的 canonical handoff。详细过程由 Git history、Issue 和 PR 保存，不创建 dated、attempt 或 campaign 副本。

## PawWeaver 持续 dogfooding 本地候选 · 2026-09-09

- PawWeaver 交付与 KMA 改进始终共同推进：主对话与各子 agent 无需用户提醒，在需要处主动读取并应用 KMA，让指导实际减少过度设计、过度防御与冗余，提高开发效率、缩短科研闭环并推进最小可用成果。只依据真实工作问题改进；静态检查、安装或调用次数不算成功，以实际决策与用户成果判断收益，不新增遥测或流程系统。观察到 whole-run metadata 被整包复制、自设 exact-hold gate 被延伸成后续实验前提、反复 finite probes 偏离实际学习问题。
- 保留原批量/顺序对比失败：最大 TCP 差约 0.397 mm、晚段 RMSE 差约 0.143 mm，成功/跌倒/饱和等决策一致，精确保持时长差 0.10/0.32 秒。候选区分原诊断结论与下一实验所需证据，用户验收不变。
- Skill 主动覆盖执行中出现的机制、失败处理、阻塞和证据决策；按行为读取一个规则与匹配案例。每个 agent 对自己执行中新出现的决策应用路由，master 阅读不能替代 worker。已经决定的机械工作不重复审查。新增字段本身需有消费者；有限执行或参数更新不能回答学习是否改善任务。
- Reviewer seed 可审查 assigned change or decision；精确历史比较仅允许这一已知正文差异，remove-only snapshots 未变。PawWeaver 显式同步 managed block 和 reviewer 首句，保留 model、effort、sandbox 与非 managed 目标。
- 实际 pose batch-8 评估已完成，用时 49.73 秒；不再为后续批量评估重复申请授权或要求 exact-hold 串行门槛。这个观察支持执行路径改善，不证明自动 Skill 触发、学习改善、硬件有效性或正式里程碑完成。
- 本机 personal marketplace 指向的实际 Plugin 源与 dogfood 是独立副本。本次比较后仅复制九个批准文件，保留安装源的其他 docs 差异；通过 cachebuster helper 与 `codex plugin add kiss-my-agent@personal` 安装 `0.2.7+codex.20260909133617`，已核对对应 personal Plugin 版本缓存。未手改 marketplace，未 tag、push 或发布。
- 源变更的 `scripts/validate.py`、18 个 `tests.test_setup` 测试、Skill quick validation、Plugin validation 与 whitespace 检查通过；缓存内九个文件与已验证源逐字节相同。此为静态和安装证据；现有对话 catalog 不会据此自动更新。
- 随后的真实 fresh `pose_result_comparison` 子任务没有额外 KMA 提醒，自行读取新安装 Skill、实验规则与 product-contract 案例，并选择 artifact 局部比较，未扩展同策略跨引擎 API。这支持本次自然触发已发生；但它在固定 suite identity 与 case 已检查后仍添加整份 `trajectory` metadata equality gate，RentTest 判断仍失误。Root 主动 review 自行发现并要求修正；实际 owner 已删除该 gate。真实 pre artifact 的内存说明字段差异不再阻断，case 集合不一致仍按预期报错，两项检查整体 exit 0；未伪造 post artifact。
- 该观察对应的 mutable 源候选仅在既有 product-contract 案例 reject 段补充：所需输入与 identity 已检查时，不将含描述性或无关字段的整个 metadata 容器相等作为额外前提。入口 Step 2 与其他规则保持不变：现有案例已足以判断，没有证据表明强制再读第二规则能改变行为。这个局部修复不证明稳定自发指导效果或问题全面解决，公开前继续在真实 PawWeaver 工作中自测，尚未发布。 本次仅同步该案例到独立实际 Plugin 源，保留其不同 HANDOFF；标准 cachebuster/install 流程已安装 `0.2.7+codex.20260909134518`，缓存案例与源逐字节相同。最终文档写入后再次通过静态与 whitespace 校验，Plugin validation 通过；这些检查不替代后续真实行为验证。本次文档校验发现此前安装记录写入私有绝对路径，已改为源与缓存角色描述；此前源校验发生在安装记录写入前，不覆盖该最终文档。
- 第二个真实 fresh、`fork_turns=none` 的 MuJoCo coder 在任务未额外点名 KMA 的情况下，自行读取 `0.2.7+codex.20260909134518` 入口、实验规则与 product-contract 案例，选择扩展现有 runner、复用 `training_inputs` 与编译前参数，没有新建评估框架。该实现通过独立 review，真实 CPU MuJoCo 八例闭环均完成 20 秒且无跌倒。两次有限自然触发及这些局部选择支持实际指导开始发生，不证明广泛成熟或稳定自发效果；首个比较任务仍需 root 发现并纠正 metadata equality gate 的不足保留。
- PawWeaver 本轮完成 1000 次训练迭代、98.304M transitions、20k 次优化。固定 PhysX 八例位置指标全部改善，但朝向全部退步：local 组从 0.0854 增至 0.1505 rad，moving 组从 0.0939 增至 0.2885 rad。独立 MuJoCo 保持位置效果，也存在朝向问题；不能把位置改善与无跌倒写成全位姿任务成功或硬件有效性证据。
- 原 OpenBLAS 原生失败保留；针对同一 policy 与 suite 的单线程重试成功，没有增加证明门槛。下一步针对真实负面朝向结果继续学习。此次没有新的 KMA 规则缺陷观察，保持规则、版本与安装不变；公开前继续真实 PawWeaver 自测，当前仍未发布。

- 后续用户再次指出 KMA 未持续主动指导、master 推进计划遗漏共同目标。只读核对确认当时 dogfood、实际 Plugin 源、`134518` 缓存入口及 setup producer 相同，Paw managed block 也与 producer 相同；但运行任务仍拿到 `092529` 旧 catalog description 与旧 managed 指令快照。`fork_turns=none` 不证明宿主重新发现目录；安装成功与两次主动读取都不能解释为持续指导已经解决。
- 本轮 mutable 候选把入口读取前移到每个 KMA-managed assignment 开始，由每个 agent 先读当前入口一次再判断适用；随后将路由绑定到下一步选择或修改、分工、研究结果或执行状态结论，复用仍有效的指导，机械执行不反复阅读、审查或记录。Managed producer 与本仓库 AGENTS 用简短入口引用承接；engineering 规则明确 master 在委派与交接保留全部未完成授权目标，worker 保留自己完整 assignment。安全、权限、单资源 owner 与真人架构/验收边界不变，无新状态、审批、遥测或 startup marker。
- 独立 review 发现拟加的 seed 前缀会破坏既有角色 remove 匹配；master 复核当前消费者后直接撤去此前缀及只为它增加的兼容快照和校验，因为现有与新设角色均已由 managed block 承接入口要求。现有角色与原 remove 匹配保持不变，无需为冗余前缀维护历史。精简候选通过独立 review 后，仅同步四个审查过的入口/规则文件到实际 Plugin 源，保留其独立 HANDOFF；标准 cachebuster/add 安装为 `0.2.7+codex.20260909152724`，四个缓存文件与审查源逐字节相同。Paw managed block 已刷新，用户目标段、config 与三个角色逐字保留。最终文档写入后的静态和 whitespace 校验、Plugin validation 通过；未 tag、push 或发布。宿主旧目录问题不能由插件文字修改保证修复，不宣称 catalog 热刷新；静态与安装通过不替代实际指导效果；后续真实任务观察如下。

- 安装后的两个 fresh `fork_turns=none` 任务均未额外点名 KMA：`pose_pair_next_step` 与 `pose_visual_run` 遇到旧 `092529` catalog 路径不存在后，自行找到 `152724` 完整读取入口与实验规则。前者核实 w1/w4 的实际完成状态并纠正 runbook/validation；保留 PhysX 八例位置全退步、朝向全改善与 MuJoCo 位置四好四差、朝向全改善，失败空文件不算报告。它选择复用已保存 trace 做 CPU 关联分析作为下一步建议，未新增机制，也未把关联分析写成动态因果证据。
- 后者确认既有 `run_visual` 可接诊断 runner，选择 artifact 驱动而未增加新 CLI 或生产改动；真实 20 秒固定世界目标 RGB-D 闭环 exit 0、墙钟 27.38 秒。已只读核对 Paw artifact `diagnostic_pose_visual_control/README.md` 与 `closed_loop20/summary.json`：601/601 捕获检测成功、999/1000 控制步有有效测量，仅初始一步等待图像而 hold；TCP RMSE 为 0.0188959 m / 0.0852529 rad，现有跌倒判据未触发，视频第 0/499/999 帧验证可解码。该证据使用仿真里程计与临时参数，只覆盖固定目标短闭环，不证明动态目标、稳定站立、实物相机精度、60 秒视觉里程碑或正式位姿验收。
- 这两次观察支持本次自然调用与有用取舍：复用实际产物、保留负面结果，并让短探查服务于可运行闭环；不证明持续稳定指导、普遍成熟或宿主 catalog 热刷新。未观察到新的 KMA 行为缺陷，本轮不再修改规则或安装；继续在实际 Paw 决策中观察效果，未发布。


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
