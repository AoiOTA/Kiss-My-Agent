# Configure existing agents

Use this reference only after the user explicitly asks to configure existing Agents or make selected roles follow the Master. This is a Codex conversation, not a separate terminal program, and it must not require Python, Node.js, or another external runtime.

## Boundary

- Require an explicit project or global scope. Never infer global configuration.
- Configure only existing standalone role TOML files in the selected scope. Do not create, delete, rename, copy, or restore roles.
- Ordinary role configuration edits only `model`, `model_reasoning_effort`, and `sandbox_mode`. The explicit `follow master` mode additionally removes selected-scope config overrides as described below. Preserve `name`, `description`, `developer_instructions`, comments, and every unrelated key.
- A project or global wizard may include user-added roles. It is not limited to the three bundled seeds.

## Scope map

| Scope | Role directory |
| --- | --- |
| Project | `<unique Host project or active workspace root>/.codex/agents` |
| Global | `<resolved Codex home>/agents` |

For project scope, use the Host's unique current project root or sole active workspace root, not the shell's current child directory. If the Host exposes multiple roots or no unique root, ask the user to choose an absolute project target and do not write before that choice.

For global scope, resolve the Codex home from a non-empty `CODEX_HOME` environment value; otherwise use the current user's `~/.codex`. Never repurpose or rewrite the environment value. Resolve and show the absolute role-directory path before inspecting or asking which roles to configure.

## Inspect

1. Resolve the selected role directory and inspect its metadata. Reject a symlinked directory or a directory whose type cannot be established safely.
2. If the user explicitly named one or more roles or paths, resolve only those targets. A bare role name maps to `<role-directory>/<name>.toml`; a supplied path must resolve to a direct `.toml` child of the selected role directory. Reject traversal, a symlinked target, a duplicate target, a missing target, or a non-regular file. Do not list, read, or parse unselected role files.
3. If the user did not name a role, list only the direct `.toml` paths in the selected role directory without reading or parsing their contents. Show those paths and ask which one or more to configure. If none exist, stop and explain that setup or a manual role definition is needed first. Do not select every role by default.
4. After the targets are selected, read and parse only those files. Stop if a selected file has invalid TOML or a missing or empty string `name`, `description`, or `developer_instructions` field. An invalid or duplicate identity in an unselected role does not block this operation; the Host owns broader catalog validation and warnings.
5. Require selected `model`, `model_reasoning_effort`, and `sandbox_mode` values to be non-empty strings; require `sandbox_mode`, when present, to be `read-only`, `workspace-write`, or `danger-full-access`. Do not normalize an invalid value by guesswork.
6. If a selected role has `default_permissions`, do not add `sandbox_mode`; those settings cannot be combined. If it has `sandbox_workspace_write`, do not change away from `workspace-write` without a separate manual edit that owns the related table.
7. Show a compact table for the selected roles with identity, path, and current values. Label omitted fields as `inherit`.

## Ask for settings

For each selected role, offer `keep current`, `inherit`, or `set explicitly`:

When multiple roles are selected, the user may apply one shared choice to all of them. `inherit` removes the selected key; an explicit model or effort interrupts that field's inheritance. Preview every affected file separately before writing. Do not maintain fixed model or effort defaults.

- `model`
  - `inherit` removes the key. Codex first resolves an explicit spawn model, then `agents.default_subagent_model`, then the parent's model.
  - An explicit value must be the exact model identifier chosen by the user from the current Host. Do not maintain a hard-coded model catalog or claim availability that the current Host did not expose.
- `model_reasoning_effort`
  - `inherit` removes the key. Codex first resolves an explicit spawn effort, then `agents.default_subagent_reasoning_effort`, then the parent's effort. If an explicit spawn or `[agents]` default selects a model but neither source specifies effort, Codex instead uses that model's default effort. A role file that overrides only `model` preserves the effort resolved before applying the role file; it does not recompute effort from the role model.
  - Offer only values exposed or documented for the user's current Host and selected model. If support cannot be verified, request an exact value and disclose that a new-session load is the real validation.
