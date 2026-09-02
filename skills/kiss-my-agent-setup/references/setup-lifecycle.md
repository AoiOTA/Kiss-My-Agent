# Setup lifecycle

Use this reference only for an explicit `setup`, `check`, or `remove` action. The workflow is file-tool native and must not invoke Python, Node.js, a package manager, or another external runtime.

## Scope map

| Scope | Base | Config | Roles | Instructions | Opposite role catalog |
| --- | --- | --- | --- | --- | --- |
| Project | Explicit target project | `<target>/.codex/config.toml` | `<target>/.codex/agents/*.toml` | `<target>/AGENTS.md` | `$CODEX_HOME/agents/*.toml` |
| Global | Explicit Codex home | `$CODEX_HOME/config.toml` | `$CODEX_HOME/agents/*.toml` | `$CODEX_HOME/AGENTS.md` | Current project `.codex/agents/*.toml`, when a project is active |

Resolve `$CODEX_HOME` from a non-empty `CODEX_HOME` environment value; otherwise use the current user's `~/.codex`. Resolve and report the absolute path before inspection. Never repurpose or rewrite the environment value.

For an explicit "this project" request, use the Host's current project root or sole active workspace root. Do not substitute the current shell child directory, the Plugin source directory, or a different workspace root. When the Host exposes multiple roots or no unique project root, ask the user to select an absolute target and do not write before that choice.

The bundled seed sources are the plugin's [kiss_explorer](../../../.codex/agents/kiss_explorer.toml), [kiss_coder](../../../.codex/agents/kiss_coder.toml), and [kiss_reviewer](../../../.codex/agents/kiss_reviewer.toml) files. The Skill remains plugin-owned; never copy the plugin `skills/` tree into a target.

## Managed content

Only the following config assignments are owned, and only when the same line includes the marker `# KISS My Agent managed`:

```toml
[features]
multi_agent = true # KISS My Agent managed

[agents]
enabled = true # KISS My Agent managed
```

The owned instructions block is exactly delimited by these markers:

```markdown
<!-- BEGIN KISS MY AGENT MANAGED BLOCK -->
## KISS My Agent

People own the goal, architecture, acceptance criteria, non-goals, and stop boundary. Multi-agent work is available by default, but an explicit user instruction or effective configuration that disables it takes precedence. Select dynamically only from the current Host-exposed role catalog; `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` are initial seeds that users may remove, rename, or replace, not a fixed team or workflow. Keep one operator for each shared resource, preserve unrelated changes, prefer the smallest sufficient change, propagate internal failures, and state evidence only at the level actually reached.
<!-- END KISS MY AGENT MANAGED BLOCK -->
```

## Preflight for every action

Complete the full preflight before the first write or deletion.

1. Resolve the selected base, config, roles, instructions, override, bundled seed, and opposite-catalog paths. Project setup requires an existing directory. Never turn a project request into global setup.
2. Inspect path metadata. Reject a symlinked managed file or directory, a managed path with the wrong file type, or a path whose type cannot be established safely.
3. Stop if `AGENTS.override.md` exists at the selected base. Do not write an ineffective lower-priority `AGENTS.md`.
4. Read the complete current config, instructions, every role TOML in the selected catalog, every bundled seed, and the opposite catalog. Keep exact before-content for any path that could change.
5. Parse TOML with the Host's available configuration understanding. If syntax, table shape, assignment ownership, encoding, or role identity is ambiguous, stop without writing instead of repairing by guesswork.
6. Require every role TOML to have non-empty string `name`, `description`, and `developer_instructions` fields and a unique `name` in its catalog.
7. Stop on any of these selected-scope conflicts:
   - a bundled filename exists with a different `name`;
   - another filename in the same catalog declares a bundled seed name;
   - the managed block has unequal, duplicate, reversed, or nested markers;
   - a managed config key occurs more than once or has a non-boolean value.
8. For `setup` and `check`, also stop when a bundled seed name appears in both project and global catalogs. Do not apply this cross-scope rejection to `remove`: removing one selected scope is the recovery path for that conflict, while every selected-scope path and identity check still applies.
9. Compute the complete proposed change set and the directories that would be created before writing. Immediately before each write, re-read every planned target: an already-written target must still equal this operation's exact after-content, while a pending target must still equal its preflight before-content. If any target differs, stop and restore only already-applied KISS changes whose after-content still matches exactly. Remove a directory created by this operation during rollback only when it is still empty.

## Setup

Apply only the following changes:

- Config:
  - If `features.multi_agent` or `agents.enabled` is absent, add the marked `true` assignment to its existing table or append a new table.
  - Preserve any existing boolean value and its complete assignment line, whether marked or unmarked. Report a `false` observed in the selected config as `disabled`; never silently enable it or claim that a static file check resolved every runtime layer. The marker controls remove ownership only, not whether setup may change a value.
  - Preserve comments, unrelated keys, table order, encoding, and the file's newline style when the editing tool supports them. Stop if a safe minimal merge is not possible.
- Instructions:
  - With no managed markers, append one managed block without replacing existing instructions.
  - With one valid managed block, replace only its interior and markers with the current block above.
- Roles:
  - When the managed block did not exist at preflight, create each missing bundled seed from its exact plugin source.
  - Preserve an existing correctly identified role, including user edits.
  - When the managed block already existed, treat missing initial seeds as intentionally removed and do not recreate them.

Use the smallest file edit available. After all writes, re-read and validate every affected file and the complete role catalog. If validation fails, restore only files still equal to this operation's after-content. Preserve a concurrent user change and report that rollback could not safely replace it.

Report `configured` plus `disabled` when applicable, the explicit scope, paths created or changed, preserved roles, and any intentionally absent seeds. File success is static setup evidence only.

## Check

`check` is read-only. Run the same path, TOML, marker, role-identity, and cross-scope conflict inspection without repairing anything.

Classify the managed block separately as `current`, `outdated`, or `absent`. A block is `current` only when the complete delimited content equals the current block above. Define a setup trace as any KISS-marked config assignment, any KISS managed-block marker, or any role declaring a bundled seed identity.

Report one of:

- `structurally-valid`: both required boolean keys exist, the managed block is valid, and role catalogs have no relevant conflict. Initial seeds may be intentionally absent after a prior setup.
- `disabled`: the structure is valid but at least one feature value observed in the selected config is explicitly `false`.
- `absent`: no setup trace exists.
- `incomplete`: a setup trace exists but required structure is partial, a required value is missing, or the managed block is well-formed but `outdated`.
- `conflict`: syntax, ownership, path type, markers, or role identity prevents a safe conclusion.

List the exact inspected paths and observed feature values. Never claim project trust, active discovery, permissions, plugin publication, or role behavior from `check`.

## Remove

After preflight, prepare all removals before changing anything:

- Remove only the two config assignment lines that contain the exact KISS marker. Preserve unmarked values even when they equal the defaults. Do not remove now-empty tables unless their ownership is unambiguous and they were created by this operation, which normal remove cannot establish.
- Remove exactly one valid managed instructions block and its adjacent separator newline; preserve all other instructions.
- Delete a bundled role only when its complete bytes still equal the current bundled seed. Preserve every changed or differently identified role and report it.
- Track directories created by this action. Leave pre-existing directories in place; remove an action-created directory during rollback only when it is still empty.

Re-read all targets after removal. On failure, use the same exact-content rollback rule as setup. Report `removed`, preserved modified roles, and remaining unowned configuration. A later `check` should normally report `absent`; the plugin itself remains installed until the user removes it separately.
