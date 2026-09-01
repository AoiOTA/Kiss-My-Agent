# Installation and coexistence

[README](../README.md) · [简体中文](../README.zh-CN.md) · [Configuration](CONFIGURATION.md) · [Extending](EXTENDING.md) · [FAQ](FAQ.md)

KISS My Agent is a set of independent source components, not an installer. You may validate the repository directly or adopt only the AGENTS guidance, Skill, or prefixed custom roles that add value to an existing setup.

The default rule is simple: **keep existing configuration and stop before every collision**. Never overwrite an unknown `config.toml`, instruction file, Skill, or Agent.

## Prerequisites

- A current Codex or ChatGPT desktop installation that supports repository Skills and custom Agent TOML files.
- An existing checkout of this repository, referenced as `$KISS_REPO_ROOT`.
- A target project, referenced as `$TARGET_PROJECT`, only when project-scoped adoption is desired.
- Authority to write the selected destination. Installation never grants filesystem, network, account, or authentication permission.

```bash
export KISS_REPO_ROOT=/absolute/path/to/kiss-my-agent
# Set this only for project-scoped adoption:
export TARGET_PROJECT=/absolute/path/to/your-project
: "${KISS_REPO_ROOT:?set KISS_REPO_ROOT first}"
```

## Test the checkout without installing anything

The zero-install, repository-local check is the static validator:

```bash
if [ ! -x "$KISS_REPO_ROOT/scripts/validate.sh" ]; then
  printf 'KISS_REPO_ROOT does not contain an executable scripts/validate.sh.\n' >&2
else
  (cd "$KISS_REPO_ROOT" && ./scripts/validate.sh)
fi
```

To verify live Host discovery, start a new authenticated session only if normal Host-state updates are acceptable:

```bash
codex
```

Inside the new session, use `/skills` to confirm `kiss-my-agent` and invoke it only for a matching non-obvious decision. The KISS Agent files are optional templates and require registration in the intended config layer before their names are available.

The validator does not write user configuration. A live CLI or Desktop Host may still update its own project trust, history, caches, or marketplace timestamps under the configured home. That is Host behavior, not KISS installation. No sandbox package or extra test project is required; use a disposable OS account or Host profile only when absolutely no user-state write is acceptable.

## Inventory an existing setup first

Before copying anything, inspect the effective destinations:

```bash
printf 'CODEX_HOME=%s\n' "${CODEX_HOME:-$HOME/.codex}"
find "${CODEX_HOME:-$HOME/.codex}/agents" -maxdepth 1 -type f -name '*.toml' -print 2>/dev/null
find "$HOME/.agents/skills" -mindepth 1 -maxdepth 1 -type d -print 2>/dev/null
if [ -n "${TARGET_PROJECT:-}" ]; then
  find "$TARGET_PROJECT/.codex/agents" -maxdepth 1 -type f -name '*.toml' -print 2>/dev/null
  find "$TARGET_PROJECT/.agents/skills" -mindepth 1 -maxdepth 1 -type d -print 2>/dev/null
fi
```

Also check these files manually when they exist:

```text
$CODEX_HOME/config.toml
$CODEX_HOME/AGENTS.override.md
$CODEX_HOME/AGENTS.md
$TARGET_PROJECT/.codex/config.toml
$TARGET_PROJECT/AGENTS.override.md
$TARGET_PROJECT/AGENTS.md
```

Codex may load deeper project instructions and configured fallback filenames as well. Confirm the actual project root and effective instruction chain before merging AGENTS guidance.

## Collision decisions

| Existing destination | Default action |
| --- | --- |
| User or project `config.toml` | Keep it; copy only individually reviewed keys if needed |
| `AGENTS.override.md` | Treat it as the effective source at that directory; do not edit a hidden base and claim success |
| Existing `AGENTS.md` | Keep it; manually merge only applicable KISS principles |
| Existing `explorer`, `coder`, or `review` Agent | Keep it; KISS roles use separate `kiss_*` names |
| Existing `kiss_explorer`, `kiss_coder`, or `kiss_reviewer` | Stop and diff; do not overwrite |
| Existing `kiss-my-agent` Skill at any chosen scope | Stop and diff; keep one authoritative copy |
| User-level and project-level `kiss-my-agent` both present | Choose one intended scope; same-name Skills are not merged |
| Unknown owner or precedence | Skip that component until ownership is clear |