- `sandbox_mode`
  - Offer `inherit`, `read-only`, `workspace-write`, and `danger-full-access`.
  - `inherit` removes the key.
  - Require a separate explicit confirmation immediately before writing `danger-full-access`.

Explain precedence before confirmation. Codex first resolves each model or effort field from an explicit spawn value, then the corresponding `[agents]` default, then the parent. If an explicit spawn or `[agents]` default selects a model without an effort from either source, that model's default effort is used. Codex then applies an explicit `model` or `model_reasoning_effort` from the custom-Agent role file as the final role override; a role-only model override keeps the already-resolved effort. Separately, the child inherits the parent's current sandbox policy, and Codex reapplies the parent turn's live sandbox and approval overrides when spawning it; administrator requirements can further constrain permissions. A role file supplies defaults and overrides inside those live boundaries, never a permission grant.

## Follow Master in the selected scope

For an explicit request to make selected roles `follow master`, remove both `model` and `model_reasoning_effort` from those existing role files. Preserve sandbox settings and every other field. Never read historical seed snapshots or infer ownership from role similarity.

Also inspect the selected scope's config (`<project>/.codex/config.toml` or `<resolved Codex home>/config.toml`). Reject symlinks, unsafe types, invalid TOML, duplicate keys, or ambiguous tables before any write. If absent, report absence and do not create it. Read only this selected config; do not mutate another scope or a profile. Preview removal of `agents.default_subagent_model` and `agents.default_subagent_reasoning_effort` when present, because they would otherwise block following the Master for all children in that scope. Explain this wider impact in the displayed diff. Remove them only under the user's authorization for the displayed selected-scope change. Unselected role overrides and higher-precedence Host layers may still block inheritance; report that limitation without claiming runtime success.

Top-level Master settings are a separate optional selection, never removed merely because roles were selected. When the user explicitly selects removal of legacy KMA Master pins, remove only exact owned assignments: `model = "gpt-6-astra"` or `model_reasoning_effort = "high"` independently, with the exact `# KISS My Agent managed` marker on the same complete line; or the complete once-only marked `gpt-5.6-sol` / `max` pair. Preserve an unmarked, changed, or partial legacy pair and all user-selected Master values. Do not replace these fields with another fixed model. Show any preserved value and explain that the Host/session choice remains authoritative at its effective precedence.

The default delegation call omits model and effort overrides. Newly spawned roles then follow the current Master's effective settings when no role, spawn, or `[agents]` override intervenes. Do not automatically lower effort. A setting change does not live-update an existing child: let its active operation finish, consume its result, and use a new child for subsequent work if the old child's settings differ. New model IDs need no KMA catalog update. Unsupported Host combinations are reported, without fallback or effort downgrade.

## Preview, write, and verify

1. Build the complete proposed diff for only the selected role files and any explicitly selected config changes and show it before mutation.
2. If the user already authorized the exact selected scope, roles and fields, proceed with the displayed changes without another confirmation. Otherwise obtain authorization for the missing selection before writing. Removal of `[agents]` defaults requires explicit selected-scope authorization because it also affects other children. The separate full-access confirmation remains mandatory when applicable.
3. Immediately before mutating each selected file, re-read every planned target: pending files must still equal their preview base and already-written files must still equal this operation's exact after-content. If a pending target differs, or an already-written target changed, preserve that concurrent-change cause, stop forward work, and restore only already-written files that still equal this operation's exact after-content. Never overwrite a concurrent change during rollback.
4. Apply the minimal edit to that file, then re-read and parse it. For a role, confirm required identity and instruction fields are unchanged; for config, confirm all non-selected fields are unchanged. Confirm only the selected settings changed before continuing to the next selected file.
5. If a write or verification fails, preserve the original failure and use the same exact-after-content guarded rollback for already-written files.

Report the exact roles and fields changed, inherited fields removed, preserved fields, scope, and paths. Tell the user to start a new Codex session. Do not claim the configured model exists, the role was discovered, or the requested permission became effective until the new session demonstrates it.
