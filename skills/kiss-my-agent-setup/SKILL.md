---
name: kiss-my-agent-setup
description: Explicitly set up, inspect, configure existing KISS My Agent roles, or remove KISS My Agent Codex configuration for one project or one Codex home. Use only for a user-requested setup, check, configure, or remove action. Static checks do not prove live Codex loading.
---

# KISS My Agent Setup

Use Codex's existing file inspection and editing tools. Do not require Python, Node.js, a package manager, or a bundled executable for setup operations.

Operational discipline: preserve linked relative-path text and perform each resource operation from the directory of the file containing its link, or reuse an already resolved exact path unchanged; never repeatedly transcribe, rebase, reconstruct, or infer cache, marketplace, plugin, or version path components. Run lifecycle filesystem operations serially: perform one simple direct file operation per tool call, and make exactly one such operation in each outer tool or orchestration call; do not batch or parallelize them; do not generate compound shell commands or suppress diagnostics. Inspect and interpret each tool or subprocess status. Stop after a tool or subprocess failure or an unexpected nonzero status, before any further operation or mutation. An expected absence or no-match is not a failure, but explicitly interpret and report it; never suppress it.

1. Identify the exact action and scope before changing anything. Project scope may be inferred only from an explicit phrase such as "this project" and must resolve to the Host's current unique project or active workspace root, not an arbitrary child working directory. Show the absolute target before writing; ask when multiple roots exist or the target is not unique. Global scope must always be explicit.
2. Read exactly one matching reference:
   - For project/global `setup`, `check`, or `remove`, read [references/setup-lifecycle.md](references/setup-lifecycle.md).
   - For the optional wizard that configures existing agents, read [references/configure-agents.md](references/configure-agents.md).
3. Inspect every affected file before writing. Preserve unrelated settings, instructions, roles, and user changes. Stop on ambiguous ownership or a state the selected reference does not safely cover.
4. Do not install or uninstall the plugin itself, establish project trust, restart Codex, or claim that the current session hot-loaded changed files.
5. After a successful mutation, re-read the affected files, report the exact scope and paths changed, and tell the user to start a new Codex session before testing discovery or behavior.
