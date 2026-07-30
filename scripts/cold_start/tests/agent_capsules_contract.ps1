param(
    [string]$Generator = (Join-Path (Split-Path -Parent $PSScriptRoot) 'update_agent_capsules.ps1')
)

$ErrorActionPreference = 'Stop'

function Invoke-Generator {
    param([string]$Root, [string]$Mode)

    $output = @(& powershell -NoProfile -ExecutionPolicy Bypass -File $Generator -Root $Root -Mode $Mode 2>&1)
    [pscustomobject]@{ ExitCode = $LASTEXITCODE; Output = ($output -join "`n") }
}

function Assert-Result {
    param($Result, [int]$ExitCode, [string]$Pattern)

    if ($Result.ExitCode -ne $ExitCode -or $Result.Output -notmatch $Pattern) {
        throw "Expected exit=$ExitCode pattern=$Pattern; got exit=$($Result.ExitCode) output=$($Result.Output)"
    }
}

function Write-Utf8NoBom {
    param([string]$Path, [string]$Text)
    [IO.File]::WriteAllText($Path, $Text, (New-Object Text.UTF8Encoding($false, $true)))
}

function New-Fixture {
    $root = Join-Path $env:TEMP ('projectb-capsule-' + [guid]::NewGuid().ToString())
    New-Item -ItemType Directory -Path (Join-Path $root 'docs\cold-start') -Force | Out-Null
    $spec = "# Spec`n<!-- AGENT_CAPSULE:SPEC:BEGIN -->`nold`n<!-- AGENT_CAPSULE:SPEC:END -->`n## Goal`nAlpha body.`n## Security`nBeta body.`n"
    $plan = "# Plan`n<!-- AGENT_CAPSULE:PLAN:BEGIN -->`nold`n<!-- AGENT_CAPSULE:PLAN:END -->`n## Gates`nGamma body.`n## Task`nDelta body.`n"
    Write-Utf8NoBom (Join-Path $root 'SPEC.md') $spec
    Write-Utf8NoBom (Join-Path $root 'PLAN.md') $plan
    $manifest = [ordered]@{
        version = 1
        documents = [ordered]@{
            SPEC = [ordered]@{ path = 'SPEC.md'; max_words = 20; source_anchors = @('## Goal','## Security'); source_sha256 = ''; content = "Agent spec capsule.`n" }
            PLAN = [ordered]@{ path = 'PLAN.md'; max_words = 20; source_anchors = @('## Gates','## Task'); source_sha256 = ''; content = "Agent plan capsule.`n" }
        }
    }
    Write-Utf8NoBom -Path (Join-Path $root 'docs\cold-start\agent-capsules.json') -Text ($manifest | ConvertTo-Json -Depth 8)
    return $root
}

