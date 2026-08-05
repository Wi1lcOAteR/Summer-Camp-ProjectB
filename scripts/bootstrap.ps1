param(
    [string]$RuntimeRoot,
    [switch]$Offline
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
