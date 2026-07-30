param(
    [ValidateSet('Auto','English','Chinese')]
    [string]$AgentLanguage = 'Auto',
    [ValidateSet('claude-sonnet-4-6')]
    [string]$Model = 'claude-sonnet-4-6',
    [ValidateRange(0.01, 1.00)]
    [decimal]$MaxTotalBudgetUsd = [decimal]1.00,
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Fa-f0-9]{64}$')]
    [string]$ExpectedSpecSha256,
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Fa-f0-9]{64}$')]
    [string]$ExpectedPlanSha256,
    [string]$ProjectRoot,
    [string]$ClaudeCli,
    [ValidateSet('https://ai2.1343263.xyz')]
    [string]$BaseUrl = 'https://ai2.1343263.xyz',
    [string]$EvidenceRoot,
    [ValidateSet('None','IntakeAmbiguous','Gateway504','MissingArtifacts','UnhandledError','Ready')]
    [string]$TestScenario = 'None'
)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
}
. (Join-Path $PSScriptRoot 'g03_runner_core.ps1')
if ([string]::IsNullOrWhiteSpace($ClaudeCli)) {
    $ClaudeCli = Join-Path $ProjectRoot 'tmp\toolchains\claude-code\node_modules\@anthropic-ai\claude-code\bin\claude.exe'
}
$ClaudeCli = Resolve-G03ClaudeCliPath -ProjectRoot $ProjectRoot -ClaudeCli $ClaudeCli

$intakeBudgetUsd = [decimal]0.20
$executionBudgetUsd = [decimal]0.80
$intakeWallSeconds = 300
$executionWallSeconds = 1200
$sessionId = [guid]::NewGuid().ToString()
$coldRoot = Join-Path $env:TEMP ("projectb-g03-$sessionId")
if ([string]::IsNullOrWhiteSpace($EvidenceRoot)) {
    $EvidenceRoot = Join-Path $ProjectRoot ("tmp\g03-evidence\$sessionId")
}
$script:G03StatusLogPath = Join-Path $EvidenceRoot 'status.log'
$heartbeatSeconds = 15

function Write-G03Progress {
    param(
        [Parameter(Mandatory = $true)][ValidatePattern('^[a-z0-9_]+$')][string]$Stage,
        [Parameter(Mandatory = $true)][ValidatePattern('^[A-Za-z0-9_]+$')][string]$Event,
        [int]$ElapsedSeconds = -1
    )
    $record = [ordered]@{
        timestamp = (Get-Date).ToUniversalTime().ToString('o')
        stage = $Stage
        event = $Event
    }
    if ($ElapsedSeconds -ge 0) { $record.elapsed_seconds = $ElapsedSeconds }
    $line = ($record | ConvertTo-Json -Compress) + "`n"
    [IO.File]::AppendAllText($script:G03StatusLogPath, $line, (New-Object Text.UTF8Encoding($false, $true)))
    $elapsedSuffix = if ($ElapsedSeconds -ge 0) { " elapsed_seconds=$ElapsedSeconds" } else { '' }
    [Console]::Out.WriteLine("G03_PROGRESS stage=$Stage event=$Event$elapsedSuffix")
}

function Write-G03JsonNoBom {
    param([string]$Path, $Value)
    [IO.File]::WriteAllText($Path, ($Value | ConvertTo-Json -Depth 12), (New-Object Text.UTF8Encoding($false, $true)))
}

function Write-G03Completion {
    param([string]$Status, [int]$ExitCode)
    $isTest = $TestScenario -ne 'None'
    $receipt = [ordered]@{
        schema = if ($isTest) { 'projectb.g03.test.v1' } else { 'projectb.g03.formal.v1' }
        formal = -not $isTest
        status = $Status
        exit_code = $ExitCode
        session_id = $sessionId
        completed_at = (Get-Date).ToString('o')
        cold_root = $coldRoot
        evidence_root = $EvidenceRoot
        status_log = 'status.log'
    }
    Write-G03JsonNoBom (Join-Path $EvidenceRoot 'completion.json') $receipt
}

