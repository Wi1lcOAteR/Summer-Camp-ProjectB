param(
    [Parameter(Mandatory = $true)][string]$Artifact,
    [Parameter(Mandatory = $true)][string]$DataRoot,
    [int]$Port = 4173
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$artifactPath = [IO.Path]::GetFullPath($Artifact)
$dataPath = [IO.Path]::GetFullPath($DataRoot)
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
$tmpRoot = [IO.Path]::GetFullPath((Join-Path $repo "tmp"))
$name = [IO.Path]::GetFileNameWithoutExtension($artifactPath)
$preexistingProcessIds = @()
$ownedProcessIds = @()
$process = $null

function Assert-NoReparse([string]$Candidate) {
    if (-not (Test-Path -LiteralPath $Candidate)) { return }
    $item = Get-Item -LiteralPath $Candidate -Force
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw "reparse_path" }
    foreach ($child in @(Get-ChildItem -LiteralPath $Candidate -Force -Recurse -ErrorAction Stop)) {
        if (($child.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw "reparse_path" }
    }
}

try {
    if (-not (Test-Path -LiteralPath $artifactPath -PathType Leaf)) { throw "artifact_missing" }
    if (-not $dataPath.StartsWith($tmpRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "data_root_must_be_disposable"
    }
    $preexistingProcessIds = @(Get-Process -Name $name -ErrorAction SilentlyContinue |
        Where-Object { $_.Path -eq $artifactPath } |
        Select-Object -ExpandProperty Id)
    if ($preexistingProcessIds.Count -gt 0) { throw "artifact_already_running" }
    Assert-NoReparse $dataPath
    if (Test-Path -LiteralPath $dataPath) { Remove-Item -LiteralPath $dataPath -Recurse -Force }
    New-Item -ItemType Directory -Force -Path $dataPath | Out-Null
    $processArguments = '--data-dir "{0}" --port {1}' -f $dataPath, $Port
    $process = Start-Process -FilePath $artifactPath -ArgumentList $processArguments -PassThru
    $ownedProcessIds = @($process.Id)
    $settings = $null
    for ($attempt = 0; $attempt -lt 60; $attempt++) {
        Start-Sleep -Milliseconds 250
        try {
            $response = Invoke-WebRequest -UseBasicParsing -Uri ("http://127.0.0.1:{0}/api/settings" -f $Port) -TimeoutSec 2
            if ($response.StatusCode -eq 200) { $settings = $response.Content | ConvertFrom-Json; break }
        } catch { if ($process.HasExited) { throw "process_exited" } }
    }
    if ($null -eq $settings) { throw "startup_timeout" }
    if ($settings.profile -ne "local" -or $settings.bind_host -ne "127.0.0.1" -or $settings.provider_mode -ne "L") {
        throw "local_profile_contract"
    }
    $webResponse = Invoke-WebRequest -UseBasicParsing -Uri ("http://127.0.0.1:{0}/" -f $Port)
    if ($webResponse.StatusCode -ne 200 -or $webResponse.Content -notmatch 'id="root"') { throw "webui_resource_contract" }
    $coursesResponse = Invoke-WebRequest -UseBasicParsing -Uri ("http://127.0.0.1:{0}/api/courses" -f $Port)
    $courses = $coursesResponse.Content | ConvertFrom-Json
    if ($coursesResponse.StatusCode -ne 200 -or "courses" -notin $courses.PSObject.Properties.Name) {
        throw "courses_contract"
    }
    $credentialResponse = Invoke-WebRequest -UseBasicParsing -Uri ("http://127.0.0.1:{0}/api/credentials/provider" -f $Port)
    $credential = $credentialResponse.Content | ConvertFrom-Json
    if ($credential.configured -ne $false) { throw "credential_status_contract" }
    if (-not (Test-Path -LiteralPath (Join-Path $dataPath "projectb.sqlite3") -PathType Leaf)) {
        throw "data_root_contract"
    }
    $ownedProcessIds += @(Get-Process -Name $name -ErrorAction SilentlyContinue |
        Where-Object { $_.Path -eq $artifactPath -and $_.Id -notin $preexistingProcessIds } |
        Select-Object -ExpandProperty Id)
    $listenerProcessIds = @($ownedProcessIds)
    $listeners = @($listenerProcessIds | Sort-Object -Unique | ForEach-Object {
        Get-NetTCPConnection -OwningProcess $_ -State Listen -ErrorAction SilentlyContinue
    })
    foreach ($listener in $listeners) {
        if ($listener.LocalAddress -notin @("127.0.0.1", "::1")) { throw "non_loopback_listener" }
    }
    Write-Output ("WINDOWS_SMOKE_PASS profile={0} credential_configured={1}" -f $settings.profile, $credential.configured)
} finally {
    if ($null -ne $process) { $ownedProcessIds += $process.Id }
    Assert-NoReparse $dataPath
    foreach ($processId in @($ownedProcessIds | Sort-Object -Unique)) {
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
    foreach ($processId in @($ownedProcessIds | Sort-Object -Unique)) {
        Wait-Process -Id $processId -Timeout 5 -ErrorAction SilentlyContinue
    }
    if ($dataPath.StartsWith($tmpRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        Remove-Item -LiteralPath $dataPath -Recurse -Force -ErrorAction SilentlyContinue
    }
}
