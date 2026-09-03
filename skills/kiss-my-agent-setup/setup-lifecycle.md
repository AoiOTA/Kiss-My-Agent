# Setup lifecycle

Use this reference only for an explicit `setup`, `check`, or `remove` action. The workflow is file-tool native and must not invoke Python, Node.js, a package manager, or another external runtime.

## Scope map

| Scope | Base | Config | Roles directory | Bundled role targets | Instructions |
| --- | --- | --- | --- | --- | --- |
| Project | Explicit target project | `<target>/.codex/config.toml` | `<target>/.codex/agents` | `<roles>/{kiss_explorer,kiss_coder,kiss_reviewer}.toml` | `<target>/AGENTS.md` |
| Global | Explicit Codex home | `$CODEX_HOME/config.toml` | `$CODEX_HOME/agents` | `<roles>/{kiss_explorer,kiss_coder,kiss_reviewer}.toml` | `$CODEX_HOME/AGENTS.md` |

Resolve `$CODEX_HOME` from a non-empty `CODEX_HOME` environment value; otherwise use the current user's `~/.codex`. Resolve and report the absolute path before inspection. Never repurpose or rewrite the environment value.

For an explicit "this project" request, use the Host's current project root or sole active workspace root. Do not substitute the current shell child directory, the Plugin source directory, or a different workspace root. When the Host exposes multiple roots or no unique project root, ask the user to select an absolute target and do not write before that choice.

The current bundled seed sources are the plugin's [kiss_explorer](../../.codex/agents/kiss_explorer.toml), [kiss_coder](../../.codex/agents/kiss_coder.toml), and [kiss_reviewer](../../.codex/agents/kiss_reviewer.toml) files. The Skill-owned known v0.1 snapshots are the role seeds [kiss_explorer](assets/v0.1-agents/kiss_explorer.toml), [kiss_coder](assets/v0.1-agents/kiss_coder.toml), and [kiss_reviewer](assets/v0.1-agents/kiss_reviewer.toml). Current seeds are fresh-setup output templates and remove comparison inputs; known v0.1 seeds are remove-only comparison inputs. The Skill remains plugin-owned; never copy the plugin `skills/` tree into a target.

## Managed content

Only the following config assignments are owned, and only when the same line includes the marker `# KISS My Agent managed`:

```toml
model = "gpt-5.6-sol" # KISS My Agent managed
model_reasoning_effort = "max" # KISS My Agent managed

[features]
multi_agent = true # KISS My Agent managed

[agents]
enabled = true # KISS My Agent managed
```

The owned instructions block is exactly delimited by these markers:

```markdown
<!-- BEGIN KISS MY AGENT MANAGED BLOCK -->
## KISS My Agent

People own the goal, architecture, acceptance criteria, non-goals, and stop boundary. Prioritize the user's goal and requested outcome over visible process. For genuine uncertainty, prefer the smallest safe, low-cost, reversible probe that can be run or tested now over more speculative planning or a new mechanism: exercise the real path, let unexpected failures surface with their causes, then use the observed result to iterate or stop. This never relaxes authorization, permissions, irreversible-action, or high-consequence safety boundaries. Multi-agent work is available by default, but an explicit user instruction or effective configuration that disables it takes precedence. Select dynamically only from the current Host-exposed role catalog; `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` are initial seeds that users may remove, rename, or replace, not a fixed team or workflow. Multiple instances of any role may be used. Coordination is flat by default: the master directly fans out to explorer, coder, reviewer, or other current roles. Only when an independent subsystem needs substantial parallel work and direct aggregation would pollute the master's context may the master temporarily give one existing Agent a bounded department-lead assignment. Within that scope, the lead may delegate to same-role or related-role instances and synthesize their results for the master, but those workers must not delegate again. The assignment disappears when the task ends: at most one intermediate management layer, with no deep nesting, fixed department, new role, fixed headcount, or organization schema. The master owns orchestration, architecture and acceptance decisions, conflict resolution, evidence interpretation, and final synthesis; it must delegate delegable bulk exploration, implementation, validation, and review instead of taking on that routine work itself. A coordinator wait window ending without an update is not an agent timeout or failure; let bounded non-conflicting work continue, and interrupt only when it is obsolete, out of scope, conflicting, or explicitly stopped by the user. If delegation is disabled or unavailable, or no suitable role exists, the master must not silently take over delegated work. Report the staffing issue and ask the user to choose between repairing or enabling a suitable role and explicitly switching this task to ordinary single-conversation execution; only the latter choice authorizes the master to execute the work directly. Keep one operator for each shared resource, preserve unrelated changes, prefer the smallest sufficient change, propagate internal failures, and state evidence only at the level actually reached.
<!-- END KISS MY AGENT MANAGED BLOCK -->
```

