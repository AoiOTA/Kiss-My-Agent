# KISS My Agent 当前状态 Handoff

这是本仓库唯一的 canonical handoff。详细过程由 Git history、Issue 和 PR 保存，不创建 dated、attempt 或 campaign 副本。

## 当前 Release：v0.2.9（2026-09-12）

本候选整理 PawCerto 实际开发中已采用的八处指导与双语文档修正：对齐主动使用入口，明确完整委派包含执行、观察与常规恢复，并在最终依赖未完成时推进其他已就绪工作。未增加角色、工作流或运行时机制。

已有任务证据复用，不作为本轮重新执行：一次真实导出审查由主会话及原生 reviewer 主动读取指导并发现三项实际缺陷；一次真实报告任务在最终种子结果未到达时完成可用章节，收到结果后完成交付。期间也发生过用户纠正重复进度检查和遗漏就绪工作，故这些局部案例不证明持续调度可靠性或总体提速。最后指导审查未发现新的可操作冲突。本次仅补候选确定性检查、精确提交原生 CI、公开分发和新会话发现。

正式 [`v0.2.9`](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.2.9) 已于 `2026-09-12T06:17:59Z` 发布，非 draft、非 prerelease，无开发 cachebuster。[PR #29](https://github.com/AoiOTA/Kiss-My-Agent/pull/29) 候选 `4850229d308bfefb20513f89a04c7c8941c2a4b1` 通过本地完整 45 测试、16 页构建，以及 Linux/macOS/Windows × Python 3.11/3.12 六项原生 CI 和 Pages build；合并提交与不可变 tag 指向 `c2aa4ae1d18482c25b3a6e46c008aaa36a8fb243`，与已测候选的树相同。系统 Python 首次因缺少 Markdown 依赖停止；隔离环境安装既定 requirements 后通过，不是产品失败。

按 [TESTING](TESTING.md#upgrade-smoke) 在 tag 后验证：公开 ZIP 完整解码通过，含 82 个文件，manifest 与更新指导正确；双语 Pages HTTP 200 且显示 v0.2.9。隔离 Codex home 从公开 Git marketplace 安装 v0.2.8 后升级为 installed/enabled v0.2.9；Linux/bash、Codex CLI 0.153.4 的新 regular authenticated 会话在隔离 trusted project 的实际 catalog 中发现并读取两个 v0.2.9 Plugin Skills，exit 0。临时 home 的 PATH alias warning 未阻止安装或发现。原项目的活动安装未替换；此次结果不声称生产会话热加载。公共检查通过后才创建 GitHub Release。PawCerto 的行为验收与发布独立，不受 KMA 发布结果替代。

## 历史 Release：v0.2.8（2026-09-11）

- **用户恢复范围**：发布追踪见 [#26](https://github.com/AoiOTA/Kiss-My-Agent/issues/26)。本轮按用户授权完成 KMA v0.2.8 发布与本地安装更新。PawWeaver 继续暂停，原未完成目标保留，不启动新实验，也不追加 KMA 行为规则。
- **候选与发布内容**：基于已合并的 [PR #25](https://github.com/AoiOTA/Kiss-My-Agent/pull/25)，复用其中的完整交付与委派修正、指导加载复用、实验及真实 consumer 约束、原 v0.2.7 角色移除兼容和 build metadata 校验。候选 `342d559` 仅将 manifest、marketplace ref 与双语 README badge 对齐到 `0.2.8` / `v0.2.8` 并更新交接；历史 tag、兼容 snapshots 和测试 fixture 保留。[PR #27](https://github.com/AoiOTA/Kiss-My-Agent/pull/27) 已合并。
- **正式发布**：[`v0.2.8`](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.2.8) 于 `2026-09-11T05:42:40Z` 发布；API latest 指向该版本，非 draft、非 prerelease。发布提交为 [`f51716eae9b1b0d1f7ff9a926645bcd3ede87ff5`](https://github.com/AoiOTA/Kiss-My-Agent/commit/f51716eae9b1b0d1f7ff9a926645bcd3ede87ff5)，不可变 annotated tag 对象为 `59ece882da8fb60f06a172b211a9e9cbeed2009a`。
- **确定性检查**：候选及合并提交的 `python scripts/test_all.py` 均通过：45 tests、16 页隔离站点构建、repository validation、Git whitespace 与工作树不变检查。PR 的 [Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34566608041) 六个 native jobs 和 [Pages build](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34566608081) 通过；合并提交的 [Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34566686228)、[Pages build/deploy](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34566686224) 与 [tag Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34566707837) 均通过。
- **公开分发**：Release 页面与 GitHub 源码 ZIP / TAR 链接（跳转 codeload）均返回 HTTP 200；[English Pages](https://aoiota.github.io/Kiss-My-Agent/) 与[简体中文 Pages](https://aoiota.github.io/Kiss-My-Agent/zh-CN/) 均返回 HTTP 200，HTML 包含 `v0.2.8`。公开 codeload ZIP 与 TAR 均返回 HTTP 200，各自全部 82 个 tracked files 与 tag 逐字节一致。隔离 Codex home 通过公开 Git marketplace 的 `v0.2.8` ref 安装后为 installed/enabled `0.2.8`，安装缓存的 82 个文件也与 tag 一致；CLI 仅报告临时 home 的 PATH alias warning，没有安装失败。
- **本地更新与新会话**：生产 personal 插件源及缓存已由开发 suffix 更新为精确 `0.2.8`，各自 82 个文件均与 tag 一致。Fresh Codex CLI `0.153.4` 会话的实际 catalog 发现并读取 `0.2.8` 缓存中的两个 Skills，确认指导复用与停止边界。
- **证据边界与停止**：复用 PR #25 未变的局部行为证据；本轮没有重跑 Desktop 生命周期、setup 或完整 upgrade 矩阵。检查、公开分发和 CLI 发现不证明普遍行为可靠性、量化效率收益或机器人学习成功。KMA 发布与本地更新完成后停止推进，Paw 的暂停边界不变。

## PawWeaver dogfooding · 发布后暂停（2026-09-11）

- **当前停止边界**：用户已授权完成当前最后一轮奖励诊断后，将 KMA 与 PawWeaver 分别提交、推送远程，然后暂停推进。不再启动新训练或新规则修改；原来的稳定全身控制、完整末端位姿与 KMA 实际行为收益目标仍未完成，暂停后不自动继续。
- **Paw 当前证据**：full500 与 alpha25 STOP326 均为负结果；normalizer 的闭环对照不支持直接换回旧 N 作为修复。最后的 reward6case 已完成：共同末期宽度下，前进／后退／高位的保持窗实际加权非终止奖励均降低（6.36999→5.65574、6.55069→.54430、2.34501→2.10926，乘控制dt前），不支持这些固定任务上退化行为获得更高配置奖励；仍未确定唯一训练根因。首次原生启动失败139，原样单次重试后两组各3例均完整60秒；本地读出语法错误已修正并复用原轨迹，GPU已释放。短诊断、稳定片段与减少跌倒均不证明学习成功；单一 18 关节 Actor、原性能要求、完整位姿及支撑协调目标和临时硬件证据边界保留。
- **KMA 已有改动及实际使用**：`40cfc16` 澄清无可用委派时可继续授权工作；`8931a47` 将委派选择放在完整交付与上下文中判断；`a217b97` 保留组件诊断所需的真实下游 consumer 约束。这些已有修正已部署到稳定技能入口，随后真实工作使用小范围 CPU 因子诊断、纠正评估及数据 caller、合并 dev11 以减少重复案例，并在出现明确遗忘时正常停止。它们支持具体局部行为记录，不证明量化效率提升、普遍遵循或机器人学习成功；本次收尾不增加规则。
- **当时合并与发布范围**：dogfood 分支以普通 merge 保留本地累积提交及远程 `f3f6204` 的 v0.2.7 发布证据。该阶段仅提交并推送开发结果，不改版本、不创建 tag 或 Release，不把这批未打标改动描述为已发布 v0.2.7 的验收结果。

## PawWeaver dogfooding · 上一阶段记录（2026-09-10）

- **按用户要求收尾后停止**：PawWeaver的稳定全身控制与KMA的整体行为收益均未证明完成。用户明确要求完成当前阶段后测、视频、提交和Paw远程推送后停止推进；不再启动训练、速度指令分支或KMA新修正。后续工作需要用户重新提出，不因原持续目标自动延长本阶段。
- **已定位的触发故障**：此前新delegated explorer收到旧Host技能目录，版本化入口已不存在，首次读取报ENOENT。Paw项目以非受管本地说明指向稳定personal插件源；通用模板不嵌入机器路径。随后master与已有文献explorer的实际Host目录均更新到`0.2.7+codex.20260910054223`，入口读取成功；这支持这两个实际消费者的发现路径恢复，不能推广为所有旧child已热加载或所有Host故障解决。
- **当前产品修正**：`276da57` 将入口、仓库指令和setup模板的逐assignment读取要求改为每agent首次KMA工作加载、跨后续分工和continuation复用；只为已知更新或缺失相关细节重读，保留在行动选择、分工和结果解释时主动应用。随后 `82b2241` 针对本轮仅借用部分成熟配方后继续调参的失误，重写已有配方段：适配方法未产生预期行为时，先看少数可能提供该行为的遗漏／变化条件，再选下一实验，不形成全量复现清单。personal插件现安装 `0.2.7+codex.20260910054223`；这条新指导尚无独立行为收益证据。18项setup契约、skill与plugin检查通过；初次repo validator暴露本handoff既存机器绝对路径，本次更新移除，不隐去失败。
- **行为收益的实际边界**：已有运动读出、2ms对齐、PD映射和旧对照得到复用；CPU后测与GPU后测、视频按实际资源重叠执行，没有扩建调度平台。任务参数和调度仍受master明确限定，不能独立归因于KMA。Master还低估了相同奖励宽度下的持续退化，需用户再次指出后才停止最后一轮；入口被读取与这些局部改进不能替代研究决策有效性的证明。保留该失败，不为本阶段收尾再叠加同义规则。
- **Paw当前结果**：2000轮训练及双引擎全部后测、状态回放视频已完成。PhysX独立64例11通过位置条件、24跌倒；MuJoCo12通过、36跌倒；静态16例仅3/2成功。长期悬足、贴限位与远目标倒地未达到用户参考视频的效果。已有局部精度、移支撑和身体／臂共同运动证据，不能替代稳定全身控制。临时硬件参数仍不支持硬件有效性或正式验收。
- **本阶段追加实验结果**：支撑配方在记录336轮后停止，所选最新301轮策略完成全部后测和视频；双引擎独立64例均0位置通过，跌倒4/7，远目标出现大腿持续接触，不能称合理支撑改善。固定低噪声候选从旧2000轮策略开始，在274轮后因同奖励宽度下持续退化停止，采用最新已保存251轮策略；独立64例两引擎仍均0位置通过、跌倒16/27。两轮都没有跑完原定1000轮，也未采用为完整WBC成果。减小采样噪声并未解决整体学习问题；大KL与奖励裁零不能单独证明某个失败原因。原性能数值、单18关节Actor和临时硬件证据边界保持。用户允许的速度指令＋EE路线只核实了来源和任务坐标系差异，本阶段未实现。
- **继续复用**：Paw的 `wbc_random_training/` 已有完整训练、跨引擎结果和动作读出；没有关节顺序／单位错误证据，不为新checkpoint重复该检查。MuJoCo读出5.26mm残差已定位为2ms积分前后状态错位，同轨迹CPU修复保留真实失败；这是必要测量修正。旧softsign、单独越界正则及progress负结果继续有效，详细过程留在原Paw产物和Git。此前metadata equality gate误阻断已在现有product-contract案例修复，不重新建立证明包。

## v0.2.7 历史 Release：Astra 增量升级（基于 v0.2.6）

- 基线：`v0.2.6` / `38f29be1a224a0687e5a6fdba3b1c18fff0a2bb8`。保留原有规则、案例和保护机制，只修委派矛盾与默认配置。
- 缺失 Master 配置默认 Astra/high，新角色 Astra/medium，实验上下文默认 true；已有显式值与已有角色保留。准确完整的受管 Sol/max pair 更新为 Astra/high。
- 升级路径：更新插件 → 原 scope setup → 显式 configure 选定角色 → 新建可信客户端任务。静态配置与实际加载分别验收。
- 当时 supported Release：[`v0.2.7`](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.2.7)，manifest 为 `0.2.7`、marketplace ref 为 `v0.2.7`；2026-09-06 发布后 API latest 指向该版本，非 draft、非 prerelease。
- 发布提交为 [`12db499b58b6ac4929ad42af8366622bdeec7bd3`](https://github.com/AoiOTA/Kiss-My-Agent/commit/12db499b58b6ac4929ad42af8366622bdeec7bd3)，tree 为 `7865fde48c029947f8c18b917f4e4a794fceefa0`；不可变 annotated tag 对象为 `33f93d10465d5b0ded2d5cee148d348a7e30e5e6`，解引用至该发布提交。实现 PR [#23](https://github.com/AoiOTA/Kiss-My-Agent/pull/23) 已 squash 合并；发布追踪见 [#22](https://github.com/AoiOTA/Kiss-My-Agent/issues/22)。本节之外的 v0.2.6 历史事实不作为 v0.2.7 验证结果。
- PR 的 [Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34021930732) 与 [Pages build](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34021930737) 通过；合并提交的 [Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34022627262)、[Pages build/deploy](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34022627859) 与 [tag Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34022770572) 通过。合并提交的完整 deterministic 检查通过；中英文 Pages 已核对新版内容。
- 本轮静态证据：完整 `scripts/test_all.py` 通过，42 tests、16 页隔离站点构建、whitespace 与 repository-state 检查通过；两个 Skill 的 `quick_validate` 和 Plugin validation 通过。独立审查发现的两处安装文档矛盾已修复并复核关闭；原有角色正文与历史 snapshots 的保留已核验。
- 隔离 CLI 运行：Codex `0.153.2`、ChatGPT 登录、临时 Codex home 和本地 marketplace，使用临时 cachebuster 的隔离候选缓存（临时后缀不用于发布元数据）。Fresh setup 经独立断言确认 Master Astra/high、三个 seeds Astra/medium、context true，并保留 AGENTS 外部前缀。CLI features 报告 context/multi_agent true；这属于配置加载证据，不是历史检索行为证明。
- 一次有界三角色 Smoke 通过：宿主 rollout turn context 确认 Master Astra/high 与三个不同子代理 Astra/medium；explorer 读取 fixture，coder 独占创建、验证并删除临时文件，reviewer 识别 add→subtract 回归。Fixture、config 与 AGENTS 无遗留修改。
- 升级首轮经独立断言确认：完整标记 Sol/max 更新为 Astra/high，显式 context false 保留，自定义 explorer 与原 v0.2.6 coder 字节不变，已删除 reviewer 未恢复，AGENTS 外部前缀保留且受管块刷新。同一升级 fixture 的后续生命周期经独立断言确认：check 为 `structurally-valid`，context false 单独报告且不判为 disabled；重复 setup 前后文件映射逐字节相同；remove 删除精确 v0.2.6 coder，保留自定义 explorer，reviewer 仍缺失，AGENTS 恢复为原外部文本，剩余 TOML 保留用户注释、原表（包括 context 子表）与显式 context false。本轮运行覆盖不扩展为 global、configure、fresh-remove 或完整失败矩阵。
- 运行限制：首次 workspace-write 因 `.codex` 只读保护被阻止，属于 invalid harness，零产品修改；随后仅对隔离 fixture 使用 danger-full-access，因此没有 sandbox enforcement 证据。Smoke 中 `python` 不存在并返回 127，保留原失败后改用 `python3` 成功。
- 公开分发：tag ZIP/TAR 与全部 79 个 tracked files 精确相符；隔离 Codex home 通过公开 Git marketplace 新装和新 CLI 会话发现两个 v0.2.7 Skills。现有 `kiss-my-agent` marketplace 定向更新后，实际插件为 installed/enabled v0.2.7；其他 marketplace 未更新。正式发布后 Release 页面和两种源码归档均 HTTP 200。
- Ubuntu 桌面验收：Host `0.153.4`（记录中的 source 为 `vscode`）重启后的新任务实际加载两个 v0.2.7 Skills。独立项目 setup 补入 Astra/high/context true，三个旧角色逐字节保留；显式 configure 对每个选定角色仅增加 `model = "gpt-6-astra"`，medium、sandbox 与正文不变。
- 新桌面有界协作任务完成并由 Master 验收：Host 记录确认 parent Astra/high；三次 spawn 没有 model/effort override，三个不同 child 各为 Astra/medium。Explorer 给出正确 fixture 锚点，coder 独占创建、逐字节读回并删除 31 字节临时文件，reviewer 找出 add→subtract 错误。用户原工作区改动、全局 config、AGENTS 与角色保持不变。
- 桌面上下文证据为项目静态 true、Host 实际注入 context management guidance 和 `get_context_remaining` 工具；Host 未直接暴露有效 `experimental_mode` 布尔值，因此不声明该值的独立运行时读取，也未测试跨窗口或长上下文行为。
- 首次桌面新任务仍暴露 v0.2.6 Skill catalog，按停止线未执行 setup/configure/smoke；完整重启客户端后解除。后续 setup 子代理一次 `server_overloaded`，保留失败后在同一 Astra 模型重试成功。这两项属于 Host 环境观察，不是 tagged source 缺陷，tag 未改变。

## v0.2.6 历史 Release

- Canonical repository：[`AoiOTA/Kiss-My-Agent`](https://github.com/AoiOTA/Kiss-My-Agent)，公开 branch 为 `main`。
- 当时 supported release：[`v0.2.6`](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.2.6)；Plugin manifest 为 `0.2.6`，Git-backed marketplace ref 为 `v0.2.6`。
- v0.2.6 tag 与 Release commit 为 [`38f29be1a224a0687e5a6fdba3b1c18fff0a2bb8`](https://github.com/AoiOTA/Kiss-My-Agent/commit/38f29be1a224a0687e5a6fdba3b1c18fff0a2bb8)。实现 PR [#19](https://github.com/AoiOTA/Kiss-My-Agent/pull/19) 与 tracking issue [#18](https://github.com/AoiOTA/Kiss-My-Agent/issues/18) 均已关闭。
- Pages：[English](https://aoiota.github.io/Kiss-My-Agent/) · [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)。

## v0.2.6 历史行为

- v0.2.6 KISS 不再固定 Master 的 model 或 reasoning effort；两者由 Host、对话选择或更高优先级配置决定。若账号可用，复杂 KISS 任务可从 Astra High 开始，但这不是强制默认。
- v0.2.6 `kiss_explorer`、`kiss_coder` 与 `kiss_reviewer` seeds 均无 KISS role-level model pin，并将 `model_reasoning_effort` 设为 `medium`。显式 spawn 或 Host 的 `[agents]` 默认仍可能覆盖 Parent。
- Fresh setup 只创建缺失 starters。角色一旦存在即由用户所有；setup 与 Plugin update 不覆盖、自动迁移或判定其版本，用户后来删除的 starter 也不会被重建。
- Setup 只在两个旧 Master assignments 均为顶层唯一键、值精确为 `gpt-5.6-sol` / `max`、且各自带精确 managed marker 时成对删除。部分、无标记、修改过或冲突的状态保留，并提示用户手工恢复继承。
- v0.2.6 显式 remove 可按字节识别该版本、v0.2.5 与 v0.1 role seeds；这些历史 snapshots 仅供 remove 比较，setup、check 与 configure 不读取它们来判版本或迁移角色。
- Setup、check 与 remove 只检查当前 scope 中会读取、创建、修改或删除的 KISS targets，不验证无关自定义角色。Plugin 暴露 `kiss-my-agent` 与 `kiss-my-agent-setup` 两个 Skills。

## v0.2.6 历史证据

- v0.2.6 tag 的 [Validate run](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34011252597) 在六个 OS/Python jobs 上全部通过；该 release commit 的 [Pages build/deploy](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34011174208) 通过。
- Candidate fresh-session 验证通过 setup、check 与再次 setup no-op。精确带标记的旧 Sol/max pair 被清理；已有 v0.2.5 roles保持不变；单角色 configure 与 remove-only compatibility 均通过。
- Desktop candidate 验证中，对话切换后连续两轮保持 Astra/high；Master 只委派一个 `kiss_explorer`，该 child 使用 Astra/medium。
- Public marketplace upgrade 后，Plugin 为 installed/enabled v0.2.6，fresh public CLI 成功发现两个 v0.2.6 Skills。Public parent thread `01a074f9-7cd8-7f21-8ccd-e281d2e3d045` 使用 Astra/high；其唯一 `kiss_explorer` child `01a074f9-ae2e-70d3-8d2e-f8f8bc888716` 使用 Astra/medium。

## 已知限制

- Plugin 用户不需要 Python、Node.js 或 Docker；Git-backed marketplace 安装和更新仍需要可用的 Git 与 GitHub 网络访问。
- Setup 的静态 `check` 只证明被检查文件的状态；加载、discovery 或模型切换仍需可信的新会话验证。
- v0.2.6 发布时观察到一个长时间运行的 Desktop process：CLI 已升级且旧 cache 已不存在后，它创建的新任务仍持有旧 v0.2.5 Skill catalog；fresh public CLI 能正确加载 v0.2.6。若 fresh Desktop 验证出现旧 cache path，应先完全退出并重新打开 Codex。这是 Host lifecycle 证据，不是 KISS 产品失败。
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
| `v0.2.7` | 有 | 保留 v0.2.6 设计，设置缺失 Astra/high 与角色 Astra/medium 默认值，实验上下文默认开启；局部委派修复、生命周期兼容、公开分发及桌面三角色有界验收通过。 |
| `v0.2.8` | 有 | 发布 PawWeaver dogfood 的有据局部修正；确定性检查、公开归档、新装、本地更新和 fresh CLI 发现通过，未扩大行为收益声明。 |

所有已推送 tags 都保留且不可移动、删除或重建。没有 GitHub Release 的 tag 不描述为正式发布版本。

## 停止线

- 不移动、删除、重建任何已推送 tag，也不 force-push `main`。Candidate 阶段解决产品行为问题；tag 后只补 public-only evidence，不重复未受影响的 candidate checks。
- Tagged source 中的产品缺陷阻止创建 Release，并由下一 patch 修复；harness、command、environment 或 evaluator failure 修复其 owner 后针对同一 tag 补证据，不自动触发 patch。
- 后续只根据真实用户缺陷、Host 变化或明确的新目标重新立项；满足有界验收或得到受支持的 no-change 结论后停止。
