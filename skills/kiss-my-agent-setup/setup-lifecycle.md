# Setup lifecycle

Use this reference only for an explicit `setup`, `check`, or `remove` action. The workflow is file-tool native and must not invoke Python, Node.js, a package manager, or another external runtime.

## Scope map

| Scope | Base | Config | Roles directory | Bundled role targets | Instructions |
| --- | --- | --- | --- | --- | --- |
| Project | Explicit target project | `<target>/.codex/config.toml` | `<target>/.codex/agents` | `<roles>/{kiss_explorer,kiss_coder,kiss_reviewer}.toml` | `<target>/AGENTS.md` |
| Global | Explicit Codex home | `$CODEX_HOME/config.toml` | `$CODEX_HOME/agents` | `<roles>/{kiss_explorer,kiss_coder,kiss_reviewer}.toml` | `$CODEX_HOME/AGENTS.md` |

Resolve `$CODEX_HOME` from a non-empty `CODEX_HOME` environment value; otherwise use the current user's `~/.codex`. Resolve and report the absolute path before inspection. Never repurpose or rewrite the environment value.

For an explicit "this project" request, use the Host's current project root or sole active workspace root. Do not substitute the current shell child directory, the Plugin source directory, or a different workspace root. When the Host exposes multiple roots or no unique project root, ask the user to select an absolute target and do not write before that choice.

The current bundled seed sources are the plugin's [kiss_explorer](../../.codex/agents/kiss_explorer.toml), [kiss_coder](../../.codex/agents/kiss_coder.toml), and [kiss_reviewer](../../.codex/agents/kiss_reviewer.toml) files. The Skill-owned remove-only snapshots are the original v0.2.7 role seeds [kiss_explorer](assets/v0.2.7-agents/kiss_explorer.toml), [kiss_coder](assets/v0.2.7-agents/kiss_coder.toml), and [kiss_reviewer](assets/v0.2.7-agents/kiss_reviewer.toml), the v0.2.6 role seeds [kiss_explorer](assets/v0.2.6-agents/kiss_explorer.toml), [kiss_coder](assets/v0.2.6-agents/kiss_coder.toml), and [kiss_reviewer](assets/v0.2.6-agents/kiss_reviewer.toml), the v0.2.5 role seeds [kiss_explorer](assets/v0.2.5-agents/kiss_explorer.toml), [kiss_coder](assets/v0.2.5-agents/kiss_coder.toml), and [kiss_reviewer](assets/v0.2.5-agents/kiss_reviewer.toml), plus the v0.1 role seeds [kiss_explorer](assets/v0.1-agents/kiss_explorer.toml), [kiss_coder](assets/v0.1-agents/kiss_coder.toml), and [kiss_reviewer](assets/v0.1-agents/kiss_reviewer.toml). Current seeds are fresh-setup output templates and remove comparison inputs. Historical snapshots are exact-byte remove comparison inputs only: setup, check, and configure must not read them, compare against them, infer a version from them, or migrate an existing role. The Skill remains plugin-owned; never copy the plugin `skills/` tree into a target.

## Managed content

Only the following current config assignments are owned, and only when the same line includes the marker `# KISS My Agent managed`:

```toml
model = "gpt-6-astra" # KISS My Agent managed
model_reasoning_effort = "high" # KISS My Agent managed

[features]
multi_agent = true # KISS My Agent managed

[features.context_management]
experimental_mode = true # KISS My Agent managed

[agents]
enabled = true # KISS My Agent managed
```

Setup supplies missing top-level `model` and `model_reasoning_effort` defaults independently as `gpt-6-astra` and `high`. Existing explicit values are preserved except for the complete exact legacy pair below. The Host still resolves the runtime-effective model and effort from its active configuration layers and conversation selection; static defaults do not prove support or loading.

For compatibility with v0.2.5 setup output, recognize this legacy pair only when both top-level assignments occur exactly once, their parsed values are exactly `gpt-5.6-sol` and `max`, and each complete assignment line includes the exact marker `# KISS My Agent managed`:

```text
model = "gpt-5.6-sol" # KISS My Agent managed
model_reasoning_effort = "max" # KISS My Agent managed
```

Setup updates that exact legacy pair together to the marked Astra/high defaults. A missing member, an unmarked line, or a changed value makes the existing master settings user-owned and preserved; fill only genuinely missing fields with the current marked defaults. Report each preserved explicit value. Duplicate assignments, ambiguous ownership, or invalid TOML remain a conflict. Remove also recognizes and deletes the complete exact legacy pair, but never deletes an unmarked or changed master setting.

The owned instructions block is exactly delimited by these markers:

