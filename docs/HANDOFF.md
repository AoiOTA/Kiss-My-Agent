# KISS My Agent 当前状态 Handoff

这是本仓库唯一的 canonical handoff。不要创建 dated、attempt、final 或其他平行副本；Git history 保存详细过程。

## 当前 Release

- Canonical repository：[`AoiOTA/Kiss-My-Agent`](https://github.com/AoiOTA/Kiss-My-Agent)，公开 branch 为 `main`。
- 当前 supported release：[`v0.2.4`](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.2.4)；Plugin manifest 为 `0.2.4`，Git-backed marketplace ref 为 `v0.2.4`。
- Release implementation commit 为 [`95406cd0c02f7d7ae868a7f7fadf86d05bb8f0b4`](https://github.com/AoiOTA/Kiss-My-Agent/commit/95406cd0c02f7d7ae868a7f7fadf86d05bb8f0b4)；release PR 为 [#10](https://github.com/AoiOTA/Kiss-My-Agent/pull/10)。后续 `main` 以远程实时状态为准，本文件不维护会自引用的 handoff commit。
- Pages：[English](https://aoiota.github.io/Kiss-My-Agent/) · [简体中文](https://aoiota.github.io/Kiss-My-Agent/zh-CN/)。

## 当前行为

- `.codex/config.toml` 为 Master 提供 `gpt-5.6-sol` / `max` 初始默认值，并独立补默认 `features.multi_agent = true` 与 `agents.enabled = true`。
- 开放的 standalone role catalog 初始提供 `kiss_explorer`、`kiss_coder` 与 `kiss_reviewer`；默认 model 均为 `gpt-5.6-sol`，effort 分别为 `high`、`high`、`xhigh`。Master 默认扁平直接调度，可按需使用同角色多个实例。
- Fresh setup 只创建缺失 starters。角色一旦存在即由用户所有；setup 与 Plugin update 不覆盖、迁移或判定其版本，用户后来删除的 starter 也不会被重建。
- Recognized-outdated v0.1 managed block 可刷新为当前 block；两个 Master keys 都缺失时才成对补入默认值。已有 feature assignments 与 role bytes 保持不变。
- Plugin 暴露 `kiss-my-agent` 与 `kiss-my-agent-setup` 两个 Skills。Setup、check、remove 与已有 role 配置由 conversational Setup Skill 完成，不恢复 v0.1 Python CLI。

## 当前证据

- PR #10、merged `main` 与 `v0.2.4` tag 的原生 CI 均通过：[PR Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33755984050)、[PR Pages](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33755984039)、[main Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33756235515)、[main Pages](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33756235507)、[tag Validate](https://github.com/AoiOTA/Kiss-My-Agent/actions/runs/33756413784)。
- v0.2.4 的 Release 页面、tag zip、tag tar.gz 与中英文 Pages 均已匿名访问并返回 HTTP `200`；Release 非 draft、非 prerelease，无 binary assets。
- v0.2.4 公开验证复用了 v0.2.3 中未受影响的 public fresh install、fresh setup/role discovery 与 intentional starter absence 结果，没有把复用伪称为 v0.2.4 fresh 重跑。v0.2.4 另行观察到 outdated setup 分类修正和从 pinned old source 返回 unpinned current channel；两项均通过。
- 一名新用户阅读修订后的 onboarding 后由用户报告“可以通过”。这是 user-reported Pilot，不是独立日志，也不能证明普遍可用性。

## v0.1.0 正式发布证据

- [`v0.1.0`](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.1.0) 是正式 GitHub Release；release implementation commit 为 `aa99956ff1348c477a41db692a3b0acf912f45b8`。
- Release commit、Pages 与 tag 的 Ubuntu、macOS、Windows CI 均通过；公开 repository、Release 页面与 archives 可匿名访问，中英文 Pages 返回 HTTP `200`。
- 在 `codex-cli 0.152.0` 上，公开 Git marketplace 的首次安装、fresh-session Skill discovery、project setup/check、三个 starter roles 的各一次窄任务以及 remove 均观察通过。
- 首次 role 运行因额外使用不兼容的 `--ephemeral` 而在创建 child thread 前失败，属于 invalid run；去掉该非必需参数后只做了一次判别重试。它不构成产品负面证据，也没有被隐藏。

## Release 历史

| Tag | GitHub Release | 一行结果 |
| --- | --- | --- |
| `v0.1.0` | 有 | 首个正式公开版本；安装、discovery、setup 与窄 role Smoke 通过。 |
| `v0.2.0` | 无 | 公开验证暴露非 canonical Skill invocation 与 harness quoting 问题，停止发布。 |
| `v0.2.1` | 无 | Legacy-role transition 出现产品写入失败；rollback 恢复 before-state，停止发布。 |
| `v0.2.2` | 无 | Public transition 在写入前遇到 Plugin resource path 解析问题，项目零修改，停止发布。 |
| `v0.2.3` | 无 | Public setup 暴露 outdated/current 分类歧义，保留 tag，由下一 patch 修正。 |
| `v0.2.4` | 有 | 当前 supported release；分类修正、公开分发与有界升级证据通过。 |

所有已推送 tags 都保留且不可移动、删除或重建。没有 GitHub Release 的 tag 不应被描述为正式发布版本。

## 证据与剩余限制

- Source inspection、deterministic tests、CI、Pages、fresh-session discovery、Smoke、Pilot 与 Release verification 是不同证据层级；复用、user report 或 invalid run 不得提升为更强结论。
- 当前 live evidence 只覆盖记录的 Codex 0.152.x 环境、安装、项目与窄任务，不保证未来 Host、模型服从性、全部 OS/权限组合、一般研究有效性或 crash atomicity。
- Plugin 用户不需要 Python、Node.js 或 Docker；Git-backed marketplace 安装和更新仍需要可用的 Git 与 GitHub 网络访问。
- Setup 的静态 `check` 只证明被检查文件的状态；加载或 discovery 改变仍需可信的新会话验证。

## 当前停止线

- 不移动、删除、重建任何已推送 tag，也不 force-push `main`。
- Candidate 阶段解决产品行为问题；tag 后只补 public-only evidence，不重复未受影响的 candidate checks。
- Tagged source 中的产品缺陷会阻止创建 Release，并由下一 patch 修复；harness、command 或 environment failure 修复其 owner 后针对同一 tag 补证据；evaluator/invalid run 不触发 patch。正式 Release 后发现产品缺陷才发布新 patch。
- 后续只根据真实用户缺陷、Host 变化或明确的新目标重新立项；满足有界验收或得到受支持的 no-change 结论后停止。
