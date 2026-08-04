Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scanner = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\bootstrap_scan_credentials.ps1'))
if (-not (Test-Path -LiteralPath $scanner -PathType Leaf)) {
    Write-Output 'CONTRACT_RED scanner_missing'
    exit 1
}

function Stop-Contract {
    param([string]$Code)
    Write-Output "CONTRACT_FAIL $Code"
    exit 1
}

function Invoke-Scanner {
    param([string[]]$Arguments)
    $output = @(& pwsh -NoProfile -File $scanner @Arguments 2>&1 | ForEach-Object { $_.ToString() })
    [pscustomobject]@{ ExitCode = $LASTEXITCODE; Output = $output }
}

function Assert-ExactResult {
    param($Result, [int]$ExitCode, [string[]]$Output, [string]$Code)
    if ($Result.ExitCode -ne $ExitCode -or $Result.Output.Count -ne $Output.Count) {
        Stop-Contract $Code
    }
    for ($index = 0; $index -lt $Output.Count; $index++) {
        if ($Result.Output[$index] -cne $Output[$index]) { Stop-Contract $Code }
    }
}

function Assert-OperationalFailure {
    param($Result, [string]$ExpectedCode, [string]$ExpectedPath, [string]$Code)
    if ($Result.ExitCode -ne 3 -or $Result.Output.Count -ne 1) { Stop-Contract $Code }
    try { $record = $Result.Output[0] | ConvertFrom-Json -ErrorAction Stop }
    catch { Stop-Contract $Code }
    if ($record.code -cne $ExpectedCode -or $record.source -cne 'path') { Stop-Contract $Code }
    if ($ExpectedPath -and $record.path -cne $ExpectedPath) { Stop-Contract $Code }
    $allowed = @('source', 'path', 'code')
    foreach ($name in $record.PSObject.Properties.Name) {
        if ($name -notin $allowed) { Stop-Contract $Code }
    }
}

function Assert-DirectCase {
    param([string]$Name, [string]$Text, [string]$Rule, [bool]$Match, [Text.Encoding]$Encoding)
    $file = "$Name.txt"
    [IO.File]::WriteAllText((Join-Path (Get-Location).ProviderPath $file), $Text, $Encoding)
    if ($Match) {
        $expected = "{`"source`":`"path`",`"path`":`"$file`",`"rule`":`"$Rule`"}"
        Assert-ExactResult (Invoke-Scanner @('-Path', $file)) 2 @($expected) $Name
    }
    else {
        Assert-ExactResult (Invoke-Scanner @('-Path', $file)) 0 @('CREDENTIAL_SCAN_PASS files=1') $Name
    }
}

