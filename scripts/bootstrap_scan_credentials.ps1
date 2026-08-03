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

    [Text.RegularExpressions.Regex]::IsMatch(
        $Text,
        '(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,200}(?![A-Za-z0-9_-])'
    )
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

if (Find-DirectSecret -Text $text) {
    Write-ScanRecord -ReceiptPath $receiptPath -Rule 'provider_api_key'
    exit 2
}

Write-Output 'CREDENTIAL_SCAN_PASS files=1'
exit 0
