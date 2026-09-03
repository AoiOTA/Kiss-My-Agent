# Frequently asked questions

[English](FAQ.md) | [简体中文](FAQ.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Configuration](CONFIGURATION.md) · [Testing](TESTING.md)

<a id="what-is-kiss"></a>
## What does KISS mean here?

“Keep It Simple, Scientist”: start with the smallest runnable, verifiable version, use real success or failure to decide the next step, and add complexity only when the result shows it is needed.

<a id="problem"></a>
## What problem does KISS My Agent solve?

It primarily reduces two tendencies that slow the research loop:

- **Overengineering:** productizing before the current hypothesis is tested by adding abstractions, configuration, migrations, compatibility layers, or platforms for future possibilities that nobody uses today.
- **Overdefense:** preventing errors from surfacing naturally by layering validation, retries, fallbacks, exception handling, approvals, or gates—and sometimes presenting failure as success.

Multi-Agent process, handoffs, and checks becoming outputs, or a passing test being inflated into product or research success, are common signs or consequences of these two problems—not two more core features.

Necessary authentication, authorization, boundary validation, cleanup, and explicit handling of a known optional outage are not overdefense. KISS allows low-cost, recoverable experimentation; it does not remove safeguards for irreversible or other high-risk operations.

<a id="why-agents-drift"></a>
## Why do coding Agents drift this way, and how does KISS respond?

Codex tends to produce answers that look complete, robust, and successful. Prompts often say “comprehensive,” “robust,” or “production-ready” without naming the current hypothesis, minimum goal, and stop condition. Frameworks, defensive code, validation, retries, and fallbacks are easy to generate and easy to present as progress; the model also tends to avoid an obvious failure, so an error may be caught, routed around, or packaged as a usable result.

Mature products can genuinely need complete architecture and safeguards when real requirements and risks justify them. Added too early in research, they slow feedback and hide real errors. KISS drives a shorter loop: `goal or hypothesis → smallest runnable validation → real run → explicit success or failure → iterate or stop`. Tests and process serve that outcome; they do not replace the real result.

<a id="fit"></a>
## Is it right for me?

It is aimed primarily at Codex users building research MVPs, validating algorithms, doing exploratory development, or debugging hidden errors—especially when real runs should quickly decide the next step. It is not a general orchestrator, permission bypass, deterministic executor, or formal evaluator, and it cannot guarantee a correct first attempt. See the landing page's [fit guide](../README.md#is-it-for-you).

<a id="install"></a>
## How do I install it?

The tested baseline is authenticated, Plugin-capable Codex CLI 0.152.1. You also need `git`, GitHub network access, and account support for the bundled default model `gpt-5.6-sol`. Earlier Codex versions are not verified. Check the client first:

