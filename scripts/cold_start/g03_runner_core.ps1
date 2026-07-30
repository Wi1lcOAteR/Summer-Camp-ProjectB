$script:G03Utf8 = New-Object Text.UTF8Encoding($false, $true)

function Read-G03StrictUtf8 {
    param([Parameter(Mandatory = $true)][string]$Path)

    try {
        $bytes = [IO.File]::ReadAllBytes($Path)
        if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
            throw 'UTF8_INVALID'
        }
        $text = $script:G03Utf8.GetString($bytes)
        if ($text.Contains([char]0xFFFD)) { throw 'UTF8_INVALID' }
        return $text
    } catch [Text.DecoderFallbackException] {
        throw 'UTF8_INVALID'
    } catch {
        if ($_.Exception.Message -eq 'UTF8_INVALID') { throw }
        throw 'UTF8_INVALID'
    }
}

function Get-G03CapsuleText {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][ValidateSet('SPEC','PLAN')][string]$Name
    )

    $begin = '<!-- AGENT_CAPSULE:' + $Name + ':BEGIN -->'
    $end = '<!-- AGENT_CAPSULE:' + $Name + ':END -->'
    $pattern = '(?s)' + [regex]::Escape($begin) + '\s*(.*?)\s*' + [regex]::Escape($end)
    $matches = [regex]::Matches($Text, $pattern)
    if ($matches.Count -ne 1 -or [string]::IsNullOrWhiteSpace($matches[0].Groups[1].Value)) {
        throw 'CAPSULE_INVALID'
    }
    return $matches[0].Groups[1].Value.Trim()
}

function Remove-G03CapsuleText {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][ValidateSet('SPEC','PLAN')][string]$Name
    )

    $begin = '<!-- AGENT_CAPSULE:' + $Name + ':BEGIN -->'
    $end = '<!-- AGENT_CAPSULE:' + $Name + ':END -->'
    $pattern = '(?s)' + [regex]::Escape($begin) + '.*?' + [regex]::Escape($end)
    if ([regex]::Matches($Text, $pattern).Count -ne 1) { throw 'CAPSULE_INVALID' }
    return ([regex]::Replace($Text, $pattern, '')).Trim()
}

function Get-G03AgentDocuments {
    param(
        [Parameter(Mandatory = $true)][string]$SpecPath,
        [Parameter(Mandatory = $true)][string]$PlanPath,
        [Parameter(Mandatory = $true)][ValidateSet('Auto','English','Chinese')][string]$AgentLanguage
    )

    $spec = Read-G03StrictUtf8 $SpecPath
    $plan = Read-G03StrictUtf8 $PlanPath
    $effective = if ($AgentLanguage -eq 'Chinese') { 'Chinese' } else { 'English' }
    if ($effective -eq 'English') {
        $specText = Get-G03CapsuleText -Text $spec -Name SPEC
        $planText = Get-G03CapsuleText -Text $plan -Name PLAN
    } else {
        $specText = Remove-G03CapsuleText -Text $spec -Name SPEC
        $planText = Remove-G03CapsuleText -Text $plan -Name PLAN
    }
    [pscustomobject]@{
        RequestedLanguage = $AgentLanguage
        EffectiveLanguage = $effective
        SpecText = $specText
        PlanText = $planText
    }
}

function Test-G03IntakeReceipt {
    param(
        [Parameter(Mandatory = $true)]$Receipt,
        [Parameter(Mandatory = $true)]$Expected
    )

    $requiredProperties = @('spec_sha256','plan_sha256','files','language','task','acceptance_id','ambiguities')
    foreach ($property in $requiredProperties) {
        if ($Receipt.PSObject.Properties.Name -notcontains $property) { return 'INTAKE_FAILED' }
    }
    if ($Receipt.spec_sha256 -cne $Expected.spec_sha256 -or
        $Receipt.plan_sha256 -cne $Expected.plan_sha256 -or
        $Receipt.language -cne $Expected.language -or
        $Receipt.task -cne $Expected.task -or
        $Receipt.acceptance_id -cne $Expected.acceptance_id) {
        return 'INTAKE_FAILED'
    }
    $actualFiles = @($Receipt.files | ForEach-Object { [string]$_ } | Sort-Object)
    $expectedFiles = @($Expected.files | ForEach-Object { [string]$_ } | Sort-Object)
    if ($actualFiles.Count -ne $expectedFiles.Count -or @(Compare-Object $actualFiles $expectedFiles -SyncWindow 0).Count -ne 0) {
        return 'INTAKE_FAILED'
    }
    if (@($Receipt.ambiguities).Count -gt 0) { return 'INTAKE_AMBIGUOUS' }
    return 'INTAKE_READY'
}

function Test-G03IntakeEnvelope {
    param(
        [Parameter(Mandatory = $true)]$Envelope,
        [Parameter(Mandatory = $true)][decimal]$MaxCostUsd
    )
    foreach ($property in @('subtype','is_error','total_cost_usd','result')) {
        if ($Envelope.PSObject.Properties.Name -notcontains $property) { return 'protocol_mismatch' }
    }
    if ($Envelope.subtype -cne 'success' -or $Envelope.is_error -ne $false -or
        $Envelope.result -isnot [string] -or [string]::IsNullOrWhiteSpace([string]$Envelope.result)) {
        return 'protocol_mismatch'
    }
    try { $cost = [decimal]::Parse(([string]$Envelope.total_cost_usd), [Globalization.CultureInfo]::InvariantCulture) } catch { return 'protocol_mismatch' }
    if ($cost -lt 0 -or $cost -gt $MaxCostUsd) { return 'protocol_mismatch' }
    return 'ok'
}

