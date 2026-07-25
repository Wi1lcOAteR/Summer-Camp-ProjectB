[CmdletBinding()]
param(
    [string]$Root = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Root)) {
    $scriptPath = $MyInvocation.MyCommand.Path
    $Root = (Resolve-Path (Join-Path (Split-Path -Parent $scriptPath) "..")).Path
}

$expectedFiles = @{
    "docs/engineering/locks/python-3.14.6-linux-amd64-ci.in" = "16d3c9b0373e7fa9d98e3764490b64e5abc3ba461bb0756089b211f4a71cac1d"
    "docs/engineering/locks/python-3.14.6-linux-amd64-ci.lock" = "d24ddf3789ea9f276ee6ba4062634fef3c85c4572a7eb62096cbd570bfb0fc35"
    "docs/engineering/locks/python-3.14.6-linux-amd64-demo.in" = "2e479a450191ebb8ad1db4d35f1b9aae811b050c74e4b0e3e18188d990468456"
    "docs/engineering/locks/python-3.14.6-linux-amd64-demo.lock" = "09ce57726c02a090f134d4f2c25f2681dce58ebf2d8425502129d42ac2be34f7"
}

$targets = @(
    @{
        Name = "ci"
        Input = "docs/engineering/locks/python-3.14.6-linux-amd64-ci.in"
        Lock = "docs/engineering/locks/python-3.14.6-linux-amd64-ci.lock"
        Count = 41
    },
    @{
        Name = "demo"
        Input = "docs/engineering/locks/python-3.14.6-linux-amd64-demo.in"
        Lock = "docs/engineering/locks/python-3.14.6-linux-amd64-demo.lock"
        Count = 14
    }
)

$expectedInputs = @{
    ci = @(
        "fastapi==0.139.2", "httpx==0.28.1", "httpx2==2.7.0", "mypy==2.3.0",
        "openai==2.46.0", "psutil==7.2.2", "pydantic==2.13.4", "pypdf==6.14.2",
        "pypdfium2==5.12.1", "pytest==9.1.1", "python-multipart==0.0.32",
        "ruff==0.15.22", "types-psutil==7.2.2.20260518", "tzdata==2026.3",
        "uvicorn==0.51.0"
    )
    demo = @(
        "fastapi==0.139.2", "pydantic==2.13.4", "tzdata==2026.3", "uvicorn==0.51.0"
    )
}

$errors = [System.Collections.Generic.List[string]]::new()

function Add-Error([string]$Message) {
    [void]$script:errors.Add($Message)
}

function Get-NormalizedName([string]$Name) {
    return $Name.ToLowerInvariant().Replace("_", "-").Replace(".", "-")
}

function Get-CanonicalTextSha256([string]$Path) {
    $text = [System.IO.File]::ReadAllText($Path)
    $crlf = [string][char]13 + [string][char]10
    $lf = [string][char]10
    $cr = [string][char]13
    $canonical = $text.Replace($crlf, $lf).Replace($cr, $lf)
    $encoding = New-Object System.Text.UTF8Encoding($false)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hashBytes = $sha256.ComputeHash($encoding.GetBytes($canonical))
        return (($hashBytes | ForEach-Object { $_.ToString("x2") }) -join "")
    } finally {
        $sha256.Dispose()
    }
}

function Get-InputPins([string]$Path) {
    $pins = @{}
    $lastName = $null
    foreach ($line in (Get-Content -LiteralPath $Path)) {
        if ([string]::IsNullOrWhiteSpace($line) -or $line.TrimStart().StartsWith("#")) {
            continue
        }
        if ($line -notmatch '^([A-Za-z0-9_.-]+)==([^\s]+)$') {
            Add-Error "Malformed direct requirement in $Path"
            continue
        }
        $name = Get-NormalizedName $Matches[1]
        if ($null -ne $lastName -and [string]::CompareOrdinal($lastName, $name) -ge 0) {
            Add-Error "Direct requirements are not uniquely sorted in $Path"
        }
        $lastName = $name
        if ($pins.ContainsKey($name)) {
            Add-Error "Duplicate direct requirement '$name' in $Path"
        }
        $pins[$name] = $Matches[2]
    }
    return $pins
}