## Preflight for every action

Complete the full preflight before the first write or deletion.

1. Resolve the selected base, config, roles directory, instructions, override, three exact bundled role targets, and action-applicable bundled-seed paths. Project setup requires an existing directory. Never turn a project request into global setup.
2. Inspect metadata for those selected paths. Reject a symlinked managed file or directory, a managed path with the wrong file type, or a path whose type cannot be established safely.
3. Stop if `AGENTS.override.md` exists at the selected base. Do not write an ineffective lower-priority `AGENTS.md`.
4. Read the complete current config and instructions plus each existing exact bundled role target. Keep exact before-content for any path that could change. Do not inspect other role files or another scope's roles; the Host owns role precedence and any broader catalog warnings.
5. Parse the selected config and each existing exact bundled role target with the Host's available configuration understanding. If syntax, table shape, assignment ownership, encoding, or bundled role identity is ambiguous, stop without writing instead of repairing by guesswork.
6. Require each existing exact bundled role target to have non-empty string `name`, `description`, and `developer_instructions` fields, and require its `name` to equal the target filename without `.toml`.
7. Stop on any of these selected-scope conflicts:
   - an exact bundled role target has the wrong type, invalid TOML, missing required identity fields, or a `name` different from its filename;
   - the managed block has unequal, duplicate, reversed, or nested markers;
   - a managed config key occurs more than once or has the wrong type: `model` and `model_reasoning_effort` must be non-empty strings, while `features.multi_agent` and `agents.enabled` must be booleans.
8. After the preceding marker-conflict check and before making any setup decision, classify the managed block as exactly one mutually exclusive state: `absent` when neither marker exists; `outdated` when one well-formed block exists but its complete delimited content differs from the current block above; or `current` when that content equals the current block exactly.
9. Read bundled assets only as required by the selected action:
   - `setup`: after classifying the managed block, read and identity-check a current seed only for a missing role that fresh setup may create. Do not read current seeds for existing roles or any known v0.1 seed.
   - `check`: do not read current or known v0.1 role assets. Inspect only the existing exact bundled role targets without version comparison.
   - `remove`: read current and known v0.1 role seeds as exact bytes and verify each parsed identity matches its filename before comparing a corresponding existing role.
10. Immediately before each mutation, re-read every planned target: an already-written target must still equal this operation's exact after-content, while a pending target must still equal its preflight before-content. If any target differs, stop and restore only already-applied KISS changes whose after-content still matches exactly. Remove a directory created by this operation during rollback only when it is still empty.

## Setup

Apply only the following changes:

- Config:
  - Treat the master model/effort pair and both feature values as initial defaults, not enforcement. Setup never resets an existing value during setup or a later plugin update.
  - When both top-level master keys are absent, add the marked pair `model = "gpt-5.6-sol"` and `model_reasoning_effort = "max"` before the first TOML table only when the block state is `absent` or `outdated`. When the block state is `current`, add neither because their absence records intentional user removal.
  - When either top-level master key already exists, in every block state (`absent`, `outdated`, or `current`) preserve each existing master assignment and leave the other key absent as intentional inheritance.
  - If `features.multi_agent` or `agents.enabled` is absent, add the marked `true` assignment to its existing table or append a new table.
  - Preserve any existing value for all four managed config paths and its complete assignment line, whether marked or unmarked. Report a `false` feature value observed in the selected config as `disabled`; never silently replace an existing model or effort. The marker controls remove ownership only, not whether setup may change a value.
  - Preserve comments, unrelated keys, table order, encoding, and the file's newline style when the editing tool supports them. Stop if a safe minimal merge is not possible.
- Instructions:
  - With no managed markers, append one managed block without replacing existing instructions.
  - With one valid managed block, replace only its interior and markers with the current block above.
