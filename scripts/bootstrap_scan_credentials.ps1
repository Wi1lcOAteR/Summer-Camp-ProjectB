param(
    [string]$Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-ScanRecord {
    param(
        [string]$ReceiptPath,
        [string]$Rule,
        [string]$Code
    )

    $record = [ordered]@{ source = 'path' }
    if ($ReceiptPath) { $record.path = $ReceiptPath }
    if ($Rule) { $record.rule = $Rule }
    if ($Code) { $record.code = $Code }
    $record | ConvertTo-Json -Compress
}

function Convert-SourceText {
    param([byte[]]$Bytes)

    if ($Bytes.Length -ge 3 -and
        $Bytes[0] -eq 0xEF -and $Bytes[1] -eq 0xBB -and $Bytes[2] -eq 0xBF) {
        throw [FormatException]::new('bom')
    }

    $text = [Text.UTF8Encoding]::new($false, $true).GetString($Bytes)
    if ($text.Contains([char]0xFFFD)) { throw [FormatException]::new('replacement') }
    $text
}

function Find-DirectSecret {
    param([string]$Text)

    $privateMarker = '-----' + 'BEGIN ' + '(?:RSA |EC |DSA |OPENSSH )?' + 'PRIVATE KEY' + '-----'
    $rules = [ordered]@{
        provider_api_key = '(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,200}(?![A-Za-z0-9_-])'
        github_token = '(?<![A-Za-z0-9_-])(?:ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9]{20,255}(?![A-Za-z0-9_-])'
        aws_access_key = '(?<![A-Za-z0-9_-])(?:AKIA|ASIA)[A-Z0-9]{16}(?![A-Za-z0-9_-])'
        google_api_key = '(?<![A-Za-z0-9_-])AIza[A-Za-z0-9_-]{35}(?![A-Za-z0-9_-])'
        slack_token = '(?<![A-Za-z0-9_-])(?:xoxb-|xoxp-|xoxa-|xoxr-|xoxs-)[A-Za-z0-9-]{10,200}(?![A-Za-z0-9_-])'
        private_key = $privateMarker
    }
    $found = [System.Collections.Generic.List[string]]::new()
    foreach ($entry in $rules.GetEnumerator()) {
        if ([Text.RegularExpressions.Regex]::IsMatch($Text, $entry.Value)) {
            [void]$found.Add($entry.Key)
        }
    }
    return $found.ToArray()
}

if (-not $Path -or $args.Count -gt 0) {
    Write-ScanRecord -Code 'usage_missing_scope'
    exit 3
}

$receiptPath = $Path -replace '\\', '/'
if ($receiptPath.StartsWith('./', [StringComparison]::Ordinal)) {
    $receiptPath = $receiptPath.Substring(2)
}

try {
    $resolvedReadPath = [IO.Path]::GetFullPath($Path, (Get-Location).ProviderPath)
    $attributes = [IO.File]::GetAttributes($resolvedReadPath)
    $disallowed = [IO.FileAttributes]::Directory -bor [IO.FileAttributes]::ReparsePoint -bor [IO.FileAttributes]::Device
    if (($attributes -band $disallowed) -ne 0) { throw [IO.IOException]::new('not_file') }
    $bytes = [IO.File]::ReadAllBytes($resolvedReadPath)
}
catch {
    Write-ScanRecord -ReceiptPath $receiptPath -Code 'read_failed'
    exit 3
}

try { $text = Convert-SourceText -Bytes $bytes }
catch {
    Write-ScanRecord -ReceiptPath $receiptPath -Code 'decode_failed'
    exit 3
}

$findings = @(
    foreach ($rule in @(Find-DirectSecret -Text $text)) {
        [pscustomobject]@{ source = 'path'; path = $receiptPath; rule = $rule }
    }
)
$findings = @($findings | Sort-Object source, path, rule -Unique)
if ($findings.Count -gt 0) {
    foreach ($finding in $findings) {
        Write-ScanRecord -ReceiptPath $finding.path -Rule $finding.rule
    }
    exit 2
}

Write-Output 'CREDENTIAL_SCAN_PASS files=1'
exit 0
