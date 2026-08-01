param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
)

$ErrorActionPreference = 'Stop'
$utf8 = New-Object Text.UTF8Encoding($false, $true)

function Read-StrictUtf8 {
    param([string]$RelativePath)

    $path = Join-Path $Root $RelativePath
    $bytes = [IO.File]::ReadAllBytes($path)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        throw "snapshot_utf8_bom path=$RelativePath"
    }
    return $utf8.GetString($bytes)
}

function Get-BoundHash {
    param([string]$Text, [string]$Pattern, [string]$Label)

    $matches = [regex]::Matches($Text, $Pattern)
    if ($matches.Count -ne 1) { throw "snapshot_binding_count label=$Label count=$($matches.Count)" }
    return $matches[0].Groups[1].Value.ToUpperInvariant()
}

$specHash = (Get-FileHash -LiteralPath (Join-Path $Root 'SPEC.md') -Algorithm SHA256).Hash
$planHash = (Get-FileHash -LiteralPath (Join-Path $Root 'PLAN.md') -Algorithm SHA256).Hash
$plan = Read-StrictUtf8 'PLAN.md'
$audit = Read-StrictUtf8 'docs\REQUIREMENTS_COMPLIANCE_AUDIT.md'
$runbook = Read-StrictUtf8 'docs\cold-start\G-03_CLAUDE_CODE_RUNBOOK.md'

$bindings = [ordered]@{
    plan_spec = Get-BoundHash $plan 'Current SPEC SHA-256 is `([A-Fa-f0-9]{64})`' 'plan_spec'
    audit_spec = Get-BoundHash $audit '(?m)^\*\*SPEC:\*\* `([A-Fa-f0-9]{64})`$' 'audit_spec'
    audit_plan = Get-BoundHash $audit '(?m)^\*\*PLAN current:\*\* `([A-Fa-f0-9]{64})`$' 'audit_plan'
    runbook_spec = Get-BoundHash $runbook '(?m)^- SPEC SHA-256[^`]*`([A-Fa-f0-9]{64})`$' 'runbook_spec'
    runbook_plan = Get-BoundHash $runbook '(?m)^- PLAN SHA-256[^`]*`([A-Fa-f0-9]{64})`$' 'runbook_plan'
}

foreach ($name in @('plan_spec','audit_spec','runbook_spec')) {
    if ($bindings[$name] -cne $specHash) { throw "snapshot_hash_mismatch binding=$name" }
}
foreach ($name in @('audit_plan','runbook_plan')) {
    if ($bindings[$name] -cne $planHash) { throw "snapshot_hash_mismatch binding=$name" }
}

Write-Output "G03_SNAPSHOT_CONTRACT_PASS spec=$specHash plan=$planHash"