```markdown
<!-- BEGIN KISS MY AGENT MANAGED BLOCK -->
## KISS My Agent

KMA is a minimalist research-engineering decision layer. People own the goal, architecture, acceptance, non-goals, and stop boundary. Turn the goal and hypothesis into the smallest sufficient implementation or reversible probe, run the real path, expose success or failure, then iterate or stop. Preserve authorization and safety boundaries. Do not build for imagined consumers, conceal failures with fallback or retry, equate test success with research success, or add process for its own sake.

Each agent reads `$kiss-my-agent:kiss-my-agent` once at the start of KMA work and applies it throughout implementation, debugging, experiments, delegation, and result interpretation. Reuse loaded guidance; reread only for an update or missing detail. Do not wait for a user reminder or add tool-by-tool checks. The master retains all unfinished authorized outcomes; each worker retains its assigned deliverable through execution, observation, and routine recovery. A pending install, run, or agent blocks only its dependents. Advance useful independent work while it runs; after a prerequisite repair, return to the blocked outcome within actual user budgets and resource limits.

The master owns orchestration, architecture, acceptance, conflict resolution, and evidence interpretation. The master may directly complete clear small or local work. Actively delegate substantial bulk work, independent parallel work, or work needing another perspective when the benefit outweighs coordination cost. Choose task partitioning from the deliverables and required expertise before selecting agents. Reuse an agent's specific relevant reasoning or implementation context; sharing a repository or being idle is not enough. Start fresh when the domain changes and prior context no longer helps. Match current Host role authority to the actions and give each shared resource one operator. Use owner findings unless a conflict or material evidence gap requires checking. A coordinator wait window ending without an update is not an agent timeout or failure.

Multi-agent work is available by default; explicit user or effective configuration opt-outs take precedence. Use only current Host roles; shipped names are mutable seeds. Each role may have zero, one, or multiple instances, with no fixed team or sequence. Coordination is flat by default. Only when an independent subsystem needs substantial parallel work and direct aggregation would pollute the master's context may it receive a bounded department-lead assignment; its workers must not delegate again. Keep at most one intermediate management layer and no deep nesting; the assignment ends with the task. If delegation is unavailable, continue authorized work within capability without a staffing approval step; report unmet explicit role or independence requirements and real capability gaps.

Preserve unrelated changes, keep fixes in the active owner, observe asynchronous and subprocess failures with their causes, and state evidence only at the level reached. Do not turn this guidance into product mechanisms, gates, or telemetry.
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
   - any required boolean config key occurs more than once or has the wrong type: `features.multi_agent`, `agents.enabled`, and `features.context_management.experimental_mode` must be booleans;
   - a top-level `model` or `model_reasoning_effort` assignment is duplicated or has ambiguous ownership. Any other syntactically valid value is preserved as Host configuration without KISS schema or availability validation.
8. After the preceding marker-conflict check and before making any setup decision, classify the managed block as exactly one mutually exclusive state: `absent` when neither marker exists; `outdated` when one well-formed block exists but its complete delimited content differs from the current block above; or `current` when that content equals the current block exactly.
9. Read bundled assets only as required by the selected action:
   - `setup`: after classifying the managed block, read and identity-check a current seed only for a missing role that fresh setup may create. Do not read current seeds for existing roles or any historical snapshot.
   - `check`: do not read current seeds or historical role snapshots. Inspect only the existing exact bundled role targets without version comparison.
   - `remove`: read the current, v0.2.7, v0.2.6, v0.2.5, and v0.1 role seeds as exact bytes and verify each parsed identity matches its filename before comparing a corresponding existing role.
10. Immediately before each mutation, re-read every planned target: an already-written target must still equal this operation's exact after-content, while a pending target must still equal its preflight before-content. If any target differs, stop and restore only already-applied KISS changes whose after-content still matches exactly. Remove a directory created by this operation during rollback only when it is still empty.

## Setup

Apply only the following changes:

- Config:
  - Fill each missing top-level master field independently: `model = "gpt-6-astra"` and `model_reasoning_effort = "high"`, each with the exact KISS marker. Both fields must be present for setup completion, but no particular existing value is required. This applies to fresh setup and upgrades, independently of managed-block state.
  - Update the exact marked legacy Sol/max pair together to the marked Astra/high defaults only when preflight classified both top-level assignments as that pair. Repeated setup preserves the resulting defaults.
  - Preserve every existing partial, unmarked, or changed master setting exactly and report its explicit value. Fill only missing fields; do not normalize or silently substitute an existing model or effort.
  - If `features.multi_agent`, `agents.enabled`, or `features.context_management.experimental_mode` is absent, add the marked `true` assignment to its existing table or append a new table. Preserve valid table structure without duplicate tables or keys.
  - Preserve any existing value for all three boolean paths and its complete assignment line, whether marked or unmarked. Report `disabled` only when `features.multi_agent` or `agents.enabled` is `false`. Report `features.context_management.experimental_mode` separately as configured `true` or user-disabled `false`; context opt-out does not disable delegation. The marker controls remove ownership only, not whether setup may change a value.
  - Preserve comments, unrelated keys, table order, encoding, and the file's newline style when the editing tool supports them. Stop if a safe minimal merge is not possible.
- Instructions:
  - With no managed markers, append one managed block without replacing existing instructions.
  - With one valid managed block, replace only its interior and markers with the current block above.
- Roles:
  - When the managed block was absent at preflight, create each missing bundled role from its exact current plugin seed. This is fresh setup.
  - Preserve every existing correctly identified role byte-for-byte and report it as `user-owned/preserved`, whether it equals a current seed, a known older seed, or neither. Setup and Plugin updates never modify, migrate, version-check, or replace an existing role. Use the existing `configure agents` wizard when the user wants different role model or effort settings.
  - When any well-formed managed block already existed, whether current or outdated, treat missing initial seeds as intentionally absent and do not recreate them.

Before the first setup write, state a separate decision for each master field or the exact legacy pair, each delegation switch and the context setting, the Instructions target, every Role, and any directory to create.

Use the smallest file edit available. After all writes, re-read and validate every affected file and each exact bundled role target relevant to the action. If validation fails, preserve the original failure and restore only files still equal to this operation's exact after-content. Preserve a concurrent user change and report that rollback could not safely replace it; report rollback failures without hiding the original cause.

Report `configured` plus `disabled` when applicable, the explicit scope, paths created or changed, preserved roles, and any intentionally absent seeds. A `disabled` report describes unavailable delegation, not a prohibition on authorized direct work. Report unmet explicit role or independence requirements and real capability gaps. Static setup cannot observe a higher-precedence `false`; if a real new session exposes disabled or unavailable delegation, apply the same distinction.

File success is static setup evidence only. It does not prove the runtime-effective Host configuration, conversation selection, role discovery, model, or effort. Project setup does not change the user's global config. Start a new trusted project task or new global-scope session for discovery and experimental context loading; the context flag alone is not runtime evidence. Before restarting, the user may directly edit the selected config or role TOML. If the master cannot start, offer the highest-precedence one-launch recovery command `codex --config 'model="HOST_SUPPORTED_MODEL_ID"' --config 'model_reasoning_effort="HOST_SUPPORTED_EFFORT"'`; after that session starts, edit the owning persistent Host configuration and start another new session. Never silently substitute a fallback model or effort.

## Check

`check` is read-only. Run the same selected-path, TOML, marker, and exact bundled-target identity inspection without repairing anything. Do not read role seed assets, compare role content to seeds, infer a role version, or inspect unselected role files. Report each correctly identified existing bundled role as `present user-owned`; report a missing bundled role as `intentionally absent` when a well-formed managed block exists.

Use the same mutually exclusive `absent`, `outdated`, or `current` managed-block classification and report it separately. Define a setup trace as any KISS-marked config assignment, any KISS managed-block marker, or any exact bundled role target with the matching identity.

Report one of:

- `structurally-valid`: both top-level master fields and all three required boolean keys exist, the managed block is current, and each existing exact bundled role target is valid. Existing master values do not affect completion after safe TOML and ownership classification; the Host resolves those settings. Initial seeds may also be intentionally absent after a prior setup.
- `disabled`: the structure is valid but `features.multi_agent` or `agents.enabled` observed in the selected config is explicitly `false`. A context value of `false` alone does not produce this status.
- `absent`: no setup trace exists.
- `incomplete`: a setup trace exists but required config or managed-block structure is partial, a required master field or boolean value is missing, or the managed block is well-formed but `outdated`. Role contents and missing roles do not make setup incomplete when identity and catalog structure are valid.
- `conflict`: syntax, ownership, path type, markers, or role identity prevents a safe conclusion.

List the exact inspected paths, each master setting as its explicit value or `inherit`, whether an exact legacy pair is eligible for the Astra/high update, and the observed delegation values. Report context separately as configured `true`, user-disabled `false`, or missing; missing is incomplete when a setup trace exists. Preserved partial, unmarked, or changed master settings remain user-owned; setup only fills missing fields. Report only the selected paths' structure; do not claim that the complete Host role catalog is valid. Never claim project trust, active discovery, runtime-effective Host layers, model or effort support, permissions, plugin publication, or role behavior from `check`.

## Remove

After preflight, prepare all removals before changing anything:

- Remove each current default assignment independently only when its parsed value exactly matches the current default above and its complete line contains the exact KISS marker: Astra model, high effort, and the three `true` boolean values. Also remove the complete exact legacy master pair when both marked lines satisfy its compatibility classification. Preserve changed or unmarked values and partial legacy settings; a current Astra or high field with its own marker remains independently removable. Preserve the context table and all unrelated keys and comments. Do not remove now-empty tables unless their ownership is unambiguous and they were created by this operation, which normal remove cannot establish.
- Remove exactly one valid managed instructions block and its adjacent separator newline; preserve all other instructions.
- Delete a bundled role only when its complete bytes equal the current bundled seed or the corresponding exact v0.2.7, v0.2.6, v0.2.5, or v0.1 remove-only snapshot. Preserve every other changed or differently identified role and report it.
- Track directories created by this action. Leave pre-existing directories in place; remove an action-created directory during rollback only when it is still empty.

Re-read all targets after removal. On failure, use the same exact-content rollback rule as setup. Report `removed`, preserved modified roles, and remaining unowned configuration. A later `check` should normally report `absent`; the plugin itself remains installed until the user removes it separately.
