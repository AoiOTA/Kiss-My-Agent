# 安全策略

[English](SECURITY.md) | [简体中文](SECURITY.zh-CN.md)

<a id="supported-versions"></a>
## 支持版本

KISS My Agent 仍处于早期阶段，没有正式 releases 或长期支持 branches。安全修复面向当前默认 branch；这不构成响应时间或兼容性保证。

<a id="reporting"></a>
## 报告漏洞

优先使用仓库 Host 的私有漏洞报告功能。请提供受影响文件或行为、影响、复现条件与最小安全证明。不要在公开 issue 中放入凭证、私有数据、exploit 细节或敏感日志。

若私有报告不可用，请创建标题为 `Private security contact requested` 的公开 issue，但不要包含漏洞详情。Maintainer 可以通过仓库 Host 安排私有渠道。若没有 maintainer 响应，请使用 Host 的 abuse 或 security 渠道，不要公开披露敏感细节。

<a id="assessment-boundary"></a>
## 评估边界

报告按真实 instruction discovery、安装、配置、runtime 权限或验证行为评估。Instructions 不是安全边界。静态验证不能建立 Host 隔离、模型服从、账户授权、网络策略或外部服务安全性。

<a id="safe-reproduction"></a>
## 安全复现

只提供最小复现，并删除 secrets 与私有路径。不得测试无权影响的系统、账户、数据或用户。在破坏性、不可逆或会干扰外部的动作前停止，并与 maintainers 私下协调。
