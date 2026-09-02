# Frequently asked questions

[English](FAQ.md) | [简体中文](FAQ.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Configuration](CONFIGURATION.md) · [Testing](TESTING.md)

<a id="what-is-kiss"></a>
## What does KISS mean here?

“Keep It Simple, Scientist”: choose the smallest sufficient implementation and evidence for the current problem while preserving real contracts, necessary safety, and visible failure.

<a id="problem"></a>
## What problem does KISS My Agent solve?

It reduces common Agent drift in research engineering:

- **Overengineering:** a local defect or one-consumer need grows into unnecessary abstractions, configuration, compatibility layers, workflows, or persistent systems.
- **Overdefense:** uncertainty produces broad catch-and-continue behavior, stale fallback, duplicate gates, or refusals that hide the real failure or exceed the actual boundary.
- **Process theater:** multi-agent coordination, handoffs, checks, or status machinery become outputs instead of serving the requested result.
- **Evidence inflation:** a source check or passing test is reported as proof of a product or research goal it did not measure.

Necessary authentication, authorization, boundary validation, cleanup, and narrow handling of a known optional outage are not overdefense. KISS removes unsupported machinery, not real safety.

<a id="why-agents-drift"></a>
## Why and when do coding Agents drift this way?

Models infer intent from incomplete instructions. The risk rises when “complete,” “robust,” “production-ready,” or “future-proof” is requested without explicit acceptance criteria; when failure ownership is unclear; when runtime and evaluator outputs disagree; when a claim exceeds an experiment; or when several Agents share mutable work.

Elaborate behavior can look safer or more complete to a model even when it is worse for the current consumer. KISS improves the decision context by assigning human and Agent ownership, requiring a current consumer for mechanisms, keeping failures visible, separating evidence levels, and defining a stop boundary. It reduces the tendency; it cannot guarantee identical behavior from every model or prompt.

<a id="fit"></a>
## Is it right for me?

It is aimed primarily at Codex users doing research software, experiments, debugging, infrastructure, or substantial engineering work who want bounded autonomy without a fixed multi-agent pipeline. It is not a general orchestrator, permission bypass, policy engine, formal evaluator, or guarantee against model mistakes. See the landing page's [fit guide](../README.md#is-it-for-you).

<a id="install"></a>
## How do I install it?

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
```

Start a new session, run `$kiss-my-agent-setup set up this project`, trust the project through the Host when prompted, then start another new session and run `$kiss-my-agent-setup check this project`.

<a id="after-setup"></a>
## What do I do after setup?

Use Codex normally. You do not have to invoke KISS before every task. The project `AGENTS.md` guidance is already applicable; the primary thread decides whether any role is useful. Invoke a Skill only for the specific interfaces described below.

<a id="plugin-vs-skills"></a>
## Is this a Plugin or just a Skill?

It is a versioned Codex Plugin. The Plugin is the install, distribution, and update container. It currently packages two Skills:

- `$kiss-my-agent` supplies narrow decision guidance.
- `$kiss-my-agent-setup` manages explicit project/global setup, checks, removal, and existing-role configuration.

The configured project then owns its `.codex/config.toml`, standalone role TOML files, and managed AGENTS block. A Skill is still sufficient for these file-tool workflows; an MCP service or standalone executable is not required.

<a id="when-skill"></a>
## When should I invoke `$kiss-my-agent`?

Use it for one consequential, non-obvious decision about a persistent/shared mechanism, local fix versus new system, experiment validity, evidence strength, runtime/evaluator ambiguity, or material scope expansion. Do not use it as a wrapper around ordinary implementation, tests, builds, Git, lookup, or formatting. `$kiss-my-agent-setup` is a separate operational Skill.

<a id="configure"></a>
## How do I configure the initial Agents?

The three seeds work immediately by inheriting the Host model and reasoning effort. To change existing role models, effort, or sandbox defaults in a conversational wizard, run:

```text
$kiss-my-agent-setup configure agents for this project
$kiss-my-agent-setup configure global agents
```

You can also edit `.codex/agents/*.toml` or `$CODEX_HOME/agents/*.toml` directly. The wizard does not create, delete, or rename roles and does not hard-code a changing model catalog.

<a id="python"></a>
## Do users need Python?

No. Plugin installation, setup, check, remove, Agent configuration, normal use, and updates do not require Python, Node.js, Docker, or a package manager. Python 3.11+ and the pinned Markdown package are only for contributors running repository tests or building the documentation site.

<a id="update"></a>
## How do installed users update? Is it automatic?

Use one explicit marketplace refresh and then confirm the resolved version:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

Start a new session afterward. Updates are not silent or automatic because changing Agent guidance without user review harms reproducibility. Plugin updates also do not overwrite project-owned role files.

<a id="global"></a>
## Does project setup configure every project?

No. Project scope changes only the selected project. Global setup must be explicitly requested with `$kiss-my-agent-setup set up globally` and can affect every project that loads the selected Codex home. Project and global check/configure/remove commands remain separate.

<a id="roles"></a>
## Are the three roles fixed?

No. They are editable standalone seed files, not a closed catalog or mandatory team. The `name` field is the identity; the filename is a convention. Users may add, edit, rename, or remove roles deliberately. Later setup and check operations do not recreate a deliberately removed seed.

<a id="existing-files"></a>
## What if I already have config, AGENTS, or role files?

Setup preserves unrelated content and explicit `false` values. It stops before writing on invalid TOML, unsafe path types, duplicate identities, ownership conflicts, project/global seed-name conflicts, or an applicable `AGENTS.override.md`. Explicit remove remains available to resolve a cross-scope collision.

<a id="remove"></a>
## What does remove delete?

Only KISS-marked config assignments, the delimited managed AGENTS block, and unchanged bundled roles in the explicitly selected scope. Modified or ambiguously owned roles remain. Removing setup does not uninstall the Plugin.

<a id="verification"></a>
## How do I confirm it works?

Keep evidence separate: repository tests, setup `check`, `/skills` discovery in a fresh trusted session, narrow role Smoke, upgrade testing, and a real project Pilot each support different claims. See [Testing](TESTING.md). A static PASS does not prove model behavior or the user's research goal.

<a id="windows-wsl"></a>
## Is WSL a Windows test path?

No. WSL produces Linux evidence. Native Windows compatibility requires a Windows runner or native PowerShell check. Agent-native user setup avoids a shell-language dependency, but live Host behavior still needs its own platform evidence.

<a id="other-hosts"></a>
## Can I use another Agent host?

The ideas may be adapted, but the packaged Plugin, config, roles, and tests are Codex-first. Other Hosts are not verified by this release.

<a id="pages"></a>
## Where is the documentation site?

The site is available in [English](https://aoiota.github.io/Kiss-My-Agent/) and [Simplified Chinese](https://aoiota.github.io/Kiss-My-Agent/zh-CN/). A successful deployment and real HTTP/content checks are separate evidence.
