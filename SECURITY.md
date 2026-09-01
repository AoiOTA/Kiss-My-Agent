# Security Policy

[English](SECURITY.md) | [简体中文](SECURITY.zh-CN.md)

<a id="supported-versions"></a>
## Supported Versions

KISS My Agent is early-stage and has no formal releases or long-term-support branches. Security fixes target the current default branch. This is not a response-time or compatibility guarantee.

<a id="reporting"></a>
## Reporting a Vulnerability

Use the repository host's private vulnerability-reporting feature when available. Include the affected file or behavior, impact, reproduction conditions, and smallest safe proof. Do not place credentials, private data, exploit details, or sensitive logs in a public issue.

If private reporting is unavailable, open a public issue titled `Private security contact requested` with no vulnerability details. A maintainer can arrange a private channel through the repository host. If no maintainer responds, use the host's abuse or security channel rather than disclosing sensitive details publicly.

<a id="assessment-boundary"></a>
## Assessment Boundary

Reports are assessed against actual plugin/marketplace metadata, setup/check/remove scope, instruction and standalone-role discovery, configuration, runtime permission, or validation behavior. Instructions are not a security boundary. Static validation does not establish publication, live installation, Host isolation, model compliance, account authorization, network policy, or external-service security.

<a id="safe-reproduction"></a>
## Safe Reproduction

Provide the minimum reproduction and redact secrets and private paths. Use an isolated project or `--codex-home` when reproducing setup behavior; never point a destructive remove test at an ambiguously owned scope. Do not test against systems, accounts, data, or users you are not authorized to affect. Stop before destructive, irreversible, or externally disruptive actions and coordinate privately with maintainers.