- Roles:
  - When the managed block was absent at preflight, create each missing bundled role from its exact current plugin seed. This is fresh setup.
  - Preserve every existing correctly identified role byte-for-byte and report it as `user-owned/preserved`, whether it equals a current seed, a known older seed, or neither. Setup and Plugin updates never modify, migrate, version-check, or replace an existing role. Use the existing `configure agents` wizard when the user wants different role model or effort settings.
  - When any well-formed managed block already existed, whether current or outdated, treat missing initial seeds as intentionally absent and do not recreate them.

Before the first setup write, state a separate decision for the master model/effort pair, each feature switch, the Instructions target, every Role, and any directory to create.

Use the smallest file edit available. After all writes, re-read and validate every affected file and each exact bundled role target relevant to the action. If validation fails, preserve the original failure and restore only files still equal to this operation's exact after-content. Preserve a concurrent user change and report that rollback could not safely replace it; report rollback failures without hiding the original cause.

Report `configured` plus `disabled` when applicable, the explicit scope, paths created or changed, preserved roles, and any intentionally absent seeds. A `disabled` report must explain that the executive-only workflow cannot staff delegated work and the master will not silently take it over; ask the user to choose between enabling delegation or suitable roles and explicitly switching the current task to ordinary single-conversation execution. Static setup cannot observe a higher-precedence `false`; if a real new session exposes disabled or unavailable delegation, apply the same staffing rule and choice.

File success is static setup evidence only. It does not prove that the selected Host/account supports the configured model or efforts. Before restarting, the user may directly edit the selected config or role TOML. If the master cannot start, offer the highest-precedence one-launch recovery command `codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'`; after that session starts, edit the persistent config or role TOML and start another new session. Never silently substitute a fallback model or effort.

## Check

`check` is read-only. Run the same selected-path, TOML, marker, and exact bundled-target identity inspection without repairing anything. Do not read role seed assets, compare role content to seeds, infer a role version, or inspect unselected role files. Report each correctly identified existing bundled role as `present user-owned`; report a missing bundled role as `intentionally absent` when a well-formed managed block exists.

Use the same mutually exclusive `absent`, `outdated`, or `current` managed-block classification and report it separately. Define a setup trace as any KISS-marked config assignment, any KISS managed-block marker, or any exact bundled role target with the matching identity.

Report one of:

- `structurally-valid`: both required boolean keys exist, every explicit top-level master setting has a valid type, the managed block is current, and each existing exact bundled role target is valid. Either master key may be intentionally absent for inheritance after setup. Initial seeds may also be intentionally absent after a prior setup.
- `disabled`: the structure is valid but at least one feature value observed in the selected config is explicitly `false`.
- `absent`: no setup trace exists.
- `incomplete`: a setup trace exists but required config or managed-block structure is partial, a required boolean value is missing, or the managed block is well-formed but `outdated`. Role contents and missing roles do not make setup incomplete when identity and catalog structure are valid.
- `conflict`: syntax, ownership, path type, markers, or role identity prevents a safe conclusion.

List the exact inspected paths, each master setting as its explicit value or `inherit`, and the observed feature values. Report only the selected paths' structure; do not claim that the complete Host role catalog is valid. Never claim project trust, active discovery, model or effort support, permissions, plugin publication, or role behavior from `check`.

## Remove

After preflight, prepare all removals before changing anything:

- Remove only the four managed config assignment lines that contain the exact KISS marker. Preserve unmarked values even when they equal the defaults. Do not remove now-empty tables unless their ownership is unambiguous and they were created by this operation, which normal remove cannot establish.
- Remove exactly one valid managed instructions block and its adjacent separator newline; preserve all other instructions.
- Delete a bundled role only when its complete bytes equal either the current bundled seed or the corresponding known v0.1 seed. Preserve every other changed or differently identified role and report it.
- Track directories created by this action. Leave pre-existing directories in place; remove an action-created directory during rollback only when it is still empty.

Re-read all targets after removal. On failure, use the same exact-content rollback rule as setup. Report `removed`, preserved modified roles, and remaining unowned configuration. A later `check` should normally report `absent`; the plugin itself remains installed until the user removes it separately.
