param(
    [string]$Python = "python",
    [string]$Output = "dist/ProjectB.exe"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
function Assert-NoReparse([string]$Candidate) {
    if (-not (Test-Path -LiteralPath $Candidate)) { return }
    $item = Get-Item -LiteralPath $Candidate -Force
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw "reparse_path" }
    foreach ($child in @(Get-ChildItem -LiteralPath $Candidate -Force -Recurse -ErrorAction Stop)) {
        if (($child.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw "reparse_path" }
    }
}
$architecture = if ($env:PROCESSOR_ARCHITEW6432) { $env:PROCESSOR_ARCHITEW6432 } else { $env:PROCESSOR_ARCHITECTURE }
if ($architecture -cne "AMD64") { throw "windows_x64_required" }
$pythonVersion = (& $Python --version 2>&1 | Out-String).Trim()
if ($pythonVersion -notmatch '^Python 3\.14\.6(?:\r?\n)?$') { throw "python_3_14_6_required" }
$pythonBits = (& $Python -c "import struct; print(struct.calcsize('P') * 8)" 2>&1 | Out-String).Trim()
if ($pythonBits -cne "64") { throw "python_x64_required" }
$pyinstallerVersion = (& $Python -m PyInstaller --version 2>&1 | Out-String).Trim()
if ($pyinstallerVersion -notmatch '^6\.21\.0$') { throw "pyinstaller_6_21_0_required" }
$outputPath = [IO.Path]::GetFullPath((Join-Path (Get-Location) $Output))
if ([IO.Path]::GetFileName($outputPath) -cne "ProjectB.exe") {
    throw "output_must_be_ProjectB.exe"
}
$frontendIndex = Join-Path $repo "frontend\dist\index.html"
if (-not (Test-Path -LiteralPath $frontendIndex -PathType Leaf)) {
    $npm = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if ($null -eq $npm) { throw "frontend_dist_missing" }
    $node = Get-Command node.exe -ErrorAction SilentlyContinue
    if ($null -eq $node) { throw "node_missing" }
    if ((& node.exe --version 2>&1 | Out-String).Trim() -cne "v24.18.0") { throw "node_24_18_0_required" }
    if ((& npm.cmd --version 2>&1 | Out-String).Trim() -cne "11.16.0") { throw "npm_11_16_0_required" }
    Push-Location $repo
    try {
        & npm.cmd --prefix frontend run build
        if ($LASTEXITCODE -ne 0) { throw "frontend_build_failed" }
    } finally { Pop-Location }
    if (-not (Test-Path -LiteralPath $frontendIndex -PathType Leaf)) { throw "frontend_dist_missing" }
}
$notices = Join-Path $repo "licenses\THIRD_PARTY_NOTICES.md"
if (-not (Test-Path -LiteralPath $notices -PathType Leaf)) { throw "third_party_notices_missing" }

$outputDirectory = Split-Path -Parent $outputPath
$workDirectory = Join-Path $repo "tmp\dist01-pyinstaller"
Assert-NoReparse $outputDirectory
Assert-NoReparse $workDirectory
New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
if (Test-Path -LiteralPath $outputPath) { Remove-Item -LiteralPath $outputPath -Force }
if (Test-Path -LiteralPath $workDirectory) { Remove-Item -LiteralPath $workDirectory -Recurse -Force }
New-Item -ItemType Directory -Force -Path $workDirectory | Out-Null

Push-Location $repo
try {
    & $Python -m PyInstaller --clean --noconfirm --distpath $outputDirectory --workpath $workDirectory packaging\windows\ProjectB.spec
    if ($LASTEXITCODE -ne 0) { throw "pyinstaller_failed" }
} finally { Pop-Location }
if (-not (Test-Path -LiteralPath $outputPath -PathType Leaf)) { throw "artifact_missing" }
$packageManifest = Join-Path $workDirectory "ProjectB\PKG-00.toc"
if (-not (Test-Path -LiteralPath $packageManifest -PathType Leaf)) { throw "package_manifest_missing" }
$packageText = [IO.File]::ReadAllText($packageManifest, [Text.UTF8Encoding]::new($false, $true))
foreach ($resource in @("frontend_dist\\index.html", "frontend_dist\\assets", "licenses\\THIRD_PARTY_NOTICES.md", "pypdfium2_raw\\pdfium.dll")) {
    if (-not $packageText.Contains($resource)) { throw "package_resource_missing:$resource" }
}
Write-Output ("WINDOWS_BUILD_PASS artifact={0}" -f $outputPath)