function Write-G03ProcessDiagnostic {
    param([Parameter(Mandatory = $true)]$Run, [Parameter(Mandatory = $true)][ValidateSet('intake','execution')][string]$Stage)
    Write-G03JsonNoBom (Join-Path $EvidenceRoot 'process-diagnostic.json') ([ordered]@{
        stage = $Stage
        exit_code = [int]$Run.ExitCode
        timed_out = [bool]$Run.TimedOut
        code = Get-G03ProcessDiagnosticCode -Stage $Stage -ExitCode $Run.ExitCode -TimedOut $Run.TimedOut -Stdout $Run.Stdout -Stderr $Run.Stderr
    })
}

function Stop-G03 {
    param([string]$Status, [int]$ExitCode)
    Write-G03Progress -Stage 'completion' -Event $Status
    Write-G03Progress -Stage 'runner' -Event 'finished'
    Write-G03Completion $Status $ExitCode
    Write-Output "G03_RUNNER_STATE $Status"
    exit $ExitCode
}

function Invoke-G03Claude {
    param(
        [string[]]$Arguments,
        [int]$WallSeconds,
        [string]$SecretValue,
        [ValidateSet('intake','execution')][string]$Stage
    )
    $timeoutCommand = Get-Command timeout -ErrorAction Stop
    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $timeoutCommand.Source
    $startInfo.WorkingDirectory = $coldRoot
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true
    if ($null -eq $startInfo.ArgumentList) { throw 'process_argument_list_unavailable' }
    foreach ($argument in @('--signal=TERM','--kill-after=5s',("$WallSeconds" + 's'),$ClaudeCli) + $Arguments) {
        $startInfo.ArgumentList.Add([string]$argument)
    }
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    if (-not $process.Start()) { throw 'process_start_failed' }
    try {
        Write-G03Progress -Stage $Stage -Event 'process_started'
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        $hostWallSeconds = $WallSeconds + 10
        $progressWriter = { param($ProgressStage,$ProgressEvent,$ProgressElapsed) Write-G03Progress -Stage $ProgressStage -Event $ProgressEvent -ElapsedSeconds $ProgressElapsed }
        $waitReceipt = Wait-G03ProcessWithHeartbeat -Process $process -HostWallSeconds $hostWallSeconds -HeartbeatSeconds $heartbeatSeconds -Stage $Stage -ProgressWriter $progressWriter
        $boundedExit = $waitReceipt.Exited
        if (-not $boundedExit -and -not $waitReceipt.Terminated -and -not $process.HasExited) {
            throw 'process_tree_termination_failed'
        }
        $outText = $stdoutTask.GetAwaiter().GetResult()
        $errText = $stderrTask.GetAwaiter().GetResult()
        $elapsed = $waitReceipt.ElapsedSeconds
        $timedOut = (-not $boundedExit) -or $process.ExitCode -eq 124
        Write-G03Progress -Stage $Stage -Event $(if ($timedOut) { 'timed_out' } else { 'process_finished' }) -ElapsedSeconds $elapsed
        [pscustomobject]@{
            ExitCode = $process.ExitCode
            TimedOut = $timedOut
            Stdout = if ([string]::IsNullOrEmpty($SecretValue)) { $outText } else { $outText.Replace($SecretValue, '[REDACTED]') }
            Stderr = if ([string]::IsNullOrEmpty($SecretValue)) { $errText } else { $errText.Replace($SecretValue, '[REDACTED]') }
        }
    } finally {
        if (-not $process.HasExited) {
            try { $process.Kill($true) } catch { try { $process.Kill() } catch { } }
            if (-not $process.WaitForExit(5000)) { throw 'process_tree_termination_failed' }
        }
    }
}

function Get-G03ResultObject {
    param([string]$Text)
    try {
        $outer = $Text | ConvertFrom-Json
        if ($outer.PSObject.Properties.Name -contains 'result' -and $outer.result -is [string]) {
            return ([string]$outer.result) | ConvertFrom-Json
        }
        return $outer
    } catch {
        return $null
    }
}

function Protect-G03EvidenceText {
    param([string]$Value, [string]$SecretValue)
    $safe = [string]$Value
    if (-not [string]::IsNullOrEmpty($SecretValue)) { $safe = $safe.Replace($SecretValue, '[REDACTED]') }
    $safe = [regex]::Replace($safe, '(?i)(authorization\s*[:=]\s*(?:bearer\s+)?)[^\s"'']+', '$1[REDACTED]')
    $providerPrefix = 's' + 'k-'
    return [regex]::Replace($safe, [regex]::Escape($providerPrefix) + '[A-Za-z0-9_-]{8,}', '[REDACTED]')
}