```bash
codex --version
codex plugin --help
```

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
codex plugin list
```

After the v0.2.4 tag is published, the list should show `kiss-my-agent@kiss-my-agent` as `installed, enabled` at version `0.2.4`; cache paths may differ. If Plugin commands, authentication, or marketplace access fail, check client support, login state, `git`, and GitHub network access. For a simple one-off task, stop after installation and use an ordinary single conversation. For a complex project that needs the persistent workflow, start a new session. Plugin cache roles are not automatically added to the Host catalog. On the tested Codex 0.152.1 baseline, type `$` and select `kiss-my-agent-setup (kiss-my-agent)` in the picker. The picker inserts a structured Skill reference; add the setup request and submit the prompt to invoke it. If you paste raw text, run `$kiss-my-agent:kiss-my-agent-setup set up this project`. Trust the project through the Host when prompted, then start another new session and run `$kiss-my-agent:kiss-my-agent-setup check this project`.

<a id="after-setup"></a>
## What do I do after setup?

Use Codex normally. You do not have to invoke KISS before every task. The project `AGENTS.md` instructions direct the master to coordinate, decide, and summarize while delegated roles own investigation, implementation, and review. They call for direct assignment by default, allow multiple instances of one role, and keep one person or Agent responsible for each shared resource. A qualifying large independent subsystem may have one temporary lead, but no deeper or permanent hierarchy.

If delegation is disabled or unavailable, or no suitable role exists, the instructions require the master to report the staffing issue and ask you to repair staffing or explicitly switch this task to ordinary single-conversation execution. Only that explicit switch authorizes direct work.

<a id="plugin-vs-skills"></a>
## Is this a Plugin or just a Skill?

It is a versioned Codex Plugin. The Plugin is the install, distribution, and update container. It currently packages two Skills:

- `kiss-my-agent` supplies narrow decision guidance.
- `kiss-my-agent-setup` manages explicit project/global setup, checks, removal, and existing-role configuration.

The configured project then owns its `.codex/config.toml`, standalone role TOML files, and managed AGENTS block. A Skill is still sufficient for these file-tool workflows; an MCP service or standalone executable is not required.

<a id="when-skill"></a>
## When should I invoke `$kiss-my-agent:kiss-my-agent`?

Use it for one consequential, non-obvious decision—for example, whether to keep planning or add a persistent mechanism, or first run a safe, low-cost, recoverable probe. It also applies to a local fix versus a new system, experiment validity, evidence strength, or material scope expansion. Do not use it as a wrapper around ordinary implementation, tests, builds, Git, lookup, or formatting. `kiss-my-agent-setup` is a separate operational Skill.

<a id="configure"></a>
## How do I configure the master or initial Agents?

The bundled defaults use `gpt-5.6-sol`: the master uses `max`, `kiss_explorer` and `kiss_coder` use `high`, and `kiss_reviewer` uses `xhigh`. The Host and account must support these values. The managed-block classifications are mutually exclusive: a current block never receives missing master keys; an absent or recognized-outdated block receives the pair only when both keys are absent; otherwise existing assignments are preserved and each missing key remains absent for inheritance. Later setup or Plugin updates do not reset these choices.

The master is not a role and cannot be changed by the role wizard. For project setup, edit `<project>/.codex/config.toml`. For global setup, edit `$CODEX_HOME/config.toml`, or `~/.codex/config.toml` when `CODEX_HOME` is unset. If the master cannot start because those values are unsupported, use one temporary CLI override, repair the persistent config, and start another new session:

```bash
codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'
```

Use the conversational wizard only for existing role TOML files:

```text
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
$kiss-my-agent:kiss-my-agent-setup configure global agents
```

You can also edit `.codex/agents/*.toml` or `$CODEX_HOME/agents/*.toml` directly. The wizard does not modify master config, create, delete, or rename roles, and does not hard-code a changing model catalog.

<a id="legacy-setup-cli"></a>
## What happened to the v0.1 setup CLI?

The contributor interface `skills/kiss-my-agent-setup/scripts/setup.py` was removed in v0.2. This is an intentional breaking contributor-interface change. Migrate setup, check, remove, and role configuration to the conversational `kiss-my-agent-setup` Skill, invoking it as `$kiss-my-agent:kiss-my-agent-setup` when pasting raw text. Its Agent-native engineering evidence is different from deterministic CLI or repository-test evidence; report them separately.

<a id="python"></a>
## Do users need Python?

No. Plugin installation, setup, check, remove, Agent configuration, normal use, and updates do not require Python, Node.js, Docker, or a package manager. A Git-backed install or update does require a usable `git` executable and GitHub network access. Python 3.11+ is contributor-only; the pinned Markdown package is used only to render and test the documentation site, and Plugin/Skill-only contributors may leave that site build to pull-request CI.

<a id="update"></a>
## How do installed users update? Is it automatic?

The first command updates now. The second command only verifies the result:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

On the verified Codex 0.152.1 baseline, the Host automatically refreshes a default unpinned Git marketplace at startup and reinstalls an enabled non-curated Plugin. KISS My Agent contains no updater of its own, and other Codex versions may behave differently. After v0.2.4 is published and the commands above complete, expect `kiss-my-agent@kiss-my-agent` to be `installed, enabled` at version `0.2.4`. Start a new session after an update changes the installed Plugin.

Automatic refresh and explicit marketplace upgrade update only the Plugin package. They do not change project or global config, instructions, or role files. A v0.1-managed project may run setup after updating to refresh its managed instruction block and add missing public switches, but every existing role stays directly unchanged. Use the role wizard or edit role TOML manually to adopt newer model or effort choices.

See [Installation](INSTALLATION.md#update) for explicit-only marketplace pinning, rollback, and the commands that restore the current unpinned channel.

<a id="global"></a>
## Does project setup configure every project?

No. Project scope changes only the selected project. Global setup must be explicitly requested with `$kiss-my-agent:kiss-my-agent-setup set up globally` and can affect every project that loads the selected Codex home. Project and global check/configure/remove commands remain separate.

<a id="roles"></a>
## Are the three roles fixed?

No. They are editable standalone starter-role files, not a closed list or mandatory team. The `name` field is the identity; the filename is a convention. Multiple instances of one role may run. The default shape is direct master assignment; only a qualifying large independent subsystem may receive one temporary lead layer. Fresh setup creates each missing current starter. Every role already present is immediately user-owned, and setup never overwrites, migrates, or version-classifies it. Once setup exists, a missing starter is a valid intentionally absent catalog entry and is not recreated.

<a id="existing-files"></a>
## What if I already have config, AGENTS, or role files?

Setup manages four settings but does not fill all four independently. The managed-block classifications are mutually exclusive: a current block never receives missing master keys; an absent or recognized-outdated block receives the pair only when both keys are absent; otherwise existing assignments are preserved and each missing key remains absent for inheritance. Each missing public switch is added independently. Existing marked or unmarked assignments, unrelated content, explicit `false` values, and every existing role remain byte-for-byte. Setup stops before writing on invalid TOML, unsafe path types, duplicate identities, ownership conflicts, project/global starter-role conflicts, or an applicable `AGENTS.override.md`.

Use the reported reason and exact path to resolve the conflict without overwriting user work, then rerun the same setup command. See [Installation](INSTALLATION.md#collision-policy) for the complete policy.

<a id="remove"></a>
## What does remove delete?

Only the four KISS-marked config assignments, the delimited managed AGENTS block, and role files that exactly match a current or known v0.1 bundled seed in the explicitly selected scope. Other role files and unmarked config remain. Removing setup does not uninstall the Plugin.

<a id="verification"></a>
## How do I confirm it works?

Keep evidence separate: repository tests, setup `check`, `/skills` discovery in a fresh trusted session, a narrow live **Smoke**, update testing, and a small real-world **Pilot** each support different claims. **Final** means complete acceptance against the user's criteria. See [Testing](TESTING.md). A static PASS does not prove model behavior or the user's research goal.

<a id="windows-wsl"></a>
## Is WSL a Windows test path?

No. WSL produces Linux evidence. Native Windows compatibility requires a Windows runner or native PowerShell check. Agent-native user setup avoids a shell-language dependency, but live Host behavior still needs its own platform evidence.

<a id="other-hosts"></a>
## Can I use another Agent host?

The ideas may be adapted, but the packaged Plugin, config, roles, and tests are Codex-first. Other Hosts are not verified by this release.

<a id="pages"></a>
## Where is the documentation site?

The site is available in [English](https://aoiota.github.io/Kiss-My-Agent/) and [Simplified Chinese](https://aoiota.github.io/Kiss-My-Agent/zh-CN/). A successful deployment and real HTTP/content checks are separate evidence.