function Get-G03ProcessDiagnosticCode {
    param(
        [Parameter(Mandatory = $true)][ValidateSet('intake','execution')][string]$Stage,
        [Parameter(Mandatory = $true)][int]$ExitCode,
        [Parameter(Mandatory = $true)][bool]$TimedOut,
        [AllowEmptyString()][string]$Stdout = '',
        [AllowEmptyString()][string]$Stderr = ''
    )
    if ($TimedOut -or $ExitCode -eq 124) { return 'wall_timeout' }
    $text = (($Stdout + "`n" + $Stderr).Trim())
    if ($text -match '(?i)504\s+Gateway\s+Time[- ]out|gateway\s+504') { return 'gateway_504' }
    if ($text -match '(?i)401\s+authentication_failed|invalid[_ ]api[_ ]key|authentication') { return 'provider_auth' }
    if ($text -match '(?i)invalid\s+mcp\s+configuration|mcp\s+configuration') { return 'cli_mcp_config' }
    if ($text -match '(?i)the shell cannot be started|no such file or directory|failed during initialization') { return 'cli_startup' }
    if ($ExitCode -ne 0) { return 'child_nonzero' }
    if ([string]::IsNullOrWhiteSpace($text)) { return 'child_empty_output' }
    return 'child_output_protocol'
}

function Resolve-G03ClaudeCliPath {
    param(
        [Parameter(Mandatory = $true)][string]$ProjectRoot,
        [Parameter(Mandatory = $true)][string]$ClaudeCli
    )
    $candidate = if ([IO.Path]::IsPathRooted($ClaudeCli)) { $ClaudeCli } else { Join-Path $ProjectRoot $ClaudeCli }
    if (Test-Path -LiteralPath $candidate -PathType Leaf) { return (Resolve-Path -LiteralPath $candidate).Path }
    return $candidate
}

