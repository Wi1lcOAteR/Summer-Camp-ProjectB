param(
    [ValidateSet('Check','Write')]
    [string]$Mode = 'Check',
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
)

$ErrorActionPreference = 'Stop'
$script:Utf8 = New-Object Text.UTF8Encoding($false, $true)

function Stop-Capsule {
    param([string]$Code, [string]$Path)
    [Console]::Out.WriteLine("AGENT_CAPSULE_ERROR code=$Code path=$($Path.Replace('\','/'))")
    exit 1
}

function Read-StrictUtf8 {
    param([string]$Path, [string]$RelativePath)
    try {
        $bytes = [IO.File]::ReadAllBytes($Path)
        if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
            Stop-Capsule 'utf8_bom_forbidden' $RelativePath
        }
        $text = $script:Utf8.GetString($bytes)
        if ($text.Contains([char]0xFFFD)) { Stop-Capsule 'utf8_replacement' $RelativePath }
        return $text
    } catch [Text.DecoderFallbackException] {
        Stop-Capsule 'utf8_invalid' $RelativePath
    } catch {
        Stop-Capsule 'read_failed' $RelativePath
    }
}

function Get-Sha256 {
    param([string]$Text)
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($sha.ComputeHash($script:Utf8.GetBytes($Text)))).Replace('-','')
    } finally {
        $sha.Dispose()
    }
}

function Get-DocumentState {
    param([string]$Name, $Entry)

    $relativePath = [string]$Entry.path
    $path = Join-Path $Root $relativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { Stop-Capsule 'document_missing' $relativePath }
    $text = Read-StrictUtf8 $path $relativePath
    $begin = "<!-- AGENT_CAPSULE:$Name`:BEGIN -->"
    $end = "<!-- AGENT_CAPSULE:$Name`:END -->"
    if ([regex]::Matches($text, [regex]::Escape($begin)).Count -ne 1 -or [regex]::Matches($text, [regex]::Escape($end)).Count -ne 1) {
        Stop-Capsule 'marker_count' $relativePath
    }
    $pattern = '(?s)' + [regex]::Escape($begin) + '(.*?)' + [regex]::Escape($end)
    $match = [regex]::Match($text, $pattern)
    if (-not $match.Success) { Stop-Capsule 'marker_order' $relativePath }
    foreach ($anchor in @($Entry.source_anchors)) {
        if ([string]::IsNullOrWhiteSpace([string]$anchor) -or -not $text.Contains([string]$anchor)) {
            Stop-Capsule 'source_anchor_missing' $relativePath
        }
    }
    $content = [string]$Entry.content
    foreach ($character in $content.ToCharArray()) {
        if ([int]$character -gt 127) { Stop-Capsule 'capsule_non_ascii' $relativePath }
    }
    $wordCount = @([regex]::Matches($content, '[A-Za-z0-9][A-Za-z0-9_./:+-]*')).Count
    if ($wordCount -gt [int]$Entry.max_words) { Stop-Capsule 'capsule_word_limit' $relativePath }
    $body = [regex]::Replace($text, $pattern, "$begin`n$end", 1)
    if ((Get-Sha256 $body) -ne ([string]$Entry.source_sha256).ToUpperInvariant()) {
        Stop-Capsule 'source_hash_mismatch' $relativePath
    }
    $canonicalBlock = "$begin`n$($content.TrimEnd("`r","`n"))`n$end"
    $generated = [regex]::Replace($text, $pattern, [Text.RegularExpressions.MatchEvaluator]{ param($ignored) $canonicalBlock }, 1)
    [pscustomobject]@{ Path = $path; RelativePath = $relativePath; Original = $text; Generated = $generated }
}

$manifestRelative = 'docs/cold-start/agent-capsules.json'
$manifestPath = Join-Path $Root $manifestRelative
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) { Stop-Capsule 'manifest_missing' $manifestRelative }
try {
    $manifestText = Read-StrictUtf8 $manifestPath $manifestRelative
    $manifest = $manifestText | ConvertFrom-Json
} catch {
    Stop-Capsule 'manifest_invalid' $manifestRelative
}
if ([int]$manifest.version -lt 1 -or $null -eq $manifest.documents.SPEC -or $null -eq $manifest.documents.PLAN) {
    Stop-Capsule 'manifest_invalid' $manifestRelative
}

$states = @(
    Get-DocumentState 'SPEC' $manifest.documents.SPEC
    Get-DocumentState 'PLAN' $manifest.documents.PLAN
)
if ($Mode -eq 'Check') {
    foreach ($state in $states) {
        if ($state.Original -cne $state.Generated) { Stop-Capsule 'capsule_drift' $state.RelativePath }
    }
} else {
    foreach ($state in $states) {
        if ($state.Original -cne $state.Generated) {
            [IO.File]::WriteAllText($state.Path, $state.Generated, $script:Utf8)
        }
    }
}
Write-Output "AGENT_CAPSULE_PASS documents=$($states.Count)"
