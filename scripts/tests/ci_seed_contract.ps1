Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$gitlabPath = Join-Path $repo '.gitlab-ci.yml'
$githubPath = Join-Path $repo '.github/workflows/ci.yml'
function Fail([string]$Code) { Write-Output "CONTRACT_RED $Code"; exit 1 }
function Require-Literal([string]$Text, [string]$Needle, [string]$Code) {
    if (-not $Text.Contains($Needle)) { Fail $Code }
}

if (-not (Test-Path -LiteralPath $gitlabPath -PathType Leaf)) { Fail 'gitlab_missing' }
if (-not (Test-Path -LiteralPath $githubPath -PathType Leaf)) { Fail 'github_missing' }
$gitlab = [IO.File]::ReadAllText($gitlabPath, [Text.UTF8Encoding]::new($false, $true))
$github = [IO.File]::ReadAllText($githubPath, [Text.UTF8Encoding]::new($false, $true))

$pwshImage = 'mcr.microsoft.com/powershell:7.5-ubuntu-24.04@sha256:042240d57ec9e47e511033b92625a8d95875ee5860af3015992c248b58a8be81'
$pythonImage = 'python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb'
$nodeImage = 'node:24.18.0-bookworm-slim@sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6'
$checkout = 'actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683'

Require-Literal $gitlab 'unit-test:' 'gitlab_unit_test'
foreach ($needle in @('workflow:', '$CI_PIPELINE_SOURCE == "push"', '- when: never', $pwshImage, $pythonImage, $nodeImage, 'apt-get install -y --no-install-recommends git ca-certificates', 'pwsh --version', 'git --version', 'scripts/tests/bootstrap_scanner_contract.ps1', 'scripts/tests/ci_seed_contract.ps1', 'scripts/bootstrap_scan_credentials.ps1 -Tracked', 'runner_absent_pre_feature', 'backend/projectb', 'npm ci --ignore-scripts', 'tsc --noEmit')) { Require-Literal $gitlab $needle 'gitlab_commands' }
if ($gitlab -notmatch '(?m)^\s*- npm exec -- vitest run\s*$') { Fail 'gitlab_frontend_all_tests' }
if (([regex]::Matches($gitlab, '(?m)^\s*rules\s*:')).Count -ne 1 -or $gitlab -match '(?m)^\s*(only|except|allow_failure|changes)\s*:|rules\s*:\s*[\s\S]{0,120}exists|when\s*:\s*(manual|delayed)|\|\|\s*true|passWithNoTests') { Fail 'gitlab_bypass' }

foreach ($needle in @('push:', 'permissions:', 'contents: read', 'scanner:', 'backend:', 'frontend:', $checkout, $pwshImage, $pythonImage, $nodeImage, 'apt-get install -y --no-install-recommends git ca-certificates', 'scripts/tests/bootstrap_scanner_contract.ps1', 'scripts/tests/ci_seed_contract.ps1', 'scripts/bootstrap_scan_credentials.ps1 -Tracked', 'runner_absent_pre_feature', 'backend/projectb', 'npm ci --ignore-scripts', 'tsc --noEmit')) { Require-Literal $github $needle 'github_commands' }
if ($github -notmatch '(?m)^\s*run:\s*npm exec -- vitest run\s*$') { Fail 'github_frontend_all_tests' }
if (([regex]::Matches($github, '(?m)^permissions:\s*$')).Count -ne 1 -or $github -notmatch '(?ms)^permissions:\r?\n  contents: read\r?\n\r?\njobs:') { Fail 'github_permissions' }
$checkoutRefs = @([regex]::Matches($github, 'actions/checkout@(?<ref>[^\s]+)'))
if ($checkoutRefs.Count -ne 3 -or @($checkoutRefs | Where-Object { $_.Groups['ref'].Value -cne $checkout.Substring('actions/checkout@'.Length) }).Count -ne 0) { Fail 'github_checkout_refs' }
if ($github -notmatch '(?m)^\s*runs-on:\s*ubuntu-24\.04\s*$' -or $github -match 'actions/checkout@v|permissions:\s*write|continue-on-error:\s*true|paths(?:-ignore)?\s*:|branches(?:-ignore)?\s*:|if\s*:\s*false|\|\|\s*true|passWithNoTests') { Fail 'github_policy' }

Write-Output 'push_and_pinned_images'
Write-Output 'current_suite_and_empty_failure'
Write-Output 'CI_SEED_CONTRACT_PASS'
