# KISS My Agent 当前状态 Handoff

这是本仓库唯一的 canonical handoff。不要创建 dated、attempt、final 或其他平行副本；Git history 保存详细过程。

## 当前 Release

- Canonical repository：[`AoiOTA/Kiss-My-Agent`](https://github.com/AoiOTA/Kiss-My-Agent)，公开 branch 为 `main`。
- 当前 supported release：[`v0.2.5`](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.2.5)；Plugin manifest 为 `0.2.5`，Git-backed marketplace ref 为 `v0.2.5`。Release 已于 2026-09-03 发布，非 draft、非 prerelease，无 binary assets。
- Release implementation commit 为 [`8f07260ef3f090ca8d3516add0f3dce906854402`](https://github.com/AoiOTA/Kiss-My-Agent/commit/8f07260ef3f090ca8d3516add0f3dce906854402)；release PR 为 [#16](https://github.com/AoiOTA/Kiss-My-Agent/pull/16)，head 为 `97f9d232134155cefa0de8e0a9e03475486a321b`，squash merge commit 为上述 release commit，二者 tree 均为 `79310dd98fdb881205c44613732ec8b78e5323ec`。Annotated tag object 为 `a4bc05c1f25a5e9df6952b49e66f35904364b835`，解引用到同一 release commit。
- Pages：[English](https://aoiota.github.io/Kiss-My-Agent/) · [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)；当前页面包含 `v0.2.5` badge。

## 当前行为

- `.codex/config.toml` 为 Master 提供 `gpt-5.6-sol` / `max` 初始默认值，并独立补默认 `features.multi_agent = true` 与 `agents.enabled = true`。
- 开放的 standalone role catalog 初始提供 `kiss_explorer`、`kiss_coder` 与 `kiss_reviewer`；默认 model 均为 `gpt-5.6-sol`，effort 分别为 `high`、`high`、`xhigh`。Master 默认扁平直接调度，可按需使用同角色多个实例。
- Fresh setup 只创建缺失 starters。角色一旦存在即由用户所有；setup 与 Plugin update 不覆盖、迁移或判定其版本，用户后来删除的 starter 也不会被重建。
- Setup、check 与 remove 只检查当前 scope 中 KISS 管理的 config、instructions 和三个精确 bundled role targets；不检查无关自定义角色或另一 scope 的 role catalog。Configure 只在用户选定角色后检查该精确目标。
- Recognized-outdated v0.1 managed block 可刷新为当前 block；两个 Master keys 都缺失时才成对补入默认值。已有 feature assignments 与 role bytes 保持不变。
- Plugin 暴露 `kiss-my-agent` 与 `kiss-my-agent-setup` 两个 Skills。Setup、check、remove 与已有 role 配置由 conversational Setup Skill 完成，不恢复 v0.1 Python CLI。

## 当前证据

- PR #16、merged `main` 与 `v0.2.5` tag 的原生 CI 均通过：[PR Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33793420892) 6 项成功；[PR Pages](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33793420761) build 成功、deploy 按 PR 规则跳过；[main Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33793745323) 6 项成功；[main Pages](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33793745268) build 与 deploy 成功；[tag Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33793992806) 6 项成功。
- 最终 candidate 的 setup contract 在 fresh sessions 中获得有界证据：check `01a06894` 报告 `structurally-valid`、managed block `current` 且零写入；setup `01a06896` 为 no-op；marker run `01a06898` 只创建一个 child `01a06899` 并返回 `PROJECT_MARKER`，结论为 `GO`。
- Candidate 前两次运行均为 invalid：第一次是 Agent 构造的 `apply_patch` 命令包含无效 `[?]` 并已 rollback，归属 command-construction harness；第二次使用手工准备的 stale `AGENTS.md` 并以复合 shell status 误判结果，归属 harness/evaluator。两者都没有成为产品负面证据，也没有触发新 patch。
- Public unpinned upgrade 已从 v0.2.4 更新至 v0.2.5，cache 与 marketplace 分别指向 release commit `8f07260` 和 ref `v0.2.5`，工作状态干净。Public fresh check `01a068aa` 从公开 v0.2.5 cache 加载并观察 `absent`、零写入；临时项目与精确添加的 trust 已清理，无关 config bytes 保持不变且 mode 仍为 `600`。
- Release 页面、tag zip、tag tar.gz、安装指南、Testing 与中英文 Pages 均已匿名访问并返回 HTTP `200`。Tracking [#15](https://github.com/AoiOTA/Kiss-My-Agent/issues/15) 已以 completed 关闭，并记录[最终证据](https://github.com/AoiOTA/Kiss-My-Agent/issues/15#issuecomment-5530810027)。

## Release 历史

| Tag | GitHub Release | 一行结果 |
| --- | --- | --- |
| `v0.1.0` | 有 | 首个正式公开版本；公开安装、discovery、project setup/check、三个 starter roles 的各一次窄任务与 remove 在 Codex CLI 0.152.0 上观察通过。 |
| `v0.2.0` | 无 | 公开验证暴露非 canonical Skill invocation 与 harness quoting 问题，停止发布。 |
| `v0.2.1` | 无 | Legacy-role transition 出现产品写入失败；rollback 恢复 before-state，停止发布。 |
| `v0.2.2` | 无 | Public transition 在写入前遇到 Plugin resource path 解析问题，项目零修改，停止发布。 |
| `v0.2.3` | 无 | Public setup 暴露 outdated/current 分类歧义，保留 tag，由下一 patch 修正。 |
| `v0.2.4` | 有 | 正式 Release；分类修正、公开分发与有界升级证据通过。 |
| `v0.2.5` | 有 | 当前 supported release；Setup 缩小到精确 KISS targets，candidate、CI、公开升级与 fresh check 通过。 |

所有已推送 tags 都保留且不可移动、删除或重建。没有 GitHub Release 的 tag 不应被描述为正式发布版本。`v0.1.0` 的首次 role 运行曾因额外使用不兼容的 `--ephemeral` 而在创建 child thread 前失败；去掉该非必需参数后只做一次判别重试，因此该 invalid run 不构成产品负面证据。

## 证据、限制与停止线

- Source inspection、deterministic tests、CI、Pages、fresh-session discovery、Smoke、Pilot 与 Release verification 是不同证据层级；复用、user report 或 invalid run 不得提升为更强结论。
- v0.2.5 没有运行其他 roles、global setup、remove、rollback、configure runtime、其他 Host/version 或 failure matrix。Fresh CLI 仍出现既存 icon `..` warning，但实际 Skill 加载与 check 成功；不把该 warning 隐藏或提升为产品失败。
- Plugin 用户不需要 Python、Node.js 或 Docker；Git-backed marketplace 安装和更新仍需要可用的 Git 与 GitHub 网络访问。Setup 的静态 `check` 只证明被检查文件的状态；加载或 discovery 改变仍需可信的新会话验证。
- 不移动、删除、重建任何已推送 tag，也不 force-push `main`。Candidate 阶段解决产品行为问题；tag 后只补 public-only evidence，不重复未受影响的 candidate checks。
- Tagged source 中的产品缺陷会阻止创建 Release，并由下一 patch 修复；harness、command 或 environment failure 修复其 owner 后针对同一 tag 补证据；evaluator/invalid run 不触发 patch。正式 Release 后发现产品缺陷才发布新 patch。
- 后续只根据真实用户缺陷、Host 变化或明确的新目标重新立项；满足有界验收或得到受支持的 no-change 结论后停止。
