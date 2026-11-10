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

The tested baselines are authenticated, Plugin-capable Codex CLI 0.152.1 and 0.153.0. You also need `git` and GitHub network access. Other Codex versions are not verified. Check the client first:

```bash
codex --version
codex plugin --help
```

```bash
codex plugin marketplace add AoiOTA/Kiss-My-Agent
codex plugin add kiss-my-agent@kiss-my-agent
codex plugin list --marketplace kiss-my-agent
```

The list should show `kiss-my-agent@kiss-my-agent` as `installed, enabled` at the current supported release; cache paths may differ. If Plugin commands, authentication, or marketplace access fail, check client support, login state, `git`, and GitHub network access. For a simple one-off task, stop after installation and use an ordinary single conversation. For a complex project that needs the persistent workflow, start a new session. Plugin cache roles are not automatically added to the Host catalog. On the tested Codex 0.152.1 baseline, type `$` and select `kiss-my-agent-setup (kiss-my-agent)` in the picker. The picker inserts a structured Skill reference; add the setup request and submit the prompt to invoke it. If you paste raw text, run `$kiss-my-agent:kiss-my-agent-setup set up this project`. Trust the project through the Host when prompted, then start another new session and run `$kiss-my-agent:kiss-my-agent-setup check this project`.

<a id="after-setup"></a>
## What do I do after setup?

Use Codex normally; no user reminder is needed to apply KMA guidance. The master may directly complete clear small or local work, and should actively delegate substantial bulk, independent parallel work, or work needing another perspective when the benefit outweighs coordination cost. Choose by workload, parallel opportunity, coupling, risk, and coordination cost; optional roles do not mean the master should do everything. Each available role may have zero, one, or multiple instances, with no fixed team, sequence, or required subagent launch. The master retains architecture, acceptance, and evidence judgment. Delegation is flat by default, with one operator per shared resource; a qualifying large independent subsystem may have one temporary lead, but no deeper or permanent hierarchy.

If delegation is disabled or unavailable, or no suitable role exists, the master may continue within its capabilities and existing authorization without a staffing approval step. Report unmet explicit requirements for independent checking or a specific role, and real capability gaps; direct execution must not be presented as satisfying them.

<a id="agent-reuse"></a>
## When should I reuse an Agent or start a fresh one?

Reuse an Agent for consecutive work on the same task, owner, and scope. Start a fresh Agent when prior context no longer helps, for independent review, or when Master model/effort differs from the existing child; finish its active operation and hand off safely. Configuration changes do not live-update children. A parallel-Agent limit is available capacity, not a target team size. KISS defaults experimental context management to enabled; it does not set context-window or compaction thresholds.

<a id="plugin-vs-skills"></a>
## Is this a Plugin or just a Skill?

It is a versioned Codex Plugin. The Plugin is the install, distribution, and update container. It currently packages two Skills:

- `kiss-my-agent` supplies narrow decision guidance.
- `kiss-my-agent-setup` manages explicit project/global setup, checks, removal, and existing-role configuration.

The configured project then owns its `.codex/config.toml`, standalone role TOML files, and managed AGENTS block. A Skill is still sufficient for these file-tool workflows; an MCP service or standalone executable is not required.

<a id="when-skill"></a>
## When should I invoke `$kiss-my-agent:kiss-my-agent`?

Each agent reads it when first taking on KMA-managed work, then reuses the guidance and applies it proactively when choosing or changing an action, dividing work, or interpreting results. Do not first require a decision to be consequential or non-obvious. Already-decided mechanical execution, including implementation, tests, builds, Git, lookup, and formatting, needs no repeated Skill reading, extra review, or compliance record. Reread only when the guidance changes or relevant detail is missing. `kiss-my-agent-setup` remains a separate operational Skill for explicit setup/check/configure/remove work.

<a id="configure"></a>
## How do I choose the master and configure initial Agents?

Master uses the current Host/session model and reasoning effort. New seeds omit both overrides and follow the Master; default delegation omits model and effort arguments. Setup preserves existing model choices and roles. Use explicit follow-master configuration to remove selected role and selected-scope `[agents]` overrides; legacy KMA Master pins require a separate explicit selection. Verify effective settings in a new task.

