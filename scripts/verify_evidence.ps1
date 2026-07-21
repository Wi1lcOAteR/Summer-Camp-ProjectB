[CmdletBinding()]
param(
    [string]$Root = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Root)) {
    $scriptPath = $MyInvocation.MyCommand.Path
    $Root = (Resolve-Path (Join-Path (Split-Path -Parent $scriptPath) ".." )).Path
}

$requiredFiles = @(
    "docs/engineering/DEPENDENCY_BASELINE.md",
    "docs/engineering/PROVIDER_POLICY_EVIDENCE.md",
    "docs/engineering/DISTRIBUTION_EVIDENCE.md"
)

$requiredRows = @{
    "DEPENDENCY_BASELINE.md" = @(
        "python-runtime", "backend-fastapi", "backend-asgi", "backend-schema",
        "backend-http", "openai-sdk", "parser-pdf", "renderer-pdf",
        "keyring-windows", "backend-test", "frontend-runtime", "frontend-react",
        "frontend-build", "frontend-test", "browser-test", "windows-freezer",
        "dependency-transitive"
    )
    "PROVIDER_POLICY_EVIDENCE.md" = @(
        "responses", "abuse-monitoring", "prompt-cache", "file-review",
        "files", "vector-stores", "deletion-expiry", "region", "pricing",
        "pf-unsupported"
    )
    "DISTRIBUTION_EVIDENCE.md" = @(
        "windows-freezer", "oci-base", "host-runtime", "host-https",
        "host-storage", "host-sleep", "host-quota", "host-cost",
        "host-account", "fallback"
    )
}

$errors = [System.Collections.Generic.List[string]]::new()
$rows = [System.Collections.Generic.List[object]]::new()

function Add-Error([string]$Message) {
    [void]$script:errors.Add($Message)
}

function Test-SecretPattern([string]$Text, [string]$Path) {
    $patterns = @(
        '(?i)\bsk-[A-Za-z0-9]{20,}\b',
        '(?i)\bsk-proj-[A-Za-z0-9_-]{20,}\b',
        '(?i)\bAKIA[0-9A-Z]{16}\b',
        '(?i)\bgh[pousr]_[A-Za-z0-9_]{20,}\b',
        '(?i)\bAIza[0-9A-Za-z_-]{30,}\b',
        '(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*[^`|\s]{16,}'
    )
    foreach ($pattern in $patterns) {
        if ($Text -match $pattern) {
            Add-Error "Possible credential pattern in $Path; value omitted"
            return
        }
    }
}

function Get-MarkdownRows([string]$Path) {
    $content = Get-Content -LiteralPath $Path -Raw
    Test-SecretPattern -Text $content -Path $Path
    $result = [System.Collections.Generic.List[object]]::new()
    foreach ($line in ($content -split "`r?`n")) {
        if ($line -notmatch '^\s*\|') { continue }
        $cells = @($line.Trim() -split '\|' | ForEach-Object { $_.Trim() })
        if ($cells.Count -gt 0 -and $cells[0] -eq "") { $cells = @($cells[1..($cells.Count - 1)]) }
        if ($cells.Count -gt 0 -and $cells[$cells.Count - 1] -eq "") { $cells = @($cells[0..($cells.Count - 2)]) }
        if ($cells.Count -lt 8) { continue }
        if ($cells[0] -eq "ID" -or $cells[0] -match '^[-:]+$') { continue }
        if (($cells -join "|") -match '^[-| :]+$') { continue }
        $result.Add([PSCustomObject]@{
            Id = $cells[0]
            Item = $cells[1]
            Version = $cells[2]
            Source = $cells[3]
            Authority = $cells[4]
            Verified = $cells[5]
            Status = $cells[6].ToLowerInvariant()
            Notes = ($cells[7..($cells.Count - 1)] -join " | ")
            Path = $Path
        })
    }
    return $result
}

foreach ($relative in $requiredFiles) {
    $path = Join-Path $Root $relative
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-Error "Missing evidence file: $relative"
        continue
    }
    $fileRows = @(Get-MarkdownRows -Path $path)
    foreach ($row in $fileRows) { [void]$rows.Add($row) }
    $name = Split-Path $path -Leaf
    foreach ($requiredId in $requiredRows[$name]) {
        $match = @($fileRows | Where-Object { $_.Id -eq $requiredId })
        if ($match.Count -eq 0) {
            Add-Error "Missing required row '$requiredId' in $relative"
            continue
        }
        if ($match.Count -gt 1) { Add-Error "Duplicate required row '$requiredId' in $relative" }
        $row = $match[0]
        if ([string]::IsNullOrWhiteSpace($row.Version) -or $row.Version -eq "-") {
            Add-Error "Blank exact version/term for '$requiredId' in $relative"
        }
        if ($row.Source -notmatch '^https?://[^\s|]+$') {
            Add-Error "Invalid source URL for '$requiredId' in $relative"
        }
        if ([string]::IsNullOrWhiteSpace($row.Authority) -or $row.Authority -eq "-") {
            Add-Error "Blank license/authority for '$requiredId' in $relative"
        }
        if ($row.Verified -notmatch '^\d{4}-\d{2}-\d{2}$') {
            Add-Error "Invalid verification date for '$requiredId' in $relative"
        }
        if ($row.Status -notin @("verified", "explicitly-blocked")) {
            Add-Error "Invalid status for '$requiredId' in ${relative}: $($row.Status)"
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Output "EVIDENCE_VALIDATION_FAIL errors=$($errors.Count) rows=$($rows.Count)"
    foreach ($errorMessage in $errors) { Write-Output "- $errorMessage" }
    exit 1
}

$blocked = @($rows | Where-Object { $_.Status -eq "explicitly-blocked" }).Count
Write-Output "EVIDENCE_VALIDATION_PASS rows=$($rows.Count) explicitly_blocked=$blocked"
exit 0
