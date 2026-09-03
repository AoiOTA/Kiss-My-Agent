---
name: kiss-my-agent-setup
description: Explicitly set up, inspect, configure existing KISS My Agent roles, or remove KISS My Agent Codex configuration for one project or one Codex home. Use only for a user-requested setup, check, configure, or remove action. Static checks do not prove live Codex loading.
---

# KISS My Agent Setup

Use Codex's existing file inspection and editing tools. Do not require Python, Node.js, a package manager, or a bundled executable for setup operations.

The exact loaded `SKILL.md` directory is the single base for sibling `setup-lifecycle.md` and `configure-agents.md` and every relative link they contain; preserve linked relative-path text and never reconstruct cache, marketplace, plugin, or version path components. Run lifecycle filesystem operations serially: perform one simple direct file operation per tool call, and make exactly one such operation in each outer tool or orchestration call; do not batch or parallelize them; do not generate compound shell commands or suppress diagnostics. For text mutations, use one planned target per edit call and exactly one edit operation for that path; update an existing file in place, and never combine add, delete, or update operations for the same path. The lifecycle's byte-preserving migration and rollback copies are exempt from text-editing rules; each native copy must use one resolved source, one planned existing target, operands safely quoted for the active shell, no permission or attribute override, and exactly one operation in its own call. Follow the lifecycle's failed-copy handling and apply its exact-current rollback guard independently to each successfully migrated role. Inspect and interpret each tool or subprocess status. A tool or subprocess failure or an unexpected nonzero status stops forward work. If no target has been mutated, return immediately. If the action has already mutated targets, perform only the selected reference's guarded rollback or cleanup before returning and reporting the original failure plus any rollback failure. An expected absence or no-match is not a failure, but explicitly interpret and report it; never suppress it.

1. Identify the exact action and scope before changing anything. Project scope may be inferred only from an explicit phrase such as "this project" and must resolve to the Host's current unique project or active workspace root, not an arbitrary child working directory. Show the absolute target before writing; ask when multiple roots exist or the target is not unique. Global scope must always be explicit.
2. Read exactly one matching reference:
   - For project/global `setup`, `check`, or `remove`, read [setup-lifecycle.md](setup-lifecycle.md).
   - For the optional wizard that configures existing agents, read [configure-agents.md](configure-agents.md).
3. Inspect every affected file before writing. Preserve unrelated settings, instructions, roles, and user changes. Stop on ambiguous ownership or a state the selected reference does not safely cover.
4. Do not install or uninstall the plugin itself, establish project trust, restart Codex, or claim that the current session hot-loaded changed files.
5. After a successful mutation, re-read the affected files, report the exact scope and paths changed, and tell the user to start a new Codex session before testing discovery or behavior.
