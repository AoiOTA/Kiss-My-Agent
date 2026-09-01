# Frequently Asked Questions

[README](../README.md) · [简体中文](../README.zh-CN.md) · [Installation](INSTALLATION.md) · [Extending](EXTENDING.md)

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

Use `.agents/skills/kiss-my-agent/` in a repository or `$HOME/.agents/skills/kiss-my-agent/` for user scope. `$CODEX_HOME/skills/kiss-my-agent/` is only a verified compatibility fallback for host versions that require it; do not keep both user-scope copies.

## Where do custom agents go?

Use `.codex/agents/` for project scope or `~/.codex/agents/` for personal scope. Inspect duplicates and host precedence rather than assuming that both should be installed.

## Do I copy `config.toml`?

No. This repository does not provide one. Model availability and host configuration are environment-specific.

## What if `gpt-5.6-sol` is unavailable?

Edit the affected role TOML to a model and reasoning effort supported by the host, then update the corresponding `expected_roles` entry in `scripts/validate.sh`. Preserve the role's read/write boundary.

## How do I confirm installation?

Start a new Codex session in the target scope and run `/skills`. Confirm `kiss-my-agent` appears. Discovery does not prove that a future response will satisfy the instructions.

## What does the sandbox do?

`scripts/stage-sandbox.sh` deletes and rebuilds only this repository's `.sandbox/`, creates an isolated inner Git project, copies project-scoped agents and the skill, and prints a launch command. It never starts Codex or changes real user configuration.

## What does validation prove?

It proves only the checked static repository properties: required files, TOML values, skill structure and routing, bilingual README structure, relative links, hygiene terms, shell syntax, hero presence, and the fixture chain. It does not prove model behavior, authentication, permissions, network access, research validity, releases, or compatibility with other hosts.

## Does this work with other agent hosts?

The content may be adaptable, but this repository is Codex-first and other hosts have not been verified. Their discovery, precedence, roles, tools, and permission semantics may differ.

## Is there CI or a release channel?

No. Validation is local, and the project currently has no automated installer, hosted CI, formal releases, compatibility matrix, or generated evaluation score.
