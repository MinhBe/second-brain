$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Source = Join-Path $Here "index.ts"
$PiAgent = Join-Path $HOME ".pi\agent"
$Extensions = Join-Path $PiAgent "extensions"
$Target = Join-Path $Extensions "model-budget-guard.ts"
$OldDir = Join-Path $Extensions "model-budget-guard"

if (-not (Test-Path $Source)) {
    throw "Cannot find source extension: $Source"
}

New-Item -ItemType Directory -Force $Extensions | Out-Null

# Remove the old directory-style install to avoid duplicate discovery when the
# single-file install is present. This only touches this extension's old path.
if (Test-Path $OldDir) {
    Remove-Item -Recurse -Force $OldDir
}

Copy-Item -Force $Source $Target

if (-not (Test-Path $Target)) {
    throw "Install failed: $Target was not created"
}

$bytes = (Get-Item $Target).Length
Write-Host "Installed: $Target"
Write-Host "Bytes:     $bytes"

$pi = Get-Command pi -ErrorAction SilentlyContinue
if (-not $pi) {
    Write-Warning "The 'pi' command is not on PATH. The extension is installed, but Pi cannot be launched from this shell."
    exit 0
}

Write-Host "Pi:        $($pi.Source)"
try {
    & pi --version
} catch {
    Write-Warning "Could not read Pi version: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "Verification:" -ForegroundColor Cyan
Write-Host "  1. Close every running Pi process, then start a fresh Pi session."
Write-Host "  2. Type: /ai-policy"
Write-Host ""
Write-Host "If /ai-policy is still missing, run this explicit-load diagnostic:" -ForegroundColor Yellow
Write-Host "  pi -e `"$Target`""
Write-Host "Then type /ai-policy in that Pi session. Any extension load error printed by Pi is the useful part."
