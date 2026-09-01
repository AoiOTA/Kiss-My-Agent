#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd -P)
sandbox_root="$repo_root/.sandbox"

case "$sandbox_root" in
  "$repo_root/.sandbox") ;;
  *) echo "refusing unexpected sandbox path" >&2; exit 1 ;;
esac

rm -rf -- "$sandbox_root"
mkdir -p "$sandbox_root/codex-home/agents"
mkdir -p "$sandbox_root/codex-home/skills"
mkdir -p "$sandbox_root/project/fixture"

# Keep project-root discovery inside the sandbox instead of inheriting the
# repository that contains this staging area.
git init -q -b main "$sandbox_root/project"

cp -- "$repo_root/AGENTS.md" "$sandbox_root/project/AGENTS.md"
cp -R -- "$repo_root/.codex/agents/." "$sandbox_root/codex-home/agents/"
cp -R -- "$repo_root/.agents/skills/research-mvp-engineering" "$sandbox_root/codex-home/skills/"
cp -R -- "$repo_root/tests/fixtures/layered-project/." "$sandbox_root/project/fixture/"

printf 'Sandbox staged inside repository:\n'
printf '  CODEX_HOME=%q codex --cd %q\n' "$sandbox_root/codex-home" "$sandbox_root/project/fixture/component-b/subsystem"
printf 'The command was printed only; Codex was not started.\n'
