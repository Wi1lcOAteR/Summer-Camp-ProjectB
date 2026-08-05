param(
    [string]$RuntimeRoot,
    [switch]$Offline,
    [switch]$LicenseOnly,
    [string]$LicenseRoot,
    [string]$LicenseEvidencePath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not $RuntimeRoot) {
    $RuntimeRoot = Join-Path $repo 'tmp/toolchains/f01a'
}
$RuntimeRoot = [IO.Path]::GetFullPath($RuntimeRoot)

$artifacts = @(
    [pscustomobject]@{
        Name = 'python'
        Uri = 'https://www.python.org/ftp/python/3.14.6/python-3.14.6-embed-amd64.zip'
        Hash = 'df901e84a896ff1ee720ad03377e0c8d8c2244fda79808aeeaff6316df1cb75c'
        Archive = 'python-3.14.6-embed-amd64.zip'
        Destination = 'python-3.14.6'
    },
    [pscustomobject]@{
        Name = 'uv'
        Uri = 'https://github.com/astral-sh/uv/releases/download/0.11.14/uv-x86_64-pc-windows-msvc.zip'
        Hash = '52ba5d19409aaa688a8a1a6ec8dfb6a4817230d20186e75f4006105c3e39a846'
        Archive = 'uv-0.11.14-windows-x64.zip'
        Destination = 'uv-0.11.14'
    },
    [pscustomobject]@{
        Name = 'node'
        Uri = 'https://nodejs.org/dist/v24.18.0/node-v24.18.0-win-x64.zip'
        Hash = '0ae68406b42d7725661da979b1403ec9926da205c6770827f33aac9d8f26e821'
        Archive = 'node-v24.18.0-win-x64.zip'
        Destination = 'node-v24.18.0-win-x64'
    }
)

function Stop-Bootstrap {
    param([string]$Code)
    throw [IO.InvalidDataException]::new("BOOTSTRAP_ERROR $Code")
}

$projectLocalRoot = [IO.Path]::GetFullPath((Join-Path $repo 'tmp'))
$projectLocalPrefix = $projectLocalRoot.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
if (-not $RuntimeRoot.StartsWith($projectLocalPrefix, [StringComparison]::OrdinalIgnoreCase)) {
    Stop-Bootstrap 'runtime_root_outside_project'
}

function Assert-NoReparsePath {
    param([string]$Path)

    $candidate = [IO.Path]::GetFullPath($Path)
    while ($true) {
        if (Test-Path -LiteralPath $candidate) {
            $item = Get-Item -LiteralPath $candidate -Force
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                Stop-Bootstrap 'runtime_root_reparse'
            }
        }
        if ($candidate.Equals($projectLocalRoot, [StringComparison]::OrdinalIgnoreCase)) { break }
        $parent = [IO.Directory]::GetParent($candidate)
        if ($null -eq $parent) { break }
        $candidate = $parent.FullName
    }
}

function Assert-ChildPath {
    param([string]$Path)
    $fullPath = [IO.Path]::GetFullPath($Path)
    $rootPrefix = $RuntimeRoot.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if (-not $fullPath.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        Stop-Bootstrap 'path_escape'
    }
    Assert-NoReparsePath $fullPath
}

Assert-NoReparsePath $RuntimeRoot

