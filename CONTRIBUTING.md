# Contributing

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

<a id="before-you-start"></a>
## Before You Start

KISS My Agent is a research-engineering plugin for keeping Agent work proportionate, failure-visible, and evidence-honest. Read [`AGENTS.md`](AGENTS.md) before changing the repository. For Skill, Rule, or Case changes, also read [Extending](docs/EXTENDING.md). Runtime and test behavior belong in [Configuration](docs/CONFIGURATION.md) and [Testing](docs/TESTING.md).

Installing or updating the released Plugin through its Git-backed marketplace requires a usable Git executable and GitHub network access, but not Python, Node.js, Docker, or another language runtime. The contributor toolchain is separate: Git and Python 3.11 or newer are sufficient for the standard-library validation and Setup contract tests. Plugin- or Skill-only contributors do not need to install Markdown or build the site locally; pull-request CI validates the site. Codex is needed only for live discovery and dogfooding checks.

The v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` was removed in v0.2. This is a breaking contributor-interface change. Migrate setup, check, remove, and role configuration to the conversational `kiss-my-agent-setup` Skill, invoke it as `$kiss-my-agent:kiss-my-agent-setup` when pasting raw text, and keep its Agent-native engineering evidence separate from deterministic repository-test evidence.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

<a id="where-to-participate"></a>
## Where to Participate

- Use a [bug report](https://github.com/AoiOTA/Kiss-My-Agent/issues/new?template=bug-report.md) for a reproducible defect against the current documented contract.
- Use a [documentation report](https://github.com/AoiOTA/Kiss-My-Agent/issues/new?template=documentation.md) when instructions are missing, contradictory, or hard to follow.
- Use a [feature request](https://github.com/AoiOTA/Kiss-My-Agent/issues/new?template=feature-request.md) for a bounded outcome with a current consumer. Changes to plugin/marketplace layout, setup scope, role schema, Skill trigger boundaries, Pages publication, or permanent rules need an issue before implementation.
- Use the specialized Rule or Case proposal template for a recurring decision method or a concrete contrast. Small, scoped corrections can go directly to a pull request.
- Use [Q&A Discussions](https://github.com/AoiOTA/Kiss-My-Agent/discussions/categories/q-a) for usage help and [Ideas Discussions](https://github.com/AoiOTA/Kiss-My-Agent/discussions/categories/ideas) for open-ended exploration that is not ready to become a scoped change.
- Report vulnerabilities privately according to [Security](SECURITY.md). Never put credentials, exploit details, private data, or sensitive logs in an issue or Discussion.

<a id="contributor-bootstrap"></a>
## Contributor Bootstrap

Fork the repository on GitHub, clone your fork, and add the canonical repository as `upstream`:

```bash
git clone https://github.com/YOUR_ACCOUNT/Kiss-My-Agent.git
cd Kiss-My-Agent
git remote add upstream https://github.com/AoiOTA/Kiss-My-Agent.git
git fetch upstream
```

Confirm the contributor interpreter. No virtual environment or package installation is required for Plugin, Skill, configuration, or Setup contract changes.

Linux or macOS:

```bash
python3 --version
```

Windows native PowerShell:

```powershell
py -3 --version
```

The reported Python version must be 3.11 or newer. WSL follows the Linux instructions and produces Linux, not Windows, evidence. Documentation contributors can optionally create the isolated environment described under [Local Validation](#local-validation).

<a id="change-boundaries"></a>
## Change Boundaries

- Preserve human ownership of the goal, architecture, acceptance criteria, non-goals, and stop boundary.
- Keep `kiss-my-agent` precisely routed and non-catch-all. Add a Rule only for a recurring method and a Case only for a useful concrete contrast.
- Do not expand setup, workflow, release, compatibility, telemetry, scoring, or evaluation machinery without an approved current consumer.
- Preserve the three owners: four config paths in `config.toml` (the paired master model/effort defaults plus two independently defaulted public switches), standalone role TOML discovery, and dynamic dispatch in AGENTS. The marker controls remove ownership; it does not authorize resetting an existing value. Config must not enumerate role files.
- Treat the supplied roles as editable fresh-setup seeds rather than a closed catalog; role `name` is identity and filename is only a convention. Once a role exists it is user-owned, and setup or Plugin update must never overwrite, migrate, or version-classify it.
- Keep the master on coordination, decisions, and synthesis. Default to flat direct fan-out, allow multiple instances of one role, and keep one writer/operator for each shared resource. A qualifying large independent subsystem may use one temporary bounded lead whose workers do not delegate; never add deeper or permanent hierarchy.
- Keep master settings and role settings distinct. The editable bundled defaults are `gpt-5.6-sol` / `max` in scope config for the master, `gpt-5.6-sol` / `high` for explorer/coder roles, and `gpt-5.6-sol` / `xhigh` for reviewer. Preserve existing choices; later setup and updates must not reset them, and the role wizard must not edit master config.
- Preserve unrelated user and Agent changes. Keep refactors, generated artifacts, and formatting outside the scoped diff.
- Keep every English developer document synchronized with its Simplified Chinese companion: language switch, explicit anchor IDs, section order, and fenced command blocks.
- Keep Codex-facing AGENTS, Skills, Rules, Cases, role TOML, `LICENSE`, and `CODE_OF_CONDUCT.md` English-only.
- Never add credentials, private paths, private data, logs, sessions, local plugin caches, virtual environments, or generated test content.

<a id="development-workflow"></a>
## Development Workflow

Start a focused branch from the latest canonical `main`. Use a short descriptive branch name; the example below is not a required naming scheme.

```bash
git fetch upstream
git switch -c docs/clear-onboarding upstream/main
```

Trace the active producer-consumer path before editing. Reproduce a defect with the smallest valid input, change the owning module only, add a regression check that fails before the fix, and run focused checks while iterating. A supported no-change finding is acceptable when evidence shows no code or documentation change is needed.

Before opening a pull request, inspect the complete diff, confirm unrelated work is absent, run the applicable required local checks below, commit only the intended files, and push the branch to your fork:

```bash
git status --short
git diff upstream/main
git add path/to/intended-file path/to/another-intended-file
git diff --cached --check
git commit -m "docs: clarify onboarding"
git diff --stat upstream/main...HEAD
git push -u origin docs/clear-onboarding
```

Replace the example paths and commit message with the actual scoped change; do not use `git add .`. Do not rewrite another contributor's branch, force-push shared work, or mix release preparation with an unrelated fix.

<a id="local-validation"></a>
## Local Validation

Plugin-, Skill-, configuration-, and Setup-only contributions have no third-party Python dependency. Run both standard-library checks locally.

Linux or macOS:

```bash
python3 scripts/validate.py
python3 -m unittest tests.test_setup -v
```

Windows native PowerShell:

```powershell
py -3 scripts/validate.py
py -3 -m unittest tests.test_setup -v
```

These checks validate source and Setup contracts; they do not execute a live Codex setup or prove Host behavior.

They also validate removal of the v0.1 `skills/kiss-my-agent-setup/scripts/setup.py` interface. Do not restore or replace it with another repository staging or setup script; the supported setup interface is the conversational Skill.

For documentation or site changes, CI is the required site-build evidence. A contributor may optionally preview the site locally by creating an isolated environment outside the checkout.

Linux or macOS:

```bash
python3 -m venv ../kiss-my-agent-docs-venv
. ../kiss-my-agent-docs-venv/bin/activate
python -m pip install -r requirements-site.txt
python -m unittest tests.test_build_site -v
python scripts/build_site.py --output _site
```

Windows native PowerShell:

```powershell
py -3 -m venv ..\kiss-my-agent-docs-venv
..\kiss-my-agent-docs-venv\Scripts\Activate.ps1
python -m pip install -r requirements-site.txt
python -m unittest tests.test_build_site -v
python scripts/build_site.py --output _site
```

`_site/` is an ignored local preview. Do not commit it. Contributors are not required to install Markdown solely to run the complete suite locally.

CI and the release maintainer own the complete deterministic entrypoint after installing `requirements-site.txt`:

```bash
python scripts/test_all.py
```

It runs repository validation, all unit tests, a temporary documentation-site build, Git whitespace validation, and a before/after working-tree check. A failure is part of the result: preserve the first decisive error and fix its actual owner. A configured workflow is not evidence that it passed: the pull request requires the green native jobs for its current commit. macOS or Windows support requires that platform's exact green job; WSL remains Linux evidence.

<a id="dogfooding"></a>
## Dogfooding KISS My Agent

Use KISS My Agent while developing KISS My Agent, but keep the feedback loop bounded by the issue's human-owned goal and acceptance criteria. Dogfooding can reveal ambiguity or defects; it does not authorize the plugin to redefine its architecture, expand its own scope, or treat its own judgment as acceptance evidence.

Record the source and Host baseline before a live check:

```bash
git rev-parse HEAD
git status --short
codex --version
```

There are two distinct live checks:

1. **Project instructions and roles.** Start a trusted new Codex session from this checkout. Give it a real, bounded contribution task. Keep the master on coordination, decisions, and synthesis: use flat direct fan-out to `kiss_explorer`, `kiss_coder`, and `kiss_reviewer`, with multiple same-role instances when justified and one owner for every shared resource. Use a temporary lead only for a qualifying large independent subsystem, never a deeper hierarchy. Confirm that unrelated dirty-tree changes survive and that subprocess failures remain visible.
2. **The edited plugin package.** Do not change the tracked release manifest or Git-backed marketplace merely to invalidate a local cache. Use Codex's Plugin Creator local-update workflow to stage a disposable copy in a separate local marketplace, point that marketplace at the staged copy, and add exactly one `+codex.<cachebuster>` suffix to the staged manifest only. Install from that local marketplace into an isolated Codex home, then start a new thread so the Host loads the staged Skills.

External contributors can invoke that workflow with this Codex prompt:

```text
$plugin-creator update this existing KISS My Agent plugin for local development. Stage a disposable candidate copy outside the checkout in a separate local marketplace, point that marketplace only at the candidate copy, add exactly one +codex.<cachebuster> suffix to the copy's manifest version, reinstall it from that marketplace into an isolated Codex home, and tell me to start a new thread. Do not modify tracked release files or the Git-backed marketplace.
```

See the official OpenAI [Plugin Creator and local marketplace guidance](https://developers.openai.com/plugins/build/plugins#package-with-plugin-creator) and [marketplace add/upgrade commands](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli). Do not add a repository staging script for this workflow.

In the new thread, confirm `/skills` shows the canonical Plugin Skills `kiss-my-agent:kiss-my-agent` and `kiss-my-agent:kiss-my-agent-setup`. Exercise `$kiss-my-agent:kiss-my-agent` only on a matching non-obvious decision. Exercise `$kiss-my-agent:kiss-my-agent-setup` for setup, check, Agent configuration, and removal only in a disposable project scope; do not use a real global scope for a development test. Preserve any first failed precondition instead of hiding it with retries.

Report each evidence level separately:

| Evidence | Supports | Does not support |
| --- | --- | --- |
| Source inspection | What the checked files say | Loaded runtime behavior |
| `test_all.py` PASS | The checks actually implemented by that exact source | Publication, Host loading, or Agent compliance |
| Native CI PASS | That platform, job, and exact commit | Every OS version or future compatibility |
| Fresh-session discovery | Skills or roles visible in that session | Future behavior or permission safety |
| One bounded Smoke | The observed task and environment | General reliability or product acceptance |
| New-user Pilot | That participant completed the stated scenario without help | Universal usability |
| Release verification | The tested public tag, archive, install, or upgrade path | Unreleased changes or future releases |

Record the platform, native shell, exact source state, Codex version, trust state, whether the session was new, marketplace source/version, prompt, expected outcome, actual outcome, and untested surfaces. Stop when the stated question is answered; do not repeat runs merely to manufacture confidence.

A coordinator wait window that returns without an update is not evidence that a child Agent timed out or failed. Let bounded non-conflicting work continue, and interrupt only when the assignment is obsolete, out of scope, competing for a shared resource, or explicitly stopped by the user.

If delegation is disabled or unavailable, or no suitable role exists, report the staffing issue and ask the user to repair or enable staffing or explicitly switch this task to ordinary single-conversation execution. The master may work directly only after the latter choice; it must not silently take over.

<a id="pull-requests"></a>
## Pull Requests

Open a pull request to canonical `main`. Every pull request must provide only the template's **Outcome**, **Change summary**, **Validation**, and **Limitations** fields. Link an issue when one was required. Add the current consumer, smallest-change rationale, and explicit non-goals only when the change affects a public interface, adds a mechanism, prepares a release, or the linked issue requires them.

Keep the pull request focused and reviewable. Resolve material review findings without broad cleanup. Green checks must belong to the current pull-request commit. Maintainers merge accepted changes with **Squash and merge** and may delete the merged branch; contributors do not need to rewrite a clear local commit history solely to create one commit.

A passing test is not proof of model behavior, usability, publication, or release success. State every untested surface directly.

<a id="release-process"></a>
## Release Process

This section is maintainer-only. In the examples, replace every `vX.Y.Z` with the one selected release tag and every `X.Y.Z` with the matching manifest version. Every pushed tag is immutable: never move, delete, or recreate it.

1. Open a bounded release issue with acceptance criteria, compatibility constraints, and explicit non-goals.
2. Complete behavior work in a disposable candidate before tagging. Run the applicable local checks, the complete suite, and native Ubuntu, macOS, and Windows pull-request CI for the exact candidate commit. Candidate evidence does not prove public installation or live Host behavior.
3. Land the focused pull request. Align the Plugin manifest version and marketplace ref at `X.Y.Z` / `vX.Y.Z`, synchronize English and Chinese documentation, and verify the exact merged `origin/main` commit.

   ```bash
   git fetch origin
   git switch main
   git pull --ff-only origin main
   ```

4. Run the complete deterministic entrypoint for that commit. On Linux or macOS:

   ```bash
   python3 scripts/test_all.py
   ```

   On Windows native PowerShell:

   ```powershell
   py -3 scripts/test_all.py
   ```

5. Create and push the immutable annotated tag. Do not create the GitHub Release yet:

   ```bash
   git tag -a vX.Y.Z -m "KISS My Agent vX.Y.Z"
   git push origin vX.Y.Z
   ```

6. Run only checks that require the pushed public distribution surface. Reuse prior evidence when its source and covered behavior are unchanged, say that it was reused, and do not repeat candidate checks after tagging. Verify only the public archive, marketplace install or upgrade, fresh-session discovery, or other public-only behavior required by the release acceptance criteria.

   ```bash
   codex plugin marketplace upgrade kiss-my-agent
   codex plugin list --marketplace kiss-my-agent
   ```

7. Classify the first decisive post-tag failure before acting:
   - A defect in the tagged product source: preserve the tag, do not create a Release for it, fix the source, and use the next patch version.
   - A harness, command-construction, or environment failure: fix that owner and obtain only the missing evidence against the same tag.
   - An evaluator error or another invalid run: correct the evaluation and rerun only the invalid observation; it is not product-negative evidence and does not trigger a patch version.
   - A product defect found after a GitHub Release is published: preserve the released tag and publish the correction as a new patch version.
8. Only after the required public checks pass, create the GitHub Release as the last publication step:

   ```bash
   gh release create vX.Y.Z --verify-tag --title "KISS My Agent vX.Y.Z" --generate-notes
   ```

9. Verify the public Release page and archives, then record the exact commit, CI links, bounded public checks, reused evidence, and residual limits in the canonical handoff.

Never force-push `main`, move a pushed tag, suppress a failing check, relabel an invalid run as success, or create a new patch tag for a harness or environment failure.