function Get-HashedLockPins([string]$Path) {
    $lines = @(Get-Content -LiteralPath $Path)
    $pins = @{}
    $currentName = $null
    $currentHasHash = $false
    $lastName = $null

    foreach ($line in $lines) {
        if ($line -match '^([A-Za-z0-9_.-]+)==([^\s\\]+)\s*\\?\s*$') {
            if ($null -ne $currentName -and -not $currentHasHash) {
                Add-Error "Lock entry '$currentName' has no SHA-256 hash in $Path"
            }
            $currentName = Get-NormalizedName $Matches[1]
            if ($null -ne $lastName -and [string]::CompareOrdinal($lastName, $currentName) -ge 0) {
                Add-Error "Lock requirements are not uniquely sorted in $Path"
            }
            $lastName = $currentName
            $currentHasHash = $false
            if ($pins.ContainsKey($currentName)) {
                Add-Error "Duplicate lock package '$currentName' in $Path"
            }
            $pins[$currentName] = $Matches[2]
            continue
        }
        if ($line -match '^\s+--hash=sha256:[0-9a-f]{64}(?:\s+\\)?\s*$') {
            if ($null -eq $currentName) {
                Add-Error "Orphan hash in $Path"
            } else {
                $currentHasHash = $true
            }
            continue
        }
        if ($line -match '^\s*(#.*)?$') {
            continue
        }
        Add-Error "Unexpected lock syntax in $Path"
    }
    if ($null -ne $currentName -and -not $currentHasHash) {
        Add-Error "Lock entry '$currentName' has no SHA-256 hash in $Path"
    }
    return $pins
}

function Get-ReviewedLicensePins([string]$Path) {
    $pins = @{}
    foreach ($line in (Get-Content -LiteralPath $Path)) {
        if ($line -notmatch '^\|\s*python\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(https?://[^|]+?)\s*\|') {
            continue
        }
        $name = Get-NormalizedName $Matches[1].Trim()
        $version = $Matches[2].Trim()
        $license = $Matches[3].Trim()
        $source = $Matches[4].Trim()
        if ([string]::IsNullOrWhiteSpace($license) -or [string]::IsNullOrWhiteSpace($source)) {
            Add-Error "Incomplete reviewed license row for '$name'"
        }
        $pins[$name] = $version
    }
    return $pins
}

foreach ($relative in $expectedFiles.Keys) {
    $path = Join-Path $Root $relative
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-Error "Missing frozen Linux evidence file: $relative"
        continue
    }
    $actualHash = Get-CanonicalTextSha256 $path
    if ($actualHash -ne $expectedFiles[$relative]) {
        Add-Error "Canonical SHA-256 mismatch for $relative"
    }
}

$baselinePath = Join-Path $Root "docs/engineering/DEPENDENCY_BASELINE.md"
$linuxBaselinePath = Join-Path $Root "docs/engineering/LINUX_DEPENDENCY_BASELINE.md"
$distributionPath = Join-Path $Root "docs/engineering/DISTRIBUTION_EVIDENCE.md"

foreach ($required in @($baselinePath, $linuxBaselinePath, $distributionPath)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        Add-Error "Missing ledger: $required"
    }
}

$standardScript = Join-Path $Root "scripts/verify_evidence.ps1"
if (Test-Path -LiteralPath $standardScript -PathType Leaf) {
    $standardOutput = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $standardScript -Root $Root 2>&1)
    $standardExit = $LASTEXITCODE
    $standardText = ($standardOutput | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
    if ($standardExit -ne 0) {
        Add-Error "Standard evidence verifier failed before Linux validation"
    } elseif ($standardText -notmatch 'EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166') {
        Add-Error "Standard evidence receipt changed"
    }
} else {
    Add-Error "Missing standard evidence verifier"
}

$reviewedPins = if (Test-Path -LiteralPath $baselinePath) {
    Get-ReviewedLicensePins $baselinePath
} else {
    @{}
}

