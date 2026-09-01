# Testing

[English](TESTING.md) | [简体中文](TESTING.zh-CN.md)

[README](../README.md) · [Installation](INSTALLATION.md) · [Configuration](CONFIGURATION.md) · [FAQ](FAQ.md)

<a id="test-surfaces"></a>
## Test Surfaces

KISS My Agent has four distinct test surfaces:

1. Native static validation of repository files.
2. Setup `check` of one explicit filesystem scope.
3. Live discovery of plugin Skills and standalone roles in a trusted new Codex session.
4. Harmless role Smoke checks that exercise one narrow responsibility per role.

Do not combine these into one stronger claim. Static PASS is not setup or publication evidence; setup `check` is not live discovery; discovery is not behavioral qualification; Smoke is not research or product evidence.

<a id="static-validation"></a>
## Static Validation

Python 3.11 or newer is required. The POSIX wrapper uses `python3` on Linux or macOS. The Windows wrapper accepts the `py -3` launcher or `python`.

Linux or macOS:

```bash
cd /absolute/path/to/kiss-my-agent
./scripts/validate.sh
```

Windows native PowerShell:

```powershell
Set-Location C:\absolute\path\to\kiss-my-agent
.\scripts\validate.ps1
```

WSL uses the Linux command and produces Linux evidence, not Windows evidence. The native wrappers are exercised by the [`Validate` workflow](../.github/workflows/validate.yml). A configured CI job is not a passing result; cite the green job for the exact commit.

The validator needs no Codex sandbox package, copied `CODEX_HOME`, container, VM, or extra test project. It checks only the properties named in its output and source.

<a id="project-defaults"></a>
## Project Defaults

The tracked `.codex/config.toml` explicitly sets `features.multi_agent = true` and `agents.enabled = true` without enumerating roles. The Host auto-discovers standalone role TOML files; each file's `name` field is the identity and its filename is only a convention.

The three supplied roles are editable seeds, not a closed catalog. The configuration does not choose trust, model, permissions, context, concurrency, provider, or credentials. Role model and effort inherit Host settings when omitted. The Host must trust the project before project config can load, and an effective explicit `false` remains a disablement.

<a id="setup-check"></a>
## Setup Check

After setup, start a new session and inspect the same explicit scope:

```text
$kiss-my-agent-setup check this project
$kiss-my-agent-setup check global setup
```

Use only the command matching the scope you changed. A setup `check` supports claims about the managed config, standalone seed files, and AGENTS block it inspected. It does not establish project trust, prove active-session discovery, restore deleted roles, or strengthen source/static evidence into remote-install evidence.

<a id="fresh-session"></a>
## Trusted New Session

After installing the plugin, changing config, instructions, Skills, or role TOML, close or leave the old session and start a new authenticated session from the repository root.

Linux or macOS:

```bash
cd /absolute/path/to/kiss-my-agent
codex
```

Windows native PowerShell:

```powershell
Set-Location C:\absolute\path\to\kiss-my-agent
codex
```

Establish project trust through the Host when prompted. Current already-running sessions are not guaranteed to hot-load any of these surfaces. A result from an old session is therefore not evidence that the new project config did or did not load.

<a id="skill-smoke"></a>
## Skill Discovery Smoke

In the trusted new session, run `/skills` and confirm the plugin-owned `kiss-my-agent` and `kiss-my-agent-setup` entries. Then invoke `$kiss-my-agent` only for a matching non-obvious mechanism or evidence decision. The setup Skill is reserved for explicit project/global setup, check, and remove operations.

This proves discovery and routing for that session and prompt. It does not prove compliance on future prompts.

<a id="role-smoke"></a>
## Three-Role Smoke

Use the Host's custom-agent interface or explicitly ask the primary thread to delegate to the named discovered role. Run one at a time and keep the tasks harmless:

1. `kiss_explorer`: ask it to read `README.md`, list the explicit HTML anchor IDs, and make no changes.
2. `kiss_coder`: ask it to create `tests/.kiss-coder-smoke.txt` only if absent, write one line, report it, and remove only that owned file before returning. If the path already exists, it must stop without overwriting.
3. `kiss_reviewer`: give it the current documentation diff and ask for read-only material findings with exact locations, without editing.

Before and after the Smoke, inspect the working tree. Preserve unrelated changes. A coder Smoke interrupted after creation may leave the named owned file; inspect it and remove it only after confirming it is the Smoke artifact.

The expected ownership is read-only explorer, state-changing coder within assignment, and independent read-only reviewer. Successful invocation supports only role discovery and the observed narrow behavior.

<a id="manual-scenarios"></a>
## Manual Scenarios

[`tests/scenarios.md`](../tests/scenarios.md) contains discussion fixtures for the permanent rules and Skill routing. They are not automated scores, release gates, or guarantees that every model behaves identically.

<a id="evidence-boundaries"></a>
## Evidence Boundaries

| Evidence | Supports | Does not support |
| --- | --- | --- |
| Source inspection | What tracked files say | Loaded runtime identity or behavior |
| Static validator PASS | Checked repository invariants | Plugin publication, agent compliance, Host support, research validity |
| Setup `check` PASS | Managed files in that explicit scope | Trust, active loading, remote install, role behavior |
| CI green job | Native wrapper PASS on that job, platform, and commit | Every OS version or future compatibility |
| `/skills` discovery | Plugin Skills visible in that new session | Future compliance or permission |
| One role Smoke | That discovered role completed that narrow task | General role reliability or product acceptance |
| Manual scenario discussion | Human interpretation of a case | Automated evaluation or qualification |

Always record platform, native shell, exact commit when attribution matters, Host version for live checks, whether the project was trusted, and whether the session was new. Report failures and untested surfaces directly.

<a id="stop-boundary"></a>
## Stop Boundary

Stop when the test answers its stated question. Do not repeat Smoke checks to manufacture confidence, create persistent test installations, or promote a narrow result into a compatibility or behavioral guarantee.
