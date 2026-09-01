$ErrorActionPreference = "Stop"

$validator = Join-Path $PSScriptRoot "validate.py"
$root = Join-Path $PSScriptRoot ".."

$pyLauncher = Get-Command py -CommandType Application -ErrorAction SilentlyContinue
if ($null -ne $pyLauncher) {
    & $pyLauncher.Source -3 $validator --root $root @args
    exit $LASTEXITCODE
}

$python = Get-Command python -CommandType Application -ErrorAction SilentlyContinue
if ($null -ne $python) {
    & $python.Source $validator --root $root @args
    exit $LASTEXITCODE
}

[Console]::Error.WriteLine("validation failed: Python 3.11 or newer was not found")
exit 1
