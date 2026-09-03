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

For a simple one-off task, use an ordinary single conversation; no setup evidence is required. To verify the persistent executive workflow after Plugin installation or update, start a new session and use the Plugin-owned interfaces:

```text
$kiss-my-agent:kiss-my-agent-setup set up this project
$kiss-my-agent:kiss-my-agent-setup check this project
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
```

These operations use Codex file tools and require no Python, Node.js, Docker, or package manager. Git-backed Plugin installation or refresh separately requires a usable `git` executable and GitHub network access. `check` proves only the inspected file state. Use `/skills` and a narrow role Smoke when live discovery matters. If delegation is unavailable or no role can staff the test, record the failed precondition and obtain the user's explicit choice before switching to an ordinary single-conversation test.

<a id="contributor-suite"></a>
## Contributor test suite

Plugin/Skill-only contributors need Python 3.11 or newer but no third-party package. Run the local core checks:

```bash
python3 scripts/validate.py
python3 -m unittest tests.test_setup -v
```

Local site construction is not required for those changes. Pull-request CI installs `requirements-site.txt` and runs `python scripts/test_all.py`, which performs static validation, all unit tests, and a documentation build in a temporary output directory. It must leave tracked files unchanged. Linux/macOS and native Windows CI run the same complete entrypoint; shell wrappers remain narrow checks of their native launch behavior.

The test suite verifies repository-owned contracts. It cannot execute a model-driven setup workflow in CI without a real authenticated Codex session, so those cases remain explicit engineering runs rather than fake unit coverage. The v0.1 contributor CLI `skills/kiss-my-agent-setup/scripts/setup.py` was removed in v0.2; validation should prove that breaking interface is absent and that documentation routes users to the conversational Skill, not pretend Agent-native behavior is deterministic CLI coverage.

<a id="setup-scenarios"></a>
## Agent-native setup scenarios

Run setup scenarios only in disposable projects and an explicitly isolated Codex home. Preserve the before/after files for review, but do not commit logs or temporary user data.

Required scenarios cover:

- pristine project setup, repeated setup, check, and remove;
- mutually exclusive managed-block classification: a current block never receives missing master keys; an absent or recognized-outdated block receives the pair only when both keys are absent; otherwise existing assignments are preserved and each missing key remains absent for inheritance;
- each missing feature switch added independently, while marked and unmarked values for all four paths, unrelated config, comments, newline style, AGENTS content, and existing roles are preserved;
- intentional `false` values and deliberately deleted seed roles;
- malformed managed config or exact bundled-role TOML, unsafe managed path types, `AGENTS.override.md`, and an exact bundled filename/identity mismatch; an invalid unselected custom role remains outside KISS ownership and does not block setup, check, remove, or a configuration request that selected another role;
- different observable definitions for the same bundled role filename in project and global scopes: project setup/check inspects only the project target and leaves the global role unchanged, while a fresh project session demonstrates the Host's project-over-global precedence without KISS rejecting or reconciling the duplicate;
- remove deleting only the four marked config assignments and current/v0.1 exact role seeds, while preserving unmarked config and modified roles;
- configuring one selected role while all other fields and files remain unchanged;
- restoring inheritance by removing only the selected optional key;
- applying `gpt-5.6-sol` / `max` as the paired initial master default and `gpt-5.6-sol` / `high`, `high`, `xhigh` only to missing roles during fresh setup, while preserving every existing role;
- refusal to write `danger-full-access` without its separate confirmation;
- recognition of a project created by v0.1.0 markers as `outdated`, followed by a setup refresh that may update the managed block and config but leaves all role files directly unchanged;
- a missing starter under a current or outdated managed block reported as intentionally absent rather than recreated, outdated, or incomplete.

A process or machine crash during model-driven file edits is outside transactional proof. Report it directly rather than claiming atomic recovery.

<a id="local-plugin"></a>
## Test a changed Plugin, not a stale cache

For development, use an isolated local marketplace that already points to a temporary copy of the edited Plugin. Apply one Codex cachebuster to that copy with the current Plugin Creator helper, reinstall it from that local marketplace, and start a new session.

Use this copyable Codex prompt:

```text
$plugin-creator update this existing KISS My Agent plugin for local development. Stage a disposable candidate copy outside the checkout in a separate local marketplace, point that marketplace only at the candidate copy, add exactly one +codex.<cachebuster> suffix to the copy's manifest version, reinstall it from that marketplace into an isolated Codex home, and tell me to start a new thread. Do not modify tracked release files or the Git-backed marketplace.
```