function Get-FileSha256 {
    param([string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-GitBlobSha1 {
    param([byte[]]$Bytes)
    $header = [Text.Encoding]::ASCII.GetBytes("blob $($Bytes.Length)`0")
    $payload = [byte[]]::new($header.Length + $Bytes.Length)
    [Array]::Copy($header, 0, $payload, 0, $header.Length)
    [Array]::Copy($Bytes, 0, $payload, $header.Length, $Bytes.Length)
    return ([Security.Cryptography.SHA1]::Create().ComputeHash($payload) | ForEach-Object { $_.ToString('x2') }) -join ''
}

function Stop-License {
    param([string]$Code)
    throw [IO.InvalidDataException]::new("BOOTSTRAP_LICENSE_ERROR $Code")
}

function Install-BootstrapLicenses {
    param(
        [string]$Root,
        [string]$EvidencePath,
        [switch]$OfflineMode
    )

    $expectedEvidenceHash = 'FD65C5D2F8421F7B99AE4D540B80A8BBED1C28C78EF45851F7C6E5051034F310'
    function Test-LicenseFile {
        param([string]$Path, $Identity)
        if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
        if (((Get-Item -LiteralPath $Path -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { return $false }
        $content = [IO.File]::ReadAllBytes($Path)
        return $content.Length -eq $Identity.Bytes -and (Get-FileSha256 $Path) -ieq $Identity.Hash -and (Get-GitBlobSha1 $content) -ceq $Identity.Blob
    }

    $repoPrefix = $repo.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    $rootFull = [IO.Path]::GetFullPath($Root)
    if (-not $rootFull.StartsWith($repoPrefix, [StringComparison]::OrdinalIgnoreCase)) { Stop-License 'license_root_outside_project' }
    Assert-NoReparsePath $rootFull
    if (-not (Test-Path -LiteralPath $EvidencePath -PathType Leaf)) { Stop-License 'evidence_missing' }
    if ((Get-FileSha256 $EvidencePath) -ine $expectedEvidenceHash) { Stop-License 'evidence_hash_mismatch' }

    $text = [IO.File]::ReadAllText($EvidencePath, [Text.UTF8Encoding]::new($false, $true))
    $rows = @{}
    foreach ($line in ($text -split "`r?`n")) {
        if ($line -notmatch '^\| `(?<target>licenses/bootstrap/[^`]+)` \| [^|]+ \| (?<immutable>[^|]+) \| `(?<blob>[0-9a-f]{40})` \| (?<bytes>[1-9][0-9]*) \| `(?<hash>[0-9A-Fa-f]{64})` \|') { continue }
        if ($rows.ContainsKey($Matches.target)) { Stop-License 'duplicate_evidence_target' }
        $rows[$Matches.target] = [pscustomobject]@{ Target = $Matches.target; Immutable = $Matches.immutable.Trim(); Blob = $Matches.blob; Bytes = [int64]$Matches.bytes; Hash = $Matches.hash }
    }
    $expected = @('licenses/bootstrap/uv-LICENSE-APACHE','licenses/bootstrap/uv-LICENSE-MIT','licenses/bootstrap/cpython-LICENSE','licenses/bootstrap/node-LICENSE','licenses/bootstrap/npm-LICENSE')
    if ($rows.Count -ne $expected.Count) { Stop-License 'evidence_row_count' }

    [void](New-Item -ItemType Directory -Path $rootFull -Force)
    foreach ($target in $expected) {
        if (-not $rows.ContainsKey($target)) { Stop-License 'evidence_target_missing' }
        $row = $rows[$target]
        $immutable = $row.Immutable.Trim().Trim('`').Trim()
        $raw = [regex]::Match($immutable, 'https://raw\.githubusercontent\.com/(?<owner>[^/\s`]+)/(?<project>[^/\s`]+)/(?<commit>[0-9a-f]{40})/(?<path>[^\s`]+)(?:`)?$')
        $commits = @([regex]::Matches($row.Immutable, '(?i)[0-9a-f]{40}') | ForEach-Object { $_.Value.ToLowerInvariant() } | Select-Object -Unique)
        if (-not $raw.Success -or $commits.Count -ne 1 -or $raw.Groups['commit'].Value.ToLowerInvariant() -cne $commits[0]) { Stop-License 'evidence_not_immutable' }
        $destination = Join-Path $rootFull ($target.Substring('licenses/bootstrap/'.Length))
        $destinationExists = Test-Path -LiteralPath $destination
        if ($destinationExists -and (-not (Test-Path -LiteralPath $destination -PathType Leaf) -or ((Get-Item -LiteralPath $destination -Force).Attributes -band [IO.FileAttributes]::ReparsePoint))) { Stop-License 'license_destination_not_file' }
        $validExisting = Test-LicenseFile $destination $row
        if ($destinationExists) {
            if (-not $validExisting -and $OfflineMode) { Stop-License 'license_bytes_mismatch' }
        }
        if ($validExisting) { continue }
        if ($OfflineMode) { Stop-License 'license_missing' }

        $bytes = $null
        $apiUri = "https://api.github.com/repos/$($raw.Groups['owner'].Value)/$($raw.Groups['project'].Value)/contents/$($raw.Groups['path'].Value)?ref=$($raw.Groups['commit'].Value)"
        $headers = @{ Accept = 'application/vnd.github+json'; 'X-GitHub-Api-Version' = '2022-11-28'; 'User-Agent' = 'ProjectB-bootstrap' }
        $api = $null
        try { $api = Invoke-RestMethod -Uri $apiUri -Headers $headers -TimeoutSec 30 }
        catch { $api = $null }
        if ($null -ne $api) {
            if ($api.encoding -cne 'base64' -or $api.sha -cne $row.Blob -or [int64]$api.size -ne $row.Bytes) { Stop-License 'license_api_metadata_mismatch' }
            try { $bytes = [Convert]::FromBase64String(([string]$api.content)) }
            catch { Stop-License 'license_api_decode_failed' }
        }
        else {
            try {
                $response = Invoke-WebRequest -UseBasicParsing -Uri ("https://raw.githubusercontent.com/$($raw.Groups['owner'].Value)/$($raw.Groups['project'].Value)/$($raw.Groups['commit'].Value)/$($raw.Groups['path'].Value)") -Headers @{ 'User-Agent' = 'ProjectB-bootstrap' } -TimeoutSec 30
                $bytes = [byte[]]$response.RawContentStream.ToArray()
            }
            catch { Stop-License 'license_transport_failed' }
        }
        if ($bytes.Length -ne $row.Bytes -or (Get-GitBlobSha1 $bytes) -cne $row.Blob) { Stop-License 'license_blob_mismatch' }
        $actualHash = ([Security.Cryptography.SHA256]::Create().ComputeHash($bytes) | ForEach-Object { $_.ToString('x2') }) -join ''
        if ($actualHash -ine $row.Hash) { Stop-License 'license_hash_mismatch' }
        $partial = "$destination.partial"
        if (Test-Path -LiteralPath $partial) { Stop-License 'license_partial_exists' }
        $createdPartial = $false
        try {
            try {
                $stream = [IO.File]::Open($partial, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
                $createdPartial = $true
            }
            catch { Stop-License 'license_partial_exists' }
            try { $stream.Write($bytes, 0, $bytes.Length); $stream.Flush($true) }
            finally { $stream.Dispose() }
            Move-Item -LiteralPath $partial -Destination $destination -Force
        }
        finally { if ($createdPartial -and (Test-Path -LiteralPath $partial)) { Remove-Item -LiteralPath $partial -Force -ErrorAction SilentlyContinue } }
    }
    foreach ($target in $expected) {
        $destination = Join-Path $rootFull ($target.Substring('licenses/bootstrap/'.Length))
        if (-not (Test-LicenseFile $destination $rows[$target])) { Stop-License 'license_final_validation_failed' }
    }
    Write-Output 'BOOTSTRAP_LICENSE_PASS files=5'
}

function Get-NpmCommand {
    param([string]$NodeRoot)
    $command = Join-Path $NodeRoot 'npm.cmd'
    if ([IO.Path]::GetFileName($command) -cne 'npm.cmd' -or [IO.Path]::GetExtension($command) -ceq '.ps1') {
        Stop-Bootstrap 'npm_ps1_blocked'
    }
    return $command
}

function Enable-PythonSitePackages {
    param([string]$PythonRoot)

    $pathFile = Join-Path $PythonRoot 'python314._pth'
    Assert-ChildPath $pathFile
    if (-not (Test-Path -LiteralPath $pathFile -PathType Leaf)) { Stop-Bootstrap 'python_path_config_missing' }
    $content = [IO.File]::ReadAllText($pathFile, [Text.UTF8Encoding]::new($false, $true))
    if ($content -match '(?m)^import site\s*$') { return }
    if ($content -notmatch '(?m)^#import site\s*$') { Stop-Bootstrap 'python_path_config_invalid' }
    $updated = [regex]::Replace($content, '(?m)^#import site\s*$', 'import site')
    [IO.File]::WriteAllText($pathFile, $updated, [Text.UTF8Encoding]::new($false))
}

function Test-PythonRuntime {
    param([string]$Python)
    if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { return $false }
    $output = (& $Python --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $output -cne 'Python 3.14.6') {
        Stop-Bootstrap 'python_version_mismatch'
    }
    return $true
}

function Test-NodeRuntime {
    param([string]$Node, [string]$Npm)
    if (-not (Test-Path -LiteralPath $Node -PathType Leaf) -or -not (Test-Path -LiteralPath $Npm -PathType Leaf)) { return $false }
    $nodeVersion = (& $Node --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $nodeVersion -cne 'v24.18.0') { Stop-Bootstrap 'node_version_mismatch' }
    $npmVersion = (& $Npm --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $npmVersion -cne '11.16.0') { Stop-Bootstrap 'npm_version_mismatch' }
    return $true
}

function Test-UvRuntime {
    param([string]$Uv)
    if (-not (Test-Path -LiteralPath $Uv -PathType Leaf)) { return $false }
    $output = (& $Uv --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $output -notmatch '^uv 0\.11\.14(?: |$)') {
        Stop-Bootstrap 'uv_version_mismatch'
    }
    return $true
}

if (-not $LicenseRoot) { $LicenseRoot = Join-Path $repo 'licenses/bootstrap' }
if (-not $LicenseEvidencePath) { $LicenseEvidencePath = Join-Path $repo 'docs/engineering/BOOTSTRAP_LICENSE_EVIDENCE.md' }
$licenseReceipt = @(Install-BootstrapLicenses -Root $LicenseRoot -EvidencePath $LicenseEvidencePath -OfflineMode:$Offline)
if ($LicenseOnly) { $licenseReceipt | Write-Output; exit 0 }

$downloads = Join-Path $RuntimeRoot 'downloads'
$runtimes = Join-Path $RuntimeRoot 'runtimes'
$pythonRoot = Join-Path $runtimes 'python-3.14.6'
$uvRoot = Join-Path $runtimes 'uv-0.11.14'
$nodeRoot = Join-Path $runtimes 'node-v24.18.0-win-x64'
$python = Join-Path $pythonRoot 'python.exe'
$uv = Join-Path $uvRoot 'uv.exe'
$node = Join-Path $nodeRoot 'node.exe'
$npm = Get-NpmCommand $nodeRoot

foreach ($path in @($downloads, $runtimes, $pythonRoot, $uvRoot, $nodeRoot)) {
    Assert-ChildPath $path
}

if (Test-Path -LiteralPath $python -PathType Leaf) { Enable-PythonSitePackages $pythonRoot }
$pythonReady = Test-PythonRuntime $python
$nodeReady = Test-NodeRuntime $node $npm
$uvReady = Test-UvRuntime $uv
if (-not ($pythonReady -and $nodeReady -and $uvReady)) {
    [void](New-Item -ItemType Directory -Path $downloads -Force)
    [void](New-Item -ItemType Directory -Path $runtimes -Force)

    foreach ($artifact in $artifacts) {
        $archive = Join-Path $downloads $artifact.Archive
        Assert-ChildPath $archive
        if (Test-Path -LiteralPath $archive -PathType Leaf) {
            if ((Get-FileSha256 $archive) -cne $artifact.Hash) {
                Remove-Item -LiteralPath $archive -Force
                Stop-Bootstrap "artifact_hash_mismatch $($artifact.Name)"
            }
        }
        else {
            if ($Offline) { Stop-Bootstrap "artifact_missing $($artifact.Name)" }
            $partial = "$archive.partial"
            Assert-ChildPath $partial
            try {
                Invoke-WebRequest -UseBasicParsing -Uri $artifact.Uri -OutFile $partial -TimeoutSec 120
                if ((Get-FileSha256 $partial) -cne $artifact.Hash) {
                    Stop-Bootstrap "artifact_hash_mismatch $($artifact.Name)"
                }
                Move-Item -LiteralPath $partial -Destination $archive
            }
            finally {
                if (Test-Path -LiteralPath $partial) { Remove-Item -LiteralPath $partial -Force }
            }
        }
    }

    foreach ($artifact in $artifacts) {
        $destination = Join-Path $runtimes $artifact.Destination
        $archive = Join-Path $downloads $artifact.Archive
        Assert-ChildPath $destination
        if (-not (Test-Path -LiteralPath $destination -PathType Container)) {
            $staging = "$destination.extracting"
            Assert-ChildPath $staging
            try {
                [void](New-Item -ItemType Directory -Path $staging -Force)
                Expand-Archive -LiteralPath $archive -DestinationPath $staging
                if ($artifact.Name -eq 'node') {
                    $nested = Join-Path $staging 'node-v24.18.0-win-x64'
                    if (-not (Test-Path -LiteralPath $nested -PathType Container)) { Stop-Bootstrap 'node_archive_layout' }
                    Move-Item -LiteralPath $nested -Destination $destination
                }
                else {
                    Move-Item -LiteralPath $staging -Destination $destination
                    $staging = $null
                }
            }
            finally {
                if ($staging -and (Test-Path -LiteralPath $staging)) { Remove-Item -LiteralPath $staging -Recurse -Force }
            }
        }
    }

    Enable-PythonSitePackages $pythonRoot
    $pythonReady = Test-PythonRuntime $python
    $nodeReady = Test-NodeRuntime $node $npm
    $uvReady = Test-UvRuntime $uv
    if (-not ($pythonReady -and $nodeReady -and $uvReady)) { Stop-Bootstrap 'runtime_incomplete' }
}

[pscustomobject]@{
    Py = [IO.Path]::GetFullPath($python)
    Npm = [IO.Path]::GetFullPath($npm)
    Node = [IO.Path]::GetFullPath($node)
    Uv = [IO.Path]::GetFullPath($uv)
    RuntimeRoot = $RuntimeRoot
}