For child Agents, Codex resolves an explicit spawn setting first, then the corresponding `[agents]` default, then the parent; an explicit role-file value is the final override. Current seeds omit both fields. Master remains the parent Agent, not a separate role file.

Use the conversational wizard only for existing role TOML files:

```text
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
$kiss-my-agent:kiss-my-agent-setup configure global agents
```

Plugin updates and setup preserve every existing role. To make the three existing roles follow the Master, use this qualified project prompt:

```text
$kiss-my-agent:kiss-my-agent-setup configure agents in this project: make kiss_explorer, kiss_coder, and kiss_reviewer follow master
```

You can also edit `.codex/agents/*.toml` or `$CODEX_HOME/agents/*.toml` directly. Ordinary configuration changes roles only; follow-master mode additionally previews selected-scope config removals. It never creates, deletes, or renames roles, and maintains no fixed model catalog.

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
codex plugin list --marketplace kiss-my-agent
```

On the verified Codex 0.152.1 baseline, the Host automatically refreshes a default unpinned Git marketplace at startup and reinstalls an enabled non-curated Plugin. KISS My Agent contains no updater of its own, and other versions may behave differently. After the commands above complete, expect `kiss-my-agent@kiss-my-agent` to be `installed, enabled` at the current supported release. Start a new session after an update changes the installed Plugin.

Host refresh and marketplace upgrade update only the Plugin package. They do not change project/global config, instructions, or role files. Setup may refresh the managed instruction block and add missing feature switches; it never adds or migrates model/effort fields or existing roles. Use the follow-master prompt above for explicit selected migration, or edit TOML manually.

See [Installation](INSTALLATION.md#update) for explicit-only marketplace pinning, rollback, and the commands that restore the current unpinned channel.

<a id="global"></a>
## Does project setup configure every project?

No. Project scope changes only the selected project. Global setup must be explicitly requested with `$kiss-my-agent:kiss-my-agent-setup set up globally` and can affect every project that loads the selected Codex home. Project and global check/configure/remove commands remain separate.

<a id="roles"></a>
## Are the three roles fixed?

No. They are editable standalone starter-role files, not a closed list or mandatory team. The `name` field is the identity; the filename is a convention. Multiple instances of one role may run. The default shape is direct master assignment; only a qualifying large independent subsystem may receive one temporary lead layer. Fresh setup creates each missing current starter. Every role already present is immediately user-owned, and setup never overwrites, migrates, or version-classifies it. Once setup exists, a missing starter is a valid intentionally absent catalog entry and is not recreated.

<a id="existing-files"></a>
## What if I already have config, AGENTS, or role files?

Setup fills only missing feature switches with marked `true`, including `features.context_management.experimental_mode`. It preserves all existing model, effort and role settings, including older marked Master pins; missing model fields mean inheritance and are valid. Duplicate assignments, invalid TOML and ambiguous ownership are conflicts. Setup changes only the selected project or global scope.

Setup, check, and remove inspect only the selected KISS config and AGENTS paths plus the exact `kiss_explorer.toml`, `kiss_coder.toml`, and `kiss_reviewer.toml` targets in that scope. An unsafe or invalid managed target, a mismatched bundled identity, an ownership conflict, or an applicable `AGENTS.override.md` stops the operation before writing. Other role files and the other scope are not parsed or reconciled: the Host owns catalog warnings and project-over-global precedence. For role configuration, a named request parses only the named targets; an unnamed request lists paths first and parses only the roles you then select. Invalid unselected roles do not block it.

Use the reported reason and exact path to resolve the conflict without overwriting user work, then rerun the same setup command. See [Installation](INSTALLATION.md#collision-policy) for the complete policy.

<a id="remove"></a>
## What does remove delete?

Only exact current default values with their KISS markers and any exact legacy marked master pair, the delimited managed AGENTS block, and role files that exactly match a current, exact v0.2.9/v0.2.9-active-guidance/v0.2.7/v0.2.6/v0.2.5/v0.1 bundled seed in the explicitly selected scope. Other role files and unmarked config remain. Removing setup does not uninstall the Plugin. Remove preserves the context table and other user fields; a current config field is removed only when both its exact default value and marker match.

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
