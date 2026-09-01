# 安装与共存

[English](INSTALLATION.md) | [简体中文](INSTALLATION.zh-CN.md)

[README](../README.zh-CN.md) · [配置](CONFIGURATION.zh-CN.md) · [测试](TESTING.zh-CN.md) · [常见问题](FAQ.zh-CN.md)

<a id="scope"></a>
## 范围

KISS My Agent 是一组源码组件，不是 installer。仓库 checkout 已包含项目 Skill、角色文件和 `.codex/config.toml`。使用该 checkout 时，只需验证、信任项目并启动新的 Codex 会话。只有将组件采用到其他项目或个人 scope 时才需要复制。

下方每条命令都会在输入缺失或目标冲突时停止，绝不覆盖已有 Skill、角色、instruction 文件或 config。目标已存在时应人工检查和合并。

<a id="prerequisites"></a>
## 前提条件

- Linux 或 macOS 使用 POSIX shell；Windows 使用原生 PowerShell。
- Python 3.11 或更高版本：Linux 或 macOS 使用 `python3`；Windows 使用 `py -3` launcher 或 `python`。
- 仓库 checkout，下文记为 `KISS_REPO_ROOT` / `$KissRepoRoot`。
- 目标项目，下文记为 `TARGET_PROJECT` / `$TargetProject`。
- 真实发现检查需要当前 Codex 安装。WSL 按 Linux 路径处理，不构成 Windows 支持证据。

Linux 或 macOS：

```bash
set -eu
KISS_REPO_ROOT=/absolute/path/to/kiss-my-agent
TARGET_PROJECT=/absolute/path/to/your-project
export KISS_REPO_ROOT TARGET_PROJECT
test -d "$KISS_REPO_ROOT"
test -d "$TARGET_PROJECT"
```

Windows PowerShell：

```powershell
$ErrorActionPreference = 'Stop'
$KissRepoRoot = 'C:\absolute\path\to\kiss-my-agent'
$TargetProject = 'C:\absolute\path\to\your-project'
if (!(Test-Path -LiteralPath $KissRepoRoot -PathType Container)) { throw 'KissRepoRoot is missing.' }
if (!(Test-Path -LiteralPath $TargetProject -PathType Container)) { throw 'TargetProject is missing.' }
```

<a id="validate-checkout"></a>
## 验证 checkout

Linux 或 macOS：

```bash
set -eu
cd "$KISS_REPO_ROOT"
./scripts/validate.sh
```

Windows PowerShell：

```powershell
Set-Location -LiteralPath $KissRepoRoot
.\scripts\validate.ps1
```

Validator 位于仓库内，不需要安装、复制 `CODEX_HOME`、sandbox package、容器或额外测试项目；它不写用户配置。后续真实 Host 会话可能写入正常的 trust、历史、缓存或 marketplace 状态。

<a id="collision-policy"></a>
## 冲突策略

| 已有目标 | 必须采取的动作 |
| --- | --- |
| `config.toml` | 保留；只人工合并审核过的 tables 或 keys。 |
| `AGENTS.override.md` | 视为该目录的有效来源；不要用新 base 文件掩盖它。 |
| `AGENTS.md` | 保留；只人工合并适用的 KISS 边界。 |
| 通用 `explorer`、`coder` 或 `review` 角色 | 保留；KISS 使用独立的 `kiss_*` 名称。 |
| 已有 `kiss_explorer`、`kiss_coder` 或 `kiss_reviewer` | 停止并 diff；绝不覆盖。 |
| 任一活跃 scope 已有 `kiss-my-agent` Skill | 停止并选择一个权威副本。 |
| owner 或优先级未知 | 在明确 owner 前跳过该组件。 |

<a id="adopt-skill"></a>
## 采用 Skill

只选择一个 scope。下列命令安装到目标项目。用户 scope 使用同样的冲突规则，POSIX 目标为 `$HOME/.agents/skills/kiss-my-agent`，Windows 目标为相应 user-home 下的 `.agents\skills\kiss-my-agent`。

Linux 或 macOS：

```bash
set -eu
skill_source=$KISS_REPO_ROOT/.agents/skills/kiss-my-agent
skill_parent=$TARGET_PROJECT/.agents/skills
skill_target=$skill_parent/kiss-my-agent
test -d "$skill_source"
test -d "$TARGET_PROJECT"
if [ -e "$skill_target" ]; then
  printf '%s\n' 'kiss-my-agent already exists; nothing was copied.' >&2
  exit 1
fi
mkdir -p "$skill_parent"
mkdir "$skill_target"
cp -R "$skill_source/." "$skill_target/"
```

Windows PowerShell：

```powershell
$skillSource = Join-Path $KissRepoRoot '.agents\skills\kiss-my-agent'
$skillParent = Join-Path $TargetProject '.agents\skills'
$skillTarget = Join-Path $skillParent 'kiss-my-agent'
if (!(Test-Path -LiteralPath $skillSource -PathType Container)) { throw 'Skill source is missing.' }
if (Test-Path -LiteralPath $skillTarget) { throw 'kiss-my-agent already exists; nothing was copied.' }
[System.IO.Directory]::CreateDirectory($skillParent) | Out-Null
Copy-Item -LiteralPath $skillSource -Destination $skillTarget -Recurse
```

同一项目不要同时激活项目级与用户级副本；同名 Skills 不会合并。

<a id="adopt-roles"></a>
## 采用角色

三个前缀角色是 `kiss_explorer`、`kiss_coder` 和 `kiss_reviewer`。下列命令完整预检后才将三者复制到项目 scope。

