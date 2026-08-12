param(
    [string]$Path,
    [switch]$Tracked,
    [switch]$Staged
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-ScanRecord {
    param(
        [string]$Source,
        [string]$ReceiptPath,
        [string]$Rule,
        [string]$Code
    )

    $record = [ordered]@{}
    if ($Code) { $record.code = $Code }
    if ($Source) { $record.source = $Source }
    if ($ReceiptPath) { $record.path = $ReceiptPath }
    if ($Rule) { $record.rule = $Rule }
    $record | ConvertTo-Json -Compress
}

function Fail-Scan {
    param(
        [string]$Code,
        [string]$Source,
        [string]$ReceiptPath
    )

    throw [IO.IOException]::new(($Code, $Source, $ReceiptPath -join "`0"))
}

function Convert-SourceText {
    param([byte[]]$Bytes)

    if (
        $Bytes.Length -ge 4 -and
        (($Bytes[0] -eq 0xFF -and $Bytes[1] -eq 0xFE -and $Bytes[2] -eq 0x00 -and $Bytes[3] -eq 0x00) -or
        ($Bytes[0] -eq 0x00 -and $Bytes[1] -eq 0x00 -and $Bytes[2] -eq 0xFE -and $Bytes[3] -eq 0xFF))
    ) {
        throw [FormatException]::new('unsupported_bom')
    }
    elseif ($Bytes.Length -ge 2 -and $Bytes[0] -eq 0xFF -and $Bytes[1] -eq 0xFE) {
        $text = [Text.UnicodeEncoding]::new($false, $false, $true).GetString($Bytes, 2, $Bytes.Length - 2)
    }
    elseif ($Bytes.Length -ge 2 -and $Bytes[0] -eq 0xFE -and $Bytes[1] -eq 0xFF) {
        $text = [Text.UnicodeEncoding]::new($true, $false, $true).GetString($Bytes, 2, $Bytes.Length - 2)
    }
    else {
        $offset = 0
        if (
        $Bytes.Length -ge 3 -and
        $Bytes[0] -eq 0xEF -and
        $Bytes[1] -eq 0xBB -and
        $Bytes[2] -eq 0xBF
        ) {
            $offset = 3
        }
        $text = [Text.UTF8Encoding]::new($false, $true).GetString(
            $Bytes,
            $offset,
            $Bytes.Length - $offset
        )
    }
    if ($text.Contains([char]0xFFFD)) {
        throw [FormatException]::new('replacement')
    }
    $text
}

function Find-DirectSecret {
    param([string]$Text)

    $rules = [ordered]@{
        provider_api_key = '(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,200}(?![A-Za-z0-9_-])'
        github_token = '(?<![A-Za-z0-9_-])(?:ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9]{20,255}(?![A-Za-z0-9_-])'
        aws_access_key = '(?<![A-Za-z0-9_-])(?:AKIA|ASIA)[A-Z0-9]{16}(?![A-Za-z0-9_-])'
        google_api_key = '(?<![A-Za-z0-9_-])AIza[A-Za-z0-9_-]{35}(?![A-Za-z0-9_-])'
        slack_token = '(?<![A-Za-z0-9_-])(?:xoxb-|xoxp-|xoxa-|xoxr-|xoxs-)[A-Za-z0-9-]{10,200}(?![A-Za-z0-9_-])'
        private_key = '-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'
    }

    $found = [Collections.Generic.List[string]]::new()
    foreach ($entry in $rules.GetEnumerator()) {
        if ([regex]::IsMatch($Text, $entry.Value)) {
            [void]$found.Add($entry.Key)
        }
    }
    return $found.ToArray()
}

function Find-AssignmentSecret {
    param([string]$Text)

    $pattern = '(?i)(?<![A-Za-z0-9_-])(?:api_key|api-key|apikey|access_token|auth_token|client_secret|password|passwd|secret|token)[ \t]*[:=][ \t]*(?:"(?<d>(?:[^"\\\r\n]|\\["\\])*)"|''(?<s>(?:[^''\\\r\n]|\\[''\\])*)''|(?<u>[A-Za-z0-9_./+=:@-]{8,512})(?![A-Za-z0-9_./+=:@-]))'
    foreach ($match in [regex]::Matches($Text, $pattern)) {
        if ($match.Groups['d'].Success) {
            $value = [regex]::Replace($match.Groups['d'].Value, '\\(["\\])', '$1')
        }
        elseif ($match.Groups['s'].Success) {
            $value = [regex]::Replace($match.Groups['s'].Value, '\\([''\\])', '$1')
        }
        else {
            $value = $match.Groups['u'].Value
        }

        $length = @($value.EnumerateRunes()).Count
        if ($length -lt 8 -or $length -gt 512) { continue }

        $safe = $value.Trim([char[]](0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x20))
        if ($safe -in @('example', 'placeholder', 'changeme', 'not-set', 'none', 'null', 'redacted')) {
            continue
        }
        if ($safe -match '(?i)^(?:<[^<>\r\n]+>|\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})|\[[^\]\r\n]*redacted[^\]\r\n]*\])$') {
            continue
        }
        return @('assignment_secret')
    }
    return @()
}

function Find-EncodedSecret {
    param([string]$Text)

    $families = @(
        [pscustomobject]@{
            Type = 'base64'
            Pattern = '(?<![A-Za-z0-9+/=])(?<v>[A-Za-z0-9+/]{16,4096}={0,2})(?![A-Za-z0-9+/=])'
        },
        [pscustomobject]@{
            Type = 'base64url'
            Pattern = '(?<![A-Za-z0-9_=-])(?<v>[A-Za-z0-9_-]{16,4096}={0,2})(?![A-Za-z0-9_=-])'
        },
        [pscustomobject]@{
            Type = 'hex'
            Pattern = '(?<![0-9A-Fa-f])(?<v>[0-9A-Fa-f]{32,8192})(?![0-9A-Fa-f])'
        }
    )

    foreach ($family in $families) {
        foreach ($match in [regex]::Matches($Text, $family.Pattern)) {
            $value = $match.Groups['v'].Value
            try {
                if ($family.Type -eq 'hex') {
                    if ($value.Length % 2) { continue }
                    $bytes = [Convert]::FromHexString($value)
                }
                else {
                    if ($value.Length % 4) { continue }
                    $canonical = if ($family.Type -eq 'base64url') {
                        $value.Replace('-', '+').Replace('_', '/')
                    }
                    else {
                        $value
                    }
                    $bytes = [Convert]::FromBase64String($canonical)
                    if ([Convert]::ToBase64String($bytes) -cne $canonical) { continue }
                }
                $decoded = [Text.UTF8Encoding]::new($false, $true).GetString($bytes)
            }
            catch {
                continue
            }
            if (@(Find-DirectSecret $decoded).Count) {
                return @('encoded_secret')
            }
        }
    }
    return @()
}

function Invoke-GitProcess {
    param([string[]]$Arguments)

    $process = $null
    $memory = $null
    try {
        $git = (Get-Command git -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
        $start = [Diagnostics.ProcessStartInfo]::new()
        $start.UseShellExecute = $false
        $start.RedirectStandardOutput = $true
        $start.RedirectStandardError = $true
        $start.CreateNoWindow = $true

        if ([IO.Path]::GetExtension($git) -in @('.cmd', '.bat')) {
            $start.FileName = $env:ComSpec
            $quoted = @($Arguments | ForEach-Object { '"' + $_.Replace('"', '""') + '"' })
            $start.Arguments = '/d /s /c ""' + $git + '" ' + ($quoted -join ' ') + '"'
        }
        else {
            $start.FileName = $git
            foreach ($argument in $Arguments) {
                [void]$start.ArgumentList.Add($argument)
            }
        }

        $process = [Diagnostics.Process]::new()
        $process.StartInfo = $start
        if (-not $process.Start()) { throw 'start' }

        # Capture stdout as bytes so index blobs are never decoded by the process wrapper.
        $memory = [IO.MemoryStream]::new()
        $copy = $process.StandardOutput.BaseStream.CopyToAsync($memory)
        $standardError = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit(30000)) {
            $process.Kill($true)
            $process.WaitForExit()
            throw 'timeout'
        }
        [void]$copy.GetAwaiter().GetResult()
        [void]$standardError.GetAwaiter().GetResult()
        [pscustomobject]@{
            ExitCode = $process.ExitCode
            Bytes = $memory.ToArray()
        }
    }
    catch {
        [pscustomobject]@{
            ExitCode = -1
            Bytes = [byte[]]@()
        }
    }
    finally {
        if ($process) { $process.Dispose() }
        if ($memory) { $memory.Dispose() }
    }
}

function Get-GitRoot {
    $result = Invoke-GitProcess @('rev-parse', '--show-toplevel')
    if ($result.ExitCode -ne 0) { Fail-Scan 'git_root_failed' }
    try {
        $root = (Convert-SourceText $result.Bytes).TrimEnd("`r", "`n")
        if (-not [IO.Path]::IsPathFullyQualified($root)) { throw 'root' }
        [IO.Path]::GetFullPath($root)
    }
    catch {
        Fail-Scan 'git_root_failed'
    }
}

function Get-GitItems {
    param(
        [string]$Source,
        [switch]$Stage
    )

    $arguments = if ($Stage) {
        @('ls-files', '--stage', '-z')
    }
    else {
        @('ls-files', '-z')
    }
    $result = Invoke-GitProcess $arguments
    if ($result.ExitCode -ne 0) { Fail-Scan 'git_list_failed' $Source }
    if (-not $result.Bytes.Length) { return @() }

    try {
        $text = Convert-SourceText $result.Bytes
        if ($text[$text.Length - 1] -ne [char]0) { throw 'nul' }
        return @($text.Substring(0, $text.Length - 1).Split([char]0))
    }
    catch {
        Fail-Scan 'git_list_failed' $Source
    }
}

function Assert-RepoPath {
    param(
        [string]$ReceiptPath,
        [string]$Source
    )

    if (
        -not $ReceiptPath -or
        $ReceiptPath.Contains('\') -or
        $ReceiptPath.StartsWith('/') -or
        [IO.Path]::IsPathFullyQualified($ReceiptPath) -or
        $ReceiptPath.EndsWith('/') -or
        $ReceiptPath.Contains('//')
    ) {
        Fail-Scan 'path_escape' $Source $ReceiptPath
    }

    $parts = $ReceiptPath.Split('/')
    if ($parts | Where-Object { $_ -in @('', '.', '..') }) {
        Fail-Scan 'path_escape' $Source $ReceiptPath
    }
}

function Get-WorktreeSources {
    $root = Get-GitRoot
    foreach ($path in @(Get-GitItems 'worktree')) {
        Assert-RepoPath $path 'worktree'
        [pscustomobject]@{
            source = 'worktree'
            path = $path
            root = $root
        }
    }
}

function Get-IndexSources {
    [void](Get-GitRoot)
    $paths = @(Get-GitItems 'index')
    $rows = @(Get-GitItems 'index' -Stage)

    foreach ($path in $paths) {
        Assert-RepoPath $path 'index'
        $entries = @()
        foreach ($row in $rows) {
            $tab = $row.IndexOf("`t")
            if ($tab -lt 0) { continue }
            $metadata = $row.Substring(0, $tab)
            $rowPath = $row.Substring($tab + 1)
            if (
                $rowPath -cne $path -or
                $metadata -notmatch '^(?<mode>[0-9]{6}) (?<oid>(?:[0-9a-f]{40}|[0-9a-f]{64})) (?<stage>[0-3])$' -or
                $Matches.stage -cne '0'
            ) {
                continue
            }
            $entries += , [pscustomobject]@{
                mode = $Matches.mode
                oid = $Matches.oid
            }
        }

        if ($entries.Count -ne 1) { Fail-Scan 'index_entry_failed' 'index' $path }
        if ($entries[0].mode -notin @('100644', '100755')) {
            Fail-Scan 'index_mode_unsupported' 'index' $path
        }
        [pscustomobject]@{
            source = 'index'
            path = $path
            oid = $entries[0].oid
        }
    }
}

function Read-WorktreeBytes {
    param($Item)

    try {
        $candidate = [IO.Path]::GetFullPath(
            $Item.path.Replace('/', [IO.Path]::DirectorySeparatorChar),
            $Item.root
        )
        $relative = [IO.Path]::GetRelativePath($Item.root, $candidate)
        if (
            $relative -eq '..' -or
            $relative.StartsWith('..' + [IO.Path]::DirectorySeparatorChar) -or
            [IO.Path]::IsPathFullyQualified($relative)
        ) {
            Fail-Scan 'path_escape' 'worktree' $Item.path
        }

        $cursor = $Item.root
        foreach ($part in $Item.path.Split('/')) {
            $cursor = Join-Path $cursor $part
            $attributes = [IO.File]::GetAttributes($cursor)
            if ($attributes -band [IO.FileAttributes]::ReparsePoint) {
                Fail-Scan 'reparse_point' 'worktree' $Item.path
            }
        }
        $notRegular = [IO.FileAttributes]::Directory -bor [IO.FileAttributes]::Device
        if ($attributes -band $notRegular) {
            Fail-Scan 'not_regular_file' 'worktree' $Item.path
        }
        , [IO.File]::ReadAllBytes($candidate)
    }
    catch {
        if ($_.Exception.Message.Contains("`0")) { throw }
        Fail-Scan 'read_failed' 'worktree' $Item.path
    }
}

function Read-IndexBlobBytes {
    param($Item)

    $result = Invoke-GitProcess @('cat-file', 'blob', $Item.oid)
    if ($result.ExitCode -ne 0) { Fail-Scan 'read_failed' 'index' $Item.path }
    , $result.Bytes
}

function Invoke-BootstrapScan {
    param(
        [string]$InputPath,
        [switch]$IncludeTracked,
        [switch]$IncludeStaged,
        [object[]]$ExtraArguments = @()
    )

    $invalidScope =
        $ExtraArguments.Count -or
        ($InputPath -and ($IncludeTracked -or $IncludeStaged)) -or
        (-not $InputPath -and -not $IncludeTracked -and -not $IncludeStaged)
    if ($invalidScope) {
        return [pscustomobject]@{
            ExitCode = 3
            Output = @(Write-ScanRecord 'path' -Code 'usage_missing_scope')
        }
    }

    try {
    if ($InputPath) {
        $receipt = $InputPath -replace '\\', '/'
        if ($receipt.StartsWith('./', [StringComparison]::Ordinal)) {
            $receipt = $receipt.Substring(2)
        }
        try {
            $resolved = [IO.Path]::GetFullPath($InputPath, (Get-Location).ProviderPath)
            $attributes = [IO.File]::GetAttributes($resolved)
            $notFile =
                [IO.FileAttributes]::Directory -bor
                [IO.FileAttributes]::ReparsePoint -bor
                [IO.FileAttributes]::Device
            if ($attributes -band $notFile) { throw 'file' }
            $items = @(
                [pscustomobject]@{
                    source = 'path'
                    path = $receipt
                    bytes = [IO.File]::ReadAllBytes($resolved)
                }
            )
        }
        catch {
            Fail-Scan 'read_failed' 'path' $receipt
        }
    }
    else {
        $items = @()
        if ($IncludeTracked) {
            foreach ($item in @(Get-WorktreeSources)) {
                $items += , [pscustomobject]@{
                    source = $item.source
                    path = $item.path
                    bytes = [byte[]](Read-WorktreeBytes $item)
                }
            }
        }
        if ($IncludeStaged) {
            foreach ($item in @(Get-IndexSources)) {
                $items += , [pscustomobject]@{
                    source = $item.source
                    path = $item.path
                    bytes = [byte[]](Read-IndexBlobBytes $item)
                }
            }
        }
    }

    $binaryExtensions = @('.png', '.jpg', '.jpeg', '.gif', '.webp', '.pdf', '.ico', '.zip', '.gz', '.7z', '.exe', '.dll', '.pyd', '.so', '.woff', '.woff2', '.ttf', '.mp3', '.mp4', '.sqlite', '.db')
    $textExtensions = @('.md', '.txt', '.json', '.jsonl', '.toml', '.yaml', '.yml', '.ini', '.cfg', '.conf', '.env', '.example', '.py', '.pyi', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.html', '.css', '.scss', '.sql', '.spec', '.ps1', '.psm1', '.psd1', '.sh', '.bash', '.cmd', '.bat', '.lock', '.in')
    $extensionlessNames = @('.gitignore', '.gitattributes', '.dockerignore', '.python-version', '.npmrc', 'Dockerfile', 'Makefile', 'LICENSE', 'NOTICE', 'uv-LICENSE-APACHE', 'uv-LICENSE-MIT', 'cpython-LICENSE', 'node-LICENSE', 'npm-LICENSE')
    $findings = @()
    $scannedCount = 0
    foreach ($item in $items) {
        $extension = [IO.Path]::GetExtension($item.path).ToLowerInvariant()
        if ($extension -in $binaryExtensions) {
            continue
        }
        $name = [IO.Path]::GetFileName($item.path)
        if ($extension -notin $textExtensions -and $name -notin $extensionlessNames -and -not $name.ToLowerInvariant().EndsWith('.dockerignore')) {
            Fail-Scan 'unsupported_file_type' $item.source $item.path
        }
        $scannedCount++
        $utf32Marked =
            $item.bytes.Length -ge 4 -and
            (($item.bytes[0] -eq 0xFF -and $item.bytes[1] -eq 0xFE -and $item.bytes[2] -eq 0x00 -and $item.bytes[3] -eq 0x00) -or
            ($item.bytes[0] -eq 0x00 -and $item.bytes[1] -eq 0x00 -and $item.bytes[2] -eq 0xFE -and $item.bytes[3] -eq 0xFF))
        $marked = $utf32Marked -or
            ($item.bytes.Length -ge 2 -and (($item.bytes[0] -eq 0xFF -and $item.bytes[1] -eq 0xFE) -or ($item.bytes[0] -eq 0xFE -and $item.bytes[1] -eq 0xFF))) -or
            ($item.bytes.Length -ge 3 -and $item.bytes[0] -eq 0xEF -and $item.bytes[1] -eq 0xBB -and $item.bytes[2] -eq 0xBF)
        if (-not $marked -and ($item.bytes -contains [byte]0)) {
            Fail-Scan 'nul_unmarked' $item.source $item.path
        }
        try {
            $text = Convert-SourceText $item.bytes
        }
        catch {
            Fail-Scan 'decode_failed' $item.source $item.path
        }

        $rules = @(
            (Find-DirectSecret $text) +
            (Find-AssignmentSecret $text) +
            (Find-EncodedSecret $text)
        )
        foreach ($rule in $rules) {
            if ($rule) {
                $findings += , [pscustomobject]@{
                    source = $item.source
                    path = $item.path
                    rule = $rule
                }
            }
        }
    }

    $findings = @($findings | Sort-Object source, path, rule -Unique)
    if ($findings.Count) {
        return [pscustomobject]@{
            ExitCode = 2
            Output = @($findings | ForEach-Object { Write-ScanRecord $_.source $_.path $_.rule })
        }
    }
    return [pscustomobject]@{
        ExitCode = 0
        Output = @("CREDENTIAL_SCAN_PASS files=$scannedCount")
    }
}
catch {
    $parts = $_.Exception.Message.Split([char]0)
    if ($parts.Count -eq 3) {
        return [pscustomobject]@{
            ExitCode = 3
            Output = @(Write-ScanRecord $parts[1] $parts[2] -Code $parts[0])
        }
    }
    throw
}
}

try {
    $result = Invoke-BootstrapScan -InputPath $Path -IncludeTracked:$Tracked -IncludeStaged:$Staged -ExtraArguments $args
    $result.Output | Write-Output
    exit $result.ExitCode
}
catch {
    Write-ScanRecord -Code 'scan_failed'; exit 3
}
