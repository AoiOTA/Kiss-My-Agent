# Configure existing agents

Use this reference only after the user explicitly asks for the Agent configuration wizard. This is a Codex conversation, not a separate terminal program, and it must not require Python, Node.js, or another external runtime.

## Boundary

- Require an explicit project or global scope. Never infer global configuration.
- Configure only existing standalone role TOML files in the selected scope. Do not create, delete, rename, copy, or restore roles.
- Edit only `model`, `model_reasoning_effort`, and `sandbox_mode`. Preserve `name`, `description`, `developer_instructions`, comments, and every unrelated key.
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

## Preview, write, and verify

1. Build the complete proposed diff for only the selected files and show it before mutation.
2. Ask once for confirmation of the displayed non-dangerous changes. The separate full-access confirmation remains mandatory when applicable.
3. Immediately before mutating each selected file, re-read that file and require it to still equal its preview base. If a pending target differs, preserve that concurrent-change cause, stop forward work, and restore only already-written files that still equal this operation's exact after-content. Never overwrite a concurrent change during rollback.
4. Apply the minimal edit to that file, then re-read and parse it. Confirm the required role fields are unchanged and only the selected optional settings changed before continuing to the next selected file.
5. If a write or verification fails, preserve the original failure and use the same exact-after-content guarded rollback for already-written files.

Report the exact roles and fields changed, inherited fields removed, preserved fields, scope, and paths. Tell the user to start a new Codex session. Do not claim the configured model exists, the role was discovered, or the requested permission became effective until the new session demonstrates it.
