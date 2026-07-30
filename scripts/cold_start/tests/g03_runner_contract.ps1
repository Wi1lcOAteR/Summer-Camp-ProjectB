$ErrorActionPreference = 'Stop'

$coldStartRoot = Split-Path -Parent $PSScriptRoot
$core = Join-Path $coldStartRoot 'g03_runner_core.ps1'
if (-not (Test-Path -LiteralPath $core -PathType Leaf)) {
    Write-Output 'G03_RUNNER_CONTRACT_RED core_missing'
    exit 1
}
. $core

function Assert-Equal {
    param($Actual, $Expected, [string]$Message)
    if ($Actual -cne $Expected) { throw "$Message expected=$Expected actual=$Actual" }
}

function Write-Utf8NoBom {
    param([string]$Path, [string]$Text)
    [IO.File]::WriteAllText($Path, $Text, (New-Object Text.UTF8Encoding($false, $true)))
}

$root = Join-Path $env:TEMP ('projectb-g03-runner-' + [guid]::NewGuid().ToString())
try {
    New-Item -ItemType Directory -Path $root -Force | Out-Null
    $specPath = Join-Path $root 'SPEC.md'
    $planPath = Join-Path $root 'PLAN.md'
    Write-Utf8NoBom $specPath "# 规约`n<!-- AGENT_CAPSULE:SPEC:BEGIN -->`nAgent spec capsule.`n<!-- AGENT_CAPSULE:SPEC:END -->`n中文正文`n"
    Write-Utf8NoBom $planPath "# Plan`n<!-- AGENT_CAPSULE:PLAN:BEGIN -->`nAgent plan capsule.`n<!-- AGENT_CAPSULE:PLAN:END -->`n中文计划`n"

    $auto = Get-G03AgentDocuments -SpecPath $specPath -PlanPath $planPath -AgentLanguage Auto
    Assert-Equal $auto.EffectiveLanguage 'English' 'Auto must deterministically select English.'
    Assert-Equal $auto.SpecText 'Agent spec capsule.' 'Auto must extract only the SPEC capsule.'
    Assert-Equal $auto.PlanText 'Agent plan capsule.' 'Auto must extract only the PLAN capsule.'

    $english = Get-G03AgentDocuments -SpecPath $specPath -PlanPath $planPath -AgentLanguage English
    Assert-Equal $english.EffectiveLanguage 'English' 'English must remain English.'
    $chinese = Get-G03AgentDocuments -SpecPath $specPath -PlanPath $planPath -AgentLanguage Chinese
    Assert-Equal $chinese.EffectiveLanguage 'Chinese' 'Chinese diagnostic mode must remain Chinese.'
    if ($chinese.SpecText -notmatch '中文正文' -or $chinese.SpecText -match 'Agent spec capsule') {
        throw 'Chinese mode must return the body without the generated capsule.'
    }
    'language_modes'

    $bomPath = Join-Path $root 'bom.md'
    [IO.File]::WriteAllBytes($bomPath, [byte[]](0xEF,0xBB,0xBF,0x61))
    try { Read-G03StrictUtf8 $bomPath | Out-Null; throw 'BOM input unexpectedly passed.' } catch { Assert-Equal $_.Exception.Message 'UTF8_INVALID' 'BOM must fail closed.' }
    $invalidPath = Join-Path $root 'invalid.md'
    [IO.File]::WriteAllBytes($invalidPath, [byte[]](0xC3,0x28))
    try { Read-G03StrictUtf8 $invalidPath | Out-Null; throw 'Invalid UTF-8 unexpectedly passed.' } catch { Assert-Equal $_.Exception.Message 'UTF8_INVALID' 'Invalid UTF-8 must fail closed.' }
    $replacementPath = Join-Path $root 'replacement.md'
    Write-Utf8NoBom $replacementPath ([string][char]0xFFFD)
    try { Read-G03StrictUtf8 $replacementPath | Out-Null; throw 'U+FFFD unexpectedly passed.' } catch { Assert-Equal $_.Exception.Message 'UTF8_INVALID' 'U+FFFD must fail closed.' }
    'strict_utf8'

    $expected = [ordered]@{ spec_sha256 = 'SPEC-HASH'; plan_sha256 = 'PLAN-HASH'; files = @('PLAN.md','SPEC.md'); language = 'English'; task = 'F-01S1'; acceptance_id = 'F01S1_RED_GREEN_ARTIFACT_SAFETY_V1' }
    $goodReceipt = [pscustomobject]@{ spec_sha256 = 'SPEC-HASH'; plan_sha256 = 'PLAN-HASH'; files = @('PLAN.md','SPEC.md'); language = 'English'; task = 'F-01S1'; acceptance_id = 'F01S1_RED_GREEN_ARTIFACT_SAFETY_V1'; ambiguities = @() }
    Assert-Equal (Test-G03IntakeReceipt -Receipt $goodReceipt -Expected $expected) 'INTAKE_READY' 'Valid intake must be ready.'
    $ambiguous = $goodReceipt.PSObject.Copy(); $ambiguous.ambiguities = @('question')
    Assert-Equal (Test-G03IntakeReceipt -Receipt $ambiguous -Expected $expected) 'INTAKE_AMBIGUOUS' 'Ambiguity must block execution.'
    $wrong = $goodReceipt.PSObject.Copy(); $wrong.task = 'F-01S4'
    Assert-Equal (Test-G03IntakeReceipt -Receipt $wrong -Expected $expected) 'INTAKE_FAILED' 'Protocol mismatch must fail intake.'
    $wrongAcceptance = $goodReceipt.PSObject.Copy(); $wrongAcceptance.acceptance_id = 'arbitrary'
    Assert-Equal (Test-G03IntakeReceipt -Receipt $wrongAcceptance -Expected $expected) 'INTAKE_FAILED' 'Wrong acceptance identity must fail intake.'
    $goodEnvelope = [pscustomobject]@{ subtype='success'; is_error=$false; total_cost_usd=0.10; result='{}' }
    Assert-Equal (Test-G03IntakeEnvelope -Envelope $goodEnvelope -MaxCostUsd ([decimal]0.20)) 'ok' 'Successful bounded intake envelope must pass.'
    foreach ($badEnvelope in @(
        [pscustomobject]@{ subtype='error'; is_error=$true; total_cost_usd=0.10; result='{}' },
        [pscustomobject]@{ subtype='success'; is_error=$false; total_cost_usd=-0.01; result='{}' },
        [pscustomobject]@{ subtype='success'; is_error=$false; total_cost_usd=0.21; result='{}' },
        [pscustomobject]@{ subtype='success'; is_error=$false; total_cost_usd=0.10; result='' }
    )) {
        Assert-Equal (Test-G03IntakeEnvelope -Envelope $badEnvelope -MaxCostUsd ([decimal]0.20)) 'protocol_mismatch' 'Invalid intake envelope must fail closed.'
    }
    'intake_protocol'

    $artifactRoot = Join-Path $root 'artifacts'
    New-Item -ItemType Directory -Path $artifactRoot -Force | Out-Null
    Copy-Item $specPath $artifactRoot
    Copy-Item $planPath $artifactRoot
    Assert-Equal (Test-G03ColdStartArtifacts -ColdRoot $artifactRoot).Code 'required_artifact_missing' 'Missing outputs must fail.'
    New-Item -ItemType Directory -Path (Join-Path $artifactRoot 'scripts\tests') -Force | Out-Null
    Write-Utf8NoBom (Join-Path $artifactRoot 'scripts\bootstrap_scan_credentials.ps1') 'scanner'
    Write-Utf8NoBom (Join-Path $artifactRoot 'scripts\tests\bootstrap_scanner_contract.ps1') 'contract'
    Assert-Equal (Test-G03ColdStartArtifacts -ColdRoot $artifactRoot).Code 'ok' 'Exact output set must pass.'
    Write-Utf8NoBom (Join-Path $artifactRoot 'extra.txt') 'extra'
    Assert-Equal (Test-G03ColdStartArtifacts -ColdRoot $artifactRoot).Code 'unexpected_artifact' 'Extra output must fail.'
    'artifact_postcondition'

    Assert-Equal (Resolve-G03State -CapsuleValid:$false -Utf8Valid:$true -IntakeState INTAKE_READY -ExecutionExit 0 -ExecutionSignal ok -ArtifactsValid:$true) 'CAPSULE_INVALID' 'Capsule failure must dominate.'
    Assert-Equal (Resolve-G03State -CapsuleValid:$true -Utf8Valid:$false -IntakeState INTAKE_READY -ExecutionExit 0 -ExecutionSignal ok -ArtifactsValid:$true) 'UTF8_INVALID' 'UTF-8 failure must dominate.'
    Assert-Equal (Resolve-G03State -CapsuleValid:$true -Utf8Valid:$true -IntakeState INTAKE_FAILED -ExecutionExit 0 -ExecutionSignal ok -ArtifactsValid:$true) 'INTAKE_FAILED' 'Failed intake must stop.'
    Assert-Equal (Resolve-G03State -CapsuleValid:$true -Utf8Valid:$true -IntakeState INTAKE_AMBIGUOUS -ExecutionExit 0 -ExecutionSignal ok -ArtifactsValid:$true) 'INTAKE_AMBIGUOUS' 'Ambiguous intake must stop.'
    foreach ($signal in @('empty_end_turn','gateway_504','budget_exceeded','wall_timeout')) {
        Assert-Equal (Resolve-G03State -CapsuleValid:$true -Utf8Valid:$true -IntakeState INTAKE_READY -ExecutionExit 1 -ExecutionSignal $signal -ArtifactsValid:$false) 'EXECUTION_FAILED' "$signal must fail execution."
    }
    Assert-Equal (Resolve-G03State -CapsuleValid:$true -Utf8Valid:$true -IntakeState INTAKE_READY -ExecutionExit 0 -ExecutionSignal ok -ArtifactsValid:$false) 'COLD_START_INCOMPLETE' 'Missing artifacts must remain incomplete.'
    Assert-Equal (Resolve-G03State -CapsuleValid:$true -Utf8Valid:$true -IntakeState INTAKE_READY -ExecutionExit 0 -ExecutionSignal ok -ArtifactsValid:$true) 'G03_EVIDENCE_READY' 'Only the full success state may be ready.'
    'completion_state_machine'

    if (Test-G03SandboxPlatform -Platform Windows) { throw 'Native Windows must fail the OS sandbox preflight.' }
    if (-not (Test-G03SandboxPlatform -Platform Linux)) { throw 'Linux must be eligible for Claude sandbox startup.' }
    if (-not (Test-G03SandboxPlatform -Platform WSL2)) { throw 'WSL2 must be eligible for Claude sandbox startup.' }
    'sandbox_platform'

    $coreText = Get-Content -Raw -Encoding UTF8 $core
    if ($coreText -notlike "*@('/etc','/usr','/bin','/lib','/lib64'*") {
        throw 'Bubblewrap preflight must expose /etc read-only for PowerShell initialization.'
    }
    'sandbox_runtime_mounts'

    $cliRoot = Join-Path $root 'cli-root'
    New-Item -ItemType Directory -Path (Join-Path $cliRoot 'tmp/toolchains') -Force | Out-Null
    $cliFixture = Join-Path $cliRoot 'tmp/toolchains/claude'
    Write-Utf8NoBom $cliFixture 'cli'
    Assert-Equal (Resolve-G03ClaudeCliPath -ProjectRoot $cliRoot -ClaudeCli './tmp/toolchains/claude') $cliFixture 'Relative Claude CLI paths must resolve against ProjectRoot.'
    Assert-Equal (Resolve-G03ClaudeCliPath -ProjectRoot $cliRoot -ClaudeCli $cliFixture) $cliFixture 'Absolute Claude CLI paths must remain stable.'
    'cli_path_resolution'

    Assert-Equal (Get-G03ProcessDiagnosticCode -Stage 'intake' -ExitCode 1 -TimedOut:$false -Stdout '' -Stderr 'Invalid MCP configuration') 'cli_mcp_config' 'MCP failures must be classified without persisting raw stderr.'
    Assert-Equal (Get-G03ProcessDiagnosticCode -Stage 'intake' -ExitCode 1 -TimedOut:$false -Stdout '' -Stderr '401 authentication_failed') 'provider_auth' 'Authentication failures must be classified.'
    Assert-Equal (Get-G03ProcessDiagnosticCode -Stage 'intake' -ExitCode 1 -TimedOut:$false -Stdout '' -Stderr '504 Gateway Time-out') 'gateway_504' 'Gateway failures must be classified.'
    Assert-Equal (Get-G03ProcessDiagnosticCode -Stage 'intake' -ExitCode 1 -TimedOut:$false -Stdout '' -Stderr 'The shell cannot be started: No such file or directory') 'cli_startup' 'CLI startup failures must be classified.'
    Assert-Equal (Get-G03ProcessDiagnosticCode -Stage 'intake' -ExitCode 1 -TimedOut:$false -Stdout '' -Stderr 'opaque failure') 'child_nonzero' 'Unknown failures must use a bounded diagnostic code.'
    Assert-Equal (Get-G03ProcessDiagnosticCode -Stage 'intake' -ExitCode 0 -TimedOut:$false -Stdout '' -Stderr '') 'child_empty_output' 'Empty successful output must be classified.'
    Assert-Equal (Get-G03ProcessDiagnosticCode -Stage 'intake' -ExitCode 0 -TimedOut:$false -Stdout '{not-json' -Stderr '') 'child_output_protocol' 'Malformed successful output must be classified.'
    Assert-Equal (Get-G03ProcessDiagnosticCode -Stage 'intake' -ExitCode 124 -TimedOut:$true -Stdout '' -Stderr '') 'wall_timeout' 'Timeouts must be classified.'
    'process_diagnostics'

    $intakeJson = '{"subtype":"success","is_error":false,"total_cost_usd":0.10,"result":"{}"}'
    $permissionNoticeTail = 'Permission mode forced to default '
    $permissionNoticeSuffix = 'CLAUDE_CODE_SUBPROCESS_ENV_SCRUB is set (allowed_non_write_users hardening). Declare allowedTools explicitly, or set CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=0 to opt out.'
    $unicodePermissionNotice = ([string][char]0x26A0) + $permissionNoticeTail + ([string][char]0x2014) + $permissionNoticeSuffix
    $mojibakePermissionNotice = ([string][char]0x923F) + '?' + $permissionNoticeTail + ([string][char]0x9225) + '?' + $permissionNoticeSuffix
    Assert-Equal (Get-G03ClaudeJsonPayload -Text $intakeJson) $intakeJson 'Plain Claude JSON output must remain unchanged.'
    Assert-Equal (Get-G03ClaudeJsonPayload -Text ($unicodePermissionNotice + "`n" + $intakeJson)) $intakeJson 'The exact Unicode Claude permission notice may precede intake JSON.'
    Assert-Equal (Get-G03ClaudeJsonPayload -Text ($unicodePermissionNotice + "`r`n" + $intakeJson)) $intakeJson 'The exact Unicode notice must work with CRLF output.'
    Assert-Equal (Get-G03ClaudeJsonPayload -Text ($mojibakePermissionNotice + "`n" + $intakeJson)) $intakeJson 'The exact observed mojibake permission notice may precede intake JSON.'
    Assert-Equal (Get-G03ClaudeJsonPayload -Text (([string][char]0xFEFF) + ([string][char]0xFEFF) + $mojibakePermissionNotice + "`n" + $intakeJson)) $null 'Repeated BOMs must fail closed.'
    Assert-Equal (Get-G03ClaudeJsonPayload -Text ('Permission mode forced to default - ' + $permissionNoticeSuffix + "`n" + $intakeJson)) $null 'An unobserved ASCII notice variant must fail closed.'
    Assert-Equal (Get-G03ClaudeJsonPayload -Text ('ABCDEFGPermission mode forced to default!!!!' + $permissionNoticeSuffix + "`n" + $intakeJson)) $null 'Arbitrary notice prefixes and separators must fail closed.'
    Assert-Equal (Get-G03ClaudeJsonPayload -Text ($unicodePermissionNotice.Replace('Permission', 'permission') + "`n" + $intakeJson)) $null 'Notice matching must remain case-sensitive.'
    Assert-Equal (Get-G03ClaudeJsonPayload -Text ('arbitrary provider text' + "`n" + $intakeJson)) $null 'Arbitrary stdout preambles must fail closed.'
    Assert-Equal (Get-G03ClaudeJsonPayload -Text ($unicodePermissionNotice + "`n" + $unicodePermissionNotice + "`n" + $intakeJson)) $null 'Repeated permission notices must fail closed.'
    'claude_json_payload'

    $heartbeatStartInfo = [Diagnostics.ProcessStartInfo]::new()
    $heartbeatStartInfo.FileName = (Get-Process -Id $PID).Path
    $heartbeatStartInfo.UseShellExecute = $false
    $heartbeatStartInfo.CreateNoWindow = $true
    $heartbeatStartInfo.Arguments = '-NoProfile -Command "Start-Sleep -Seconds 3"'
    $heartbeatProcess = [Diagnostics.Process]::new()
    $heartbeatProcess.StartInfo = $heartbeatStartInfo
    if (-not $heartbeatProcess.Start()) { throw 'Heartbeat fixture process did not start.' }
    $heartbeatRecords = [Collections.Generic.List[object]]::new()
    $heartbeatWriter = {
        param([string]$Stage,[string]$Event,[int]$ElapsedSeconds)
        $heartbeatRecords.Add([pscustomobject]@{ Stage=$Stage; Event=$Event; ElapsedSeconds=$ElapsedSeconds })
    }
    $waitReceipt = Wait-G03ProcessWithHeartbeat -Process $heartbeatProcess -HostWallSeconds 5 -HeartbeatSeconds 1 -Stage 'intake' -ProgressWriter $heartbeatWriter
    if (-not $waitReceipt.Exited -or $waitReceipt.ElapsedSeconds -lt 2 -or $heartbeatRecords.Count -lt 1) {
        throw 'A running child process must produce heartbeat evidence before it exits.'
    }
    foreach ($record in $heartbeatRecords) {
        if ($record.Stage -cne 'intake' -or $record.Event -cne 'heartbeat' -or $record.ElapsedSeconds -lt 1) {
            throw 'Heartbeat evidence must use the requested stage and non-negative elapsed seconds.'
        }
    }
    'process_heartbeat'

    $writerFailureStartInfo = [Diagnostics.ProcessStartInfo]::new()
    $writerFailureStartInfo.FileName = (Get-Process -Id $PID).Path
    $writerFailureStartInfo.UseShellExecute = $false
    $writerFailureStartInfo.CreateNoWindow = $true
    $writerFailureStartInfo.Arguments = '-NoProfile -Command "Start-Sleep -Seconds 10"'
    $writerFailureProcess = [Diagnostics.Process]::new()
    $writerFailureProcess.StartInfo = $writerFailureStartInfo
    if (-not $writerFailureProcess.Start()) { throw 'Writer-failure fixture process did not start.' }
    $writerFailureCaught = $false
    try {
        $null = Wait-G03ProcessWithHeartbeat -Process $writerFailureProcess -HostWallSeconds 5 -HeartbeatSeconds 1 -Stage 'execution' -ProgressWriter { throw 'progress_write_failed' }
    } catch {
        $writerFailureCaught = $_.Exception.Message -match 'progress_write_failed'
    }
    if (-not $writerFailureCaught -or -not $writerFailureProcess.HasExited) {
        try { $writerFailureProcess.Kill() } catch { }
        throw 'A progress-writer failure must propagate only after terminating the child process.'
    }
    'process_writer_failure_cleanup'

    $timeoutMarker = Join-Path $root 'timeout-survivor.txt'
    $timeoutStartInfo = [Diagnostics.ProcessStartInfo]::new()
    $timeoutStartInfo.FileName = (Get-Process -Id $PID).Path
    $timeoutStartInfo.UseShellExecute = $false
    $timeoutStartInfo.CreateNoWindow = $true
    $escapedTimeoutMarker = $timeoutMarker.Replace("'", "''")
    $timeoutStartInfo.Arguments = '-NoProfile -Command "Start-Sleep -Seconds 3; Set-Content -LiteralPath ''' + $escapedTimeoutMarker + ''' -Value survived"'
    $timeoutProcess = [Diagnostics.Process]::new()
    $timeoutProcess.StartInfo = $timeoutStartInfo
    if (-not $timeoutProcess.Start()) { throw 'Timeout fixture process did not start.' }
    $timeoutReceipt = Wait-G03ProcessWithHeartbeat -Process $timeoutProcess -HostWallSeconds 1 -HeartbeatSeconds 1 -Stage 'execution' -ProgressWriter { param($Stage,$Event,$ElapsedSeconds) }
    Start-Sleep -Seconds 3
    if ($timeoutReceipt.Exited -or -not $timeoutReceipt.Terminated -or -not $timeoutProcess.HasExited -or (Test-Path -LiteralPath $timeoutMarker)) {
        try { $timeoutProcess.Kill() } catch { }
        throw 'A host-wall timeout must terminate the process before its delayed marker can be written.'
    }
    'process_timeout_cleanup'

    $candidateRoot = Join-Path $root 'candidate'
    New-Item -ItemType Directory -Path (Join-Path $candidateRoot 'scripts\tests') -Force | Out-Null
    Write-Utf8NoBom (Join-Path $candidateRoot 'SPEC.md') 'spec-input'
    Write-Utf8NoBom (Join-Path $candidateRoot 'PLAN.md') 'plan-input'
    $contractText = @'
$scanner = Join-Path (Split-Path -Parent $PSScriptRoot) 'bootstrap_scan_credentials.ps1'
if (-not (Test-Path -LiteralPath $scanner -PathType Leaf)) { 'CONTRACT_RED scanner_missing'; exit 1 }
'usage_and_output'
'token_rules'
'artifact_direct_safety'
'BOOTSTRAP_SCANNER_CORE_PASS'
'@
    $scannerText = @'
param([string]$Path)
$utf8 = New-Object Text.UTF8Encoding($false,$true)
function Write-ScanRecord { param([string]$Source,[string]$Path,[string]$Rule) 'CREDENTIAL_SCAN_FINDING ' + ([ordered]@{source=$Source;path=$Path;rule=$Rule}|ConvertTo-Json -Compress) }
function Convert-SourceText { param([byte[]]$Bytes) $utf8.GetString($Bytes) }
function Find-DirectSecret {
    param([string]$Text)
    $alpha='[A-Za-z0-9_-]';$alnum='[A-Za-z0-9]';$upper='[A-Z0-9]';$hyphen='[A-Za-z0-9-]'
    $rules=[ordered]@{
        provider_api_key='s'+'k-'+$alpha+'{20,200}'
        github_token='(?:ghp_|gho_|ghu_|ghs_|ghr_)'+$alnum+'{20,255}'
        aws_access_key='(?:AKIA|ASIA)'+$upper+'{16}'
        google_api_key='AI'+'za'+$alpha+'{35}'
        slack_token='(?:xoxb-|xoxp-|xoxa-|xoxr-|xoxs-)'+$hyphen+'{10,200}'
        private_key='-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'
    }
    foreach($entry in $rules.GetEnumerator()) {
        $pattern=if($entry.Key -eq 'private_key'){$entry.Value}else{'(?<![A-Za-z0-9_-])(?:'+$entry.Value+')(?![A-Za-z0-9_-])'}
        if([regex]::IsMatch($Text,$pattern)){ $entry.Key }
    }
}
if([string]::IsNullOrWhiteSpace($Path)){ 'CREDENTIAL_SCAN_ERROR {"code":"usage_missing_scope"}';exit 3 }
try{$text=Convert-SourceText ([IO.File]::ReadAllBytes($Path))}catch{'CREDENTIAL_SCAN_ERROR {"code":"read_failed"}';exit 3}
$rules=@(Find-DirectSecret $text|Sort-Object -Unique)
if($rules.Count-eq0){'CREDENTIAL_SCAN_PASS files=1';exit 0}
foreach($rule in $rules){Write-ScanRecord -Source 'path' -Path $Path -Rule $rule}
exit 2
'@
    Write-Utf8NoBom (Join-Path $candidateRoot 'scripts\tests\bootstrap_scanner_contract.ps1') $contractText
    Write-Utf8NoBom (Join-Path $candidateRoot 'scripts\bootstrap_scan_credentials.ps1') $scannerText
    $candidateEvidence = Join-Path $root 'candidate-evidence'
    $candidateSpecHash = (Get-FileHash -LiteralPath (Join-Path $candidateRoot 'SPEC.md') -Algorithm SHA256).Hash
    $candidatePlanHash = (Get-FileHash -LiteralPath (Join-Path $candidateRoot 'PLAN.md') -Algorithm SHA256).Hash
    $localInvoker = {
        param([string]$WorkingDirectory,[string[]]$CommandArguments,[int]$WallSeconds)
        Push-Location $WorkingDirectory
        try {
            $output = @(& (Get-Process -Id $PID).Path @CommandArguments 2>&1)
            [pscustomobject]@{ ExitCode=$LASTEXITCODE; TimedOut=$false; Stdout=($output -join "`n"); Stderr='' }
        } finally { Pop-Location }
    }
    $verifiedCandidate = Test-G03CandidateEvidence -ColdRoot $candidateRoot -EvidenceRoot $candidateEvidence -ExpectedSpecSha256 $candidateSpecHash -ExpectedPlanSha256 $candidatePlanHash -CommandInvoker $localInvoker
    if (-not $verifiedCandidate.Valid -or $verifiedCandidate.Code -ne 'ok') { throw "Valid candidate replay failed: $($verifiedCandidate.Code) detail=$($verifiedCandidate.Detail)" }
    $encodedValidScanner = [Convert]::ToBase64String((New-Object Text.UTF8Encoding($false,$true)).GetBytes($scannerText))
    $swapContract = @"
`$scanner = Join-Path (Split-Path -Parent `$PSScriptRoot) 'bootstrap_scan_credentials.ps1'
if (-not (Test-Path -LiteralPath `$scanner -PathType Leaf)) { 'CONTRACT_RED scanner_missing'; exit 1 }
`$bytes=[Convert]::FromBase64String('$encodedValidScanner')
[IO.File]::WriteAllBytes(`$scanner,`$bytes)
'usage_and_output'
'token_rules'
'artifact_direct_safety'
'BOOTSTRAP_SCANNER_CORE_PASS'
"@
    $fixedPassScanner = @'
param([string]$Path)
function Write-ScanRecord { }
function Convert-SourceText { }
function Find-DirectSecret { }
if([string]::IsNullOrWhiteSpace($Path)){ 'CREDENTIAL_SCAN_ERROR {"code":"usage_missing_scope"}';exit 3 }
'CREDENTIAL_SCAN_PASS files=1';exit 0
'@
    Write-Utf8NoBom (Join-Path $candidateRoot 'scripts\tests\bootstrap_scanner_contract.ps1') $swapContract
    Write-Utf8NoBom (Join-Path $candidateRoot 'scripts\bootstrap_scan_credentials.ps1') $fixedPassScanner
    $swapCandidate = Test-G03CandidateEvidence -ColdRoot $candidateRoot -EvidenceRoot $candidateEvidence -ExpectedSpecSha256 $candidateSpecHash -ExpectedPlanSha256 $candidatePlanHash -CommandInvoker $localInvoker
    if ($swapCandidate.Valid -or $swapCandidate.Code -ne 'artifact_mutated') { throw 'A candidate contract that replaces the scanner during green replay must fail.' }
    Write-Utf8NoBom (Join-Path $candidateRoot 'scripts\tests\bootstrap_scanner_contract.ps1') $contractText
    $emptyScanner = @'
param([string]$Path)
function Write-ScanRecord { }
function Convert-SourceText { }
function Find-DirectSecret { }
if([string]::IsNullOrWhiteSpace($Path)){ 'CREDENTIAL_SCAN_ERROR {"code":"usage_missing_scope"}';exit 3 }
'CREDENTIAL_SCAN_PASS files=1';exit 0
'@
    Write-Utf8NoBom (Join-Path $candidateRoot 'scripts\bootstrap_scan_credentials.ps1') $emptyScanner
    $forgedCandidate = Test-G03CandidateEvidence -ColdRoot $candidateRoot -EvidenceRoot $candidateEvidence -ExpectedSpecSha256 $candidateSpecHash -ExpectedPlanSha256 $candidatePlanHash -CommandInvoker $localInvoker
    if ($forgedCandidate.Valid -or $forgedCandidate.Code -ne 'behavior_oracle_failed') { throw 'A fixed-PASS empty implementation must fail the coordinator behavior oracle.' }
    $wrongOrderScanner = $scannerText.Replace('[ordered]@{source=$Source;path=$Path;rule=$Rule}','[ordered]@{rule=$Rule;path=$Path;source=$Source}')
    Write-Utf8NoBom (Join-Path $candidateRoot 'scripts\bootstrap_scan_credentials.ps1') $wrongOrderScanner
    $wrongOrderCandidate = Test-G03CandidateEvidence -ColdRoot $candidateRoot -EvidenceRoot $candidateEvidence -ExpectedSpecSha256 $candidateSpecHash -ExpectedPlanSha256 $candidatePlanHash -CommandInvoker $localInvoker
    if ($wrongOrderCandidate.Valid -or $wrongOrderCandidate.Code -ne 'behavior_oracle_failed') { throw 'A finding with non-contract JSON key order must fail the coordinator behavior oracle.' }
    $lineAnchoredScanner = $scannerText.Replace("'(?<![A-Za-z0-9_-])(?:'+`$entry.Value+')(?![A-Za-z0-9_-])'","'(?m)^(?:'+`$entry.Value+')$'")
    Write-Utf8NoBom (Join-Path $candidateRoot 'scripts\bootstrap_scan_credentials.ps1') $lineAnchoredScanner
    $lineAnchoredCandidate = Test-G03CandidateEvidence -ColdRoot $candidateRoot -EvidenceRoot $candidateEvidence -ExpectedSpecSha256 $candidateSpecHash -ExpectedPlanSha256 $candidatePlanHash -CommandInvoker $localInvoker
    if ($lineAnchoredCandidate.Valid -or $lineAnchoredCandidate.Code -ne 'behavior_oracle_failed') { throw 'A line-anchored scanner that rejects valid punctuation neighbors must fail the coordinator behavior oracle.' }
    Write-Utf8NoBom (Join-Path $candidateRoot 'scripts\bootstrap_scan_credentials.ps1') $scannerText
    Write-Utf8NoBom (Join-Path $candidateRoot 'SPEC.md') 'mutated-input'
    $mutatedCandidate = Test-G03CandidateEvidence -ColdRoot $candidateRoot -EvidenceRoot $candidateEvidence -ExpectedSpecSha256 $candidateSpecHash -ExpectedPlanSha256 $candidatePlanHash -CommandInvoker $localInvoker
    if ($mutatedCandidate.Valid -or $mutatedCandidate.Code -ne 'input_hash_mismatch') { throw 'Mutated input must fail candidate verification.' }
    'candidate_replay'

    $executionResult = [ordered]@{
        task = 'F-01S1'
        acceptance_id = 'F01S1_RED_GREEN_ARTIFACT_SAFETY_V1'
        ambiguities = @()
        questions = @()
        red_command = 'pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1'
        green_command = 'pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1'
    } | ConvertTo-Json -Compress
    $redId = 'red-1'; $greenId = 'green-1'
    $stream = @(
        ([ordered]@{ type='assistant'; message=[ordered]@{ content=@([ordered]@{ type='tool_use'; id=$redId; name='Bash'; input=[ordered]@{command='pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1'} }) } } | ConvertTo-Json -Compress -Depth 8),
        ([ordered]@{ type='user'; message=[ordered]@{ content=@([ordered]@{ type='tool_result'; tool_use_id=$redId; is_error=$true; content="Exit code 1`nCONTRACT_RED scanner_missing" }) } } | ConvertTo-Json -Compress -Depth 8),
        ([ordered]@{ type='assistant'; message=[ordered]@{ content=@([ordered]@{ type='tool_use'; id=$greenId; name='Bash'; input=[ordered]@{command='pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1'} }) } } | ConvertTo-Json -Compress -Depth 8),
        ([ordered]@{ type='user'; message=[ordered]@{ content=@([ordered]@{ type='tool_result'; tool_use_id=$greenId; is_error=$false; content="usage_and_output`ntoken_rules`nartifact_direct_safety`nBOOTSTRAP_SCANNER_CORE_PASS" }) } } | ConvertTo-Json -Compress -Depth 8),
        ([ordered]@{ type='result'; subtype='success'; is_error=$false; total_cost_usd=0.50; result=$executionResult } | ConvertTo-Json -Compress -Depth 8)
    ) -join "`n"
    $streamEvidence = Get-G03ExecutionEvidence -StreamText $stream -MaxCostUsd ([decimal]0.80)
    if (-not $streamEvidence.Valid -or $streamEvidence.BashCalls -ne 2 -or $streamEvidence.EditCalls -ne 0 -or $streamEvidence.CostUsd -ne [decimal]0.50) {
        throw "Valid execution stream failed: $($streamEvidence.Code)"
    }
    if (@($streamEvidence.TddReceipt).Count -ne 2 -or $streamEvidence.TddReceipt[0].phase -cne 'red' -or $streamEvidence.TddReceipt[1].phase -cne 'green') {
        throw 'Validated execution evidence must expose a two-step ordered TDD receipt.'
    }
    if ($streamEvidence.TddReceipt[0].exit_code -ne 1 -or
        @($streamEvidence.TddReceipt[0].output).Count -ne 1 -or
        $streamEvidence.TddReceipt[0].output[0] -cne 'CONTRACT_RED scanner_missing') {
        throw 'The persisted red receipt must normalize the Claude wrapper to exit code 1 and the single allowed contract line.'
    }
    $noticeStream = Get-G03ExecutionEvidence -StreamText ($unicodePermissionNotice + "`n" + $stream) -MaxCostUsd ([decimal]0.80)
    if (-not $noticeStream.Valid) { throw "The exact Unicode permission notice may precede execution stream JSON: $($noticeStream.Code)" }
    $arbitraryPreambleStream = Get-G03ExecutionEvidence -StreamText ('ARBITRARY PREAMBLE' + "`n" + $stream) -MaxCostUsd ([decimal]0.80)
    if ($arbitraryPreambleStream.Valid -or $arbitraryPreambleStream.Code -ne 'stream_output_protocol') { throw 'Arbitrary execution stdout preambles must fail closed.' }
    $repeatedNoticeStream = Get-G03ExecutionEvidence -StreamText ($unicodePermissionNotice + "`n" + $unicodePermissionNotice + "`n" + $stream) -MaxCostUsd ([decimal]0.80)
    if ($repeatedNoticeStream.Valid -or $repeatedNoticeStream.Code -ne 'stream_output_protocol') { throw 'Repeated execution permission notices must fail closed.' }
    $missingToolResult = Get-G03ExecutionEvidence -StreamText (($stream -split "`n" | Where-Object { -not ($_ -match $greenId -and $_ -match '"type":"tool_result"') }) -join "`n") -MaxCostUsd ([decimal]0.80)
    if ($missingToolResult.Valid -or $missingToolResult.Code -ne 'tdd_evidence_missing') { throw "Self-reported red/green commands without matching tool results must fail: $($missingToolResult.Code)" }
    $nullAmbiguitiesResult = ($executionResult | ConvertFrom-Json); $nullAmbiguitiesResult.ambiguities = $null
    $nullResultJson = $nullAmbiguitiesResult | ConvertTo-Json -Compress
    $nullStreamLines = @($stream -split "`n")
    $nullStreamLines[-1] = ([ordered]@{ type='result'; subtype='success'; is_error=$false; total_cost_usd=0.50; result=$nullResultJson } | ConvertTo-Json -Compress -Depth 8)
    $nullStream = $nullStreamLines -join "`n"
    $nullAmbiguities = Get-G03ExecutionEvidence -StreamText $nullStream -MaxCostUsd ([decimal]0.80)
    if ($nullAmbiguities.Valid -or $nullAmbiguities.Code -ne 'protocol_mismatch') { throw "Null ambiguities must not be accepted as an empty array: $($nullAmbiguities.Code)" }
    $wrongExitRedStream = $stream.Replace('Exit code 1\nCONTRACT_RED scanner_missing','Exit code 2\nCONTRACT_RED scanner_missing')
    $wrongExitRed = Get-G03ExecutionEvidence -StreamText $wrongExitRedStream -MaxCostUsd ([decimal]0.80)
    if ($wrongExitRed.Valid -or $wrongExitRed.Code -ne 'tdd_evidence_missing') { throw 'A Claude wrapper reporting any exit code other than 1 must fail evidence validation.' }
    $extraRedStream = $stream.Replace('Exit code 1\nCONTRACT_RED scanner_missing','Exit code 1\nnoise-before-red\nCONTRACT_RED scanner_missing')
    $extraRed = Get-G03ExecutionEvidence -StreamText $extraRedStream -MaxCostUsd ([decimal]0.80)
    if ($extraRed.Valid -or $extraRed.Code -ne 'tdd_evidence_missing') { throw 'Red tool output with any extra line must fail exact evidence validation.' }
    $overBudget = Get-G03ExecutionEvidence -StreamText $stream.Replace('0.5','0.9') -MaxCostUsd ([decimal]0.80)
    if ($overBudget.Valid -or $overBudget.Code -ne 'budget_exceeded') { throw 'Over-budget stream must fail.' }
    $empty = Get-G03ExecutionEvidence -StreamText '{"type":"result","total_cost_usd":0.1,"result":""}' -MaxCostUsd ([decimal]0.80)
    if ($empty.Valid -or $empty.Code -ne 'empty_end_turn') { throw 'Empty result must fail.' }
    'execution_evidence'

    'G03_RUNNER_CONTRACT_PASS cases=13'
} finally {
    if (Test-Path -LiteralPath $root) { Remove-Item -LiteralPath $root -Recurse -Force }
}
