[CmdletBinding()]
param(
    [string]$Root = "",
    [switch]$RequireDependencyReady,
    [switch]$RequireProviderReady,
    [switch]$RequireDistributionReady
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

$lockFiles = @{
    Python = "docs/engineering/locks/python-3.14.6-windows-x64.lock"
    Npm = "docs/engineering/locks/frontend-package-lock.json"
}

$dependencyEvidenceFiles = @(
    "scripts/evidence/g02a_python_smoke.py",
    "scripts/evidence/g02a_node_smoke.mjs"
)

$expectedLockHashes = @{
    Python = "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6"
    Npm = "071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f"
}

$pythonDirectDependencies = @{
    "backend-fastapi" = @{ Package = "fastapi"; Version = "0.139.2" }
    "backend-asgi" = @{ Package = "uvicorn"; Version = "0.51.0" }
    "backend-schema" = @{ Package = "pydantic"; Version = "2.13.4" }
    "backend-http" = @{ Package = "httpx"; Version = "0.28.1" }
    "backend-http2" = @{ Package = "httpx2"; Version = "2.7.0" }
    "openai-sdk" = @{ Package = "openai"; Version = "2.46.0" }
    "parser-pdf" = @{ Package = "pypdf"; Version = "6.14.2" }
    "renderer-pdf" = @{ Package = "pypdfium2"; Version = "5.12.1" }
    "parser-image" = @{ Package = "Pillow"; Version = "12.3.0" }
    "keyring-windows" = @{ Package = "keyring"; Version = "25.7.0" }
    "timezone-data" = @{ Package = "tzdata"; Version = "2026.3" }
    "upload-parser" = @{ Package = "python-multipart"; Version = "0.0.32" }
    "process-metrics" = @{ Package = "psutil"; Version = "7.2.2" }
    "backend-test" = @{ Package = "pytest"; Version = "9.1.1" }
    "backend-lint" = @{ Package = "ruff"; Version = "0.15.22" }
    "backend-type" = @{ Package = "mypy"; Version = "2.3.0" }
    "backend-type-psutil" = @{ Package = "types-psutil"; Version = "7.2.2.20260518" }
    "windows-freezer" = @{
        Package = "pyinstaller"
        Version = "6.21.0"
        Authority = "GPL-2.0-or-later WITH Bootloader-exception; runtime hooks Apache-2.0"
    }
}

$npmDirectDependencies = @{
    "frontend-react" = @{ Package = "react"; Version = "19.2.7"; Section = "dependencies" }
    "frontend-react-dom" = @{ Package = "react-dom"; Version = "19.2.7"; Section = "dependencies" }
    "frontend-icons" = @{ Package = "lucide-react"; Version = "1.25.0"; Section = "dependencies" }
    "frontend-build" = @{ Package = "vite"; Version = "8.1.5"; Section = "devDependencies" }
    "frontend-build-react" = @{ Package = "@vitejs/plugin-react"; Version = "6.0.3"; Section = "devDependencies" }
    "frontend-typescript" = @{ Package = "typescript"; Version = "7.0.2"; Section = "devDependencies" }
    "frontend-test" = @{ Package = "vitest"; Version = "4.1.10"; Section = "devDependencies" }
    "frontend-testing-dom" = @{ Package = "@testing-library/dom"; Version = "10.4.1"; Section = "devDependencies" }
    "frontend-testing-react" = @{ Package = "@testing-library/react"; Version = "16.3.2"; Section = "devDependencies" }
    "frontend-testing-user" = @{ Package = "@testing-library/user-event"; Version = "14.6.1"; Section = "devDependencies" }
    "frontend-jsdom" = @{ Package = "jsdom"; Version = "29.1.1"; Section = "devDependencies" }
    "browser-test" = @{ Package = "@playwright/test"; Version = "1.61.1"; Section = "devDependencies" }
    "browser-a11y" = @{ Package = "@axe-core/playwright"; Version = "4.12.1"; Section = "devDependencies" }
    "frontend-types-react" = @{ Package = "@types/react"; Version = "19.2.17"; Section = "devDependencies" }
    "frontend-types-react-dom" = @{ Package = "@types/react-dom"; Version = "19.2.3"; Section = "devDependencies" }
    "frontend-types-node" = @{ Package = "@types/node"; Version = "24.13.3"; Section = "devDependencies" }
}

$allowedPythonLicenses = @(
    "Apache-2.0", "Apache-2.0 OR BSD-2-Clause", "BSD-2-Clause", "BSD-3-Clause",
    "BSD-3-Clause plus Apache-2.0 and dependency notices including CC-BY-4.0",
    "GPL-2.0-or-later standard hooks; Apache-2.0 runtime hooks",
    "GPL-2.0-or-later WITH Bootloader-exception", "MIT", "MIT plus bundled vendor notices",
    "MIT OR Apache-2.0", "MIT-CMU", "MPL-2.0", "MPL-2.0 AND MIT", "PSF-2.0"
)

$allowedNpmLicenses = @(
    "0BSD", "Apache-2.0", "BlueOak-1.0.0", "BSD-2-Clause", "BSD-3-Clause",
    "CC0-1.0", "ISC", "MIT", "MIT-0", "MPL-2.0"
)

$requiredRows = @{
    "DEPENDENCY_BASELINE.md" = @(
        "python-runtime", "backend-fastapi", "backend-asgi", "backend-schema",
        "backend-http", "backend-http2", "openai-sdk", "parser-pdf",
        "renderer-pdf", "parser-image", "keyring-windows", "timezone-data",
        "upload-parser", "process-metrics", "backend-test", "backend-lint",
        "backend-type", "backend-type-psutil", "frontend-runtime",
        "frontend-react", "frontend-react-dom", "frontend-icons", "frontend-build",
        "frontend-build-react", "frontend-typescript", "frontend-test",
        "frontend-testing-dom", "frontend-testing-react", "frontend-testing-user",
        "frontend-jsdom", "browser-test", "browser-a11y", "frontend-types-react",
        "frontend-types-react-dom", "frontend-types-node", "windows-freezer",
        "python-lock-closure", "npm-lock-closure", "dependency-transitive"
    )
    "PROVIDER_POLICY_EVIDENCE.md" = @(
        "responses", "abuse-monitoring", "prompt-cache", "file-review",
        "files", "vector-stores", "deletion-expiry", "region", "model-reference",
        "p-input-file", "input-token-count", "f-filter-results", "pricing", "pf-unsupported"
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

function Get-CanonicalTextSha256([string]$Path) {
    $text = [System.IO.File]::ReadAllText($Path)
    $canonical = $text.Replace("`r`n", "`n").Replace("`r", "`n")
    $encoding = New-Object System.Text.UTF8Encoding($false)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hashBytes = $sha256.ComputeHash($encoding.GetBytes($canonical))
        return (($hashBytes | ForEach-Object { $_.ToString("x2") }) -join "")
    } finally {
        $sha256.Dispose()
    }
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

function Get-PythonClosureRows([string]$Path) {
    $result = [System.Collections.Generic.List[object]]::new()
    foreach ($line in ((Get-Content -LiteralPath $Path -Raw) -split "`r?`n")) {
        if ($line -notmatch '^\s*\|\s*python\s*\|') { continue }
        $cells = @($line.Trim() -split '\|' | ForEach-Object { $_.Trim() })
        if ($cells[0] -eq "") { $cells = @($cells[1..($cells.Count - 1)]) }
        if ($cells[$cells.Count - 1] -eq "") { $cells = @($cells[0..($cells.Count - 2)]) }
        if ($cells.Count -lt 6) {
            Add-Error "Malformed Python closure row in $Path"
            continue
        }
        $result.Add([PSCustomObject]@{
            Ecosystem = $cells[0]
            Package = $cells[1]
            Version = $cells[2]
            License = $cells[3]
            Source = $cells[4]
            Role = ($cells[5..($cells.Count - 1)] -join " | ")
        })
    }
    return $result
}

function Get-NormalizedPackageName([string]$Name) {
    return $Name.ToLowerInvariant().Replace("_", "-").Replace(".", "-")
}

function Test-NpmIntegrity([string]$Integrity) {
    if ($Integrity -notmatch '^sha(512|256)-([A-Za-z0-9+/]+={0,2})$') { return $false }
    try {
        $decoded = [Convert]::FromBase64String($Matches[2])
        return (($Matches[1] -eq "512" -and $decoded.Length -eq 64) -or
            ($Matches[1] -eq "256" -and $decoded.Length -eq 32))
    } catch {
        return $false
    }
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

$dependencyPath = Join-Path $Root "docs/engineering/DEPENDENCY_BASELINE.md"
foreach ($relative in $dependencyEvidenceFiles) {
    if (-not (Test-Path -LiteralPath (Join-Path $Root $relative) -PathType Leaf)) {
        Add-Error "Missing dependency smoke evidence file: $relative"
    }
}
if (Test-Path -LiteralPath $dependencyPath -PathType Leaf) {
    $dependencyText = Get-Content -LiteralPath $dependencyPath -Raw
    $bootstrapExpectations = @{
        "uv 0.11.14 Windows x64" = @{
            Source = @(
                "https://github.com/astral-sh/uv/releases/download/0.11.14/uv-x86_64-pc-windows-msvc.zip",
                "52ba5d19409aaa688a8a1a6ec8dfb6a4817230d20186e75f4006105c3e39a846"
            )
            License = @("Apache-2.0 OR MIT", "LICENSE-APACHE", "LICENSE-MIT")
            Verification = @("2026-07-26")
        }
        "CPython 3.14.6 embeddable x64" = @{
            Source = @(
                "https://www.python.org/ftp/python/3.14.6/python-3.14.6-embed-amd64.zip",
                "df901e84a896ff1ee720ad03377e0c8d8c2244fda79808aeeaff6316df1cb75c"
            )
            License = @("PSF-2.0", "Python license")
            Verification = @("2026-07-21")
        }
        "Node 24.18.0 Windows x64" = @{
            Source = @(
                "https://nodejs.org/dist/v24.18.0/node-v24.18.0-win-x64.zip",
                "0ae68406b42d7725661da979b1403ec9926da205c6770827f33aac9d8f26e821"
            )
            License = @("Node.js MIT", "npm 11.16.0 is Artistic-2.0")
            Verification = @("2026-07-21")
        }
    }
    $bootstrapRows = @{}
    foreach ($line in ($dependencyText -split "`r?`n")) {
        if ($line -notmatch '^\s*\|') { continue }
        $cells = @($line.Trim() -split '\|' | ForEach-Object { $_.Trim() })
        if ($cells.Count -gt 0 -and $cells[0] -eq "") { $cells = @($cells[1..($cells.Count - 1)]) }
        if ($cells.Count -gt 0 -and $cells[$cells.Count - 1] -eq "") { $cells = @($cells[0..($cells.Count - 2)]) }
        if ($cells.Count -ne 4 -or -not $bootstrapExpectations.ContainsKey($cells[0])) { continue }
        if ($bootstrapRows.ContainsKey($cells[0])) {
            Add-Error "Duplicate bootstrap evidence row '$($cells[0])'"
            continue
        }
        $bootstrapRows[$cells[0]] = $cells
    }
    foreach ($artifact in $bootstrapExpectations.Keys) {
        if (-not $bootstrapRows.ContainsKey($artifact)) {
            Add-Error "Missing bootstrap evidence row '$artifact'"
            continue
        }
        $cells = $bootstrapRows[$artifact]
        foreach ($term in $bootstrapExpectations[$artifact].Source) {
            if (-not $cells[1].Contains($term)) { Add-Error "Bootstrap source/digest mismatch for '$artifact': $term" }
        }
        foreach ($term in $bootstrapExpectations[$artifact].License) {
            if (-not $cells[2].Contains($term)) { Add-Error "Bootstrap license/notice mismatch for '$artifact': $term" }
        }
        foreach ($term in $bootstrapExpectations[$artifact].Verification) {
            if (-not $cells[3].Contains($term)) { Add-Error "Bootstrap verification mismatch for '$artifact': $term" }
        }
    }
    $pythonClosure = @(Get-PythonClosureRows -Path $dependencyPath)
    if ($pythonClosure.Count -ne 54) {
        Add-Error "Python license closure must contain 54 rows; observed $($pythonClosure.Count)"
    }
    $pythonClosureKeys = @{}
    $pythonClosureByKey = @{}
    foreach ($entry in $pythonClosure) {
        if ([string]::IsNullOrWhiteSpace($entry.Package) -or
            [string]::IsNullOrWhiteSpace($entry.Version) -or
            [string]::IsNullOrWhiteSpace($entry.License) -or
            [string]::IsNullOrWhiteSpace($entry.Role)) {
            Add-Error "Blank Python closure field for package '$($entry.Package)'"
        }
        if ($entry.Source -notmatch '^https://pypi\.org/pypi/[^\s|]+/[^\s|]+/json$') {
            Add-Error "Invalid exact PyPI source for '$($entry.Package)'"
        }
        $expectedSource = "https://pypi.org/pypi/$($entry.Package)/$($entry.Version)/json"
        if ($entry.Source -ine $expectedSource) {
            Add-Error "PyPI source does not match package/version for '$($entry.Package)'"
        }
        if ($entry.License -notin $allowedPythonLicenses) {
            Add-Error "Unreviewed Python license '$($entry.License)' for '$($entry.Package)'"
        }
        $key = "$(Get-NormalizedPackageName $entry.Package)==$($entry.Version)"
        if ($pythonClosureKeys.ContainsKey($key)) {
            Add-Error "Duplicate Python closure entry '$key'"
        }
        $pythonClosureKeys[$key] = $true
        $pythonClosureByKey[$key] = $entry
    }
    $pythonDirectClosureKeys = @($pythonClosure | Where-Object { $_.Role -match '^direct(?:$|-)' } | ForEach-Object {
        "$(Get-NormalizedPackageName $_.Package)==$($_.Version)"
    })
    $expectedPythonDirectKeys = @($pythonDirectDependencies.Values | ForEach-Object {
        "$(Get-NormalizedPackageName $_.Package)==$($_.Version)"
    })
    if ($pythonDirectClosureKeys.Count -ne $pythonDirectDependencies.Count) {
        Add-Error "Python closure must contain exactly $($pythonDirectDependencies.Count) direct-role rows"
    }
    foreach ($key in $pythonDirectClosureKeys) {
        if ($key -notin $expectedPythonDirectKeys) {
            Add-Error "Unexpected Python direct-role dependency '$key'"
        }
    }
    foreach ($id in $pythonDirectDependencies.Keys) {
        $expected = $pythonDirectDependencies[$id]
        $matchingRows = @($rows | Where-Object {
            $_.Id -eq $id -and (Split-Path $_.Path -Leaf) -eq "DEPENDENCY_BASELINE.md"
        })
        if ($matchingRows.Count -ne 1) {
            Add-Error "Expected one direct Python evidence row '$id'"
            continue
        }
        $row = $matchingRows[0]
        $expectedSource = "https://pypi.org/pypi/$($expected.Package)/$($expected.Version)/json"
        if ($row.Source -ine $expectedSource -or
            $row.Version -notmatch "^$([regex]::Escape($expected.Version))(?:;|$)") {
            Add-Error "Direct Python evidence row '$id' does not match $($expected.Package)==$($expected.Version)"
        }
        $key = "$(Get-NormalizedPackageName $expected.Package)==$($expected.Version)"
        if (-not $pythonClosureKeys.ContainsKey($key)) {
            Add-Error "Direct Python dependency missing from closure: '$key'"
        } else {
            $expectedAuthority = $pythonClosureByKey[$key].License
            if ($expected.ContainsKey("Authority")) { $expectedAuthority = $expected.Authority }
            if ($row.Authority -ne $expectedAuthority) {
                Add-Error "Direct Python evidence license does not match reviewed closure for '$id'"
            }
        }
    }
}

$pythonLockPath = Join-Path $Root $lockFiles.Python
if (-not (Test-Path -LiteralPath $pythonLockPath -PathType Leaf)) {
    Add-Error "Missing lock evidence file: $($lockFiles.Python)"
} else {
    $pythonHash = Get-CanonicalTextSha256 -Path $pythonLockPath
    if ($pythonHash -ne $expectedLockHashes.Python) {
        Add-Error "Python lock hash mismatch"
    }
    $pythonLockLines = @(Get-Content -LiteralPath $pythonLockPath)
    $pythonPins = @($pythonLockLines | Where-Object { $_ -match '^([A-Za-z0-9_.-]+)==([^\s\\]+)' })
    if ($pythonPins.Count -ne 54) {
        Add-Error "Python lock must contain 54 exact pins; observed $($pythonPins.Count)"
    }
    $pythonPinKeys = @{}
    for ($index = 0; $index -lt $pythonLockLines.Count; $index++) {
        if ($pythonLockLines[$index] -notmatch '^([A-Za-z0-9_.-]+)==([^\s\\]+)') { continue }
        $name = $Matches[1]
        $version = $Matches[2]
        $key = "$(Get-NormalizedPackageName $name)==$version"
        if ($pythonPinKeys.ContainsKey($key)) { Add-Error "Duplicate Python lock pin '$key'" }
        $pythonPinKeys[$key] = $true
        $hasHash = $false
        for ($scan = $index + 1; $scan -lt $pythonLockLines.Count; $scan++) {
            if ($pythonLockLines[$scan] -match '^[A-Za-z0-9_.-]+==') { break }
            if ($pythonLockLines[$scan] -match '--hash=sha256:[0-9a-f]{64}') { $hasHash = $true }
        }
        if (-not $hasHash) { Add-Error "Python lock pin '$key' has no SHA-256 artifact hash" }
    }
    if ($pythonClosureKeys) {
        foreach ($key in $pythonPinKeys.Keys) {
            if (-not $pythonClosureKeys.ContainsKey($key)) {
                Add-Error "Python lock pin missing from license closure: '$key'"
            }
        }
        foreach ($key in $pythonClosureKeys.Keys) {
            if (-not $pythonPinKeys.ContainsKey($key)) {
                Add-Error "Python license row missing from lock: '$key'"
            }
        }
    }
}

$npmLockPath = Join-Path $Root $lockFiles.Npm
if (-not (Test-Path -LiteralPath $npmLockPath -PathType Leaf)) {
    Add-Error "Missing lock evidence file: $($lockFiles.Npm)"
} else {
    $npmHash = Get-CanonicalTextSha256 -Path $npmLockPath
    if ($npmHash -ne $expectedLockHashes.Npm) {
        Add-Error "npm lock hash mismatch"
    }
    Add-Type -AssemblyName System.Web.Extensions
    $serializer = New-Object System.Web.Script.Serialization.JavaScriptSerializer
    $serializer.MaxJsonLength = [int]::MaxValue
    $npmLock = $serializer.DeserializeObject((Get-Content -LiteralPath $npmLockPath -Raw))
    if ($npmLock["lockfileVersion"] -ne 3) { Add-Error "npm lockfileVersion must be 3" }
    $npmRoot = $npmLock["packages"][""]
    foreach ($id in $npmDirectDependencies.Keys) {
        $expected = $npmDirectDependencies[$id]
        $matchingRows = @($rows | Where-Object {
            $_.Id -eq $id -and (Split-Path $_.Path -Leaf) -eq "DEPENDENCY_BASELINE.md"
        })
        if ($matchingRows.Count -ne 1) {
            Add-Error "Expected one direct npm evidence row '$id'"
            continue
        }
        $row = $matchingRows[0]
        $encodedPackage = $expected.Package.Replace("/", "%2F")
        $expectedSource = "https://registry.npmjs.org/$encodedPackage/$($expected.Version)"
        if ($row.Source -ine $expectedSource -or $row.Version -ne $expected.Version) {
            Add-Error "Direct npm evidence row '$id' does not match $($expected.Package)@$($expected.Version)"
        }
        if ($npmRoot[$expected.Section][$expected.Package] -ne $expected.Version) {
            Add-Error "npm root $($expected.Section) does not match $($expected.Package)@$($expected.Version)"
        }
        $packageKey = "node_modules/$($expected.Package)"
        if ($npmLock["packages"][$packageKey]["version"] -ne $expected.Version) {
            Add-Error "npm package entry does not match $($expected.Package)@$($expected.Version)"
        }
        if ($row.Authority -ne $npmLock["packages"][$packageKey]["license"]) {
            Add-Error "Direct npm evidence license does not match lock for '$id'"
        }
    }
    if ($npmRoot["dependencies"].Count -ne 3 -or $npmRoot["devDependencies"].Count -ne 13) {
        Add-Error "npm root must contain exactly 3 dependencies and 13 devDependencies"
    }
    $npmPackages = @($npmLock["packages"].GetEnumerator() | Where-Object { $_.Key -ne "" })
    if ($npmPackages.Count -ne 166) {
        Add-Error "npm closure must contain 166 package entries; observed $($npmPackages.Count)"
    }
    foreach ($property in $npmPackages) {
        $package = $property.Value
        if ([string]::IsNullOrWhiteSpace([string]$package["version"]) -or
            [string]::IsNullOrWhiteSpace([string]$package["resolved"]) -or
            [string]::IsNullOrWhiteSpace([string]$package["integrity"]) -or
            [string]::IsNullOrWhiteSpace([string]$package["license"])) {
            Add-Error "Incomplete npm closure entry '$($property.Key)'"
            continue
        }
        $packageName = @($property.Key -split 'node_modules/')[-1]
        $packageBaseName = @($packageName -split '/')[-1]
        $expectedTarballSuffix = "/$packageName/-/$packageBaseName-$($package["version"]).tgz"
        $resolvedUri = $null
        try { $resolvedUri = [Uri]$package["resolved"] } catch { }
        if ($null -eq $resolvedUri -or
            $resolvedUri.Scheme -ne "https" -or
            $resolvedUri.Host -ne "registry.npmjs.org" -or
            [Uri]::UnescapeDataString($resolvedUri.AbsolutePath) -ine $expectedTarballSuffix -or
            -not (Test-NpmIntegrity -Integrity ([string]$package["integrity"]))) {
            Add-Error "Invalid npm registry/integrity evidence for '$($property.Key)'"
        }
        if ([string]$package["license"] -notin $allowedNpmLicenses) {
            Add-Error "Unreviewed npm license '$($package["license"])' for '$($property.Key)'"
        }
    }
}

$readyChecks = @(
    @{ Enabled = $RequireDependencyReady; Name = "DEPENDENCY_BASELINE.md" },
    @{ Enabled = $RequireProviderReady; Name = "PROVIDER_POLICY_EVIDENCE.md" },
    @{ Enabled = $RequireDistributionReady; Name = "DISTRIBUTION_EVIDENCE.md" }
)
foreach ($check in $readyChecks) {
    if (-not $check.Enabled) { continue }
    $blockedForFile = @($rows | Where-Object {
        (Split-Path $_.Path -Leaf) -eq $check.Name -and $_.Status -eq "explicitly-blocked"
    })
    if ($blockedForFile.Count -gt 0) {
        Add-Error "$($check.Name) is not ready; explicitly-blocked rows=$($blockedForFile.Count)"
    }
}

if ($errors.Count -gt 0) {
    Write-Output "EVIDENCE_VALIDATION_FAIL errors=$($errors.Count) rows=$($rows.Count)"
    foreach ($errorMessage in $errors) { Write-Output "- $errorMessage" }
    exit 1
}

$blocked = @($rows | Where-Object { $_.Status -eq "explicitly-blocked" }).Count
Write-Output "EVIDENCE_VALIDATION_PASS rows=$($rows.Count) explicitly_blocked=$blocked python_pins=54 npm_packages=166"
exit 0
