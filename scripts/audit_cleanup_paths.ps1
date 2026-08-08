param(
    [Parameter(Mandatory = $true)][string]$Root,
    [Parameter(Mandatory = $true)][string]$Inventory,
    [Parameter(Mandatory = $true)][string]$Output,
    [string[]]$DisposableTmpRun = @()
)

$ErrorActionPreference = 'Stop'
$rootPath = (Resolve-Path -LiteralPath $Root).Path.TrimEnd([IO.Path]::DirectorySeparatorChar)
$inventoryPath = (Resolve-Path -LiteralPath $Inventory).Path
$inventoryData = Get-Content -Raw -LiteralPath $inventoryPath | ConvertFrom-Json
if ($inventoryData.schema_version -ne 1 -or -not $inventoryData.records) { throw 'cleanup_inventory_invalid' }

$checkNames = @('containment', 'process_use', 'reference_scan', 'credential_scan', 'ownership')
$hardPaths = @('.', '.git', '.worktrees', 'tmp/stage-b-archive-20260725', 'tmp/toolchains', 'tmp/playwright-browsers')
$cachePaths = @('.mypy_cache', '.pytest_cache', '.ruff_cache', 'frontend/dist', 'frontend/test-results', 'test-results')
$credentialScanner = Join-Path $PSScriptRoot 'scan_credentials.py'

function New-Checks {
    $checks = [ordered]@{}
    foreach ($name in $checkNames) { $checks[$name] = 'unknown' }
    return $checks
}

function Test-Contained([string]$Candidate) {
    $full = [IO.Path]::GetFullPath($Candidate)
    return $full -eq $rootPath -or $full.StartsWith($rootPath + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)
}

function Test-Reparse([string]$Candidate) {
    if (-not (Test-Path -LiteralPath $Candidate)) { return $false }
    $relative = [IO.Path]::GetRelativePath($rootPath, $Candidate)
    $cursor = $rootPath
    foreach ($part in $relative -split '[\\/]') {
        if ($part -in @('', '.')) { continue }
        $cursor = Join-Path $cursor $part
        $item = Get-Item -Force -LiteralPath $cursor
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { return $true }
    }
    return $false
}

function Test-TreeHasReparse([string]$Candidate) {
    try {
        $pending = [Collections.Generic.Stack[string]]::new()
        $pending.Push($Candidate)
        while ($pending.Count -gt 0) {
            foreach ($item in Get-ChildItem -Force -LiteralPath $pending.Pop() -ErrorAction Stop) {
                if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { return $true }
                if ($item.PSIsContainer) { $pending.Push($item.FullName) }
            }
        }
        return $false
    }
    catch { throw 'cleanup_reparse_scan_failed' }
}

function Test-ProcessUse([string]$Candidate) {
    try {
        $needle = [IO.Path]::GetFullPath($Candidate)
        foreach ($process in Get-CimInstance Win32_Process -ErrorAction Stop) {
            if ($process.CommandLine -and $process.CommandLine.IndexOf($needle, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
                return $false
            }
        }
        return $null
    }
    catch { return $null }
}

function Test-Unreferenced([string]$Relative) {
    & git -C $rootPath ls-files --error-unmatch -- $Relative *> $null
    if ($LASTEXITCODE -eq 0) { return $false }
    & git -C $rootPath check-ignore -q -- $Relative
    if ($LASTEXITCODE -ne 0) { return $null }
    $references = @(& git -C $rootPath grep -l -F -- $Relative)
    if ($LASTEXITCODE -notin @(0, 1)) { return $null }
    $housekeeping = @(
        '.gitignore', 'AGENT_LOG.md', 'SPEC_PROCESS.md', 'DECISIONS_NEEDED.md',
        'docs/REQUIREMENTS_COMPLIANCE_AUDIT.md',
        'scripts/audit_repository.py', 'scripts/audit_cleanup_paths.ps1',
        'scripts/tests/test_repository_audit.py', 'scripts/tests/test_cleanup_paths.ps1'
    )
    $activeReferences = @($references | Where-Object {
        $_ -and $_ -notin $housekeeping -and -not $_.StartsWith('docs/archive/', [StringComparison]::OrdinalIgnoreCase)
    })
    if ($activeReferences.Count -gt 0) { return $false }

    $untracked = @(& git -C $rootPath -c core.quotepath=false ls-files --others --exclude-standard)
    if ($LASTEXITCODE -ne 0) { return $null }
    foreach ($path in $untracked) {
        if (-not $path -or $path -in $housekeeping -or $path.StartsWith('docs/archive/', [StringComparison]::OrdinalIgnoreCase)) { continue }
        $candidate = [IO.Path]::GetFullPath((Join-Path $rootPath $path))
        if (-not (Test-Contained $candidate)) { return $null }
        try {
            if (Test-Reparse $candidate) { return $null }
            $item = Get-Item -Force -LiteralPath $candidate -ErrorAction Stop
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { return $null }
            if ($item.PSIsContainer) { continue }
            if ($item.Length -gt 10485760) { return $null }
            $text = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($candidate))
            if ($text.IndexOf($Relative, [StringComparison]::Ordinal) -ge 0) { return $false }
        }
        catch { return $null }
    }
    return $true
}

