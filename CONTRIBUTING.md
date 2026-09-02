# Contributing

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

<a id="before-you-start"></a>
## Before You Start

KISS My Agent is a research-engineering plugin for keeping Agent work proportionate, failure-visible, and evidence-honest. Read [`AGENTS.md`](AGENTS.md) before changing the repository. For Skill, Rule, or Case changes, also read [Extending](docs/EXTENDING.md). Runtime and test behavior belong in [Configuration](docs/CONFIGURATION.md) and [Testing](docs/TESTING.md).

Installing or configuring the released plugin does not require Python, Node.js, or another language runtime. The contributor toolchain is separate: Git and Python 3.11 or newer are sufficient for the standard-library validation and Setup contract tests. Plugin- or Skill-only contributors do not need to install Markdown or build the site locally. Codex is needed only for live discovery and dogfooding checks.

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
- Keep `$kiss-my-agent` precisely routed and non-catch-all. Add a Rule only for a recurring method and a Case only for a useful concrete contrast.
- Do not expand setup, workflow, release, compatibility, telemetry, scoring, or evaluation machinery without an approved current consumer.
- Preserve the three owners: two public switches in config, standalone role TOML discovery, and dynamic dispatch in AGENTS. Config must not enumerate role files.
- Treat the supplied roles as editable seeds rather than a closed catalog; role `name` is identity and filename is only a convention.
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
git diff --check
git diff --stat upstream/main...HEAD
git push -u origin docs/clear-onboarding
```

Do not rewrite another contributor's branch, force-push shared work, or mix release preparation with an unrelated fix.

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

1. **Project instructions and roles.** Start a trusted new Codex session from this checkout. Give it a real, bounded contribution task. When delegation is useful, have `kiss_explorer` inspect read-only, give `kiss_coder` exclusive ownership of named files, and ask `kiss_reviewer` for an independent read-only review. Confirm that unrelated dirty-tree changes survive and that subprocess failures remain visible.
2. **The edited plugin package.** Do not change the tracked release manifest or Git-backed marketplace merely to invalidate a local cache. Use Codex's Plugin Creator local-update workflow to stage a disposable copy in a separate local marketplace, point that marketplace at the staged copy, and add exactly one `+codex.<cachebuster>` suffix to the staged manifest only. Install from that local marketplace into an isolated Codex home, then start a new thread so the Host loads the staged Skills.

In the new thread, confirm `/skills` shows `kiss-my-agent` and `kiss-my-agent-setup`. Exercise `$kiss-my-agent` only on a matching non-obvious decision. Exercise setup, check, Agent configuration, and removal only in a disposable project scope; do not use a real global scope for a development test. Preserve any first failed precondition instead of hiding it with retries.

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

<a id="pull-requests"></a>
## Pull Requests

Open a pull request to canonical `main` and complete the repository template. Describe the user-visible outcome, current consumer, changed owner, explicit non-goals, exact validation commands, evidence level, and limitations. Link the issue when one was required.

Keep the pull request focused and reviewable. Resolve material review findings without broad cleanup. Green checks must belong to the current pull-request commit. Maintainers merge accepted changes with **Squash and merge** and may delete the merged branch; contributors do not need to rewrite a clear local commit history solely to create one commit.

A passing test is not proof of model behavior, usability, publication, or release success. State every untested surface directly.

<a id="release-process"></a>
## v0.2.0 Release Process

This section is maintainer-only. The `v0.1.0` tag is immutable and must never be moved or recreated.

1. Track v0.2.0 in an issue with acceptance criteria, compatibility constraints, and non-goals.
2. Land implementation through a focused pull request. Align the plugin manifest version and marketplace ref at `0.2.0` / `v0.2.0`, synchronize English and Chinese documentation, and require the complete test suite plus green native Ubuntu, macOS, and Windows CI for the exact release commit.
3. Complete a fresh-install Smoke, an isolated `v0.1.0` to `v0.2.0` marketplace-upgrade Smoke, fresh-session Skill discovery, harmless role Smokes, and the README-only new-user Pilot. Do not claim an upgrade path until the installed cache actually reports and loads v0.2.0.
4. After the pull request is squash-merged and the exact `origin/main` commit is verified, create an immutable annotated tag and GitHub Release:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
python scripts/test_all.py
git tag -a v0.2.0 -m "KISS My Agent v0.2.0"
git push origin v0.2.0
gh release create v0.2.0 --verify-tag --title "KISS My Agent v0.2.0" --generate-notes
```

5. Verify the public Release page and archives, then test the documented user upgrade in an isolated installation and a trusted new session:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

6. Verify both deployed Pages languages over HTTPS and record the exact commit, CI runs, public install/upgrade result, live Smokes, Pilot result, and residual limits in the canonical handoff through a follow-up pull request.

If a published release is defective, preserve its tag and publish a new patch version. Never force-push `main`, move a published tag, suppress a failing check, or relabel an invalid run as success.