$sandbox = Join-Path ([IO.Path]::GetTempPath()) ('projectb-f01s1a-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($sandbox) | Out-Null
try {
    Push-Location $sandbox
    try {
        $utf8 = [Text.UTF8Encoding]::new($false)
        [IO.File]::WriteAllText((Join-Path $sandbox 'clean.txt'), 'ordinary public text', $utf8)
        [IO.File]::WriteAllText((Join-Path $sandbox 'other.txt'), 'more public text', $utf8)
        [IO.File]::WriteAllBytes((Join-Path $sandbox 'invalid.txt'), [byte[]](0xC3, 0x28))
        [IO.File]::WriteAllBytes((Join-Path $sandbox 'bom.txt'), [byte[]](0xEF, 0xBB, 0xBF, 0x61))
        [IO.File]::WriteAllText((Join-Path $sandbox 'replacement.txt'), "bad$([char]0xFFFD)text", $utf8)
        [IO.Directory]::CreateDirectory((Join-Path $sandbox 'folder')) | Out-Null

        Assert-OperationalFailure (Invoke-Scanner @()) 'usage_missing_scope' '' 'usage_missing_scope'
        Assert-OperationalFailure (Invoke-Scanner @('-Path', '.\missing.txt')) 'read_failed' 'missing.txt' 'missing_read'
        Assert-OperationalFailure (Invoke-Scanner @('-Path', '.\folder')) 'read_failed' 'folder' 'non_file_read'
        Assert-OperationalFailure (Invoke-Scanner @('-Path', '.\invalid.txt')) 'decode_failed' 'invalid.txt' 'invalid_utf8'
        Assert-OperationalFailure (Invoke-Scanner @('-Path', '.\bom.txt')) 'decode_failed' 'bom.txt' 'bom_rejected'
        Assert-OperationalFailure (Invoke-Scanner @('-Path', '.\replacement.txt')) 'decode_failed' 'replacement.txt' 'replacement_rejected'
        Assert-ExactResult (Invoke-Scanner @('-Path', '.\clean.txt')) 0 @('CREDENTIAL_SCAN_PASS files=1') 'clean_receipt'
        Assert-OperationalFailure (Invoke-Scanner @('-Path', '.\clean.txt', '.\other.txt')) 'usage_missing_scope' '' 'single_path_only'
        Write-Output 'usage_and_output'

        [IO.Directory]::CreateDirectory((Join-Path $sandbox 'nested')) | Out-Null
        $fragmentOne = 'sk-' + ('A' * 10)
        $fragmentTwo = 'B' * 10
        $positive = $fragmentOne + $fragmentTwo
        [IO.File]::WriteAllText((Join-Path $sandbox 'nested\case.txt'), "[$positive]`n$positive", $utf8)
        $expected = '{"source":"path","path":"nested/case.txt","rule":"provider_api_key"}'
        Assert-ExactResult (Invoke-Scanner @('-Path', '.\nested\case.txt')) 2 @($expected) 'provider_match_unique'
        $doublePrefixExpected = '{"source":"path","path":"./nested/case.txt","rule":"provider_api_key"}'
        Assert-ExactResult (Invoke-Scanner @('-Path', '.\.\nested\case.txt')) 2 @($doublePrefixExpected) 'provider_double_prefix_receipt'

        $maxFragmentOne = 's'
        $maxFragmentTwo = 'k-' + ('A1_-' * 50)
        $maximum = $maxFragmentOne + $maxFragmentTwo
        [IO.File]::WriteAllText((Join-Path $sandbox 'maximum.txt'), $maximum, $utf8)
        $maximumExpected = '{"source":"path","path":"maximum.txt","rule":"provider_api_key"}'
        Assert-ExactResult (Invoke-Scanner @('-Path', '.\maximum.txt')) 2 @($maximumExpected) 'provider_maximum_alphabet'

        $short = ('s' + 'k-') + ('C' * 19)
        $long = ('s' + 'k-') + ('D' * 201)
        $maximal = ('s' + 'k-') + ('E' * 200)
        $negative = "x$positive`n${maximal}_`n$short`n$long"
        [IO.File]::WriteAllText((Join-Path $sandbox 'negative.txt'), $negative, $utf8)
        Assert-ExactResult (Invoke-Scanner @('-Path', '.\negative.txt')) 0 @('CREDENTIAL_SCAN_PASS files=1') 'provider_boundaries'
        Write-Output 'provider_rule'

        $github = 'gh' + 'p_' + ('A' * 20)
        $aws = 'AK' + 'IA' + ('A0' * 8)
        $google = 'AI' + 'za' + ('a_-' * 11) + 'aa'
        $slack = 'xo' + 'xb-' + ('A-' * 5)
        $private = ('-----BEGIN ' + 'RSA ' + 'PRIVATE KEY-----')
        $directText = "$github`n$github`n$aws`n$google`n$slack`n$private"
        [IO.File]::WriteAllText((Join-Path $sandbox 'direct.txt'), $directText, $utf8)
        $directExpected = @(
            '{"source":"path","path":"direct.txt","rule":"aws_access_key"}',
            '{"source":"path","path":"direct.txt","rule":"github_token"}',
            '{"source":"path","path":"direct.txt","rule":"google_api_key"}',
            '{"source":"path","path":"direct.txt","rule":"private_key"}',
            '{"source":"path","path":"direct.txt","rule":"slack_token"}'
        )
        Assert-ExactResult (Invoke-Scanner @('-Path', '.\direct.txt')) 2 $directExpected 'direct_rules_and_order'
        Assert-DirectCase 'github_max' ('gh' + 'r_' + ('Z' * 255)) 'github_token' $true $utf8
        Assert-DirectCase 'github_gho' ('gh' + 'o_' + ('Z' * 20)) 'github_token' $true $utf8
        Assert-DirectCase 'github_ghu' ('gh' + 'u_' + ('Z' * 20)) 'github_token' $true $utf8
        Assert-DirectCase 'github_ghs' ('gh' + 's_' + ('Z' * 20)) 'github_token' $true $utf8
        Assert-DirectCase 'github_short' ('gh' + 'o_' + ('Z' * 19)) 'github_token' $false $utf8
        Assert-DirectCase 'github_long' ('gh' + 'u_' + ('Z' * 256)) 'github_token' $false $utf8
        Assert-DirectCase 'github_neighbor' ('xgh' + 's_' + ('Z' * 20)) 'github_token' $false $utf8
        Assert-DirectCase 'github_right_neighbor' (('gh' + 'p_' + ('Z' * 20)) + '_') 'github_token' $false $utf8
        Assert-DirectCase 'aws_short' ('AS' + 'IA' + ('Z' * 15)) 'aws_access_key' $false $utf8
        Assert-DirectCase 'aws_long' ('AS' + 'IA' + ('Z' * 17)) 'aws_access_key' $false $utf8
        Assert-DirectCase 'aws_neighbor' (('AS' + 'IA' + ('Z' * 16)) + '_') 'aws_access_key' $false $utf8
        Assert-DirectCase 'aws_left_neighbor' ('xAK' + 'IA' + ('Z' * 16)) 'aws_access_key' $false $utf8
        Assert-DirectCase 'aws_asia' ('AS' + 'IA' + ('Z' * 16)) 'aws_access_key' $true $utf8
        Assert-DirectCase 'google_short' ('AI' + 'za' + ('Z' * 34)) 'google_api_key' $false $utf8
        Assert-DirectCase 'google_long' ('AI' + 'za' + ('Z' * 36)) 'google_api_key' $false $utf8
        Assert-DirectCase 'google_neighbor' ('xAI' + 'za' + ('Z' * 35)) 'google_api_key' $false $utf8
        Assert-DirectCase 'google_right_neighbor' (('AI' + 'za' + ('Z' * 35)) + '_') 'google_api_key' $false $utf8
        Assert-DirectCase 'slack_max' ('xo' + 'xs-' + ('Z-' * 100)) 'slack_token' $true $utf8
        Assert-DirectCase 'slack_xoxp' ('xo' + 'xp-' + ('Z' * 10)) 'slack_token' $true $utf8
        Assert-DirectCase 'slack_xoxa' ('xo' + 'xa-' + ('Z' * 10)) 'slack_token' $true $utf8
        Assert-DirectCase 'slack_xoxr' ('xo' + 'xr-' + ('Z' * 10)) 'slack_token' $true $utf8
        Assert-DirectCase 'slack_short' ('xo' + 'xp-' + ('Z' * 9)) 'slack_token' $false $utf8
        Assert-DirectCase 'slack_long' ('xo' + 'xa-' + ('Z' * 201)) 'slack_token' $false $utf8
        Assert-DirectCase 'slack_neighbor' (('xo' + 'xr-' + ('Z' * 10)) + '_') 'slack_token' $false $utf8
        Assert-DirectCase 'slack_left_neighbor' ('xxo' + 'xb-' + ('Z' * 10)) 'slack_token' $false $utf8
        Assert-DirectCase 'private_plain' ('-----BEGIN ' + 'PRIVATE KEY-----') 'private_key' $true $utf8
        Assert-DirectCase 'private_ec' ('-----BEGIN ' + 'EC ' + 'PRIVATE KEY-----') 'private_key' $true $utf8
        Assert-DirectCase 'private_dsa' ('-----BEGIN ' + 'DSA ' + 'PRIVATE KEY-----') 'private_key' $true $utf8
        Assert-DirectCase 'private_openssh' ('-----BEGIN ' + 'OPENSSH ' + 'PRIVATE KEY-----') 'private_key' $true $utf8
        Write-Output 'direct_rules_and_order'

        foreach ($owned in @($scanner, $PSCommandPath)) {
            $ownedResult = Invoke-Scanner @('-Path', $owned)
            Assert-ExactResult $ownedResult 0 @('CREDENTIAL_SCAN_PASS files=1') 'artifact_direct_safety'
        }
        Write-Output 'artifact_direct_safety'
        Write-Output 'BOOTSTRAP_SCANNER_CORE_PASS'
    }
    finally {
        Pop-Location
    }
}
finally {
    if ([IO.Directory]::Exists($sandbox)) { [IO.Directory]::Delete($sandbox, $true) }
}
