# Installation

[README](../README.md) · [简体中文](../README.zh-CN.md) · [Extending](EXTENDING.md) · [FAQ](FAQ.md)

KISS My Agent is distributed as source files. There is no automatic installer. Choose one scope, inspect existing files, and keep one authoritative copy at that scope.

## Prerequisites

- An existing checkout of this repository, referenced below as `$KISS_REPO_ROOT`.
- A target project, referenced as `$TARGET_PROJECT`, for project-scoped adoption.
- A Codex version that supports repository skills and custom agent TOML files.
- Authority to read and write the chosen destination. Installation does not grant permissions or authentication.

Set paths explicitly:

```bash
export KISS_REPO_ROOT=/absolute/path/to/kiss-my-agent
export TARGET_PROJECT=/absolute/path/to/your-project
```

## Option 1: project skill

The repository skill location is `.agents/skills/kiss-my-agent/`. Install it into the same location in the target project:

```bash
mkdir -p "$TARGET_PROJECT/.agents/skills"
test ! -e "$TARGET_PROJECT/.agents/skills/kiss-my-agent"
cp -R "$KISS_REPO_ROOT/.agents/skills/kiss-my-agent" "$TARGET_PROJECT/.agents/skills/"
```

If the destination exists, stop and compare it first:

```bash
diff -ru "$TARGET_PROJECT/.agents/skills/kiss-my-agent" "$KISS_REPO_ROOT/.agents/skills/kiss-my-agent"
```

Decide which changes to merge; do not keep parallel authoritative copies in one scope.

## Option 2: user skill

The supported user skill location is `$HOME/.agents/skills/kiss-my-agent/`:

```bash
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/kiss-my-agent"
cp -R "$KISS_REPO_ROOT/.agents/skills/kiss-my-agent" "$HOME/.agents/skills/"
```

`$CODEX_HOME/skills/kiss-my-agent/` is a verified compatibility fallback for hosts that still discover skills there. Use it only after confirming that behavior for the installed host version. Do not install the same skill in both the supported user location and the fallback; two copies create ambiguous authority.

## Option 3: project agents

Project-local custom agents live in `.codex/agents/`:

```bash
test ! -e "$TARGET_PROJECT/.codex/agents"
mkdir -p "$TARGET_PROJECT/.codex"
cp -R "$KISS_REPO_ROOT/.codex/agents" "$TARGET_PROJECT/.codex/"
```

If the directory already exists, compare and manually merge each role instead of replacing it. The supplied role settings are:

| Role | Model | Reasoning | Sandbox |
| --- | --- | --- | --- |
| explorer | `gpt-5.6-sol` | `medium` | `read-only` |
| coder | `gpt-5.6-sol` | `high` | `workspace-write` |
| review | `gpt-5.6-sol` | `xhigh` | `read-only` |

If that model or effort is unavailable, edit the affected TOML deliberately and update the matching `expected_roles` entry in `scripts/validate.sh`. Keep the role boundary intact and validate the resulting schema.

## Personal agents

Personal custom agents live in `~/.codex/agents/`. Inspect any existing role with the same name and merge manually. For a new empty personal agent directory:

```bash
test ! -e "$HOME/.codex/agents"
mkdir -p "$HOME/.codex"
cp -R "$KISS_REPO_ROOT/.codex/agents" "$HOME/.codex/"
```

Project and personal agents with the same role name may have host-specific precedence. Prefer one intentional authority rather than duplicates.

## Merge project instructions safely

Never overwrite an existing `AGENTS.md`. Review the difference:

```bash
diff -u "$TARGET_PROJECT/AGENTS.md" "$KISS_REPO_ROOT/AGENTS.md"
```

If the target has no `AGENTS.md`, copying is safe after confirming that no deeper or fallback instruction source already owns the policy:

```bash
test ! -e "$TARGET_PROJECT/AGENTS.md"
cp "$KISS_REPO_ROOT/AGENTS.md" "$TARGET_PROJECT/AGENTS.md"
```

When instructions already exist, manually merge only the boundaries that fit the project. Preserve domain safety, ownership, acceptance, and stop rules. Do not copy a `config.toml`; this repository does not provide one.

## Confirm discovery

Start a **new** Codex session in the destination after changing skills or agents. Run:

```text
/skills
```

Confirm `kiss-my-agent` appears, then invoke it only for a matching task with:

```text
$kiss-my-agent
```

Discovery confirms that the host found the skill. It does not prove task behavior, permissions, authentication, or compatibility with another host.

## Update or remove

For updates, diff the installed directory against the new source and merge or replace only after reviewing local changes. For removal, delete exactly the installed `kiss-my-agent` directory from the one chosen scope and start a new session. Also remove any manually merged project instructions only through a reviewed diff; there is no automated uninstall.

## Sandbox before adoption

Inside this repository:

```bash
./scripts/validate.sh
./scripts/stage-sandbox.sh
./scripts/validate.sh
```

The staging script rebuilds only `.sandbox/`, installs the skill and agents at project scope inside an isolated inner Git project, and prints a launch command without running it.
