---
name: kiss-my-agent-setup
description: Explicitly set up, inspect, or remove KISS My Agent Codex configuration, managed AGENTS.md guidance, and bundled role files for one project or a Codex home. Use only when the user asks to install, configure, check, or remove the KISS My Agent multi-agent setup. The check command is static and does not prove live Codex loading.
---

# KISS My Agent Setup

Run the bundled script only after the user explicitly asks to change or inspect setup state. The skill itself is loaded from the plugin and is never copied into the target.

```bash
python3 scripts/setup.py setup --scope project --target /path/to/project
python3 scripts/setup.py check --scope project --target /path/to/project
python3 scripts/setup.py remove --scope project --target /path/to/project
```

Use `--scope global` to manage `config.toml`, `AGENTS.md`, and `agents/` under the selected Codex home. `--codex-home` selects an explicit Codex home and also supplies the opposite-scope collision check for project setup. `--target` defaults to the current directory; `--codex-home` defaults to `CODEX_HOME` or `~/.codex`.

`setup` preserves existing `false` feature values and reports a prominent `disabled` status. `check` performs only static file and catalog inspection: it does not invoke Codex or claim that a running process loaded the configuration. It exits nonzero with `absent` for a never-configured target and with `incomplete` for partial managed artifacts. A current managed block remains structurally valid when users delete any initial seed roles; explicit `false` values report `disabled` without making the installed structure invalid. `remove` removes only the managed AGENTS block, marked configuration keys, and unchanged bundled roles; it reports modified roles that it preserves.

All commands reject an applicable `AGENTS.override.md`, symlinked managed paths, malformed TOML, unsupported config shapes, role-name collisions, and duplicate bundled role names across project and global catalogs. A failed setup or removal rolls back its own completed file changes.
