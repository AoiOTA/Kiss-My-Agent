# KISS My Agent 当前状态 Handoff

这是本仓库唯一的 canonical handoff。详细过程由 Git history、Issue 和 PR 保存，不创建 dated、attempt 或 campaign 副本。

## 当前 Release

- Canonical repository：[`AoiOTA/Kiss-My-Agent`](https://github.com/AoiOTA/Kiss-My-Agent)，公开 branch 为 `main`。
- 当前 supported release：[`v0.2.6`](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.2.6)；Plugin manifest 为 `0.2.6`，Git-backed marketplace ref 为 `v0.2.6`。
- Release 与 `main` commit 为 [`38f29be1a224a0687e5a6fdba3b1c18fff0a2bb8`](https://github.com/AoiOTA/Kiss-My-Agent/commit/38f29be1a224a0687e5a6fdba3b1c18fff0a2bb8)。实现 PR [#19](https://github.com/AoiOTA/Kiss-My-Agent/pull/19) 与 tracking issue [#18](https://github.com/AoiOTA/Kiss-My-Agent/issues/18) 均已关闭。
- Pages：[English](https://aoiota.github.io/Kiss-My-Agent/) · [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)。

## 当前行为

- KISS 不再固定 Master 的 model 或 reasoning effort；两者由 Host、对话选择或更高优先级配置决定。若账号可用，复杂 KISS 任务可从 Astra High 开始，但这不是强制默认。
- 当前 `kiss_explorer`、`kiss_coder` 与 `kiss_reviewer` seeds 均无 KISS role-level model pin，并将 `model_reasoning_effort` 设为 `medium`。显式 spawn 或 Host 的 `[agents]` 默认仍可能覆盖 Parent。
- Fresh setup 只创建缺失 starters。角色一旦存在即由用户所有；setup 与 Plugin update 不覆盖、自动迁移或判定其版本，用户后来删除的 starter 也不会被重建。
- Setup 只在两个旧 Master assignments 均为顶层唯一键、值精确为 `gpt-5.6-sol` / `max`、且各自带精确 managed marker 时成对删除。部分、无标记、修改过或冲突的状态保留，并提示用户手工恢复继承。
- 显式 remove 可按字节识别当前、v0.2.5 与 v0.1 role seeds；这些历史 snapshots 仅供 remove 比较，setup、check 与 configure 不读取它们来判版本或迁移角色。
- Setup、check 与 remove 只检查当前 scope 中会读取、创建、修改或删除的 KISS targets，不验证无关自定义角色。Plugin 暴露 `kiss-my-agent` 与 `kiss-my-agent-setup` 两个 Skills。

## 当前证据

- v0.2.6 tag 的 [Validate run](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34011252597) 在六个 OS/Python jobs 上全部通过；`main` 的 [Pages build/deploy](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/34011174208) 通过。
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