function Set-SourceHashes {
    param([string]$Root)
    $manifestPath = Join-Path $Root 'docs\cold-start\agent-capsules.json'
    $manifest = Get-Content -Raw -LiteralPath $manifestPath -Encoding UTF8 | ConvertFrom-Json
    foreach ($name in @('SPEC','PLAN')) {
        $entry = $manifest.documents.$name
        $text = Get-Content -Raw -LiteralPath (Join-Path $Root $entry.path) -Encoding UTF8
        $begin = "<!-- AGENT_CAPSULE:$name`:BEGIN -->"
        $end = "<!-- AGENT_CAPSULE:$name`:END -->"
        $body = [regex]::Replace($text, '(?s)' + [regex]::Escape($begin) + '.*?' + [regex]::Escape($end), "$begin`n$end")
        $bytes = (New-Object Text.UTF8Encoding($false, $true)).GetBytes($body)
        $sha = [Security.Cryptography.SHA256]::Create()
        try { $entry.source_sha256 = ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','') } finally { $sha.Dispose() }
    }
    Write-Utf8NoBom -Path $manifestPath -Text ($manifest | ConvertTo-Json -Depth 8)
}

$roots = [Collections.Generic.List[string]]::new()
try {
    $missing = New-Fixture; $roots.Add($missing); Remove-Item -LiteralPath (Join-Path $missing 'docs\cold-start\agent-capsules.json')
    Assert-Result (Invoke-Generator $missing Check) 1 'AGENT_CAPSULE_ERROR code=manifest_missing path=docs/cold-start/agent-capsules.json'

    $root = New-Fixture; $roots.Add($root); Set-SourceHashes $root
    Assert-Result (Invoke-Generator $root Write) 0 '^AGENT_CAPSULE_PASS documents=2$'
    Assert-Result (Invoke-Generator $root Check) 0 '^AGENT_CAPSULE_PASS documents=2$'

    $root = New-Fixture; $roots.Add($root); Set-SourceHashes $root
    $specPath = Join-Path $root 'SPEC.md'
    $specText = (Get-Content -Raw -LiteralPath $specPath -Encoding UTF8).Replace('<!-- AGENT_CAPSULE:SPEC:BEGIN -->', '')
    Write-Utf8NoBom $specPath $specText
    Assert-Result (Invoke-Generator $root Check) 1 'AGENT_CAPSULE_ERROR code=marker_count path=SPEC.md'

    $root = New-Fixture; $roots.Add($root); Set-SourceHashes $root
    [IO.File]::WriteAllBytes((Join-Path $root 'PLAN.md'), [byte[]](0xC3,0x28))
    Assert-Result (Invoke-Generator $root Check) 1 'AGENT_CAPSULE_ERROR code=utf8_invalid path=PLAN.md'

    Add-Content -LiteralPath (Join-Path $root 'SPEC.md') -Value 'changed' -Encoding UTF8
    Assert-Result (Invoke-Generator $root Check) 1 'AGENT_CAPSULE_ERROR code=source_hash_mismatch path=SPEC.md'

    $root = New-Fixture; $roots.Add($root); Set-SourceHashes $root
    $manifestPath = Join-Path $root 'docs\cold-start\agent-capsules.json'
    $manifest = Get-Content -Raw -LiteralPath $manifestPath -Encoding UTF8 | ConvertFrom-Json
    $manifest.documents.SPEC.source_anchors = @('## Missing')
    Write-Utf8NoBom -Path $manifestPath -Text ($manifest | ConvertTo-Json -Depth 8)
    Assert-Result (Invoke-Generator $root Check) 1 'AGENT_CAPSULE_ERROR code=source_anchor_missing path=SPEC.md'

    $root = New-Fixture; $roots.Add($root); Set-SourceHashes $root
    $manifestPath = Join-Path $root 'docs\cold-start\agent-capsules.json'
    $manifest = Get-Content -Raw -LiteralPath $manifestPath -Encoding UTF8 | ConvertFrom-Json
    $manifest.documents.SPEC.content = 'non-ascii-' + [char]0x4E2D
    Write-Utf8NoBom -Path $manifestPath -Text ($manifest | ConvertTo-Json -Depth 8)
    Assert-Result (Invoke-Generator $root Check) 1 'AGENT_CAPSULE_ERROR code=capsule_non_ascii path=SPEC.md'

    $root = New-Fixture; $roots.Add($root); Set-SourceHashes $root
    $manifestPath = Join-Path $root 'docs\cold-start\agent-capsules.json'
    $manifest = Get-Content -Raw -LiteralPath $manifestPath -Encoding UTF8 | ConvertFrom-Json
    $manifest.documents.PLAN.max_words = 1
    Write-Utf8NoBom -Path $manifestPath -Text ($manifest | ConvertTo-Json -Depth 8)
    Assert-Result (Invoke-Generator $root Check) 1 'AGENT_CAPSULE_ERROR code=capsule_word_limit path=PLAN.md'

    $root = New-Fixture; $roots.Add($root); Set-SourceHashes $root
    Assert-Result (Invoke-Generator $root Write) 0 '^AGENT_CAPSULE_PASS documents=2$'
    $planPath = Join-Path $root 'PLAN.md'
    $planText = (Get-Content -Raw -LiteralPath $planPath -Encoding UTF8).Replace('Agent plan capsule.', 'tampered.')
    Write-Utf8NoBom $planPath $planText
    Assert-Result (Invoke-Generator $root Check) 1 'AGENT_CAPSULE_ERROR code=capsule_drift path=PLAN.md'

    'AGENT_CAPSULE_CONTRACT_PASS cases=9'
} finally {
    foreach ($root in $roots) { if (Test-Path -LiteralPath $root) { Remove-Item -LiteralPath $root -Recurse -Force } }
}
