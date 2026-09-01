# Frequently Asked Questions

[English](FAQ.md) | [简体中文](FAQ.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Configuration](CONFIGURATION.md) · [Testing](TESTING.md)

<a id="what-is-kiss"></a>
## What does KISS mean here?

“Keep It Simple, Scientist”: choose the smallest sufficient implementation and evidence for the current question while preserving real contracts, safety, and visible failure.

<a id="when-skill"></a>
## When should I invoke `$kiss-my-agent`?

Use it for a non-obvious persistent mechanism, local repair versus new system, experiment validity, evidence strength, runtime/evaluator ambiguity, or material scope expansion. Do not invoke it for ordinary implementation, tests, builds, Git, lookups, or formatting.

<a id="fixed-workflow"></a>
## Does it run a fixed workflow?

No. One ambiguity routes to one Rule and optionally one Case. Bounded work can stay in one thread; delegation is useful only when its benefit exceeds coordination cost.

<a id="no-change"></a>
## Can no change be successful?

Yes. Evidence may show that current behavior already meets the goal, the fault is unsupported, or the cause lies outside the authorized scope.

<a id="project-config"></a>
## What does the tracked project config do?

It enables custom agents and registers only `kiss_explorer`, `kiss_coder`, and `kiss_reviewer`. It does not set trust, model, permissions, context, concurrency, provider, authentication, or telemetry. Project config requires trust and a new session; old sessions are not guaranteed to hot-load it.

<a id="disable-agents"></a>
## How do I disable custom agents for one launch?

```bash
codex --config agents.enabled=false
```

```powershell
codex --config agents.enabled=false
```

<a id="existing-files"></a>
## What if I already have config, AGENTS, Skills, or roles?

Keep them. Use one Skill scope, merge config and AGENTS manually, and add prefixed roles only when exact names are absent. The [installation guide](INSTALLATION.md) uses collision checks and exclusive file creation.

<a id="models-permissions"></a>
## Can I change role models or permissions?

Yes, when the Host supports the values and the authority change is intended. Instructions are not a security boundary. No automatic model or permission fallback is provided.

<a id="sandbox"></a>
## Do I need a sandbox to test?

No Codex sandbox package is needed for static validation. Run the native script. This does not require `danger-full-access` or bypass ordinary OS and Host permissions. Live discovery can write normal Host-owned trust, history, or cache state.

<a id="windows-wsl"></a>
## Is WSL the Windows test path?

No. WSL uses the Linux wrapper and produces Linux evidence. Windows support is tested with `scripts\validate.ps1` in native PowerShell.

<a id="confirm-installation"></a>
## How do I confirm discovery?

Trust the project, start a new authenticated session, run `/skills`, and smoke the three registered roles. See [Testing](TESTING.md). Discovery and Smoke remain narrow evidence, not behavioral guarantees.

<a id="validation-proof"></a>
## What does validation prove?

Only the invariants its output and source explicitly check. A green CI job applies to that platform, job, and exact commit. Static validation does not prove model compliance, permissions, authentication, research validity, or future compatibility.

<a id="other-hosts"></a>
## Does this work with other hosts?

The content may be adaptable, but the repository is Codex-first. Other hosts have not been verified.

<a id="ci-status"></a>
## Are macOS and Windows verified?

They are CI targets. Do not call either verified until the [`Validate` workflow](../.github/workflows/validate.yml) is green for that platform on the exact commit. A workflow definition alone is not passing evidence.
