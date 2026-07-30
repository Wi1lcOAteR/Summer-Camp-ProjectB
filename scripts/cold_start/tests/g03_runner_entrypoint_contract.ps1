$ErrorActionPreference = 'Stop'

$coldStartRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $coldStartRoot 'run_g03_claude.ps1'
if (-not (Test-Path -LiteralPath $runner -PathType Leaf)) {
    Write-Output 'G03_RUNNER_ENTRYPOINT_RED runner_missing'
    exit 1
}

$tokens = $null
$errors = $null
$ast = [Management.Automation.Language.Parser]::ParseFile($runner, [ref]$tokens, [ref]$errors)
if ($errors.Count -ne 0) { throw "Runner has PowerShell parse errors: $($errors[0].Message)" }
$parameters = @($ast.ParamBlock.Parameters | ForEach-Object { $_.Name.VariablePath.UserPath })
foreach ($name in @('AgentLanguage','Model','MaxTotalBudgetUsd','ExpectedSpecSha256','ExpectedPlanSha256')) {
    if ($parameters -notcontains $name) { throw "Runner parameter missing: $name" }
}

$text = [IO.File]::ReadAllText($runner)
$coreText = [IO.File]::ReadAllText((Join-Path $coldStartRoot 'g03_runner_core.ps1'))
$contractText = $text + "`n" + $coreText
foreach ($literal in @(
    "[decimal]0.20",
    "[decimal]0.80",
    "CLAUDE_CODE_MAX_RETRIES = '0'",
    '''failIfUnavailable'' = $true',
    '''allowUnsandboxedCommands'' = $false',
    "'deniedDomains' = @('*')",
    "denyRead = @('/mnt','/home','/root','/tmp'",
    "denyWrite = @('/mnt','/home','/root','/tmp'",
    "'--tools', 'Bash'",
    "'--tools', 'Bash'",
    "'--allowedTools', 'Bash'",
    "Remove-Item Env:ANTHROPIC_AUTH_TOKEN",
    "Test-G03BwrapPreflight",
    "descendant-marker.txt",
    "status.log",
    "G03_EVIDENCE_ROOT",
    "`$heartbeatSeconds = 15",
    "'heartbeat'",
    "'unsupported_platform'",
    "tdd_receipt = `$executionEvidence.TddReceipt",
    "'CAPSULE_INVALID'",
    "'UTF8_INVALID'",
    "'INTAKE_FAILED'",
    "'INTAKE_AMBIGUOUS'",
    "'EXECUTION_FAILED'",
    "'COLD_START_INCOMPLETE'",
    "'G03_EVIDENCE_READY'"
)) {
    if (-not $contractText.Contains($literal)) { throw "Runner contract literal missing: $literal" }
}
if ($text -match "'--tools',\s*'[^']*Read" -or $text -match "'--allowedTools',\s*'[^']*Read") {
    throw 'Runner must not grant the Claude native Read tool.'
}
if ($text -match "'--tools',\s*'[^']*Edit" -or $text -match "'--allowedTools',\s*'[^']*Edit") {
    throw 'Runner must not grant native Edit because Claude filesystem sandboxing does not govern that tool.'
}

$ErrorActionPreference = 'Continue'
$invalidLanguage = @(& powershell -NoProfile -ExecutionPolicy Bypass -File $runner -AgentLanguage Klingon -ExpectedSpecSha256 ('A' * 64) -ExpectedPlanSha256 ('B' * 64) 2>&1)
$invalidLanguageExit = $LASTEXITCODE
$ErrorActionPreference = 'Stop'
if ($invalidLanguageExit -eq 0) {
    throw 'An invalid agent language must fail parameter validation before runner execution.'
}

