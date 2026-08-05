Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$evidence = Join-Path $repo 'docs\engineering\BOOTSTRAP_LICENSE_EVIDENCE.md'
$bootstrap = Join-Path $repo 'scripts\bootstrap.ps1'
$expectedEvidenceHash = 'FD65C5D2F8421F7B99AE4D540B80A8BBED1C28C78EF45851F7C6E5051034F310'
$targets = [ordered]@{
    'licenses/bootstrap/uv-LICENSE-APACHE' = @{ bytes = 11357; hash = 'C71D239DF91726FC519C6EB72D318EC65820627232B2F796219E87DCF35D0AB4'; blob = '261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64' }
    'licenses/bootstrap/uv-LICENSE-MIT' = @{ bytes = 1077; hash = '860E3D7A86B84E6A7012C7A635FC64DF475CEBC6CCE34DFEB73A5982EC58176C'; blob = '014835144877ea9c926d027ece3e1a26290cf481' }
    'licenses/bootstrap/cpython-LICENSE' = @{ bytes = 13804; hash = 'B0E25A78CFFB43F4D92DE8B61CCFA1F1F98ECBC22330B54B5251E7B6BA010231'; blob = '20cf39097c68baa17cc566b64e76d34ebf034044' }
    'licenses/bootstrap/node-LICENSE' = @{ bytes = 157606; hash = '148EACF7863EF4329224A29398623077200A27194AA075569FAF4A0A85566CA5'; blob = '2842efa1288eef1de3a6778b5dd3519bc903308d' }
    'licenses/bootstrap/npm-LICENSE' = @{ bytes = 9742; hash = '7610D223851F421D315DF5E77974F1C68A04B97E02060E5BBBCF13D95E3CA257'; blob = '0b6c2287459632e4aaf63bd7d53eb9ba054b57ea' }
}

function Fail([string]$Code) { Write-Output "CONTRACT_FAIL $Code"; exit 1 }
if (-not (Test-Path -LiteralPath $evidence -PathType Leaf)) { Fail 'evidence_missing' }
if ((Get-FileHash -LiteralPath $evidence -Algorithm SHA256).Hash -cne $expectedEvidenceHash) { Fail 'evidence_hash' }
$evidenceText = [IO.File]::ReadAllText($evidence, [Text.UTF8Encoding]::new($false, $true))
$rows = @{}
foreach ($line in ($evidenceText -split "`r?`n")) {
    if ($line -notmatch '^\| `licenses/bootstrap/(?<name>[^`]+)` \| (?<tag>[^|]+) \| (?<source>[^|]+) \| `(?<blob>[0-9a-f]{40})` \| (?<bytes>[0-9]+) \| `(?<hash>[0-9A-Fa-f]{64})` \|') { continue }
    $rows["licenses/bootstrap/$($Matches.name)"] = $Matches
}
if ($rows.Count -ne 5) { Fail 'evidence_rows' }
foreach ($target in $targets.Keys) {
    $path = Join-Path $repo ($target -replace '/', '\')
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { Fail "missing_$($target.Split('/')[-1])" }
    $bytes = [IO.File]::ReadAllBytes($path)
    if ($bytes.Length -ne $targets[$target].bytes) { Fail "count_$($target.Split('/')[-1])" }
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -cne $targets[$target].hash) { Fail "hash_$($target.Split('/')[-1])" }
    $row = $rows[$target]
    if ($row.blob -cne $targets[$target].blob -or [int]$row.bytes -ne $bytes.Length -or $row.hash -cne $targets[$target].hash) { Fail "binding_$($target.Split('/')[-1])" }
    if ($row.source -notmatch 'https://raw\.githubusercontent\.com/[^/]+/[^/]+/(?<commit>[0-9a-f]{40})/[^\s]+$') { Fail "mutable_$($target.Split('/')[-1])" }
    if ($row.source -match '(?:releases/download|[?&]ref=|raw\.githubusercontent\.com/[^/]+/[^/]+/v\d)') { Fail "tag_$($target.Split('/')[-1])" }
}
if (-not (Test-Path -LiteralPath $bootstrap -PathType Leaf)) { Fail 'bootstrap_missing' }
$script = [IO.File]::ReadAllText($bootstrap, [Text.UTF8Encoding]::new($false, $true))
foreach ($needle in @('Install-BootstrapLicenses', 'api.github.com', 'FromBase64String', 'Get-FileHash', 'BOOTSTRAP_LICENSE_PASS')) { if ($script -notmatch [regex]::Escape($needle)) { Fail "bootstrap_$needle" } }
if ($script -match 'api\.github\.com/repos/.+ref=(?:0\.11\.14|v3\.14\.6|v24\.18\.0)') { Fail 'transport_tag_fallback' }