New-Item -ItemType Directory -Path $coldRoot -Force | Out-Null
New-Item -ItemType Directory -Path $EvidenceRoot -Force | Out-Null
[Console]::Out.WriteLine("G03_EVIDENCE_ROOT $EvidenceRoot")
Write-G03Progress -Stage 'runner' -Event 'started'
trap {
    $ErrorActionPreference = 'Continue'
    try { Write-G03Progress -Stage 'completion' -Event 'UNHANDLED_ERROR' } catch { }
    try { Write-G03Progress -Stage 'runner' -Event 'finished' } catch { }
    try { Write-G03Completion 'UNHANDLED_ERROR' 99 } catch { }
    [Console]::Error.WriteLine('G03_RUNNER_STATE UNHANDLED_ERROR')
    exit 99
}

$currentPowerShell = (Get-Process -Id $PID).Path
Write-G03Progress -Stage 'capsule' -Event 'started'
$capsuleCheck = @(& $currentPowerShell -NoProfile -File (Join-Path $PSScriptRoot 'update_agent_capsules.ps1') -Mode Check -Root $ProjectRoot 2>&1)
if ($LASTEXITCODE -ne 0 -or ($capsuleCheck -join "`n") -notmatch '^AGENT_CAPSULE_PASS documents=2$') {
    Stop-G03 'CAPSULE_INVALID' 30
}
Write-G03Progress -Stage 'capsule' -Event 'passed'

$sourceSpec = Join-Path $ProjectRoot 'SPEC.md'
$sourcePlan = Join-Path $ProjectRoot 'PLAN.md'
try {
    $agentDocuments = Get-G03AgentDocuments -SpecPath $sourceSpec -PlanPath $sourcePlan -AgentLanguage $AgentLanguage
} catch {
    if ($_.Exception.Message -eq 'CAPSULE_INVALID') { Stop-G03 'CAPSULE_INVALID' 30 }
    Stop-G03 'UTF8_INVALID' 31
}

Copy-Item -LiteralPath $sourceSpec -Destination $coldRoot
Copy-Item -LiteralPath $sourcePlan -Destination $coldRoot
$specHash = (Get-FileHash -LiteralPath (Join-Path $coldRoot 'SPEC.md') -Algorithm SHA256).Hash
$planHash = (Get-FileHash -LiteralPath (Join-Path $coldRoot 'PLAN.md') -Algorithm SHA256).Hash
if ($specHash -cne $ExpectedSpecSha256.ToUpperInvariant() -or $planHash -cne $ExpectedPlanSha256.ToUpperInvariant()) {
    Stop-G03 'INTAKE_FAILED' 32
}
$initialFiles = @(Get-ChildItem -LiteralPath $coldRoot -File -Force | Select-Object -ExpandProperty Name | Sort-Object)
if ($initialFiles.Count -ne 2 -or $initialFiles[0] -cne 'PLAN.md' -or $initialFiles[1] -cne 'SPEC.md') {
    Stop-G03 'INTAKE_FAILED' 33
}
Write-G03Progress -Stage 'input' -Event 'validated'

$metadata = [ordered]@{
    started_at = (Get-Date).ToString('o')
    session_id = $sessionId
    spec_sha256 = $specHash
    plan_sha256 = $planHash
    initial_files = $initialFiles
    requested_language = $AgentLanguage
    effective_language = $agentDocuments.EffectiveLanguage
    capsule_version = 1
    capsule_spec_sha256 = (Get-FileHash -LiteralPath (Join-Path $ProjectRoot 'docs\cold-start\agent-capsules.json') -Algorithm SHA256).Hash
    model = $Model
    max_total_budget_usd = $MaxTotalBudgetUsd
    intake_budget_usd = $intakeBudgetUsd
    execution_budget_usd = $executionBudgetUsd
    api_retries = 0
    provider_host = ([Uri]$BaseUrl).Host
}
Write-G03JsonNoBom (Join-Path $EvidenceRoot 'metadata.json') $metadata

if ($MaxTotalBudgetUsd -lt ($intakeBudgetUsd + $executionBudgetUsd)) {
    Stop-G03 'INTAKE_FAILED' 34
}

