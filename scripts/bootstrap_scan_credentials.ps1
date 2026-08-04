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

function Find-AssignmentSecret {
    param([string]$Text)
    $pattern = '(?i)(?<![A-Za-z0-9_-])(?:api_key|api-key|apikey|access_token|auth_token|client_secret|password|passwd|secret|token)[ \t]*[:=][ \t]*(?:"(?<d>(?:[^"\\\r\n]|\\["\\])*)"|''(?<s>(?:[^''\\\r\n]|\\[''\\])*)''|(?<u>[A-Za-z0-9_./+=:@-]{8,512})(?![A-Za-z0-9_./+=:@-]))'
    foreach ($match in [Text.RegularExpressions.Regex]::Matches($Text, $pattern)) {
        if ($match.Groups['d'].Success) { $value = [Text.RegularExpressions.Regex]::Replace($match.Groups['d'].Value, '\\(["\\])', '$1') }
        elseif ($match.Groups['s'].Success) { $value = [Text.RegularExpressions.Regex]::Replace($match.Groups['s'].Value, '\\([''\\])', '$1') }
        else { $value = $match.Groups['u'].Value }
        $decodedLength = @($value.EnumerateRunes()).Count
        if ($decodedLength -lt 8 -or $decodedLength -gt 512) { continue }
        $safe = $value.Trim([char[]](0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x20))
        if ($safe -in @('example', 'placeholder', 'changeme', 'not-set', 'none', 'null', 'redacted')) { continue }
        if ($safe -match '(?i)^(?:<[^<>\r\n]+>|\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})|\[[^\]\r\n]*redacted[^\]\r\n]*\])$') { continue }
        return @('assignment_secret')
    }
    return @()
}

function Find-EncodedSecret {
    param([string]$Text)
    $families = @(
        [pscustomobject]@{ Type = 'base64'; Pattern = '(?<![A-Za-z0-9+/=])(?<v>[A-Za-z0-9+/]{16,4096}={0,2})(?![A-Za-z0-9+/=])' },
        [pscustomobject]@{ Type = 'base64url'; Pattern = '(?<![A-Za-z0-9_=-])(?<v>[A-Za-z0-9_-]{16,4096}={0,2})(?![A-Za-z0-9_=-])' },
        [pscustomobject]@{ Type = 'hex'; Pattern = '(?<![0-9A-Fa-f])(?<v>[0-9A-Fa-f]{32,8192})(?![0-9A-Fa-f])' }
    )
    foreach ($family in $families) {
        foreach ($match in [Text.RegularExpressions.Regex]::Matches($Text, $family.Pattern)) {
            $value = $match.Groups['v'].Value
            try {
                if ($family.Type -eq 'hex') { if (($value.Length % 2) -ne 0) { continue }; $bytes = [Convert]::FromHexString($value) }
                else { if (($value.Length % 4) -ne 0) { continue }; $canonical = if ($family.Type -eq 'base64url') { $value.Replace('-', '+').Replace('_', '/') } else { $value }; $bytes = [Convert]::FromBase64String($canonical); if ([Convert]::ToBase64String($bytes) -cne $canonical) { continue } }
                $decoded = [Text.UTF8Encoding]::new($false, $true).GetString($bytes)
            }
            catch { continue }
            if (@(Find-DirectSecret -Text $decoded).Count -gt 0) { return @('encoded_secret') }
        }
    }
    return @()
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
    foreach ($rule in @(Find-AssignmentSecret -Text $text)) {
        [pscustomobject]@{ source = 'path'; path = $receiptPath; rule = $rule }
    }
    foreach ($rule in @(Find-EncodedSecret -Text $text)) {
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