$sandbox = Join-Path $repo ("tmp/f01b-license-contract-$([guid]::NewGuid().ToString('N'))")
try {
    $harness = Join-Path $sandbox 'transport-harness.ps1'
    [void](New-Item -ItemType Directory -Path $sandbox -Force)
    $harnessSource = @'
param([string]$Bootstrap,[string]$Root,[string]$Case,[string]$Fixture,[string]$Log)
$map = @(
    @('uv','LICENSE-APACHE','uv-LICENSE-APACHE','261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64'),
    @('uv','LICENSE-MIT','uv-LICENSE-MIT','014835144877ea9c926d027ece3e1a26290cf481'),
    @('cpython','LICENSE','cpython-LICENSE','20cf39097c68baa17cc566b64e76d34ebf034044'),
    @('node','LICENSE','node-LICENSE','2842efa1288eef1de3a6778b5dd3519bc903308d'),
    @('cli','LICENSE','npm-LICENSE','0b6c2287459632e4aaf63bd7d53eb9ba054b57ea')
)
function Get-Entry([string]$Uri){foreach($e in $map){if($Uri -match "/$($e[0])/(?:contents/|[0-9a-f]{40}/)$($e[1])(?:\?|$)"){return @($e[2],$e[3])}};throw 'unknown_uri'}
function Invoke-RestMethod { param($Uri,$Headers,$TimeoutSec) Add-Content $Log 'api'; if($Case -in @('api_fail_raw_success','raw_wrong_bytes','both_fail')){throw 'api_transport'}; if($Case -eq 'api_null'){return $null}; $e=Get-Entry $Uri; $b=[IO.File]::ReadAllBytes((Join-Path $Fixture $e[0])); if($Case -eq 'api_wrong_bytes'){$b[0]=$b[0]-bxor 1}; $sha=if($Case -eq 'api_bad_metadata'){'0000000000000000000000000000000000000000'}else{$e[1]}; $size=if($Case -eq 'api_bad_size'){'not-a-count'}else{$b.Length}; [pscustomobject]@{encoding='base64';sha=$sha;size=$size;content=[Convert]::ToBase64String($b)} }
function Invoke-WebRequest { param($Uri,$Headers,$TimeoutSec,[switch]$UseBasicParsing) Add-Content $Log 'raw'; if($Case -in @('api_success','api_bad_metadata','api_bad_size','api_wrong_bytes','api_null','both_fail')){throw 'raw_forbidden'}; $e=Get-Entry $Uri; $b=[IO.File]::ReadAllBytes((Join-Path $Fixture $e[0])); if($Case -eq 'raw_wrong_bytes'){$b[0]=$b[0]-bxor 1}; [pscustomobject]@{RawContentStream=[IO.MemoryStream]::new($b)} }
& $Bootstrap -LicenseOnly -LicenseRoot $Root
'@
    [IO.File]::WriteAllText($harness, $harnessSource, [Text.UTF8Encoding]::new($false))
    $junctionTarget = Join-Path $sandbox 'junction-target'
    $junctionRoot = Join-Path $sandbox 'junction-root'
    [void](New-Item -ItemType Directory -Path $junctionTarget -Force)
    [void](New-Item -ItemType Junction -Path $junctionRoot -Target $junctionTarget)
    $oldPreference = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    $run = @(& (Join-Path $PSHOME 'powershell.exe') -NoProfile -File $bootstrap -LicenseOnly -Offline -LicenseRoot $junctionRoot 2>&1 | % { $_.ToString() })
    $exitCode = $LASTEXITCODE; $ErrorActionPreference = $oldPreference
    if ($exitCode -eq 0 -or ($run -join "`n") -notmatch 'runtime_root_reparse') { Fail 'license_root_reparse' }
    foreach ($case in @('api_success','api_fail_raw_success','api_bad_metadata','api_bad_size','api_wrong_bytes','api_null','raw_wrong_bytes','both_fail','partial_exists','destination_directory')) {
        $caseRoot = Join-Path $sandbox "case-$case"
        $log = Join-Path $sandbox "$case.log"
        if ($case -eq 'partial_exists') { [void](New-Item -ItemType Directory -Path $caseRoot -Force); [IO.File]::WriteAllText((Join-Path $caseRoot 'uv-LICENSE-APACHE.partial'), 'do-not-overwrite') }
        if ($case -eq 'destination_directory') { [void](New-Item -ItemType Directory -Path (Join-Path $caseRoot 'uv-LICENSE-APACHE') -Force) }
        $oldPreference = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
        $run = @(& (Join-Path $PSHOME 'powershell.exe') -NoProfile -File $harness -Bootstrap $bootstrap -Root $caseRoot -Case $case -Fixture (Join-Path $repo 'licenses/bootstrap') -Log $log 2>&1 | % { $_.ToString() })
        $exitCode = $LASTEXITCODE; $ErrorActionPreference = $oldPreference
        $calls = if (Test-Path $log) { @(Get-Content $log) } else { @() }
        if ($case -in @('api_success','api_fail_raw_success')) {
            if ($exitCode -ne 0 -or $run.Count -ne 1 -or $run[0] -cne 'BOOTSTRAP_LICENSE_PASS files=5') { Fail "transport_${case}_exit_${exitCode}_calls_$($calls -join ',')_$($run -join '-')" }
            if (@($calls | ? { $_ -eq 'api' }).Count -ne 5 -or @($calls | ? { $_ -eq 'raw' }).Count -ne $(if($case -eq 'api_success'){0}else{5})) { Fail "order_$case" }
        } else {
            $code = if($case -in @('api_bad_metadata','api_bad_size','api_null')){'license_api_metadata_mismatch'}elseif($case -eq 'both_fail'){'license_transport_failed'}elseif($case -eq 'partial_exists'){'license_partial_exists'}elseif($case -eq 'destination_directory'){'license_destination_not_file'}else{'license_blob_mismatch'}
            if ($exitCode -eq 0 -or ($run -join "`n") -notmatch $code) { Fail "negative_$case" }
            if ($case -eq 'partial_exists' -and [IO.File]::ReadAllText((Join-Path $caseRoot 'uv-LICENSE-APACHE.partial')) -cne 'do-not-overwrite') { Fail 'partial_overwritten' }
            if ($case -eq 'destination_directory' -and (Test-Path -LiteralPath (Join-Path $caseRoot 'uv-LICENSE-APACHE/uv-LICENSE-APACHE.partial'))) { Fail 'moved_inside_destination' }
        }
    }
    $licenseCopy = Join-Path $sandbox 'licenses/bootstrap'
    [void](New-Item -ItemType Directory -Path $licenseCopy -Force)
    foreach ($target in $targets.Keys) {
        $sourcePath = Join-Path $repo ($target -replace '/', '\')
        Copy-Item -LiteralPath $sourcePath -Destination (Join-Path $licenseCopy ($target.Split('/')[-1]))
    }
    $mutated = [IO.File]::ReadAllBytes((Join-Path $licenseCopy 'uv-LICENSE-APACHE'))
    $mutated[0] = $mutated[0] -bxor 1
    [IO.File]::WriteAllBytes((Join-Path $licenseCopy 'uv-LICENSE-APACHE'), $mutated)
    $pwsh = Join-Path $PSHOME 'powershell.exe'
    $oldPreference = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    $run = @(& $pwsh -NoProfile -File $bootstrap -LicenseOnly -Offline -LicenseRoot $licenseCopy 2>&1 | % { $_.ToString() })
    $ErrorActionPreference = $oldPreference
    if ($LASTEXITCODE -eq 0 -or ($run -join "`n") -notmatch 'license_bytes_mismatch') { Fail 'wrong_bytes_not_fail_closed' }
    $evidenceCopy = Join-Path $sandbox 'evidence.md'
    Copy-Item -LiteralPath $evidence -Destination $evidenceCopy
    $evidenceMutation = [IO.File]::ReadAllText($evidenceCopy) -replace 'C71D239DF91726FC519C6EB72D318EC65820627232B2F796219E87DCF35D0AB4', 'D71D239DF91726FC519C6EB72D318EC65820627232B2F796219E87DCF35D0AB4'
    [IO.File]::WriteAllText($evidenceCopy, $evidenceMutation, [Text.UTF8Encoding]::new($false))
    $oldPreference = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    $run = @(& $pwsh -NoProfile -File $bootstrap -LicenseOnly -Offline -LicenseRoot $licenseCopy -LicenseEvidencePath $evidenceCopy 2>&1 | % { $_.ToString() })
    $ErrorActionPreference = $oldPreference
    if ($LASTEXITCODE -eq 0 -or ($run -join "`n") -notmatch 'evidence_hash_mismatch') { Fail 'evidence_drift_not_fail_closed' }
}
finally { if (Test-Path -LiteralPath $sandbox) { Remove-Item -LiteralPath $sandbox -Recurse -Force } }
Write-Output 'license_targets'
Write-Output 'transport_and_evidence_binding'
Write-Output 'BOOTSTRAP_LICENSE_CONTRACT_PASS'
