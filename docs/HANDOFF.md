# KISS My Agent 当前状态 Handoff

这是本仓库唯一的 canonical handoff。不要创建 dated、attempt、final 或其他平行副本；Git history 保存历史。

## Repository、release 与 implementation baseline

- canonical repository：`AoiOTA/Kiss-My-Agent`，visibility 为 Public。
- canonical SSH remote：`git@github.com:AoiOTA/Kiss-My-Agent.git`。
- canonical branch：`main`。
- 当前 supported release：`v0.2.4`；Plugin manifest 为 `0.2.4`，Git-backed marketplace ref 为 `v0.2.4`。
- release implementation commit、`main` 与 tag 解引用目标均为 `95406cd0c02f7d7ae868a7f7fadf86d05bb8f0b4`。
- annotated tag object：`cc3c7e0acda431bd1b47f7d81a863d82ccd5d8cc`。
- release PR：[PR #10](https://github.com/AoiOTA/Kiss-My-Agent/pull/10)；head 为 `592a4f723f60eac6958428a216e242127e2d414f`，squash-merged 到上述 release implementation commit。
- GitHub Release：`https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.2.4`；发布于 `2026-09-03T12:57:24Z`，非 draft、非 prerelease。
- 本 handoff 后续形成的 commit 以实时 `origin/main` 为准，不在文档中维护会自引用的 handoff SHA。

## 当前实现与行为

- `.codex/config.toml` 有四项初始默认配置：Master `model = "gpt-5.6-sol"`、`model_reasoning_effort = "max"`，以及独立的 `features.multi_agent = true`、`agents.enabled = true`。
- `.codex/agents/*.toml` 是开放的 standalone role catalog。三个可编辑 starter roles 均使用 `gpt-5.6-sol`：`kiss_explorer` 与 `kiss_coder` 为 `high`，`kiss_reviewer` 为 `xhigh`。它们支持多实例，默认由 Master 扁平直接编排，不是固定团队或封闭 catalog。
- fresh scope 的 setup 创建缺失的 starter roles；任何已经存在的 role 都由用户所有，setup 与 Plugin update 不自动判断其版本、迁移或覆盖。已经 setup 的 scope 中，用户后来删除的 starter role 不会被重建。
- outdated v0.1 managed block 会刷新为当前 block；当两个 Master keys 都缺失时，setup 会把 `gpt-5.6-sol` / `max` 这一对一起补入。现有 feature assignments 与 role bytes 仍受保护。
- `.codex-plugin/plugin.json` 继续通过 `./skills/` 暴露 `kiss-my-agent` 与 `kiss-my-agent-setup` 两个 Plugin Skills；setup、check、remove 与已有 role 配置均由 conversational Setup Skill 完成，不恢复 v0.1 Python CLI。
- dogfooding 遇到 command 或 harness 失败时，先保留首错、缩小 execution surface 并区分产品行为、harness 与 environment，再决定是否继续。candidate 必须在 tag 前解决行为问题；tag 后只做 public-only verification。harness/environment 失败不触发 patch tag。
- Pages 英文根站点：`https://aoiota.github.io/Kiss-My-Agent/`。
- Pages 简体中文站点：`https://aoiota.github.io/Kiss-My-Agent/zh-CN/`。

## 保留的 v0.1.0 发布证据

- release implementation commit 为 `aa99956ff1348c477a41db692a3b0acf912f45b8`；annotated tag object `9a5ee1345f36b0827e9d9a1ca502fed3cd44f558` 解引用到该 commit。对应 [GitHub Release](https://github.com/AoiOTA/Kiss-My-Agent/releases/tag/v0.1.0) 正式发布，非 draft、非 prerelease。
- 当时的 README、CONTRIBUTING、SECURITY、INSTALLATION、CONFIGURATION、EXTENDING、FAQ、TESTING 共八对双语文档与已验证 Pages 语言入口均已完成。
- 公开前扫描覆盖全部 `6` 个历史提交；未发现密钥、令牌、私钥、敏感文件名、异常大对象或图片元数据。Commit 与 tag 的作者邮箱随公开 Git history 可见。
- `./scripts/validate.sh`：PASS。
- setup unit tests：`21/21` PASS。
- site unit tests：`9/9` PASS。
- site builder：生成 `16` 个 HTML、`19` 个文件、`0` 个 Markdown/JavaScript 文件。
- release commit Validate run `33540596481`：Ubuntu、macOS、Windows 全部 PASS。
- release commit Pages run `33540596573`：build 与 deploy PASS；两个站点实际返回 HTTP `200`，并呈现 release commit 内容。
- tag Validate run `33541006253`：Ubuntu、macOS、Windows 全部 PASS。
- 匿名 GitHub repository/API/HTTPS Git、Release 页面、tag tar.gz 与 zip archive：均可访问。
- `codex-cli 0.152.0` 通过公开 HTTPS Git marketplace 首次安装成功；marketplace clone 的 HEAD 为 release commit、tag 为 `v0.1.0`，plugin 状态为 `installed, enabled`、version 为 `0.1.0`。
- fresh authenticated session 从安装 cache 发现 plugin-owned `kiss-my-agent` 与 `kiss-my-agent-setup`，随后通过 setup Skill 完成 project setup 与静态 `check`；结果为 `structurally-valid`，三个 seed roles 存在。
- later fresh persisted session 依次真实调用三个 Host roles：explorer 只读返回 fixture anchors `alpha`、`beta`；coder 只创建并删除自己的 Smoke 文件；reviewer 独立只读审查并报告无重大问题。前后 fixture、managed setup hashes 与 Git 状态一致。
- setup `remove` 返回 `removed`，后续 `check` 返回预期的 `absent` 与非零退出；本次临时项目和隔离构建目录已删除，正式 plugin 保留安装。

## v0.1.0 证据解释与保留错误

- 第一次 role Smoke 额外使用了 `--ephemeral`，Host 报告 session persistence disabled，随后创建 child thread 时返回 `no thread with id`。该运行在角色任务创建前失败，按 failed precondition 记为 invalid run，不作为角色行为负面证据。
- 去掉计划未要求且与 child thread 不兼容的 `--ephemeral` 后，只做一次 persisted-session 判别重试；三个角色全部真实调用成功。不要删除或重写前述首错，也不要把无效运行冒充产品失败。
- 本次真实结果只支持 `codex-cli 0.152.0`、该安装、该项目 setup、这些 fresh sessions 与观察到的窄任务；不保证未来模型服从性、其他 Host 兼容性、一般研究有效性或额外权限。
- GitHub Actions 当前对 `actions/configure-pages@v5` 报 Node.js 20 deprecation warning，但 GitHub 强制使用 Node.js 24 后 build/deploy 成功；这不是本次 release blocker，也未为其扩大 workflow 范围。

## v0.2.4 deterministic 与公开发布证据

- PR head `592a4f723f60eac6958428a216e242127e2d414f`：Validate run `33755984050` 与 Pages run `33755984039` 均为 `success`。
- merged `main` `95406cd0c02f7d7ae868a7f7fadf86d05bb8f0b4`：Validate run `33756235515` 与 Pages run `33756235507` 均为 `success`。
- `v0.2.4` tag：Validate run `33756413784` 为 `success`。
- 英文与简体中文 Pages 均实际返回匿名 HTTP `200`，并呈现 `v0.2.4` 内容。
- Release HTML、tag zip 与 tar.gz 均实际返回匿名 HTTP `200`；Release 没有 binary assets。

## v0.2.4 public consumer evidence

证据按 gate 与来源分层；复用不等于重跑。

- A/B/C 复用 v0.2.3 的公开结果，因为 v0.2.4 只澄清 setup 的 outdated/current/absent 分类并收敛既有 dogfooding/release Rules，没有改变 fresh install、fresh setup/role discovery 或 intentional absence 的对应行为。没有把这些结果伪称为 v0.2.4 fresh 重跑：
  - A fresh public install：PASS。
  - B fresh setup 与 actual role：setup thread `01a06700-3c97-7cc0-a7ac-0ccfe408a628` 完成；Master thread `01a06704-9cc9-7761-a3d6-2dd693267f94` 实际调用 `kiss_explorer` child `01a06704-bf9d-7372-87ea-d64a558eeda1`。
  - C intentional absence：setup thread `01a06706-9359-7733-91df-0a9bb440f163` 保留已删除的 `kiss_reviewer`，check thread `01a06708-e560-7c40-b496-756bfe27bb1f` 报告 `structurally-valid` 与 `intentionally absent`。
- D 在 v0.2.4 thread `01a0674b-be78-7cd1-94d8-7b588f332bd6` 通过：outdated v0.1 managed block 刷新；两个缺失 Master keys 成对补齐；两个既有 feature assignments 保留；三份 role 文件经直接字节对比保持不变。
- E 在公开渠道通过：pin 到 `v0.1.0` 后，ordinary upgrade 仍保持 pinned；移除 fixed source 并恢复 unpinned current channel 后，解析与安装版本恢复为 `v0.2.4`。

这些是各自线程、安装与公开渠道的有界 Release evidence；不证明未来 Host、模型服从性、所有权限组合或一般可靠性。

## Human Pilot 与剩余边界

- 用户明确报告：修订后的 onboarding 已交给一位新用户阅读，结果为“可以通过”。这里只记录为 user-reported human Pilot，不冒充 tool-observed 结果、独立运行日志或逐项访谈记录。
- Issue #2 的 company-model acceptance 要求新用户在限定时间内具体解释 editable、flat company model 与 role responsibilities。现有简短报告没有保存该项的独立逐条回答，因此不能单独证明这一具体 criterion；是否以补充的人类记录关闭该边界仍由 owner 决定。

## 保留的 0.2 patch tag 结果

`v0.2.0`、`v0.2.1`、`v0.2.2`、`v0.2.3` annotated tags 均保留且不移动、删除或重建；它们没有 GitHub Release。

- `v0.2.0`：公开验证发现未限定的 raw Skill 调用不是 Codex 0.152.1 的 canonical Plugin invocation，并另有注入后的 compound-shell quoting failure，因此停止。
- `v0.2.1`：公开 v0.1 migration 在更新 AGENTS 后尝试同路径 Delete+Add legacy role 并失败；guarded rollback 精确恢复 before-state，因此停止。
- `v0.2.2`：公开 legacy-role transition 在写入前因 Plugin resource workdir/path 无法正确解析而停止；项目零修改，因此停止。
- `v0.2.3`：公开 gate D 暴露 `outdated` / `current` 措辞双义，导致 outdated v0.1 block 在两个 Master keys 都缺失时漏补 pair；已有 roles 实际保持不变，因此停止并由 v0.2.4 澄清分类。

## Review 记录

- PR #9 合并后晚到两条 review comments，均已评估但未以代码修改采纳：
  - 建议断言完整禁止句；该做法会把 static assertion 耦合到 generated wording，并与现有行为检查形成重复过测。
  - 建议按 PEP 8 增加 module constant 与 top-level function 间空行；仓库没有消费这一格式的 lint owner，本 follow-up 不做无消费者的样式改动。
- 这里不声称 all comments resolved。

## 当前停止线

`v0.2.4` 的 canonical repository、Pages、annotated tag、exact-SHA PR/main/tag CI、复用的未受影响 A/B/C、v0.2.4 D/E、GitHub Release 与匿名归档验证已经记录。到此停止。

- 不移动、删除重建或 force-push 任何已发布 tag 或 `main`。
- 不把复用、静态检查、user report 或 invalid run 提升为更高证据级别。
- 不因 harness/environment failure 补发 patch tag；后续行为修复先在 candidate 阶段完成。
- 后续只根据真实用户缺陷、Host 变化或明确的新目标重新立项，并继续区分 source、tests、CI、Pages、discovery、Smoke、Pilot 与 Release evidence。
