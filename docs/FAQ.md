# Frequently Asked Questions

[English](FAQ.md) | [简体中文](FAQ.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Configuration](CONFIGURATION.md) · [Testing](TESTING.md)

<a id="what-is-kiss"></a>
## What does KISS mean here?

“Keep It Simple, Scientist”: choose the smallest sufficient implementation and evidence for the current question while preserving real contracts, safety, and visible failure.

<a id="install"></a>
## What is the main installation path?

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

Start a new session, run `$kiss-my-agent-setup set up this project`, then start another new session and run `$kiss-my-agent-setup check this project`. The `v0.1.0` Git tag must exist before the Git-backed marketplace can install it remotely; current source/static evidence is not publication evidence.

<a id="global"></a>
## Does project setup install anything globally?

No. Global setup requires the explicit `$kiss-my-agent-setup set up globally` command. Project and global check/remove commands are also distinct.

<a id="when-skill"></a>
## When should I invoke `$kiss-my-agent`?

Use it for a non-obvious persistent mechanism, local repair versus new system, experiment validity, evidence strength, runtime/evaluator ambiguity, or material scope expansion. Routine implementation, tests, builds, Git, lookups, and formatting do not need it. `$kiss-my-agent-setup` is a separate operational Skill for explicit setup/check/remove requests.

<a id="fixed-workflow"></a>
## Does it run a fixed workflow?

No. `.codex/config.toml` enables the capability, standalone role TOML files are auto-discovered, and AGENTS guidance lets the primary thread dispatch dynamically. Bounded work can stay in one thread; delegation is useful only when its benefit exceeds coordination cost.

<a id="no-change"></a>
## Can no change be successful?

Yes. Evidence may show that current behavior already meets the goal, the fault is unsupported, or the cause lies outside the authorized scope.

<a id="project-config"></a>
## What does the tracked project config do?

It explicitly sets `features.multi_agent = true` and `agents.enabled = true`. It does not enumerate roles or set a model, effort, trust, permission, context, concurrency, provider, authentication, or telemetry value.

<a id="roles"></a>
## Are the three roles fixed?

No. They are seed standalone TOML files, not a closed catalog. The `name` field is identity; the filename is only a convention. Models and efforts inherit Host values when omitted and are editable. Removing a role removes it from discovery; normal sessions and `check` do not recreate it.

<a id="disable-agents"></a>
## How do I disable it for one launch?

```bash
codex --config features.multi_agent=false --config agents.enabled=false
```

An effective explicit `false` remains authoritative. Setup must not silently undo a user or administrator disablement.

<a id="existing-files"></a>
## What if I already have config, AGENTS, or roles?

Keep unrelated content. Setup merges only KISS-managed content and stops on identity, ownership, or managed-block conflicts. If `AGENTS.override.md` exists in the selected scope, setup stops rather than writing into it or hiding a base file below it.

<a id="remove"></a>
## What does remove delete?

Only KISS-managed content in the explicitly selected project or global scope. Ambiguous or user-edited content is preserved and reported as a conflict. Removing setup output does not uninstall the plugin.

<a id="sandbox"></a>
## Do I need a sandbox to test?

No Codex sandbox package is needed for static validation. This does not require `danger-full-access` or bypass OS and Host permissions. Live discovery can update normal Host-owned trust, history, or cache state.

<a id="confirm-installation"></a>
## How do I confirm installation?

Separate the evidence: source/static validation, setup `check`, `/skills` in a trusted new session, and a harmless role Smoke each prove only their own surface. See [Testing](TESTING.md).

<a id="pages"></a>
## Where is the Pages site?

Stage 1 local build support is prepared, but this README intentionally keeps relative language links. Publish a Pages URL only after the first deployed response returns HTTP 200; do not circulate a pre-deployment 404 URL.

<a id="windows-wsl"></a>
## Is WSL the Windows test path?

No. WSL uses the Linux wrapper and produces Linux evidence. Windows support uses `scripts\validate.ps1` in native PowerShell.

<a id="other-hosts"></a>
## Does this work with other hosts?

The content may be adaptable, but the repository is Codex-first. Other hosts have not been verified.