$counts = @{}
$licensed = [System.Collections.Generic.HashSet[string]]::new()
$allPins = @{}
foreach ($target in $targets) {
    $inputPath = Join-Path $Root $target.Input
    $lockPath = Join-Path $Root $target.Lock
    if (-not (Test-Path -LiteralPath $inputPath) -or -not (Test-Path -LiteralPath $lockPath)) {
        continue
    }
    $inputPins = Get-InputPins $inputPath
    $lockPins = Get-HashedLockPins $lockPath
    $counts[$target.Name] = $lockPins.Count
    $allPins[$target.Name] = $lockPins
    if ($lockPins.Count -ne $target.Count) {
        Add-Error "Expected $($target.Count) $($target.Name) packages, found $($lockPins.Count)"
    }
    $expectedDirect = $expectedInputs[$target.Name]
    if ($inputPins.Count -ne $expectedDirect.Count) {
        Add-Error "Unexpected direct-pin count for $($target.Name)"
    }
    foreach ($requirement in $expectedDirect) {
        if ($requirement -notmatch '^([^=]+)==(.+)$') {
            Add-Error "Invalid verifier direct-pin invariant for $($target.Name)"
            continue
        }
        $expectedName = Get-NormalizedName $Matches[1]
        $expectedVersion = $Matches[2]
        if (-not $inputPins.ContainsKey($expectedName) -or $inputPins[$expectedName] -ne $expectedVersion) {
            Add-Error "Missing exact direct pin '$requirement' for $($target.Name)"
        }
    }
    foreach ($name in $inputPins.Keys) {
        if (-not $lockPins.ContainsKey($name) -or $lockPins[$name] -ne $inputPins[$name]) {
            Add-Error "Direct pin '$name==$($inputPins[$name])' is not preserved in $($target.Lock)"
        }
    }
    foreach ($name in $lockPins.Keys) {
        if (-not $reviewedPins.ContainsKey($name)) {
            Add-Error "Linux package '$name' has no reviewed license row"
            continue
        }
        if ($reviewedPins[$name] -ne $lockPins[$name]) {
            Add-Error "Linux package '$name' version differs from reviewed license row"
            continue
        }
        [void]$licensed.Add($name)
    }
}

if ($allPins.ContainsKey("ci") -and $allPins.ContainsKey("demo")) {
    foreach ($name in $allPins["demo"].Keys) {
        if (-not $allPins["ci"].ContainsKey($name) -or $allPins["ci"][$name] -ne $allPins["demo"][$name]) {
            Add-Error "Demo pin '$name' is not an exact-version subset of CI"
        }
    }
    foreach ($forbidden in @(
        "openai", "httpx", "httpcore", "httpx2", "httpcore2", "certifi",
        "python-multipart", "pypdf", "pypdfium2", "keyring", "psutil",
        "pytest", "ruff", "mypy", "types-psutil"
    )) {
        if ($allPins["demo"].ContainsKey($forbidden)) {
            Add-Error "Public demo lock contains forbidden package '$forbidden'"
        }
    }
}

if (Test-Path -LiteralPath $linuxBaselinePath) {
    $linuxText = Get-Content -LiteralPath $linuxBaselinePath -Raw
    foreach ($frozenHash in $expectedFiles.Values) {
        if (-not $linuxText.Contains($frozenHash)) {
            Add-Error "Linux baseline does not bind frozen file hash: $frozenHash"
        }
    }
    foreach ($requiredText in @(
        "x86_64-manylinux_2_28",
        "PSF-2.0",
        "Debian package-specific",
        "DIST-02",
        "sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6",
        "sha256:86f975aca15cf04a40b399eebede9aea7c82eae084d1f1a0a6ef6bcaae871a30",
        "sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb"
    )) {
        if (-not $linuxText.Contains($requiredText)) {
            Add-Error "Linux baseline is missing required term: $requiredText"
        }
    }
}

if (Test-Path -LiteralPath $distributionPath) {
    $distributionText = Get-Content -LiteralPath $distributionPath -Raw
    foreach ($digest in @(
        "sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6",
        "sha256:86f975aca15cf04a40b399eebede9aea7c82eae084d1f1a0a6ef6bcaae871a30",
        "sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb"
    )) {
        if (-not $distributionText.Contains($digest)) {
            Add-Error "Distribution evidence is missing frozen OCI digest: $digest"
        }
    }
}

if ($errors.Count -gt 0) {
    foreach ($errorMessage in $errors) {
        Write-Error $errorMessage
    }
    exit 1
}

Write-Output "LINUX_EVIDENCE_PASS ci_packages=$($counts['ci']) demo_packages=$($counts['demo']) license_rows=$($licensed.Count)"
