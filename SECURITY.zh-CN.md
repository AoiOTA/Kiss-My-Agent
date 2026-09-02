# 安全策略

[English](SECURITY.md) | [简体中文](SECURITY.zh-CN.md)

<a id="supported-versions"></a>
## 支持版本

KISS My Agent 只支持最新的正式 GitHub Release。项目没有长期支持或维护 branches；更早的 releases 与尚未发布的默认 branch snapshots 均不受支持。安全修复面向最新 release；正在准备 release 的修复可先进入默认 branch。这不构成响应时间或向后兼容性保证。

<a id="reporting"></a>
## 报告漏洞

使用仓库的[私密漏洞报告](https://github.com/AoiOTA/Kiss-My-Agent/security/advisories/new)。请提供受影响文件或行为、影响、复现条件与最小安全证明。不要在公开 issue 中放入凭证、私有数据、exploit 细节或敏感日志。

若私密报告以后不可用，请创建标题为 `Private security contact requested` 的公开 issue，但不要包含漏洞详情。Maintainer 可以通过仓库 Host 安排其他私有渠道。若没有 maintainer 响应，请使用 Host 的 abuse 或 security 渠道，不要公开披露敏感细节。

<a id="assessment-boundary"></a>
## 评估边界

报告按真实 plugin/marketplace metadata、setup/check/configure/remove scope、instruction 与 standalone-role discovery、配置、runtime 权限或验证行为评估。Instructions 不是安全边界。静态验证不能建立发布、真实安装、Host 隔离、模型服从、账户授权、网络策略或外部服务安全性。

<a id="safe-reproduction"></a>
## 安全复现

只提供最小复现，并删除 secrets 与私有路径。复现 setup 或 plugin 行为时使用隔离 project scope 与隔离 Codex home；绝不把破坏性 remove 测试指向 owner 不清的 scope。不得测试无权影响的系统、账户、数据或用户。在破坏性、不可逆或会干扰外部的动作前停止，并与 maintainers 私下协调。