function Test-G03ColdStartArtifacts {
    param([Parameter(Mandatory = $true)][string]$ColdRoot)

    $resolvedRoot = (Resolve-Path -LiteralPath $ColdRoot).Path.TrimEnd('\', '/')
    $required = @(
        'PLAN.md',
        'SPEC.md',
        'scripts/bootstrap_scan_credentials.ps1',
        'scripts/tests/bootstrap_scanner_contract.ps1'
    )
    $files = @(Get-ChildItem -LiteralPath $resolvedRoot -File -Recurse -Force)
    $directories = @(Get-ChildItem -LiteralPath $resolvedRoot -Directory -Recurse -Force)
    $relativeFiles = @($files | ForEach-Object {
        $_.FullName.Substring($resolvedRoot.Length).TrimStart('\', '/').Replace('\', '/')
    })
    foreach ($requiredPath in $required) {
        $matching = @($files | Where-Object {
            $_.FullName.Substring($resolvedRoot.Length).TrimStart('\', '/').Replace('\', '/') -eq $requiredPath
        })
        if ($matching.Count -ne 1 -or $matching[0].Length -eq 0) {
            return [pscustomobject]@{ Valid = $false; Code = 'required_artifact_missing'; FileCount = $relativeFiles.Count }
        }
        if (($matching[0].Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            return [pscustomobject]@{ Valid = $false; Code = 'reparse_artifact'; FileCount = $relativeFiles.Count }
        }
    }
    if (@($relativeFiles | Where-Object { $required -notcontains $_ }).Count -gt 0) {
        return [pscustomobject]@{ Valid = $false; Code = 'unexpected_artifact'; FileCount = $relativeFiles.Count }
    }
    $relativeDirectories = @($directories | ForEach-Object {
        $_.FullName.Substring($resolvedRoot.Length).TrimStart('\', '/').Replace('\', '/')
    })
    if (@($relativeDirectories | Where-Object { $_ -notin @('scripts','scripts/tests') }).Count -gt 0) {
        return [pscustomobject]@{ Valid = $false; Code = 'unexpected_directory'; FileCount = $relativeFiles.Count }
    }
    return [pscustomobject]@{ Valid = $true; Code = 'ok'; FileCount = $relativeFiles.Count }
}

function Resolve-G03State {
    param(
        [Parameter(Mandatory = $true)][bool]$CapsuleValid,
        [Parameter(Mandatory = $true)][bool]$Utf8Valid,
        [Parameter(Mandatory = $true)][ValidateSet('INTAKE_READY','INTAKE_FAILED','INTAKE_AMBIGUOUS')][string]$IntakeState,
        [Parameter(Mandatory = $true)][int]$ExecutionExit,
        [Parameter(Mandatory = $true)][ValidateSet('ok','empty_end_turn','gateway_504','budget_exceeded','wall_timeout','protocol_mismatch')][string]$ExecutionSignal,
        [Parameter(Mandatory = $true)][bool]$ArtifactsValid
    )

    if (-not $CapsuleValid) { return 'CAPSULE_INVALID' }
    if (-not $Utf8Valid) { return 'UTF8_INVALID' }
    if ($IntakeState -eq 'INTAKE_FAILED') { return 'INTAKE_FAILED' }
    if ($IntakeState -eq 'INTAKE_AMBIGUOUS') { return 'INTAKE_AMBIGUOUS' }
    if ($ExecutionExit -ne 0 -or $ExecutionSignal -ne 'ok') { return 'EXECUTION_FAILED' }
    if (-not $ArtifactsValid) { return 'COLD_START_INCOMPLETE' }
    return 'G03_EVIDENCE_READY'
}

function Test-G03SandboxPlatform {
    param([Parameter(Mandatory = $true)][ValidateSet('Windows','Linux','WSL2','macOS','Unknown')][string]$Platform)
    return $Platform -in @('Linux','WSL2')
}

function Wait-G03ProcessWithHeartbeat {
    param(
        [Parameter(Mandatory = $true)][Diagnostics.Process]$Process,
        [Parameter(Mandatory = $true)][ValidateRange(1, 86400)][int]$HostWallSeconds,
        [Parameter(Mandatory = $true)][ValidateRange(1, 3600)][int]$HeartbeatSeconds,
        [Parameter(Mandatory = $true)][ValidatePattern('^[a-z0-9_]+$')][string]$Stage,
        [Parameter(Mandatory = $true)][scriptblock]$ProgressWriter
    )

    $startedAt = [DateTimeOffset]::UtcNow
    $nextHeartbeat = $HeartbeatSeconds
    $exited = $false
    $terminated = $false
    try {
        while (-not $exited) {
            $elapsed = [int][Math]::Floor(([DateTimeOffset]::UtcNow - $startedAt).TotalSeconds)
            $remainingMilliseconds = [int][Math]::Max(0, ($HostWallSeconds - $elapsed) * 1000)
            if ($remainingMilliseconds -le 0) { break }
            $exited = $Process.WaitForExit([Math]::Min(1000, $remainingMilliseconds))
            $elapsed = [int][Math]::Floor(([DateTimeOffset]::UtcNow - $startedAt).TotalSeconds)
            if (-not $exited -and $elapsed -ge $nextHeartbeat) {
                $null = & $ProgressWriter $Stage 'heartbeat' $elapsed
                while ($nextHeartbeat -le $elapsed) { $nextHeartbeat += $HeartbeatSeconds }
            }
        }
    } finally {
        if (-not $exited -and -not $Process.HasExited) {
            try { $Process.Kill($true) } catch { try { $Process.Kill() } catch { } }
            if (-not $Process.WaitForExit(5000)) { throw 'process_tree_termination_failed' }
            $terminated = $true
        }
    }
    [pscustomobject]@{
        Exited = $exited
        Terminated = $terminated
        ElapsedSeconds = [int][Math]::Floor(([DateTimeOffset]::UtcNow - $startedAt).TotalSeconds)
    }
}

function Invoke-G03BwrapCommand {
    param(
        [Parameter(Mandatory = $true)][string]$WorkingDirectory,
        [Parameter(Mandatory = $true)][string[]]$CommandArguments,
        [Parameter(Mandatory = $true)][ValidateRange(1, 120)][int]$WallSeconds
    )

    $bwrap = (Get-Command bwrap -ErrorAction Stop).Source
    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $bwrap
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true
    $startInfo.WorkingDirectory = $WorkingDirectory
    $startInfo.Environment.Clear()
    $startInfo.Environment['PATH'] = '/usr/bin:/bin:/opt/microsoft/powershell/7'
    $startInfo.Environment['HOME'] = '/nonexistent'
    $arguments = [Collections.Generic.List[string]]::new()
    foreach ($value in @('--unshare-all','--die-with-parent','--new-session','--clearenv','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/home','--dir','/root')) {
        $arguments.Add($value)
    }
    foreach ($runtimePath in @('/etc','/usr','/bin','/lib','/lib64','/opt/microsoft/powershell/7')) {
        if (Test-Path -LiteralPath $runtimePath) {
            $arguments.Add('--ro-bind')
            $arguments.Add($runtimePath)
            $arguments.Add($runtimePath)
        }
    }
    foreach ($value in @('--bind',$WorkingDirectory,'/workspace','--chdir','/workspace','--setenv','PATH','/usr/bin:/bin:/opt/microsoft/powershell/7','--setenv','HOME','/nonexistent','timeout','--signal=TERM','--kill-after=2s',("$WallSeconds" + 's'),'pwsh')) {
        $arguments.Add($value)
    }
    foreach ($argument in $CommandArguments) { $arguments.Add([string]$argument) }
    foreach ($argument in $arguments) { $startInfo.ArgumentList.Add($argument) }

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    if (-not $process.Start()) { throw 'sandbox_process_start_failed' }
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $boundedExit = $process.WaitForExit(($WallSeconds + 5) * 1000)
    if (-not $boundedExit) {
        try { $process.Kill($true) } catch { try { $process.Kill() } catch { } }
        if (-not $process.WaitForExit(5000)) { throw 'sandbox_process_tree_termination_failed' }
    }
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    [pscustomobject]@{
        ExitCode = if ($boundedExit) { $process.ExitCode } else { 124 }
        TimedOut = (-not $boundedExit) -or $process.ExitCode -eq 124
        Stdout = $stdout
        Stderr = $stderr
    }
}

function Test-G03BwrapPreflight {
    param([Parameter(Mandatory = $true)][string]$SandboxRoot)

    $scriptPath = Join-Path $SandboxRoot 'g03-sandbox-preflight.ps1'
    $descendantPath = Join-Path $SandboxRoot 'g03-sandbox-descendant.ps1'
    $scriptText = @'
$ErrorActionPreference='Stop'
foreach($name in @('ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_BASE_URL')){if(Test-Path ('Env:'+$name)){throw 'credential_env_visible'}}
if(Test-Path -LiteralPath '/mnt'){throw 'host_mount_visible'}
try{[Net.Dns]::GetHostAddresses('example.com')|Out-Null;throw 'network_visible'}catch{if($_.Exception.Message -eq 'network_visible'){throw}}
[IO.File]::WriteAllText('/workspace/preflight-marker.txt','ok',(New-Object Text.UTF8Encoding($false,$true)))
'G03_SANDBOX_PREFLIGHT_PASS'
'@
    [IO.File]::WriteAllText($scriptPath, $scriptText, (New-Object Text.UTF8Encoding($false, $true)))
    $descendantText = @'
$child = "Start-Sleep -Seconds 3; [IO.File]::WriteAllText('/workspace/descendant-marker.txt','late',(New-Object Text.UTF8Encoding(`$false,`$true)))"
Start-Process -FilePath pwsh -ArgumentList @('-NoProfile','-Command',$child) | Out-Null
Start-Sleep -Seconds 30
'@
    [IO.File]::WriteAllText($descendantPath, $descendantText, (New-Object Text.UTF8Encoding($false, $true)))
    try {
        $probe = Invoke-G03BwrapCommand -WorkingDirectory $SandboxRoot -CommandArguments @('-NoProfile','-File','g03-sandbox-preflight.ps1') -WallSeconds 10
        if ($probe.TimedOut -or $probe.ExitCode -ne 0 -or $probe.Stdout.Trim() -cne 'G03_SANDBOX_PREFLIGHT_PASS') { return $false }
        if (-not (Test-Path -LiteralPath (Join-Path $SandboxRoot 'preflight-marker.txt') -PathType Leaf)) { return $false }
        $timeoutProbe = Invoke-G03BwrapCommand -WorkingDirectory $SandboxRoot -CommandArguments @('-NoProfile','-File','g03-sandbox-descendant.ps1') -WallSeconds 1
        if (-not $timeoutProbe.TimedOut -or $timeoutProbe.ExitCode -ne 124) { return $false }
        Start-Sleep -Seconds 4
        return -not (Test-Path -LiteralPath (Join-Path $SandboxRoot 'descendant-marker.txt'))
    } finally {
        Remove-Item -LiteralPath $scriptPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $descendantPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath (Join-Path $SandboxRoot 'preflight-marker.txt') -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath (Join-Path $SandboxRoot 'descendant-marker.txt') -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-G03CandidateChecked {
    param(
        [Parameter(Mandatory = $true)][scriptblock]$CommandInvoker,
        [Parameter(Mandatory = $true)][string]$WorkingDirectory,
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [int]$WallSeconds = 20
    )
    $result = & $CommandInvoker $WorkingDirectory $Arguments $WallSeconds
    if ($null -eq $result -or $result.PSObject.Properties.Name -notcontains 'ExitCode' -or
        $result.PSObject.Properties.Name -notcontains 'TimedOut' -or $result.PSObject.Properties.Name -notcontains 'Stdout') {
        throw 'sandbox_invoker_protocol_invalid'
    }
    return $result
}

function Test-G03ScannerBehavior {
    param(
        [Parameter(Mandatory = $true)][string]$ReplayRoot,
        [Parameter(Mandatory = $true)][scriptblock]$CommandInvoker
    )

    $script:G03LastOracleCase = 'usage'
    $scanner = 'scripts/bootstrap_scan_credentials.ps1'
    $usage = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $ReplayRoot -Arguments @('-NoProfile','-File',$scanner)
    if ($usage.TimedOut -or $usage.ExitCode -ne 3 -or $usage.Stdout.Trim() -cne 'CREDENTIAL_SCAN_ERROR {"code":"usage_missing_scope"}') { return $false }

    $oracleRoot = Join-Path $ReplayRoot 'oracle'
    New-Item -ItemType Directory -Path $oracleRoot -Force | Out-Null
    $cases = [ordered]@{
        provider_api_key = ('s' + 'k-' + ('A' * 20))
        github_token = ('gh' + 'p_' + ('B' * 20))
        aws_access_key = ('AK' + 'IA' + ('C' * 16))
        google_api_key = ('AI' + 'za' + ('D' * 35))
        slack_token = ('xo' + 'xb-' + ('e' * 10))
        private_key = ('-----BEGIN ' + 'PRIVATE ' + 'KEY-----')
    }
    $runOracleCase = {
        param([string]$Name,[string]$Text,[string]$ExpectedRule)
        $fixturePath = Join-Path $oracleRoot ($Name + '.txt')
        [IO.File]::WriteAllText($fixturePath, $Text, (New-Object Text.UTF8Encoding($false, $true)))
        $sandboxPath = 'oracle/' + $Name + '.txt'
        $run = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $ReplayRoot -Arguments @('-NoProfile','-File',$scanner,'-Path',$sandboxPath)
        if ([string]::IsNullOrEmpty($ExpectedRule)) {
            $valid = -not $run.TimedOut -and $run.ExitCode -eq 0 -and $run.Stdout.Trim() -ceq 'CREDENTIAL_SCAN_PASS files=1'
            if (-not $valid) { $script:G03LastOracleCase = $Name }
            return $valid
        }
        $expected = 'CREDENTIAL_SCAN_FINDING ' + ([ordered]@{source='path';path=$sandboxPath;rule=$ExpectedRule} | ConvertTo-Json -Compress)
        $valid = -not $run.TimedOut -and $run.ExitCode -eq 2 -and $run.Stdout.Trim() -ceq $expected -and -not $run.Stdout.Contains($Text)
        if (-not $valid) { $script:G03LastOracleCase = $Name }
        return $valid
    }
    foreach ($entry in $cases.GetEnumerator()) {
        $script:G03LastOracleCase = $entry.Key + '-base'
        $fixturePath = Join-Path $oracleRoot ($entry.Key + '.txt')
        [IO.File]::WriteAllText($fixturePath, [string]$entry.Value, (New-Object Text.UTF8Encoding($false, $true)))
        $sandboxPath = 'oracle/' + $entry.Key + '.txt'
        $finding = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $ReplayRoot -Arguments @('-NoProfile','-File',$scanner,'-Path',$sandboxPath)
        $lines = @($finding.Stdout -split "`r?`n" | Where-Object { $_ -ne '' })
        if ($finding.TimedOut -or $finding.ExitCode -ne 2 -or $lines.Count -ne 1 -or -not $lines[0].StartsWith('CREDENTIAL_SCAN_FINDING ')) { $script:G03LastOracleCase += '-shape'; return $false }
        $expectedRecordText = 'CREDENTIAL_SCAN_FINDING ' + ([ordered]@{source='path';path=$sandboxPath;rule=$entry.Key} | ConvertTo-Json -Compress)
        if ($lines[0] -cne $expectedRecordText) { $script:G03LastOracleCase += '-record'; return $false }
        try { $record = $lines[0].Substring(24) | ConvertFrom-Json } catch { $script:G03LastOracleCase += '-json'; return $false }
        if ($record.PSObject.Properties.Name.Count -ne 3 -or $record.source -cne 'path' -or $record.path -cne $sandboxPath -or $record.rule -cne $entry.Key) { $script:G03LastOracleCase += '-fields'; return $false }
        if ($finding.Stdout.Contains([string]$entry.Value)) { $script:G03LastOracleCase += '-leak'; return $false }
        if ($entry.Key -ne 'private_key') {
            [IO.File]::WriteAllText($fixturePath, ('X' + [string]$entry.Value + 'Y'), (New-Object Text.UTF8Encoding($false, $true)))
            $boundary = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $ReplayRoot -Arguments @('-NoProfile','-File',$scanner,'-Path',$sandboxPath)
            if ($boundary.TimedOut -or $boundary.ExitCode -ne 0 -or $boundary.Stdout.Trim() -cne 'CREDENTIAL_SCAN_PASS files=1') { $script:G03LastOracleCase += '-double-boundary'; return $false }
            if (-not (& $runOracleCase ($entry.Key + '-punct-left') ('.' + [string]$entry.Value) $entry.Key)) { return $false }
            if (-not (& $runOracleCase ($entry.Key + '-punct-right') ([string]$entry.Value + ':') $entry.Key)) { return $false }
            if (-not (& $runOracleCase ($entry.Key + '-punct-both') ('.' + [string]$entry.Value + ':') $entry.Key)) { return $false }
            $rightBoundaryValue = switch ($entry.Key) {
                'provider_api_key' { 's' + 'k-' + ('A' * 200) }
                'github_token' { 'gh' + 'p_' + ('B' * 255) }
                'slack_token' { 'xo' + 'xb-' + ('e' * 200) }
                default { [string]$entry.Value }
            }
            foreach ($neighbor in @('A','7','_','-')) {
                if (-not (& $runOracleCase ($entry.Key + '-blocked-left-' + [int][char]$neighbor) ($neighbor + [string]$entry.Value) '')) { return $false }
                if (-not (& $runOracleCase ($entry.Key + '-blocked-right-' + [int][char]$neighbor) ($rightBoundaryValue + $neighbor) '')) { return $false }
            }
        }
    }
    $lengthCases = @(
        @('provider-short',('s'+'k-'+('A'*19)),'') , @('provider-max',('s'+'k-'+('A'*200)),'provider_api_key'), @('provider-long',('s'+'k-'+('A'*201)),''),
        @('github-short',('gh'+'p_'+('B'*19)),''), @('github-max',('gh'+'p_'+('B'*255)),'github_token'), @('github-long',('gh'+'p_'+('B'*256)),''),
        @('aws-short',('AK'+'IA'+('C'*15)),''), @('aws-long',('AK'+'IA'+('C'*17)),''),
        @('google-short',('AI'+'za'+('D'*34)),''), @('google-long',('AI'+'za'+('D'*36)),''),
        @('slack-short',('xo'+'xb-'+('e'*9)),''), @('slack-max',('xo'+'xb-'+('e'*200)),'slack_token'), @('slack-long',('xo'+'xb-'+('e'*201)),'')
    )
    foreach ($case in $lengthCases) { if (-not (& $runOracleCase $case[0] $case[1] $case[2])) { return $false } }
    foreach ($prefix in @('ghp_','gho_','ghu_','ghs_','ghr_')) { if (-not (& $runOracleCase ('github-prefix-' + $prefix.TrimEnd('_')) ($prefix + ('F'*20)) 'github_token')) { return $false } }
    foreach ($prefix in @('AKIA','ASIA')) { if (-not (& $runOracleCase ('aws-prefix-' + $prefix) ($prefix + ('G'*16)) 'aws_access_key')) { return $false } }
    foreach ($prefix in @('xoxb-','xoxp-','xoxa-','xoxr-','xoxs-')) { if (-not (& $runOracleCase ('slack-prefix-' + $prefix.TrimEnd('-')) ($prefix + ('h'*10)) 'slack_token')) { return $false } }
    foreach ($kind in @('','RSA ','EC ','DSA ','OPENSSH ')) { if (-not (& $runOracleCase ('private-' + ($kind.Trim() -replace '^$','plain')) ('-----BEGIN ' + $kind + 'PRIVATE KEY-----') 'private_key')) { return $false } }
    $cleanPath = Join-Path $oracleRoot 'clean.txt'
    [IO.File]::WriteAllText($cleanPath, 'ordinary course notes', (New-Object Text.UTF8Encoding($false, $true)))
    $clean = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $ReplayRoot -Arguments @('-NoProfile','-File',$scanner,'-Path','oracle/clean.txt')
    if ($clean.TimedOut -or $clean.ExitCode -ne 0 -or $clean.Stdout.Trim() -cne 'CREDENTIAL_SCAN_PASS files=1') { return $false }

    [IO.File]::WriteAllBytes((Join-Path $oracleRoot 'invalid-utf8.txt'), [byte[]](0xC3,0x28))
    $invalidUtf8 = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $ReplayRoot -Arguments @('-NoProfile','-File',$scanner,'-Path','oracle/invalid-utf8.txt')
    if ($invalidUtf8.TimedOut -or $invalidUtf8.ExitCode -ne 3 -or $invalidUtf8.Stdout.Trim() -cne 'CREDENTIAL_SCAN_ERROR {"code":"read_failed"}') { return $false }

    $sortedPath = Join-Path $oracleRoot 'sorted.txt'
    $sortedText = $cases.provider_api_key + "`n" + $cases.aws_access_key + "`n" + $cases.provider_api_key
    [IO.File]::WriteAllText($sortedPath, $sortedText, (New-Object Text.UTF8Encoding($false, $true)))
    $sorted = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $ReplayRoot -Arguments @('-NoProfile','-File',$scanner,'-Path','oracle/sorted.txt')
    $sortedRules = @($sorted.Stdout -split "`r?`n" | Where-Object { $_ -ne '' } | ForEach-Object { ($_.Substring(24) | ConvertFrom-Json).rule })
    if ($sorted.TimedOut -or $sorted.ExitCode -ne 2 -or ($sortedRules -join ',') -cne 'aws_access_key,provider_api_key') { return $false }
    return $true
}

function Test-G03CandidateEvidence {
    param(
        [Parameter(Mandatory = $true)][string]$ColdRoot,
        [Parameter(Mandatory = $true)][string]$EvidenceRoot,
        [Parameter(Mandatory = $true)][string]$ExpectedSpecSha256,
        [Parameter(Mandatory = $true)][string]$ExpectedPlanSha256,
        [Parameter(Mandatory = $true)][scriptblock]$CommandInvoker
    )

    $artifactState = Test-G03ColdStartArtifacts -ColdRoot $ColdRoot
    if (-not $artifactState.Valid) { return [pscustomobject]@{ Valid = $false; Code = $artifactState.Code } }
    $specPath = Join-Path $ColdRoot 'SPEC.md'
    $planPath = Join-Path $ColdRoot 'PLAN.md'
    if ((Get-FileHash -LiteralPath $specPath -Algorithm SHA256).Hash -cne $ExpectedSpecSha256.ToUpperInvariant() -or
        (Get-FileHash -LiteralPath $planPath -Algorithm SHA256).Hash -cne $ExpectedPlanSha256.ToUpperInvariant()) {
        return [pscustomobject]@{ Valid = $false; Code = 'input_hash_mismatch' }
    }
    $scannerPath = Join-Path $ColdRoot 'scripts\bootstrap_scan_credentials.ps1'
    $contractPath = Join-Path $ColdRoot 'scripts\tests\bootstrap_scanner_contract.ps1'
    $expectedScannerHash = (Get-FileHash -LiteralPath $scannerPath -Algorithm SHA256).Hash
    $expectedContractHash = (Get-FileHash -LiteralPath $contractPath -Algorithm SHA256).Hash
    try {
        Read-G03StrictUtf8 $scannerPath | Out-Null
        Read-G03StrictUtf8 $contractPath | Out-Null
    } catch {
        return [pscustomobject]@{ Valid = $false; Code = 'artifact_utf8_invalid' }
    }
    $tokens = $null
    $parseErrors = $null
    $scannerAst = [Management.Automation.Language.Parser]::ParseFile($scannerPath, [ref]$tokens, [ref]$parseErrors)
    if ($parseErrors.Count -ne 0) { return [pscustomobject]@{ Valid = $false; Code = 'artifact_parse_failed' } }
    $functionNames = @($scannerAst.FindAll({ param($node) $node -is [Management.Automation.Language.FunctionDefinitionAst] }, $true) | ForEach-Object { $_.Name })
    foreach ($requiredFunction in @('Write-ScanRecord','Convert-SourceText','Find-DirectSecret')) {
        if ($functionNames -notcontains $requiredFunction) { return [pscustomobject]@{ Valid = $false; Code = 'required_function_missing' } }
    }

    $replayRoot = Join-Path $env:TEMP ('projectb-g03-replay-' + [guid]::NewGuid().ToString())
    try {
        New-Item -ItemType Directory -Path (Join-Path $replayRoot 'scripts\tests') -Force | Out-Null
        Copy-Item -LiteralPath $contractPath -Destination (Join-Path $replayRoot 'scripts\tests\bootstrap_scanner_contract.ps1')
        $redRun = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $replayRoot -Arguments @('-NoProfile','-File','scripts/tests/bootstrap_scanner_contract.ps1')
        if ($redRun.TimedOut -or $redRun.ExitCode -ne 1 -or $redRun.Stdout.Trim() -cne 'CONTRACT_RED scanner_missing') {
            return [pscustomobject]@{ Valid = $false; Code = 'red_replay_failed' }
        }
        if ((Get-FileHash -LiteralPath (Join-Path $replayRoot 'scripts\tests\bootstrap_scanner_contract.ps1') -Algorithm SHA256).Hash -cne $expectedContractHash -or
            (Test-Path -LiteralPath (Join-Path $replayRoot 'scripts\bootstrap_scan_credentials.ps1'))) {
            return [pscustomobject]@{ Valid = $false; Code = 'artifact_mutated' }
        }
        Copy-Item -LiteralPath $scannerPath -Destination (Join-Path $replayRoot 'scripts\bootstrap_scan_credentials.ps1')
        $greenRun = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $replayRoot -Arguments @('-NoProfile','-File','scripts/tests/bootstrap_scanner_contract.ps1')
        $greenLines = @($greenRun.Stdout -split "`r?`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' })
        $expectedGreen = @('usage_and_output','token_rules','artifact_direct_safety','BOOTSTRAP_SCANNER_CORE_PASS')
        if ($greenRun.TimedOut -or $greenRun.ExitCode -ne 0 -or $greenLines.Count -ne $expectedGreen.Count -or @(Compare-Object $greenLines $expectedGreen -SyncWindow 0).Count -ne 0) {
            return [pscustomobject]@{ Valid = $false; Code = 'green_replay_failed' }
        }
        if ((Get-FileHash -LiteralPath (Join-Path $replayRoot 'scripts\tests\bootstrap_scanner_contract.ps1') -Algorithm SHA256).Hash -cne $expectedContractHash -or
            (Get-FileHash -LiteralPath (Join-Path $replayRoot 'scripts\bootstrap_scan_credentials.ps1') -Algorithm SHA256).Hash -cne $expectedScannerHash) {
            return [pscustomobject]@{ Valid = $false; Code = 'artifact_mutated' }
        }
        if (-not (Test-G03ScannerBehavior -ReplayRoot $replayRoot -CommandInvoker $CommandInvoker)) {
            $detail = $script:G03LastOracleCase
            Remove-Variable G03LastOracleCase -Scope Script -ErrorAction SilentlyContinue
            return [pscustomobject]@{ Valid = $false; Code = 'behavior_oracle_failed'; Detail = $detail }
        }
        Remove-Variable G03LastOracleCase -Scope Script -ErrorAction SilentlyContinue
        if ((Get-FileHash -LiteralPath (Join-Path $replayRoot 'scripts\tests\bootstrap_scanner_contract.ps1') -Algorithm SHA256).Hash -cne $expectedContractHash -or
            (Get-FileHash -LiteralPath (Join-Path $replayRoot 'scripts\bootstrap_scan_credentials.ps1') -Algorithm SHA256).Hash -cne $expectedScannerHash) {
            return [pscustomobject]@{ Valid = $false; Code = 'artifact_mutated' }
        }
        $directOutputs = [Collections.Generic.List[string]]::new()
        foreach ($artifactPath in @(
            (Join-Path $replayRoot 'scripts\bootstrap_scan_credentials.ps1'),
            (Join-Path $replayRoot 'scripts\tests\bootstrap_scanner_contract.ps1')
        )) {
            $relativeArtifact = $artifactPath.Substring($replayRoot.Length).TrimStart('\','/').Replace('\','/')
            $scanRun = Invoke-G03CandidateChecked -CommandInvoker $CommandInvoker -WorkingDirectory $replayRoot -Arguments @('-NoProfile','-File','scripts/bootstrap_scan_credentials.ps1','-Path',$relativeArtifact)
            if ($scanRun.TimedOut -or $scanRun.ExitCode -ne 0 -or $scanRun.Stdout.Trim() -cne 'CREDENTIAL_SCAN_PASS files=1') {
                return [pscustomobject]@{ Valid = $false; Code = 'artifact_direct_scan_failed' }
            }
            $directOutputs.Add($scanRun.Stdout.Trim())
            if ((Get-FileHash -LiteralPath (Join-Path $replayRoot 'scripts\tests\bootstrap_scanner_contract.ps1') -Algorithm SHA256).Hash -cne $expectedContractHash -or
                (Get-FileHash -LiteralPath (Join-Path $replayRoot 'scripts\bootstrap_scan_credentials.ps1') -Algorithm SHA256).Hash -cne $expectedScannerHash) {
                return [pscustomobject]@{ Valid = $false; Code = 'artifact_mutated' }
            }
        }
        New-Item -ItemType Directory -Path $EvidenceRoot -Force | Out-Null
        $receipt = [ordered]@{
            red = 'CONTRACT_RED scanner_missing'
            green_output = $greenLines
            direct_scan_output = @($directOutputs)
            added_files = @('scripts/bootstrap_scan_credentials.ps1','scripts/tests/bootstrap_scanner_contract.ps1')
            scanner_sha256 = (Get-FileHash -LiteralPath $scannerPath -Algorithm SHA256).Hash
            contract_sha256 = (Get-FileHash -LiteralPath $contractPath -Algorithm SHA256).Hash
        }
        [IO.File]::WriteAllText((Join-Path $EvidenceRoot 'candidate-replay.json'), ($receipt | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false, $true)))
        $diff = @(
            "A scripts/bootstrap_scan_credentials.ps1 sha256=$($receipt.scanner_sha256)",
            "A scripts/tests/bootstrap_scanner_contract.ps1 sha256=$($receipt.contract_sha256)"
        ) -join "`n"
        [IO.File]::WriteAllText((Join-Path $EvidenceRoot 'candidate-added-files.diff'), ($diff + "`n"), (New-Object Text.UTF8Encoding($false, $true)))
        return [pscustomobject]@{ Valid = $true; Code = 'ok' }
    } finally {
        if (Test-Path -LiteralPath $replayRoot) { Remove-Item -LiteralPath $replayRoot -Recurse -Force }
    }
}

function Get-G03ExecutionEvidence {
    param(
        [Parameter(Mandatory = $true)][string]$StreamText,
        [Parameter(Mandatory = $true)][decimal]$MaxCostUsd
    )

    $bashCalls = 0
    $editCalls = 0
    $eventIndex = 0
    $toolUses = @{}
    $toolResults = @{}
    $resultObject = $null
    $cost = $null
    $resultSucceeded = $false
    foreach ($line in @($StreamText -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })) {
        $eventIndex++
        try { $event = $line | ConvertFrom-Json } catch { continue }
        if ($event.PSObject.Properties.Name -contains 'message' -and $event.message.PSObject.Properties.Name -contains 'content') {
            foreach ($item in @($event.message.content)) {
                if ($item.type -eq 'tool_use') {
                    if ($item.name -eq 'Bash') { $bashCalls++ }
                    if ($item.name -eq 'Edit') { $editCalls++ }
                    if ($item.PSObject.Properties.Name -contains 'id') {
                        $commandText = if ($item.PSObject.Properties.Name -contains 'input' -and $item.input.PSObject.Properties.Name -contains 'command') { [string]$item.input.command } else { '' }
                        $toolUses[[string]$item.id] = [pscustomobject]@{ Name=[string]$item.name; Command=$commandText; Index=$eventIndex }
                    }
                }
                if ($item.type -eq 'tool_result' -and $item.PSObject.Properties.Name -contains 'tool_use_id') {
                    $contentText = if ($item.content -is [string]) { [string]$item.content } else {
                        (@($item.content) | ForEach-Object { if ($_ -is [string]) { $_ } elseif ($_.PSObject.Properties.Name -contains 'text') { [string]$_.text } }) -join "`n"
                    }
                    $toolResults[[string]$item.tool_use_id] = [pscustomobject]@{
                        IsError = ($item.PSObject.Properties.Name -contains 'is_error' -and $item.is_error -eq $true)
                        Content = $contentText
                        Index = $eventIndex
                    }
                }
            }
        }
        if ($event.type -eq 'result') {
            $resultSucceeded = ($event.PSObject.Properties.Name -contains 'subtype' -and $event.subtype -ceq 'success' -and
                $event.PSObject.Properties.Name -contains 'is_error' -and $event.is_error -eq $false)
            if ($event.PSObject.Properties.Name -contains 'total_cost_usd') {
                try { $cost = [decimal]::Parse(([string]$event.total_cost_usd), [Globalization.CultureInfo]::InvariantCulture) } catch { }
            }
            if ($event.result -is [string] -and -not [string]::IsNullOrWhiteSpace([string]$event.result)) {
                try { $resultObject = ([string]$event.result) | ConvertFrom-Json } catch { }
            }
        }
    }
    if ($null -eq $resultObject) { return [pscustomobject]@{ Valid=$false; Code='empty_end_turn'; BashCalls=$bashCalls; EditCalls=$editCalls; CostUsd=$cost } }
    if (-not $resultSucceeded) { return [pscustomobject]@{ Valid=$false; Code='protocol_mismatch'; BashCalls=$bashCalls; EditCalls=$editCalls; CostUsd=$cost } }
    if ($null -eq $cost -or $cost -lt 0) { return [pscustomobject]@{ Valid=$false; Code='cost_missing'; BashCalls=$bashCalls; EditCalls=$editCalls; CostUsd=$cost } }
    if ($cost -gt $MaxCostUsd) { return [pscustomobject]@{ Valid=$false; Code='budget_exceeded'; BashCalls=$bashCalls; EditCalls=$editCalls; CostUsd=$cost } }
    foreach ($property in @('task','acceptance_id','ambiguities','questions','red_command','green_command')) {
        if ($resultObject.PSObject.Properties.Name -notcontains $property) {
            return [pscustomobject]@{ Valid=$false; Code='protocol_mismatch'; BashCalls=$bashCalls; EditCalls=$editCalls; CostUsd=$cost }
        }
    }
    $command = 'pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1'
    $contractUses = @($toolUses.GetEnumerator() | ForEach-Object {
        if ($_.Value.Name -ceq 'Bash' -and $_.Value.Command -ceq $command) {
            [pscustomobject]@{ Id=$_.Key; Command=$_.Value.Command; Index=$_.Value.Index }
        }
    } | Sort-Object Index)
    $tddEvidenceValid = $contractUses.Count -eq 2
    if ($tddEvidenceValid) {
        $redResult = $toolResults[$contractUses[0].Id]
        $greenResult = $toolResults[$contractUses[1].Id]
        $greenLines = if ($null -eq $greenResult) { @() } else { @($greenResult.Content -split "`r?`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }) }
        $expectedGreen = @('usage_and_output','token_rules','artifact_direct_safety','BOOTSTRAP_SCANNER_CORE_PASS')
        $redContent = if ($null -eq $redResult) { '' } else { ([string]$redResult.Content).Replace("`r`n", "`n") }
        $redNormalized = if ($redContent -ceq 'CONTRACT_RED scanner_missing' -or $redContent -ceq "Exit code 1`nCONTRACT_RED scanner_missing") { 'CONTRACT_RED scanner_missing' } else { $null }
        $tddEvidenceValid = $contractUses[0].Id -match '^[A-Za-z0-9_-]{1,128}$' -and $contractUses[1].Id -match '^[A-Za-z0-9_-]{1,128}$' -and
            $null -ne $redResult -and $null -ne $greenResult -and
            $contractUses[0].Index -lt $redResult.Index -and $redResult.Index -lt $contractUses[1].Index -and $contractUses[1].Index -lt $greenResult.Index -and
            $redResult.IsError -and $null -ne $redNormalized -and
            -not $greenResult.IsError -and $greenLines.Count -eq $expectedGreen.Count -and @(Compare-Object $greenLines $expectedGreen -SyncWindow 0).Count -eq 0
    }
    if (-not $tddEvidenceValid) {
        return [pscustomobject]@{ Valid=$false; Code='tdd_evidence_missing'; BashCalls=$bashCalls; EditCalls=$editCalls; CostUsd=$cost }
    }
    if ($resultObject.task -cne 'F-01S1' -or
        $resultObject.acceptance_id -cne 'F01S1_RED_GREEN_ARTIFACT_SAFETY_V1' -or
        $resultObject.ambiguities -isnot [Array] -or @($resultObject.ambiguities).Count -ne 0 -or
        $resultObject.questions -isnot [Array] -or
        $resultObject.red_command -cne $command -or
        $resultObject.green_command -cne $command -or
        $bashCalls -lt 2 -or $editCalls -ne 0) {
        return [pscustomobject]@{ Valid=$false; Code='protocol_mismatch'; BashCalls=$bashCalls; EditCalls=$editCalls; CostUsd=$cost }
    }
    return [pscustomobject]@{
        Valid = $true
        Code = 'ok'
        BashCalls = $bashCalls
        EditCalls = $editCalls
        CostUsd = $cost
        Questions = @($resultObject.questions)
        TddReceipt = @(
            [ordered]@{ phase='red'; tool_use_id=$contractUses[0].Id; tool_use_event=$contractUses[0].Index; tool_result_event=$redResult.Index; command=$command; exit_code=1; is_error=$true; output=@('CONTRACT_RED scanner_missing') },
            [ordered]@{ phase='green'; tool_use_id=$contractUses[1].Id; tool_use_event=$contractUses[1].Index; tool_result_event=$greenResult.Index; command=$command; is_error=$false; output=$expectedGreen }
        )
    }
}
