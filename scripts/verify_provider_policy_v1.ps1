[CmdletBinding()]
param(
    [string]$Root = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Root)) {
    $scriptPath = $MyInvocation.MyCommand.Path
    $Root = (Resolve-Path (Join-Path (Split-Path -Parent $scriptPath) "..")).Path
}

$relativeEvidence = "docs/engineering/PROVIDER_POLICY_V1_P_EVIDENCE.md"
$evidencePath = Join-Path $Root $relativeEvidence
$expectedHash = "35a3f46e036563e3fc681df3190eb56336ab48b9d9817ad48f4d5df42230f076"
$expiry = [DateTimeOffset]::Parse("2026-08-25T00:00:00+08:00")
$requiredIds = @(
    "p-scope", "responses-shape", "retention", "models", "pricing",
    "structured-output", "freshness"
)
$errors = [System.Collections.Generic.List[string]]::new()

function Add-Error([string]$Message) {
    [void]$script:errors.Add($Message)
}

function Get-CanonicalTextSha256([string]$Path) {
    $text = [System.IO.File]::ReadAllText($Path)
    $canonical = $text.Replace(
        ([string][char]13 + [string][char]10),
        [string][char]10
    ).Replace([string][char]13, [string][char]10)
    $encoding = New-Object System.Text.UTF8Encoding($false)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hashBytes = $sha256.ComputeHash($encoding.GetBytes($canonical))
        return (($hashBytes | ForEach-Object { $_.ToString("x2") }) -join "")
    } finally {
        $sha256.Dispose()
    }
}

if (-not (Test-Path -LiteralPath $evidencePath -PathType Leaf)) {
    Add-Error "Missing P-only provider evidence"
} else {
    $actualHash = Get-CanonicalTextSha256 $evidencePath
    if ($actualHash -ne $expectedHash) {
        Add-Error "P-only provider evidence canonical SHA-256 changed"
    }

    $text = Get-Content -LiteralPath $evidencePath -Raw
    foreach ($required in @(
        "gpt-5.6-terra", "gpt-5.6-luna", "store:false", "background:false",
        "tools:[]", "service_tier:default", "reasoning.effort:low",
        "20,000", "3,000", "0.11825", "0.04730", "60-second timeout",
        "zero automatic retries", "direct PDF/image/File/Vector Store",
        "up to 30 days", "up to 24 hours", "not a claim of ZDR",
        "https://api.openai.com/v1/responses",
        "https://developers.openai.com/api/docs/pricing",
        "https://developers.openai.com/api/docs/guides/your-data",
        "https://developers.openai.com/api/docs/guides/structured-outputs"
    )) {
        if (-not $text.Contains($required)) {
            Add-Error "P-only provider evidence is missing required term: $required"
        }
    }

    foreach ($pattern in @(
        '(?i)\bsk-[A-Za-z0-9_-]{20,}\b',
        '(?i)\bAKIA[0-9A-Z]{16}\b',
        '(?i)\bgh[pousr]_[A-Za-z0-9_]{20,}\b',
        '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'
    )) {
        if ($text -match $pattern) {
            Add-Error "Possible credential in P-only provider evidence; value omitted"
        }
    }

    $rows = @{}
    foreach ($line in ($text -split "`r?`n")) {
        if ($line -notmatch '^\| `([^`]+)` \|') {
            continue
        }
        $id = $Matches[1]
        if ($rows.ContainsKey($id)) {
            Add-Error "Duplicate provider evidence row '$id'"
        }
        $rows[$id] = $line
    }
    foreach ($id in $requiredIds) {
        if (-not $rows.ContainsKey($id)) {
            Add-Error "Missing provider evidence row '$id'"
        }
    }
    if ($rows.Count -ne $requiredIds.Count) {
        Add-Error "Unexpected provider evidence row count"
    }
}

$terra = [decimal]1.10 * (
    [decimal]20000 * [decimal]3.125 + [decimal]3000 * [decimal]15
) / [decimal]1000000
$luna = [decimal]1.10 * (
    [decimal]20000 * [decimal]1.25 + [decimal]3000 * [decimal]6
) / [decimal]1000000
if ($terra -ne [decimal]0.11825 -or $luna -ne [decimal]0.04730) {
    Add-Error "Provider cost-bound arithmetic changed"
}

if ([DateTimeOffset]::Now -ge $expiry) {
    Add-Error "P-only provider policy expired; refresh from official sources"
}

$standardScript = Join-Path $Root "scripts/verify_evidence.ps1"
if (Test-Path -LiteralPath $standardScript -PathType Leaf) {
    $standardOutput = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $standardScript -Root $Root 2>&1)
    $standardExit = $LASTEXITCODE
    $standardText = ($standardOutput | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
    if ($standardExit -ne 0) {
        Add-Error "Standard evidence verifier failed before P-only validation"
    } elseif ($standardText -notmatch 'EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166') {
        Add-Error "Standard evidence receipt changed"
    }
} else {
    Add-Error "Missing standard evidence verifier"
}

if ($errors.Count -gt 0) {
    foreach ($errorMessage in $errors) {
        Write-Error $errorMessage
    }
    exit 1
}

Write-Output "PROVIDER_V1_P_EVIDENCE_PASS rows=7 models=2 expires=2026-08-25"
