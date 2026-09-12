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

For a simple one-off task, use an ordinary single conversation; no setup evidence is required. To verify the persistent KMA instructions after Plugin installation or update, start a new session and use the Plugin-owned interfaces:

```text
$kiss-my-agent:kiss-my-agent-setup set up this project
$kiss-my-agent:kiss-my-agent-setup check this project
$kiss-my-agent:kiss-my-agent-setup configure agents for this project
```

These operations use Codex file tools and require no Python, Node.js, Docker, or package manager. Git-backed Plugin installation or refresh separately requires a usable `git` executable and GitHub network access. `check` proves only the inspected file state. Use `/skills` and a narrow role Smoke when live discovery matters. If a requested role Smoke cannot run, report the missing discovery evidence; direct work cannot prove role loading. Continue unrelated authorized work within available capabilities.

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
- missing master fields filled independently with Astra/high, preserved explicit fields, and missing experimental context filled with true; `check` validates presence and types;
- each missing feature switch added independently, while marked and unmarked values for both switch paths, unrelated config, comments, newline style, AGENTS content, and existing roles are preserved;
- exact paired migration of legacy top-level `gpt-5.6-sol` / `max` lines only when both occur once with the exact KISS marker, followed by a no-op repeated setup;
- preservation of existing fields plus independent filling of missing fields for four near misses: a missing companion, an unmarked pair, a modified value, and a user-chosen custom pair; duplicate or invalid assignments remain conflicts;
- intentional `false` values and deliberately deleted seed roles;
- malformed managed config or exact bundled-role TOML, unsafe managed path types, `AGENTS.override.md`, and an exact bundled filename/identity mismatch; an invalid unselected custom role remains outside KISS ownership and does not block setup, check, remove, or a configuration request that selected another role;
- different observable definitions for the same bundled role filename in project and global scopes: project setup/check inspects only the project target and leaves the global role unchanged, while a fresh project session demonstrates the Host's project-over-global precedence without KISS rejecting or reconciling the duplicate;
- remove deleting only exact current defaults with their KISS markers, any exact legacy marked master pair, and current/v0.2.6/v0.2.5/v0.1 exact role seeds, while preserving unmarked config and modified roles;
- configuring one selected role while all other fields and files remain unchanged;
- restoring inheritance by removing only the selected optional key;
- fresh setup creates missing roles with `model = "gpt-6-astra"` and `model_reasoning_effort = "medium"`, preserving every existing role;
- refusal to write `danger-full-access` without its separate confirmation;
- recognition of a project created by v0.1.0 markers as `outdated`, followed by a setup refresh that may update the managed block and config but leaves all role files directly unchanged;
- a missing starter under a current or outdated managed block reported as intentionally absent rather than recreated, outdated, or incomplete.

A process or machine crash during model-driven file edits is outside transactional proof. Report it directly rather than claiming atomic recovery.

<a id="local-plugin"></a>
## Test a changed Plugin, not a stale cache

For ordinary development, use the existing local Plugin source, preserve unrelated changes, apply one Codex cachebuster to its development manifest with the current Plugin Creator helper, and reinstall from that local marketplace. Use the development version in the authorized real task. Isolate setup or install tests when their side effects or a controlled comparison require it; isolation is not a prerequisite for dogfooding.

When guidance text changes, current agents can explicitly read the updated entry once and continue the task. This is explicit adoption, not automatic reloading or evidence of fresh-session discovery. Use a new session when startup, loading, or discovery itself needs verification.

Use this copyable Codex prompt:

```text
$plugin-creator update this existing KISS My Agent plugin for local development. Confirm the existing local marketplace source, preserve unrelated changes, apply the candidate changes there, add exactly one +codex.<cachebuster> suffix to its development manifest with the helper, and reinstall from that marketplace. Continue the authorized real task by explicitly reading updated guidance where needed. Do not modify the canonical release manifest or the Git-backed marketplace; use a new session when verifying startup, loading, or discovery.
```