$specHash = (Get-FileHash -LiteralPath (Join-Path (Split-Path -Parent (Split-Path -Parent $coldStartRoot)) 'SPEC.md') -Algorithm SHA256).Hash
$planHash = (Get-FileHash -LiteralPath (Join-Path (Split-Path -Parent (Split-Path -Parent $coldStartRoot)) 'PLAN.md') -Algorithm SHA256).Hash
$root = Join-Path $env:TEMP ('projectb-g03-entrypoint-' + [guid]::NewGuid().ToString())
try {
    New-Item -ItemType Directory -Path $root -Force | Out-Null
    $cases = [ordered]@{
        IntakeAmbiguous = 'TEST_ONLY_INTAKE_AMBIGUOUS'
        Gateway504 = 'TEST_ONLY_EXECUTION_FAILED'
        MissingArtifacts = 'TEST_ONLY_COLD_START_INCOMPLETE'
        UnhandledError = 'UNHANDLED_ERROR'
        Ready = 'TEST_ONLY_READY'
    }
    foreach ($scenario in $cases.Keys) {
        $evidence = Join-Path $root $scenario
        $ErrorActionPreference = 'Continue'
        $output = @(& powershell -NoProfile -ExecutionPolicy Bypass -File $runner -AgentLanguage Auto -Model claude-sonnet-4-6 -MaxTotalBudgetUsd 1.00 -ExpectedSpecSha256 $specHash -ExpectedPlanSha256 $planHash -EvidenceRoot $evidence -TestScenario $scenario 2>&1)
        $scenarioExit = $LASTEXITCODE
        $ErrorActionPreference = 'Stop'
        if ($scenarioExit -eq 0 -and $scenario -ne 'Ready') { throw "$scenario unexpectedly exited 0." }
        if ($scenarioExit -ne 0 -and $scenario -eq 'Ready') { throw "Ready failed: $($output -join ' ')" }
        $completion = Get-Content -Raw -LiteralPath (Join-Path $evidence 'completion.json') -Encoding UTF8 | ConvertFrom-Json
        if ($completion.status -cne $cases[$scenario]) {
            throw "$scenario expected $($cases[$scenario]) got $($completion.status)"
        }
        if ($completion.schema -cne 'projectb.g03.test.v1' -or $completion.formal -ne $false) {
            throw "$scenario test receipt is not unambiguously non-formal."
        }
        if ($completion.status_log -cne 'status.log') {
            throw "$scenario completion receipt must identify status.log."
        }
        $statusPath = Join-Path $evidence 'status.log'
        if (-not (Test-Path -LiteralPath $statusPath -PathType Leaf)) {
            throw "$scenario did not create status.log."
        }
        $statusBytes = [IO.File]::ReadAllBytes($statusPath)
        if ($statusBytes.Length -ge 3 -and $statusBytes[0] -eq 0xEF -and $statusBytes[1] -eq 0xBB -and $statusBytes[2] -eq 0xBF) {
            throw "$scenario status.log must be UTF-8 without BOM."
        }
        $statusText = (New-Object Text.UTF8Encoding($false, $true)).GetString($statusBytes)
        if ($statusText.Contains([char]0xFFFD)) { throw "$scenario status.log contains U+FFFD." }
        foreach ($forbiddenText in @($specHash,$planHash,'Agent spec capsule','test_only_unhandled_error')) {
            if ($statusText.Contains($forbiddenText)) {
                throw "$scenario status.log contains non-progress input or error text."
            }
        }
        $records = @($statusText -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | ForEach-Object { $_ | ConvertFrom-Json })
        if ($records.Count -lt 3) { throw "$scenario status.log must contain observable stage transitions." }
        $allowedKeys = @('timestamp','stage','event','elapsed_seconds')
        foreach ($record in $records) {
            $keys = @($record.PSObject.Properties.Name)
            if (@($keys | Where-Object { $allowedKeys -notcontains $_ }).Count -ne 0 -or
                $keys -notcontains 'timestamp' -or $keys -notcontains 'stage' -or $keys -notcontains 'event') {
                throw "$scenario status.log contains a non-allowlisted or missing field."
            }
            if ($keys -contains 'elapsed_seconds' -and ([int]$record.elapsed_seconds -lt 0)) {
                throw "$scenario status.log contains a negative elapsed time."
            }
        }
        if ($records[0].stage -cne 'runner' -or $records[0].event -cne 'started' -or
            $records[-1].stage -cne 'runner' -or $records[-1].event -cne 'finished') {
            throw "$scenario status.log must start and finish with runner lifecycle events."
        }
    }
    'G03_RUNNER_ENTRYPOINT_PASS cases=5'
} finally {
    if (Test-Path -LiteralPath $root) { Remove-Item -LiteralPath $root -Recurse -Force }
}
