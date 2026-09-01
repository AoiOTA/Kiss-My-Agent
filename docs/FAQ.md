# Frequently Asked Questions

[README](../README.md) · [简体中文](../README.zh-CN.md) · [Installation](INSTALLATION.md) · [Configuration](CONFIGURATION.md) · [Extending](EXTENDING.md)

## What does KISS mean here?

**Keep It Simple, Scientist.** It means choosing the smallest sufficient implementation and evidence for the present research or product question while preserving real contracts, safety, and visible failure.

## When should I invoke `$kiss-my-agent`?

Use it when there is a non-obvious decision about a persistent or shared mechanism, local repair versus a new system, experimental validity or evidence strength, runtime versus evaluator ambiguity, or expanding scope or acceptance.

Do not invoke it for an already-decided implementation, ordinary small fix, mechanical edit, routine test or build, Git operation, lookup, or formatting.

## Does the skill run a fixed workflow?

No. It routes one ambiguity to one relevant Rule and optionally one Case. The master may do bounded work directly and delegates only when the expected benefit exceeds coordination cost.

## Can “no change” be a successful result?

Yes. If current behavior already meets the goal, the reported fault is not supported, or the root cause lies outside the authorized scope, an evidence-backed no-change conclusion is valid.

## Why is there no installer?

Existing project instructions and agent roles may carry important ownership or safety constraints. Blind copying could overwrite them. The [installation guide](INSTALLATION.md) uses explicit destinations, pre-existing-file checks, and manual merge boundaries.

## Where should I install the skill?

Use `.agents/skills/kiss-my-agent/` in a repository or `$HOME/.agents/skills/kiss-my-agent/` for user scope. Choose one intended scope. Same-name Skills are not merged, so do not install duplicate project and user copies.

## Where do custom agents go?

Use `.codex/agents/` for project scope or `${CODEX_HOME:-$HOME/.codex}/agents/` for personal scope. KISS ships `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` so existing generic roles remain untouched. If a destination already has the same prefixed name, stop and diff it. Register the selected roles with `[agents.<name>].config_file` in the intended user or trusted-project config layer; copying a template file alone is not treated as proof that the Host exposed its agent type.

## What if I already have config, AGENTS, Skills, or custom Agents?

Keep them. KISS components are independent and optional. Do not overwrite a complete `config.toml` or instruction file. Merge only applicable AGENTS principles into the actual effective source, install the Skill in one scope only, and add prefixed roles only when their exact names are absent. The [installation guide](INSTALLATION.md) provides the collision matrix.

## Do I copy `config.toml`?

Do not copy or overwrite a complete unknown configuration. This repository has no active `.codex/config.toml`; it provides an inert, annotated [`config.example.toml`](../examples/config.example.toml). Copy only the settings you need into a reviewed user, trusted project, Profile, or CLI layer. See [Configuration](CONFIGURATION.md).

## How do I configure the Master or primary thread?

There is no `master.toml`. The primary thread uses the effective model, reasoning, context, permission, Profile, UI, and CLI settings of the current session. Configure it at user or trusted-project scope, through a Profile, or with a one-off launch override.

## Can I change the KISS Agent models?

Yes. Edit `model` and `model_reasoning_effort` in `kiss_explorer.toml`, `kiss_coder.toml`, or `kiss_reviewer.toml`. Choose values supported by the target host. The supplied values are examples, and the validator does not require one exact model or effort.

## What does the maximum Agent count mean?

`agents.max_concurrent_threads_per_session` is a capacity cap for open spawned-agent threads, excluding the primary. It does not tell the Master to use every slot. Leave it unset for the host default or choose a limit justified by real local resources; KISS routing still delegates only when coordination has net value.

## Should I set the context window and automatic compaction threshold?

Usually leave them unset and use model defaults. `model_context_window` cannot increase the real capability of the model. A custom `model_auto_compact_token_limit` must fit below the actual context capacity and leave room for output, tool results, and later turns. Do not reuse one numeric value across different models or providers without verification.

## Can I change read-only or write permissions?

Yes, but that changes real authority. The supplied `kiss_explorer` and `kiss_reviewer` are read-only and `kiss_coder` is workspace-write as recommended defaults. Role instructions are not a security boundary; parent live permissions and host or administrator policy can still constrain a subagent. Do not silently broaden permissions to make a task easier.

## Does KISS My Agent disable Web access?

No. Web access remains a Host and permission decision. Some local discovery tests deliberately disable Web to prove that Codex loaded the repository Skill and linked local Rule instead of masking a path failure with an online search. That narrow test condition does not change normal Agent capabilities.

## What if `gpt-5.6-sol` is unavailable?

Edit the affected role TOML to a model and reasoning effort supported by the host, then run `./scripts/validate.sh`. No automatic fallback is provided because a visible configuration error is easier to diagnose than an undisclosed model or permission change.

## How do I confirm installation?

Start a new Codex session in the target scope and run `/skills`. Confirm `kiss-my-agent` appears. Discovery does not prove that a future response will satisfy the instructions.

## Do I need a sandbox to test KISS My Agent?

No. Run the static validator in the clone. If normal Host-state updates are acceptable, optionally start a new authenticated Codex or ChatGPT Desktop session, confirm `kiss-my-agent` with `/skills`, and inspect registered prefixed roles. No copied `CODEX_HOME`, Docker image, virtual machine, Python package, or extra test project is required. The Codex `sandbox_mode` setting is a separate execution-permission feature.

The validator itself does not write user configuration. A live Host session may record project trust, history, caches, or marketplace timestamps even without installing KISS. Use a disposable OS account or Host profile only if the test must leave all Host-owned user state untouched.

## What does validation prove?

It proves only the checked static repository properties: required files, TOML values, skill structure and routing, bilingual README structure, relative links, hygiene terms, shell syntax, hero presence, and the fixture chain. It does not prove model behavior, authentication, permissions, network access, research validity, releases, or compatibility with other hosts.

The static validator is exercised locally. Codex CLI `0.152.0` passed Skill metadata discovery, explicit linked-Rule routing, and all three registered KISS Agent types. ChatGPT Desktop `26.825.51511`'s bundled Codex `0.151.0-alpha.7.2` passed Skill metadata discovery, explicit linked-Rule routing, and a registered `kiss_explorer` spawn. A separate GUI new-project session was not created because this clone is not registered as a saved Desktop project. These versions are evidence of tested snapshots, not minimum-version promises.

## Does this work with other agent hosts?

The content may be adaptable, but this repository is Codex-first and other hosts have not been verified. Their discovery, precedence, roles, tools, and permission semantics may differ.

## Is there CI or a release channel?

No. Validation is local, and the project currently has no automated installer, hosted CI, formal releases, compatibility matrix, or generated evaluation score.