See the official OpenAI [Plugin Creator and local marketplace guidance](https://developers.openai.com/plugins/build/plugins#package-with-plugin-creator) and [marketplace add/upgrade commands](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli).

Do not add a cachebuster to the canonical release manifest, hand-edit a configured marketplace, or treat a Git-backed release cache as evidence for working-tree changes. Record the loaded Plugin version and a behavior unique to the candidate.

<a id="fresh-session"></a>
## Trusted fresh session

Installation, upgrade, setup, removal, and changes to config, instructions, Skills, or roles affect startup and discovery. Open a new authenticated session at the intended project and establish trust through the Host interface when prompted.

Record the OS, native shell, Codex version, Plugin version, source identity, scope, trust state, and whether the session is new. An old session cannot prove that changed configuration loaded or failed to load.

<a id="skill-smoke"></a>
## Skill discovery Smoke

In the fresh session, run `/skills` and confirm the canonical Plugin Skills `kiss-my-agent:kiss-my-agent` and `kiss-my-agent:kiss-my-agent-setup` (the picker labels may appear as `kiss-my-agent (kiss-my-agent)` and `kiss-my-agent-setup (kiss-my-agent)` on the tested Codex 0.152.1 baseline). Then use:

- `$kiss-my-agent:kiss-my-agent` only for a real non-obvious mechanism, scope, runtime/evaluator, or evidence decision;
- `$kiss-my-agent:kiss-my-agent-setup` only for explicit setup/check/configure/remove work.

Ordinary implementation, tests, builds, Git, lookup, and formatting should not route through `kiss-my-agent`. Discovery proves visibility for that session, not future instruction following.

<a id="role-smoke"></a>
## Three-role Smoke

Keep the master on coordination, decisions, and synthesis: it assigns but does not perform the disposable investigation, implementation, or review. Default to direct flat fan-out, and use multiple instances of a role when that is the useful shape. Use the Host custom-Agent interface or explicitly ask it to delegate one bounded task to each discovered role:

1. `kiss_explorer`: read a fixture and report exact anchors without editing.
2. `kiss_coder`: own one isolated disposable file, create it only when absent, verify it, and remove only that file.
3. `kiss_reviewer`: inspect a supplied diff and report material findings with exact locations without editing.

Confirm that the configured defaults resolve to `gpt-5.6-sol` with role efforts `high`, `high`, and `xhigh`, respectively, and that the master uses the paired `gpt-5.6-sol` / `max` config defaults. If the Host or account does not support a configured value, report the failed precondition rather than weakening the expected result. Check the working tree and selected fixtures before and after. A successful call supports only discovery and the narrow behavior observed.

Test a department lead only for a large independent disposable subsystem whose direct aggregation would pollute master context. Confirm there is at most one temporary intermediate layer, workers do not delegate, the assignment ends with the task, and every shared resource retains one operator. Do not manufacture hierarchy merely to exercise it.

<a id="upgrade-smoke"></a>
## Public release Smoke

Before tagging, run the dependency-free local core checks and require the complete native pull-request CI for the exact candidate commit. Those results are candidate evidence, not public install or live Host evidence.

After the pull request is merged and the exact commit has been tagged and pushed as `vX.Y.Z`, use isolated public installs to run only the bounded checks that require a public distribution surface. Replace `vX.Y.Z` in every command with the one release version selected for this release:

```bash
codex plugin marketplace upgrade kiss-my-agent
codex plugin list --marketplace kiss-my-agent
```

Reuse prior evidence only when the source and behavior it covers are unchanged; state explicitly that the result was reused rather than rerun. Do not repeat candidate checks after tagging. Verify only the public archive, marketplace install or upgrade, fresh-session discovery, or other public-only behavior required by the release acceptance criteria. Do not add role migration, hashes, induced failures, or a repeated matrix unless the changed behavior requires them.

Classify the first decisive post-tag failure before acting:

- A defect in the tagged product source: preserve the tag, do not create a GitHub Release for it, fix the source, and use the next patch version.
- A harness, command-construction, or environment failure: fix that owner and obtain only the missing evidence against the same tag.
- An evaluator error or another invalid run: correct the evaluation and rerun only the invalid observation; it is not product-negative evidence and does not trigger a patch version.
- A product defect found after the GitHub Release is published: preserve the released tag and publish the correction as a new patch version.

Only after the required public checks pass may the maintainer create the GitHub Release. Preserve every pushed tag and the first decisive failure.

<a id="dogfooding"></a>
## Dogfooding during development

Use the current KISS project instructions and suitable real roles while developing the next version. Keep the master on orchestration, decisions, and synthesis; default to flat direct fan-out and assign investigation, implementation, and review to the corresponding roles. Record where they reduce scope, expose failure, or improve evidence, and where they cause a reproducible wrong stop or unnecessary mechanism.

Keep product runtime and evaluator ownership separate: the Plugin under test does not define its own acceptance criteria or approve its own release. Human maintainers own the goal and acceptance; deterministic tests, an independent review, and fresh-session replay judge the observed result. Dogfooding is engineering evidence, not autonomous self-certification.

A coordinator wait call returning without an update does not prove that a child Agent timed out or failed. Let bounded, non-conflicting work continue; interrupt only for an obsolete task, a scope or resource conflict, or an explicit user stop.

If delegation becomes disabled or unavailable, or no suitable role exists, record the staffing issue. The master must ask whether to repair staffing or explicitly switch this task to ordinary single-conversation execution; it must not silently continue as the worker.

<a id="readme-pilot"></a>
## README newcomer Pilot

Give only the final rendered landing page to a new user who has never encountered this project or any earlier README draft and did not participate in the change. Without extra explanation, ask them to identify within five minutes:

- the over-design and over-defensive failure modes;
- why and when an Agent tends toward them;
- how KISS My Agent helps and what it cannot guarantee;
- in plain language, the loop `goal/assumption → smallest runnable validation → real result → iterate or stop`, and the difference between a low-cost reversible trial and bypassing authentication or permissions or crossing an irreversible high-risk boundary;
- whether it fits their work;
- the company model: the Owner retains the goal, architecture, acceptance criteria, and stop point; the Master / CEO owns orchestration, decisions, and synthesis; `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` own read-only investigation, bounded implementation, and independent read-only review, respectively;
- that the defaults are editable and the Master normally delegates directly in a flat structure, not through a fixed workflow or deep organization;
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