function Test-NoCredentials([string]$Candidate) {
    try {
        $files = Get-ChildItem -Force -File -Recurse -LiteralPath $Candidate -ErrorAction Stop
        foreach ($file in $files) {
            if ($file.Name -match '(?i)(^\.env(?:\.|$)|credential|secret|token|\.pem$|\.key$)') { return $false }
            if (($file.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { return $null }
            if ($file.Length -gt 10485760) { return $null }
            $relativeFile = [IO.Path]::GetRelativePath($rootPath, $file.FullName).Replace('\', '/')
            & python $credentialScanner --root $rootPath --path $relativeFile *> $null
            if ($LASTEXITCODE -eq 2) { return $false }
            if ($LASTEXITCODE -ne 0) { return $null }
        }
        return $true
    }
    catch { return $null }
}

function Resolve-CheckoutRelative([string]$InventoryPath, [string]$CheckoutPrefix) {
    $path = $InventoryPath.Replace('\', '/')
    if ($path.StartsWith('./', [StringComparison]::Ordinal)) { $path = $path.Substring(2) }
    $prefix = $CheckoutPrefix.Replace('\', '/')
    if ($prefix.StartsWith('./', [StringComparison]::Ordinal)) { $prefix = $prefix.Substring(2) }
    $prefix = $prefix.TrimEnd('/')
    if ($CheckoutPrefix -eq '.' -or -not $prefix) { return $(if ($path) { $path } else { '.' }) }
    if ($path -eq $prefix) { return '.' }
    if ($path.StartsWith($prefix + '/', [StringComparison]::OrdinalIgnoreCase)) {
        return $path.Substring($prefix.Length + 1)
    }
    return $null
}

$decisions = foreach ($record in $inventoryData.records) {
    $path = [string]$record.path
    $kind = [string]$record.kind
    $checks = New-Checks
    $relative = Resolve-CheckoutRelative $path ([string]$inventoryData.checkout_root)
    $decision = 'retain'
    $reason = 'outside_current_checkout'

    if ($null -ne $relative) {
        $relative = $relative.Replace('\', '/').TrimStart('/')
        if (-not $relative) { $relative = '.' }
        $candidate = if ($relative -eq '.') { $rootPath } else { Join-Path $rootPath ($relative.Replace('/', [IO.Path]::DirectorySeparatorChar)) }
        if (Test-Contained $candidate) { $checks.containment = 'pass' } else { $checks.containment = 'fail' }

        $isHardPath = $hardPaths -contains $relative -or $relative.StartsWith('.git/', [StringComparison]::OrdinalIgnoreCase) -or $relative.StartsWith('.worktrees/', [StringComparison]::OrdinalIgnoreCase)
        $isHardKind = $kind -in @('coordination_root', 'checkout', 'worktree', 'symlink', 'submodule', 'runtime_file')
        $isNamedTmp = $false
        if ($relative -match '^tmp/([^/]+)$') { $isNamedTmp = $DisposableTmpRun -contains $Matches[1] }
        $isAllowed = $cachePaths -contains $relative -or $isNamedTmp

        if ($isHardPath -or $isHardKind) {
            $reason = 'hard_retain'
        }
        elseif (-not $isAllowed) {
            $reason = 'not_in_disposable_allowlist'
        }
        elseif (-not (Test-Path -LiteralPath $candidate -PathType Container)) {
            $checks.ownership = 'fail'
            $reason = 'missing_or_not_directory'
        }
        elseif ((Test-Reparse $candidate) -or (Test-TreeHasReparse $candidate)) {
            $checks.containment = 'fail'
            $reason = 'symlink_or_reparse_point'
        }
        else {
            $checks.ownership = 'pass'
            $processUse = Test-ProcessUse $candidate
            $checks.process_use = if ($processUse -eq $true) { 'pass' } elseif ($processUse -eq $false) { 'fail' } else { 'unknown' }
            $reference = Test-Unreferenced $relative
            $checks.reference_scan = if ($reference -eq $true) { 'pass' } elseif ($reference -eq $false) { 'fail' } else { 'unknown' }
            $credentials = Test-NoCredentials $candidate
            $checks.credential_scan = if ($credentials -eq $true) { 'pass' } elseif ($credentials -eq $false) { 'fail' } else { 'unknown' }

            $duplicatePass = $true
            if ($record.duplicate_group) {
                $duplicatePass = $record.duplicate_proof.owner -eq 'pass' -and
                    $record.duplicate_proof.reference_scan -eq 'pass' -and
                    $record.duplicate_proof.basis -eq 'generated_or_superseded'
            }
            $allChecksPass = @($checks.Values | Where-Object { $_ -ne 'pass' }).Count -eq 0
            if ($allChecksPass -and $duplicatePass) {
                $decision = 'eligible'
                $reason = 'verified_disposable_path'
            }
            elseif (-not $duplicatePass) { $reason = 'duplicate_proof_incomplete' }
            else { $reason = 'verification_incomplete' }
        }
    }

    [ordered]@{ path = $path; kind = $kind; decision = $decision; reason = $reason; checks = $checks }
}

$result = [ordered]@{
    schema_version = 1
    mode = 'read_only'
    root = $rootPath
    decisions = @($decisions | Sort-Object path, kind)
}
$outputPath = if ([IO.Path]::IsPathRooted($Output)) { [IO.Path]::GetFullPath($Output) } else { Join-Path $rootPath $Output }
if (-not (Test-Contained $outputPath)) { throw 'cleanup_output_escape' }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $outputPath) | Out-Null
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $outputPath -Encoding utf8NoBOM
Write-Output "CLEANUP_PATH_AUDIT_PASS decisions=$($result.decisions.Count)"
$global:LASTEXITCODE = 0