$sandboxSettings = [ordered]@{
    permissions = [ordered]@{
        defaultMode = 'dontAsk'
        deny = @('WebFetch','WebSearch')
    }
    sandbox = [ordered]@{
        enabled = $true
        'failIfUnavailable' = $true
        autoAllowBashIfSandboxed = $true
        excludedCommands = @()
        'allowUnsandboxedCommands' = $false
        filesystem = [ordered]@{
        denyRead = @('/mnt','/home','/root','/tmp',$ProjectRoot,$EvidenceRoot)
        denyWrite = @('/mnt','/home','/root','/tmp',$ProjectRoot,$EvidenceRoot)
            allowRead = @($coldRoot)
            allowWrite = @($coldRoot)
        }
        network = [ordered]@{
            allowedDomains = @()
            'deniedDomains' = @('*')
        }
    }
}
$sandboxSettingsPath = Join-Path $EvidenceRoot 'claude-sandbox-settings.json'
Write-G03JsonNoBom $sandboxSettingsPath $sandboxSettings

if ($TestScenario -ne 'None') {
    Write-G03Progress -Stage 'test_scenario' -Event 'started'
    $resolvedTemp = (Resolve-Path -LiteralPath $env:TEMP).Path.TrimEnd('\','/')
    $resolvedEvidence = (Resolve-Path -LiteralPath $EvidenceRoot).Path
    if (-not $resolvedEvidence.StartsWith($resolvedTemp + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        Stop-G03 'TEST_ONLY_ROOT_INVALID' 49
    }
    if ($TestScenario -eq 'UnhandledError') { throw 'test_only_unhandled_error' }
    if ($TestScenario -eq 'IntakeAmbiguous') { Stop-G03 'TEST_ONLY_INTAKE_AMBIGUOUS' 40 }
    $testIntake = [ordered]@{
        spec_sha256 = $specHash; plan_sha256 = $planHash; files = $initialFiles
        language = $agentDocuments.EffectiveLanguage; task = 'F-01S1'
        acceptance_id = 'F01S1_RED_GREEN_ARTIFACT_SAFETY_V1'; ambiguities = @()
    }
    Write-G03JsonNoBom (Join-Path $EvidenceRoot 'intake-receipt.json') $testIntake
    if ($TestScenario -eq 'Gateway504') { Stop-G03 'TEST_ONLY_EXECUTION_FAILED' 41 }
    if ($TestScenario -eq 'Ready') {
        New-Item -ItemType Directory -Path (Join-Path $coldRoot 'scripts\tests') -Force | Out-Null
        [IO.File]::WriteAllText((Join-Path $coldRoot 'scripts\bootstrap_scan_credentials.ps1'), 'scanner', (New-Object Text.UTF8Encoding($false, $true)))
        [IO.File]::WriteAllText((Join-Path $coldRoot 'scripts\tests\bootstrap_scanner_contract.ps1'), 'contract', (New-Object Text.UTF8Encoding($false, $true)))
    }
    $testArtifacts = Test-G03ColdStartArtifacts -ColdRoot $coldRoot
    if (-not $testArtifacts.Valid) { Stop-G03 'TEST_ONLY_COLD_START_INCOMPLETE' 42 }
    Stop-G03 'TEST_ONLY_READY' 0
}

$platform = if ($env:OS -eq 'Windows_NT') {
    'Windows'
} elseif (-not [string]::IsNullOrWhiteSpace($env:WSL_DISTRO_NAME)) {
    'WSL2'
} elseif ($IsLinux) {
    'Linux'
} elseif ($IsMacOS) {
    'macOS'
} else {
    'Unknown'
}
if (-not (Test-G03SandboxPlatform -Platform $platform)) {
    Write-G03Progress -Stage 'platform' -Event 'unsupported_platform'
    Stop-G03 'EXECUTION_FAILED' 37
}
Write-G03Progress -Stage 'platform' -Event 'supported'
foreach ($requiredCommand in @('pwsh','timeout','bwrap','socat')) {
    if ($null -eq (Get-Command $requiredCommand -ErrorAction SilentlyContinue)) {
        Write-G03Progress -Stage 'preflight' -Event 'missing_command'
        Stop-G03 'EXECUTION_FAILED' 38
    }
}
Write-G03Progress -Stage 'preflight' -Event 'started'
if (-not (Test-G03BwrapPreflight -SandboxRoot $coldRoot)) {
    Write-G03Progress -Stage 'preflight' -Event 'failed'
    Stop-G03 'EXECUTION_FAILED' 55
}
Write-G03Progress -Stage 'preflight' -Event 'passed'

if (-not (Test-Path -LiteralPath $ClaudeCli -PathType Leaf)) {
    Stop-G03 'INTAKE_FAILED' 35
}

$extractorScript = @'
$ErrorActionPreference='Stop';$u=New-Object Text.UTF8Encoding($false,$true);foreach($n in @('SPEC','PLAN')){$p=$n+'.md';$b=[IO.File]::ReadAllBytes($p);if($b.Length-ge3-and$b[0]-eq239-and$b[1]-eq187-and$b[2]-eq191){throw 'UTF8_INVALID'};$t=$u.GetString($b);if($t.Contains([char]0xFFFD)){throw 'UTF8_INVALID'};$a='<!-- AGENT_CAPSULE:'+$n+':BEGIN -->';$z='<!-- AGENT_CAPSULE:'+$n+':END -->';$m=[regex]::Matches($t,'(?s)'+[regex]::Escape($a)+'\s*(.*?)\s*'+[regex]::Escape($z));if($m.Count-ne1){throw 'CAPSULE_INVALID'};'BEGIN_'+$n;$m[0].Groups[1].Value;'END_'+$n};Get-FileHash SPEC.md,PLAN.md -Algorithm SHA256|ForEach-Object{$_.Path|Split-Path -Leaf; $_.Hash};Get-ChildItem -File -Force|Sort-Object Name|ForEach-Object{$_.Name}
'@
$extractorEncoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($extractorScript))
$extractorCommand = "pwsh -NoProfile -EncodedCommand $extractorEncoded"
$strictReadInstruction = "Run exactly this audited command and no alternative file reader: $extractorCommand. It strictly rejects BOM, invalid UTF-8, U+FFFD, missing/multiple capsules, and prints only the two capsules plus hashes and the complete root file list. Do not use the Claude native Read tool."
$intakePrompt = @"
You are the read-only intake session for ProjectB G-03. You have exactly SPEC.md and PLAN.md. $strictReadInstruction
Read the generated capsule in each file, then return one JSON object only with keys spec_sha256, plan_sha256, files, language, task, acceptance_id, ambiguities. Hashes must be uppercase SHA-256, files must be the complete sorted file list, language must be $($agentDocuments.EffectiveLanguage), task must be F-01S1, acceptance_id must be F01S1_RED_GREEN_ARTIFACT_SAFETY_V1, and ambiguities must be an array. Do not edit files, use network, or infer missing requirements.
"@
[IO.File]::WriteAllText((Join-Path $EvidenceRoot 'intake-prompt.txt'), $intakePrompt, (New-Object Text.UTF8Encoding($false, $true)))

Write-G03Progress -Stage 'credential' -Event 'waiting_hidden_input'
$secureKey = Read-Host 'Paste a new temporary Claude API key (hidden input)' -AsSecureString
$keyPointer = [IntPtr]::Zero
$plainKey = $null
try {
    $keyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
    $plainKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyPointer)
    if ([string]::IsNullOrWhiteSpace($plainKey)) { Stop-G03 'INTAKE_FAILED' 36 }
    Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
    $env:ANTHROPIC_AUTH_TOKEN = $plainKey
    $env:ANTHROPIC_BASE_URL = $BaseUrl
    $env:ANTHROPIC_MODEL = $Model
    $env:CLAUDE_CODE_SUBPROCESS_ENV_SCRUB = '1'
    $env:CLAUDE_CODE_MAX_RETRIES = '0'
    $env:API_TIMEOUT_MS = '120000'

    $intakeArgs = @(
        '--print', '--output-format', 'json', '--no-session-persistence', '--bare', '--safe-mode',
        '--setting-sources', 'project', '--settings', $sandboxSettingsPath, '--no-chrome', '--strict-mcp-config',
        '--session-id', ([guid]::NewGuid().ToString()), '--name', 'ProjectB-G03-Intake',
        '--model', $Model, '--permission-mode', 'dontAsk',
        '--tools', 'Bash', '--allowedTools', ("Bash(" + $extractorCommand + ")"),
        '--max-budget-usd', $intakeBudgetUsd.ToString([Globalization.CultureInfo]::InvariantCulture),
        $intakePrompt
    )
    $intakeRun = Invoke-G03Claude -Arguments $intakeArgs -WallSeconds $intakeWallSeconds -SecretValue $plainKey -Stage 'intake'
    if ($intakeRun.TimedOut -or $intakeRun.ExitCode -ne 0 -or $intakeRun.Stdout -match '504 Gateway Time-out') {
        Write-G03ProcessDiagnostic -Run $intakeRun -Stage 'intake'
        Stop-G03 'INTAKE_FAILED' 43
    }
    try { $intakeEnvelope = $intakeRun.Stdout | ConvertFrom-Json } catch {
        Write-G03ProcessDiagnostic -Run $intakeRun -Stage 'intake'
        Stop-G03 'INTAKE_FAILED' 44
    }
    if ((Test-G03IntakeEnvelope -Envelope $intakeEnvelope -MaxCostUsd $intakeBudgetUsd) -ne 'ok') {
        Stop-G03 'INTAKE_FAILED' 52
    }
    $intakeReceipt = Get-G03ResultObject $intakeRun.Stdout
    if ($null -eq $intakeReceipt) {
        Write-G03ProcessDiagnostic -Run $intakeRun -Stage 'intake'
        Stop-G03 'INTAKE_FAILED' 44
    }
    $afterIntakeFiles = @(Get-ChildItem -LiteralPath $coldRoot -File -Recurse -Force | ForEach-Object { $_.FullName.Substring($coldRoot.Length).TrimStart('\','/').Replace('\','/') } | Sort-Object)
    $afterIntakeDirectories = @(Get-ChildItem -LiteralPath $coldRoot -Directory -Recurse -Force)
    if ((Get-FileHash -LiteralPath (Join-Path $coldRoot 'SPEC.md') -Algorithm SHA256).Hash -cne $specHash -or
        (Get-FileHash -LiteralPath (Join-Path $coldRoot 'PLAN.md') -Algorithm SHA256).Hash -cne $planHash -or
        $afterIntakeDirectories.Count -ne 0 -or
        $afterIntakeFiles.Count -ne 2 -or $afterIntakeFiles[0] -cne 'PLAN.md' -or $afterIntakeFiles[1] -cne 'SPEC.md') {
        Stop-G03 'INTAKE_FAILED' 50
    }
    $expected = [ordered]@{ spec_sha256 = $specHash; plan_sha256 = $planHash; files = $initialFiles; language = $agentDocuments.EffectiveLanguage; task = 'F-01S1'; acceptance_id = 'F01S1_RED_GREEN_ARTIFACT_SAFETY_V1' }
    $intakeState = Test-G03IntakeReceipt -Receipt $intakeReceipt -Expected $expected
    if ($intakeState -eq 'INTAKE_AMBIGUOUS') { Stop-G03 'INTAKE_AMBIGUOUS' 45 }
    if ($intakeState -ne 'INTAKE_READY') { Stop-G03 'INTAKE_FAILED' 46 }
    $safeIntakeReceipt = [ordered]@{
        spec_sha256 = $intakeReceipt.spec_sha256
        plan_sha256 = $intakeReceipt.plan_sha256
        files = @($intakeReceipt.files)
        language = $intakeReceipt.language
        task = $intakeReceipt.task
        acceptance_id = $intakeReceipt.acceptance_id
        ambiguities = @()
        cost_usd = [decimal]$intakeEnvelope.total_cost_usd
    }
    Write-G03JsonNoBom (Join-Path $EvidenceRoot 'intake-receipt.json') $safeIntakeReceipt
    Write-G03Progress -Stage 'intake' -Event 'validated'

    $executionPrompt = @"
You are the separate execution session for ProjectB G-03. You have exactly SPEC.md and PLAN.md. $strictReadInstruction
Execute only complete task F-01S1. Create exactly scripts/tests/bootstrap_scanner_contract.ps1 and scripts/bootstrap_scan_credentials.ps1. First run the exact unchanged contract command while the scanner is missing and preserve exit 1 with CONTRACT_RED scanner_missing. Then implement only the three named helpers and minimal single-path wiring, rerun the unchanged command, and require usage_and_output, token_rules, artifact_direct_safety, and BOOTSTRAP_SCANNER_CORE_PASS. Positive fixtures are assembled from non-matching fragments. Do not modify SPEC.md or PLAN.md, use network, commit, or create any other file. Stop and report an ambiguity instead of guessing.
    Finish with one JSON object only: task F-01S1, acceptance_id F01S1_RED_GREEN_ARTIFACT_SAFETY_V1, ambiguities array, questions array, and red_command plus green_command both exactly pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1.
"@
    [IO.File]::WriteAllText((Join-Path $EvidenceRoot 'execution-prompt.txt'), $executionPrompt, (New-Object Text.UTF8Encoding($false, $true)))
    $executionArgs = @(
        '--print', '--output-format', 'stream-json', '--verbose', '--no-session-persistence', '--bare', '--safe-mode',
        '--setting-sources', 'project', '--settings', $sandboxSettingsPath, '--no-chrome', '--strict-mcp-config',
        '--session-id', ([guid]::NewGuid().ToString()), '--name', 'ProjectB-G03-Execution',
        '--model', $Model, '--permission-mode', 'dontAsk',
        '--tools', 'Bash', '--allowedTools', 'Bash',
        '--max-budget-usd', $executionBudgetUsd.ToString([Globalization.CultureInfo]::InvariantCulture),
        $executionPrompt
    )
    $executionRun = Invoke-G03Claude -Arguments $executionArgs -WallSeconds $executionWallSeconds -SecretValue $plainKey -Stage 'execution'
    if ($executionRun.TimedOut -or $executionRun.ExitCode -ne 0) {
        Write-G03ProcessDiagnostic -Run $executionRun -Stage 'execution'
        Stop-G03 'EXECUTION_FAILED' 47
    }
    $executionEvidence = Get-G03ExecutionEvidence -StreamText $executionRun.Stdout -MaxCostUsd $executionBudgetUsd
    if (-not $executionEvidence.Valid) { Stop-G03 'EXECUTION_FAILED' 53 }

    $artifacts = Test-G03ColdStartArtifacts -ColdRoot $coldRoot
    if (-not $artifacts.Valid) { Stop-G03 'COLD_START_INCOMPLETE' 48 }
    $safeQuestions = @($executionEvidence.Questions | ForEach-Object { Protect-G03EvidenceText -Value ([string]$_) -SecretValue $plainKey })
    Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_MODEL -ErrorAction SilentlyContinue
    $candidateInvoker = {
        param([string]$WorkingDirectory,[string[]]$CommandArguments,[int]$WallSeconds)
        Invoke-G03BwrapCommand -WorkingDirectory $WorkingDirectory -CommandArguments $CommandArguments -WallSeconds $WallSeconds
    }
    Write-G03Progress -Stage 'replay' -Event 'started'
    $candidate = Test-G03CandidateEvidence -ColdRoot $coldRoot -EvidenceRoot $EvidenceRoot -ExpectedSpecSha256 $specHash -ExpectedPlanSha256 $planHash -CommandInvoker $candidateInvoker
    if (-not $candidate.Valid) { Stop-G03 'COLD_START_INCOMPLETE' 51 }
    Write-G03Progress -Stage 'replay' -Event 'passed'
    Write-G03JsonNoBom (Join-Path $EvidenceRoot 'execution-summary.json') ([ordered]@{
        task = 'F-01S1'
        acceptance_id = 'F01S1_RED_GREEN_ARTIFACT_SAFETY_V1'
        ambiguities = @()
        questions = $safeQuestions
        bash_calls = $executionEvidence.BashCalls
        edit_calls = $executionEvidence.EditCalls
        cost_usd = $executionEvidence.CostUsd
        tdd_receipt = $executionEvidence.TddReceipt
        candidate_replay = 'ok'
    })
    $finalState = Resolve-G03State -CapsuleValid:$true -Utf8Valid:$true -IntakeState INTAKE_READY -ExecutionExit 0 -ExecutionSignal ok -ArtifactsValid:$candidate.Valid
    if ($finalState -ne 'G03_EVIDENCE_READY') { Stop-G03 $finalState 54 }
    Stop-G03 $finalState 0
} finally {
    Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:CLAUDE_CODE_SUBPROCESS_ENV_SCRUB -ErrorAction SilentlyContinue
    Remove-Item Env:CLAUDE_CODE_MAX_RETRIES -ErrorAction SilentlyContinue
    Remove-Item Env:API_TIMEOUT_MS -ErrorAction SilentlyContinue
    $plainKey = $null
    if ($keyPointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyPointer) }
    if ($null -ne $secureKey) { $secureKey.Dispose() }
}