See the official OpenAI [Plugin Creator and local marketplace guidance](https://developers.openai.com/plugins/build/plugins#package-with-plugin-creator) and [marketplace add/upgrade commands](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli).

Do not add a cachebuster to the canonical release manifest, hand-edit a configured marketplace, or treat a Git-backed release cache as evidence for working-tree changes. State the Plugin source and version actually used, the observed task behavior, and whether guidance was explicitly reread or loaded in a new session.

<a id="fresh-session"></a>
## Trusted fresh session

Installation, upgrade, setup, removal, and changes to config, instructions, Skills, or roles can affect startup and discovery. When verifying that loading behavior, open a new authenticated session at the intended project and establish trust through the Host interface when prompted.

Record the OS, native shell, Codex version, Plugin version, source identity, scope, trust state, and whether the session is new. An old session cannot prove that changed configuration loaded or failed to load.

When testing fresh-session native delegation, use a regular session; with `codex exec`, omit `--ephemeral`. In one PawWeaver dogfood comparison using Codex CLI 0.153.4 and KISS My Agent v0.2.7 in the same trusted project, `--ephemeral --json --sandbox read-only` exposed all three KISS roles and both Skills, but native `kiss_explorer` spawning failed twice with `no thread with id`. A regular `codex exec` session without `--ephemeral` subsequently spawned one native `kiss_explorer`, which completed its read-only investigation and returned findings.

Preserve the failed outcome as a Host/session test failure: discovery did not establish working delegation, and no child result existed. To check recovery, confirm that a native child completes the bounded task and returns its result; successful discovery or spawning alone is insufficient. This observation does not establish the root cause, general `--ephemeral` incompatibility, full CLI 0.153.4 compatibility, or KISS effectiveness.

If named roles disappear after moving a project or changing its launch path, compare the current launch path and resolved project directory with the Host's persisted project trust entry. Role TOML files can exist while that project scope is not loaded. In a separate PawWeaver observation on CLI 0.153.4, the old symlink path was trusted but the canonical launch directory was absent from persisted project trust. A temporary CLI trust override did not restore discovery; adding only the authorized canonical project trust entry restored the native role catalog in a fresh ordinary session. All three native KISS roles then completed bounded read-only tasks; spawn arguments and child session records identified the roles and Astra/medium execution. This was project trust/discovery recovery, not a KISS code defect or proof of broader task effectiveness.

Repair the observed current-project trust mismatch through the Host under the user's authorization, preserving existing entries, then check fresh native role execution. Keep role files in their intended project scope; this observation does not justify moving them into global scope, reinstalling the Plugin, or changing unrelated feature flags. File existence, discovery, and a completed native child task remain distinct evidence.

<a id="skill-smoke"></a>
## Skill discovery Smoke

In the fresh session, run `/skills` and confirm the canonical Plugin Skills `kiss-my-agent:kiss-my-agent` and `kiss-my-agent:kiss-my-agent-setup` (the picker labels may appear as `kiss-my-agent (kiss-my-agent)` and `kiss-my-agent-setup (kiss-my-agent)` on the tested Codex 0.152.1 baseline). Then use:

- Each agent reads `$kiss-my-agent:kiss-my-agent` when first taking on KMA-managed work, then reuses it across assignments and continuations and applies it proactively when choosing or changing an action, dividing work, or interpreting results, without first judging the decision non-obvious;
- `$kiss-my-agent:kiss-my-agent-setup` only for explicit setup/check/configure/remove work.

Already-decided mechanical execution, including implementation, tests, builds, Git, lookup, and formatting, needs no repeated Skill reading, extra review, or compliance record. Reread only when the guidance changes or relevant detail is missing. Discovery proves visibility for that session, not future instruction following.

<a id="role-smoke"></a>
## Three-role Smoke

This explicit role Smoke tests the three seed roles, not a required team for ordinary work. The master assigns the disposable tasks through the Host custom-Agent interface or a request to delegate one bounded task to each discovered role:

1. `kiss_explorer`: read a fixture and report exact anchors without editing.
2. `kiss_coder`: own one isolated disposable file, create it only when absent, verify it, and remove only that file.
3. `kiss_reviewer`: inspect a supplied diff and report material findings with exact locations without editing.

In a new trusted client task, confirm the effective master uses Astra/high, all three current roles use Astra/medium, and experimental context management is loaded. Use observable Host configuration or diagnostics, not Agent self-description alone; report unavailable evidence explicitly. Run the bounded three-role Smoke above once, checking the working tree and selected fixtures before and after. Static config, actual loading and observed behavior support different claims; this is not a long-context or model-performance benchmark.

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

Use the current KISS project instructions while developing the next version. The master may directly complete clear small or local work, and should actively delegate substantial bulk, independent parallel work, or work needing another perspective when the benefit outweighs coordination cost. Choose by workload, parallel opportunity, coupling, risk, and coordination cost; optional roles do not mean the master should do everything. Each available role may have zero, one, or multiple instances, with no fixed team, sequence, or required subagent launch. Keep delegated work flat by default. Observe whether the division of work reduces scope, exposes failure, or improves evidence, and whether it causes reproducible wrong stops or unnecessary mechanisms.

Keep product runtime and evaluator ownership separate: the Plugin under test does not define its own acceptance criteria or approve its own release. Human maintainers own the goal and acceptance; use deterministic tests, independent review where it adds decision value or is explicitly required, and fresh-session replay as applicable to judge the observed result. Dogfooding is engineering evidence, not autonomous self-certification.

A coordinator wait call returning without an update does not prove that a child Agent timed out or failed. Let bounded, non-conflicting work continue; interrupt only for an obsolete task, a scope or resource conflict, or an explicit user stop.

If delegation is disabled or unavailable, or no suitable role exists, the master may continue within its capabilities and existing authorization without a staffing approval step. Report unmet explicit requirements for independent checking or a specific role, and real capability gaps; direct execution must not be presented as satisfying them.

<a id="readme-pilot"></a>
## README newcomer Pilot

Give only the final rendered landing page to a new user who has never encountered this project or any earlier README draft and did not participate in the change. Without extra explanation, ask them to identify within five minutes:

- the over-design and over-defensive failure modes;
- why and when an Agent tends toward them;
- how KISS My Agent helps and what it cannot guarantee;
- in plain language, the loop `goal/assumption → smallest runnable validation → real result → iterate or stop`, and the difference between a low-cost reversible trial and bypassing authentication or permissions or crossing an irreversible high-risk boundary;
- whether it fits their work;
- the company model: the Owner retains the goal, architecture, acceptance criteria, and stop point; the Master / CEO owns orchestration, decisions, and synthesis; `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` own read-only investigation, bounded implementation, and independent read-only review, respectively;
- that KISS supplies missing Astra/high Master defaults, starter roles use Astra/medium, and the Master normally delegates directly in a flat structure rather than through a fixed workflow or deep organization;
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