## Adopt the Skill

Choose exactly one scope.

### Project scope

```bash
: "${TARGET_PROJECT:?set TARGET_PROJECT for project-scoped adoption}"
if [ ! -d "$KISS_REPO_ROOT/.agents/skills/kiss-my-agent" ] || [ ! -d "$TARGET_PROJECT" ]; then
  printf 'Skill source or target project directory is missing; nothing was copied.\n' >&2
elif [ -e "$HOME/.agents/skills/kiss-my-agent" ] || [ -e "$TARGET_PROJECT/.agents/skills/kiss-my-agent" ]; then
  printf 'kiss-my-agent already exists in user or target-project scope; inspect and choose one copy.\n' >&2
else
  mkdir -p "$TARGET_PROJECT/.agents/skills"
  cp -R "$KISS_REPO_ROOT/.agents/skills/kiss-my-agent" "$TARGET_PROJECT/.agents/skills/"
fi
```

### User scope

```bash
if [ ! -d "$KISS_REPO_ROOT/.agents/skills/kiss-my-agent" ]; then
  printf 'Skill source directory is missing; nothing was copied.\n' >&2
elif [ -e "$HOME/.agents/skills/kiss-my-agent" ]; then
  printf 'kiss-my-agent already exists in user scope; inspect it before installing.\n' >&2
else
  mkdir -p "$HOME/.agents/skills"
  cp -R "$KISS_REPO_ROOT/.agents/skills/kiss-my-agent" "$HOME/.agents/skills/"
fi
```

Do not install the same Skill in both scopes for a project where it will be used. A user-scoped install cannot inspect every repository on the machine, so check a target project's `.agents/skills/` before using it there. Current official Codex locations are repository `.agents/skills/` and user `$HOME/.agents/skills/`; this project no longer documents a legacy second user path.

## Adopt the optional KISS Agents

The project roles are deliberately prefixed to coexist with built-in and personal generic roles:

```text
kiss_explorer
kiss_coder
kiss_reviewer
```

For project scope, perform a complete collision check before copying any file:

```bash
: "${TARGET_PROJECT:?set TARGET_PROJECT for project-scoped adoption}"
personal_agent_dir="${CODEX_HOME:-$HOME/.codex}/agents"
role_conflict=0
if [ ! -d "$TARGET_PROJECT" ]; then
  printf 'Target project directory is missing; nothing was copied.\n' >&2
  role_conflict=1
fi
for role in kiss_explorer kiss_coder kiss_reviewer; do
  if [ ! -f "$KISS_REPO_ROOT/.codex/agents/$role.toml" ]; then
    printf 'Source role %s is missing; nothing was copied.\n' "$role" >&2
    role_conflict=1
  elif [ -e "$TARGET_PROJECT/.codex/agents/$role.toml" ] || [ -e "$personal_agent_dir/$role.toml" ]; then
    printf '%s already exists in personal or target-project scope; inspect before installing.\n' "$role" >&2
    role_conflict=1
  fi
done
if [ "$role_conflict" -eq 0 ]; then
  mkdir -p "$TARGET_PROJECT/.codex/agents"
  for role in kiss_explorer kiss_coder kiss_reviewer; do
    cp "$KISS_REPO_ROOT/.codex/agents/$role.toml" "$TARGET_PROJECT/.codex/agents/$role.toml"
  done
fi
```

For personal scope, check the personal destination before copying:

