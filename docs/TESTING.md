# Testing

[English](TESTING.md) | [简体中文](TESTING.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Configuration](CONFIGURATION.md) · [FAQ](FAQ.md)

<a id="test-surfaces"></a>
## Test surfaces

KISS My Agent has distinct evidence surfaces:

1. Repository validation and deterministic contributor tests.
2. Agent-native setup/check/remove/configure behavior in an isolated filesystem scope.
3. Plugin install or upgrade and Skill discovery in a fresh Codex session.
4. Narrow observed behavior from each standalone role.
5. New-user comprehension of the landing page.
6. Exact-commit native CI and deployed Pages responses.

Do not combine them into a stronger claim. A source check is not live discovery, CI is not a behavioral guarantee, one role run is not general reliability, and a documentation build is not proof that a newcomer understands the product.

<a id="user-verification"></a>
## User verification needs no Python

After Plugin installation or update, start a new session and use the Plugin-owned interfaces:

```text
$kiss-my-agent-setup set up this project
$kiss-my-agent-setup check this project
$kiss-my-agent-setup configure agents for this project
```

These operations use Codex file tools and require no Python, Node.js, Docker, or package manager. `check` proves only the inspected file state. Use `/skills` and a narrow role Smoke when live discovery matters.

<a id="contributor-suite"></a>
## Contributor test suite

Plugin/Skill-only contributors need Python 3.11 or newer but no third-party package. Run the local core checks:

```bash
python scripts/validate.py
python -m unittest tests.test_setup -v
```

Local site construction is not required for those changes. Pull-request CI installs `requirements-site.txt` and runs `python scripts/test_all.py`, which performs static validation, all unit tests, and a documentation build in a temporary output directory. It must leave tracked files unchanged. Linux/macOS and native Windows CI run the same complete entrypoint; shell wrappers remain narrow checks of their native launch behavior.

The test suite verifies repository-owned contracts. It cannot execute a model-driven setup workflow in CI without a real authenticated Codex session, so those cases remain explicit engineering runs rather than fake unit coverage.

<a id="setup-scenarios"></a>
## Agent-native setup scenarios

Run setup scenarios only in disposable projects and an explicitly isolated Codex home. Preserve the before/after files for review, but do not commit logs or temporary user data.

Required scenarios cover:

- pristine project setup, repeated setup, check, and remove;
- unrelated config, comments, newline style, AGENTS content, and existing roles;
- intentional `false` values and deliberately deleted seed roles;
- malformed TOML, unsafe path types, `AGENTS.override.md`, duplicate names, filename/identity mismatch, and project/global conflicts;
- remove as the recovery path for a cross-scope seed-name conflict;
- a modified role preserved by remove;
- configuring one selected role while all other fields and files remain unchanged;
- restoring inheritance by removing only the selected optional key;
- refusal to write `danger-full-access` without its separate confirmation;
- compatibility with a project created by v0.1.0 markers.

A process or machine crash during model-driven file edits is outside transactional proof. Report it directly rather than claiming atomic recovery.

<a id="local-plugin"></a>
## Test a changed Plugin, not a stale cache

For development, use an isolated local marketplace that already points to a temporary copy of the edited Plugin. Apply one Codex cachebuster to that copy with the current Plugin Creator helper, reinstall it from that local marketplace, and start a new session.

Do not add a cachebuster to the canonical release manifest, hand-edit a configured marketplace, or treat the Git-backed v0.1.0 cache as evidence for working-tree changes. Record the loaded Plugin version and a behavior unique to the candidate.

<a id="fresh-session"></a>
## Trusted fresh session

Installation, upgrade, setup, removal, and changes to config, instructions, Skills, or roles affect startup and discovery. Open a new authenticated session at the intended project and establish trust through the Host interface when prompted.

Record the OS, native shell, Codex version, Plugin version, source identity, scope, trust state, and whether the session is new. An old session cannot prove that changed configuration loaded or failed to load.