Linux 或 macOS：

```bash
set -eu
role_target_dir=$TARGET_PROJECT/.codex/agents
for role in kiss_explorer kiss_coder kiss_reviewer; do
  test -f "$KISS_REPO_ROOT/.codex/agents/$role.toml"
  if [ -e "$role_target_dir/$role.toml" ]; then
    printf '%s\n' "$role already exists; nothing was copied." >&2
    exit 1
  fi
done
mkdir -p "$role_target_dir"
for role in kiss_explorer kiss_coder kiss_reviewer; do
  cp "$KISS_REPO_ROOT/.codex/agents/$role.toml" "$role_target_dir/$role.toml"
done
```

Windows PowerShell：

```powershell
$roleNames = @('kiss_explorer', 'kiss_coder', 'kiss_reviewer')
$roleTargetDir = Join-Path $TargetProject '.codex\agents'
foreach ($role in $roleNames) {
  $source = Join-Path $KissRepoRoot ".codex\agents\$role.toml"
  $target = Join-Path $roleTargetDir "$role.toml"
  if (!(Test-Path -LiteralPath $source -PathType Leaf)) { throw "Role source is missing: $role" }
  if (Test-Path -LiteralPath $target) { throw "Role already exists: $role" }
}
[System.IO.Directory]::CreateDirectory($roleTargetDir) | Out-Null
foreach ($role in $roleNames) {
  $source = Join-Path $KissRepoRoot ".codex\agents\$role.toml"
  $target = Join-Path $roleTargetDir "$role.toml"
  [System.IO.File]::Copy($source, $target, $false)
}
```

只复制角色 TOML 不会完成注册；继续配置项目 config。

<a id="adopt-project-config"></a>
## 采用项目配置

跟踪的 `.codex/config.toml` 只包含 `[agents] enabled = true` 与三个 `agents.kiss_*` 注册。如果目标没有项目 config，可在完成下方预检后复制；如果已经存在，不要运行这些命令，只人工合并审核过的 agent tables，并保留所有无关设置。

Linux 或 macOS：

```bash
set -eu
config_source=$KISS_REPO_ROOT/.codex/config.toml
config_target=$TARGET_PROJECT/.codex/config.toml
test -f "$config_source"
mkdir -p "$TARGET_PROJECT/.codex"
if [ -e "$config_target" ]; then
  printf '%s\n' 'Project config already exists; merge manually.' >&2
  exit 1
fi
cp "$config_source" "$config_target"
```

Windows PowerShell：

```powershell
$configSource = Join-Path $KissRepoRoot '.codex\config.toml'
$configTargetDir = Join-Path $TargetProject '.codex'
$configTarget = Join-Path $configTargetDir 'config.toml'
if (!(Test-Path -LiteralPath $configSource -PathType Leaf)) { throw 'Project config source is missing.' }
if (Test-Path -LiteralPath $configTarget) { throw 'Project config already exists; merge manually.' }
[System.IO.Directory]::CreateDirectory($configTargetDir) | Out-Null
[System.IO.File]::Copy($configSource, $configTarget, $false)
```

相对 `config_file` 路径从该 config layer 解析。项目 config 只有在项目可信时加载，并应在新会话中测试。

<a id="adopt-agents-guidance"></a>
## 采用 AGENTS 指导

只有目标根目录同时不存在 `AGENTS.override.md` 和 `AGENTS.md` 时才直接复制。否则人工审核并合并适用边界。

Linux 或 macOS：

```bash
set -eu
agents_source=$KISS_REPO_ROOT/AGENTS.md
agents_target=$TARGET_PROJECT/AGENTS.md
test -f "$agents_source"
if [ -e "$TARGET_PROJECT/AGENTS.override.md" ] || [ -e "$agents_target" ]; then
  printf '%s\n' 'An instruction source exists; merge manually.' >&2
  exit 1
fi
cp "$agents_source" "$agents_target"
```

Windows PowerShell：

```powershell
$agentsSource = Join-Path $KissRepoRoot 'AGENTS.md'
$agentsTarget = Join-Path $TargetProject 'AGENTS.md'
$agentsOverride = Join-Path $TargetProject 'AGENTS.override.md'
if (!(Test-Path -LiteralPath $agentsSource -PathType Leaf)) { throw 'AGENTS source is missing.' }
if ((Test-Path -LiteralPath $agentsOverride) -or (Test-Path -LiteralPath $agentsTarget)) { throw 'An instruction source exists; merge manually.' }
[System.IO.File]::Copy($agentsSource, $agentsTarget, $false)
```

保留目标项目的产品 owner、安全规则、验收标准和停止边界。

<a id="confirm-discovery"></a>
## 确认发现

修改 config、Skills、角色或 instructions 后，信任目标项目并启动新会话。运行 `/skills`，确认恰好一个 `kiss-my-agent`，并只 Smoke 已注册角色。当前旧会话不保证热加载。详见[测试](TESTING.zh-CN.md)。

Discovery 只证明 Host 在该会话中找到了组件；它不证明未来行为，也不授予新权限。

<a id="update-remove"></a>
## 更新或移除

- 更新已安装组件前先 diff；安装命令会有意在冲突时停止。
- 只移除已经确认由你安装的精确文件或目录。
- 通过审核过的 diff 逆转人工合并的 config 或 AGENTS 行。
- 启动可信新会话并重新确认实际配置。

项目没有 install receipt、migration database、compatibility alias 或自动 uninstall。