```bash
personal_agent_dir="${CODEX_HOME:-$HOME/.codex}/agents"
role_conflict=0
for role in kiss_explorer kiss_coder kiss_reviewer; do
  if [ ! -f "$KISS_REPO_ROOT/.codex/agents/$role.toml" ]; then
    printf 'Source role %s is missing; nothing was copied.\n' "$role" >&2
    role_conflict=1
  elif [ -e "$personal_agent_dir/$role.toml" ]; then
    printf '%s already exists in personal scope; inspect before installing.\n' "$role" >&2
    role_conflict=1
  fi
done
if [ "$role_conflict" -eq 0 ]; then
  mkdir -p "$personal_agent_dir"
  for role in kiss_explorer kiss_coder kiss_reviewer; do
    cp "$KISS_REPO_ROOT/.codex/agents/$role.toml" "$personal_agent_dir/$role.toml"
  done
fi
```

Existing generic roles remain untouched. If a `kiss_*` role already exists, compare the files and either keep the existing role or manually merge the desired instructions. Before using personal roles in a project, also inspect that project's registrations for the same prefixed names.

After copying role files, register only the desired prefixed roles in the corresponding existing config layer. The non-active [`config.example.toml`](../examples/config.example.toml) contains these exact tables:

```toml
[agents.kiss_explorer]
description = "KISS My Agent read-only explorer"
config_file = "agents/kiss_explorer.toml"

[agents.kiss_coder]
description = "KISS My Agent implementation agent"
config_file = "agents/kiss_coder.toml"

[agents.kiss_reviewer]
description = "KISS My Agent independent read-only reviewer"
config_file = "agents/kiss_reviewer.toml"
```

Merge these tables into the selected user or trusted-project `config.toml` without replacing unrelated content. Relative `config_file` paths resolve from that config layer. If the project is untrusted, Codex ignores the project `.codex` layer; trust must be established through the Host before project registrations can load.

The supplied model, reasoning effort, and sandbox settings are editable examples. See [Configuration](CONFIGURATION.md).

## Merge AGENTS guidance

Never overwrite an existing instruction source. If the target has no applicable root instruction or override, copying the repository file is possible after inspection:

```bash
: "${TARGET_PROJECT:?set TARGET_PROJECT for project-scoped adoption}"
if [ ! -f "$KISS_REPO_ROOT/AGENTS.md" ] || [ ! -d "$TARGET_PROJECT" ]; then
  printf 'AGENTS source or target project directory is missing; nothing was copied.\n' >&2
elif [ -e "$TARGET_PROJECT/AGENTS.override.md" ] || [ -e "$TARGET_PROJECT/AGENTS.md" ]; then
  printf 'An instruction source already exists; merge manually instead of copying.\n' >&2
else
  cp "$KISS_REPO_ROOT/AGENTS.md" "$TARGET_PROJECT/AGENTS.md"
fi
```

When instructions already exist, manually merge only the KISS boundaries that fit the project. Preserve the user's ownership, domain safety, acceptance, and stop rules. If an override is active, update the intended effective source or skip AGENTS adoption; do not create a parallel hidden source.

## Preserve existing runtime configuration

The repository has no active `.codex/config.toml`. The annotated [`config.example.toml`](../examples/config.example.toml) is inert at its tracked path.

Most adopters need no config changes. If one runtime setting is useful, copy that single key into a reviewed user, trusted-project, Profile, or CLI layer. Never replace an existing config wholesale, and do not silently change models, context limits, compaction, permissions, providers, authentication, or telemetry.

## Confirm discovery

Start a new session after changing instructions, Skills, Agents, or startup configuration.

- Use `/skills` and confirm exactly one `kiss-my-agent` entry from the intended scope.
- Inspect available Agents and confirm `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` only if they were installed.
- Confirm the effective model, permissions, project root, and instruction sources.

Discovery proves that the host found a component. It does not guarantee future Agent behavior or grant new authority.

## Update or remove

- Update a component only after diffing its installed copy against the new source.
- Remove only the exact `kiss-my-agent` directory or `kiss_*.toml` files that were installed.
- Remove manually merged AGENTS lines through a reviewed diff; never restore an entire old file blindly.
- Remove copied config keys individually.
- Start a new session and confirm the resulting effective setup.

There is no install receipt, migration database, compatibility alias, or automated uninstall.
