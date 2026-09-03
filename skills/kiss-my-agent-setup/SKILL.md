---
name: kiss-my-agent-setup
description: Explicitly set up, inspect, configure existing KISS My Agent roles, or remove KISS My Agent Codex configuration for one project or one Codex home. Use only for a user-requested setup, check, configure, or remove action. Static checks do not prove live Codex loading.
---

# KISS My Agent Setup

Use Codex's existing file inspection and editing tools. Do not require Python, Node.js, a package manager, or a bundled executable for setup operations.

Use the exact loaded `SKILL.md` directory as the tool workdir for every sibling reference, linked seed, or asset operation. Preserve each linked relative-path text as its path operand, resolve and verify it from that workdir, and never reconstruct cache, marketplace, plugin, or version path components.

Run lifecycle mutations serially, with one planned target and one simple direct file operation per tool call. Do not batch mutations, run them in parallel, generate compound shell commands, or suppress diagnostics. Inspect every tool or subprocess status; an unexpected failure stops forward work. If nothing changed, return immediately. Otherwise perform only the selected reference's exact-after-content guarded rollback or cleanup, preserve the original failure, and report any rollback failure too. An expected absence or no-match is not a failure, but report it explicitly.

1. Identify the exact action and scope before changing anything. Project scope may be inferred only from an explicit phrase such as "this project" and must resolve to the Host's current unique project or active workspace root, not an arbitrary child working directory. Show the absolute target before writing; ask when multiple roots exist or the target is not unique. Global scope must always be explicit.
2. Read exactly one matching reference:
   - For project/global `setup`, `check`, or `remove`, read [setup-lifecycle.md](setup-lifecycle.md).
   - For the optional wizard that configures existing agents, read [configure-agents.md](configure-agents.md).
3. Inspect every affected file before writing. Preserve unrelated settings, instructions, roles, and user changes. Stop on ambiguous ownership or a state the selected reference does not safely cover.
4. Do not install or uninstall the plugin itself, establish project trust, restart Codex, or claim that the current session hot-loaded changed files.
5. After a successful mutation, re-read the affected files, report the exact scope and paths changed, and tell the user to start a new Codex session before testing discovery or behavior.
