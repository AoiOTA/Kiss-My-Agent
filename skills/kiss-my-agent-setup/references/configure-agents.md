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

1. Resolve the selected role directory and inspect its metadata. Stop on a symlinked directory, non-regular TOML file, invalid TOML, missing required role field, or duplicate `name`.
2. Require existing `model`, `model_reasoning_effort`, and `sandbox_mode` values to be non-empty strings; require `sandbox_mode`, when present, to be `read-only`, `workspace-write`, or `danger-full-access`. Do not normalize an invalid value by guesswork.
3. If a role has `default_permissions`, do not add `sandbox_mode`; those settings cannot be combined. If it has `sandbox_workspace_write`, do not change away from `workspace-write` without a separate manual edit that owns the related table.
4. Read each role completely and show a compact table with its identity, path, and current values. Label omitted fields as `inherit`.
5. If no roles exist, stop and explain that setup or a manual role definition is needed first.
6. Ask which one or more existing roles to configure. Do not select every role by default.

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
3. Immediately re-read every selected file. If any content differs from the preview base, stop without writing.
4. Apply minimal edits and then re-read and parse every selected file. Confirm the required role fields are unchanged and only the selected optional settings changed.
5. If a write or verification fails, restore only a file still equal to this operation's after-content. Never overwrite a concurrent change during rollback.

Report the exact roles and fields changed, inherited fields removed, preserved fields, scope, and paths. Tell the user to start a new Codex session. Do not claim the configured model exists, the role was discovered, or the requested permission became effective until the new session demonstrates it.