<a id="skill-smoke"></a>
## Skill discovery Smoke

In the fresh session, run `/skills` and confirm the Plugin-owned `kiss-my-agent` and `kiss-my-agent-setup` entries. Then use:

- `$kiss-my-agent` only for a real non-obvious mechanism, scope, runtime/evaluator, or evidence decision;
- `$kiss-my-agent-setup` only for explicit setup/check/configure/remove work.

Ordinary implementation, tests, builds, Git, lookup, and formatting should not route through `$kiss-my-agent`. Discovery proves visibility for that session, not future instruction following.

<a id="role-smoke"></a>
## Three-role Smoke

Use the Host custom-Agent interface or explicitly ask the main thread to delegate one bounded task to each discovered role:

1. `kiss_explorer`: read a fixture and report exact anchors without editing.
2. `kiss_coder`: own one isolated disposable file, create it only when absent, verify it, and remove only that file.
3. `kiss_reviewer`: inspect a supplied diff and report material findings with exact locations without editing.

Check the working tree and selected fixtures before and after. A successful call supports only discovery and the narrow behavior observed.

<a id="upgrade-smoke"></a>
## Upgrade Smoke

Use an isolated installation to prove the supported transition:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list
```

Start from an installed v0.1.0, refresh the marketplace after the real v0.2.0 tag exists, confirm that the installed cache reports 0.2.0, and open a new session. Verify a v0.2.0-only interface such as `configure agents`, then check a v0.1-managed disposable project. Also exercise the documented pinned-tag rollback. Preserve the first decisive failure if any step does not work.

<a id="dogfooding"></a>
## Dogfooding during development

Use the current KISS project instructions and suitable real roles while developing the next version. Record where they reduce scope, expose failure, or improve evidence, and where they cause a reproducible wrong stop or unnecessary mechanism.

Keep product runtime and evaluator ownership separate: the Plugin under test does not define its own acceptance criteria or approve its own release. Human maintainers own the goal and acceptance; deterministic tests, an independent review, and fresh-session replay judge the observed result. Dogfooding is engineering evidence, not autonomous self-certification.

<a id="readme-pilot"></a>
## README newcomer Pilot

Give only the rendered landing page to one person who did not build the change. Without extra explanation, ask them to identify within five minutes:

- the over-design and over-defensive failure modes;
- why and when an Agent tends toward them;
- how KISS My Agent helps and what it cannot guarantee;
- whether it fits their work;
- the install, first-use, Agent configuration, and update paths.

When practical, have them complete setup in a disposable project without installing Python. Record only anonymous pass/fail observations and blocking confusion. Revise and replay the same checklist instead of moving the criteria.

<a id="evidence-boundaries"></a>
## Evidence boundaries

| Evidence | Supports | Does not support |
| --- | --- | --- |
| Source inspection | What tracked files say | Loaded runtime identity or behavior |
| Static/unit PASS | Tested repository invariants | Agent-native workflow behavior |
| Setup engineering run | Observed files for that scope and prompt | Future model consistency or crash atomicity |
| Exact-SHA native CI | That job, platform, Python, and commit | Every OS/client version or future compatibility |
| `/skills` discovery | Skill visibility in that fresh session | General instruction following or permissions |
| Role Smoke | The observed narrow role task | General role reliability |
| Newcomer Pilot | Comprehension by that participant | Universal usability |
| HTTP 200 plus content check | Deployed page availability and inspected content | Plugin installation or behavior |

Report failed and untested surfaces directly. Invalid runs caused by a failed precondition do not become negative product evidence.

<a id="stop-boundary"></a>
## Stop boundary

Stop when the defined question has proportionate evidence. Do not repeat model Smoke to manufacture confidence, add a permanent evaluation platform for a release check, or promote narrow results into compatibility, behavioral, research, authentication, permission, or safety guarantees.
