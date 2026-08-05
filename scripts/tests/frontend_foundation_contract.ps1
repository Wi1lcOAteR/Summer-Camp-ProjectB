Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$targets = @(
    'frontend/tsconfig.json',
    'frontend/vite.config.ts',
    'frontend/src/foundation/RuntimeProbe.tsx',
    'frontend/src/foundation/RuntimeProbe.test.tsx'
)
function Fail([string]$Code) { Write-Output "CONTRACT_RED $Code"; exit 1 }
foreach ($relative in $targets) {
    if (-not (Test-Path -LiteralPath (Join-Path $repo ($relative -replace '/', '\')) -PathType Leaf)) {
        Fail "missing_$($relative -replace '/', '_')"
    }
}

$tsconfig = [IO.File]::ReadAllText((Join-Path $repo 'frontend/tsconfig.json'), [Text.UTF8Encoding]::new($false, $true))
if ($tsconfig -notmatch '"strict"\s*:\s*true' -or $tsconfig -notmatch '"noUncheckedIndexedAccess"\s*:\s*true' -or $tsconfig -notmatch '"jsx"\s*:\s*"react-jsx"') { Fail 'typescript_strict_config' }

$vite = [IO.File]::ReadAllText((Join-Path $repo 'frontend/vite.config.ts'), [Text.UTF8Encoding]::new($false, $true))
if ($vite -notmatch 'react\(\)' -or $vite -notmatch 'port\s*:\s*5173' -or $vite -notmatch 'strictPort\s*:\s*true' -or $vite -notmatch 'preview[\s\S]*port\s*:\s*4173' -or $vite -match '0\.0\.0\.0|--host') { Fail 'vite_loopback_config' }
if ($vite -notmatch 'environment\s*:\s*[''\"]jsdom[''\"]' -or $vite -notmatch 'src/\*\*/\*\.test\.\{ts,tsx\}' -or $vite -match 'passWithNoTests\s*:\s*true') { Fail 'vitest_config' }

$component = [IO.File]::ReadAllText((Join-Path $repo 'frontend/src/foundation/RuntimeProbe.tsx'), [Text.UTF8Encoding]::new($false, $true))
if ($component -notmatch 'button' -or $component -notmatch 'aria-label|role' -or $component -notmatch 'useState' -or $component -notmatch 'onClick') { Fail 'accessible_interaction_missing' }

$test = [IO.File]::ReadAllText((Join-Path $repo 'frontend/src/foundation/RuntimeProbe.test.tsx'), [Text.UTF8Encoding]::new($false, $true))
if ($test -notmatch 'render' -or $test -notmatch 'userEvent' -or $test -notmatch 'getByRole' -or $test -notmatch 'textContent' -or $test -notmatch 'click') { Fail 'interaction_test_missing' }

$npm = Get-ChildItem -LiteralPath (Join-Path $repo 'tmp/toolchains/f01a/runtimes') -Filter npm.cmd -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1
if ($null -eq $npm) { $npm = Get-Command npm.cmd, npm -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1 }
if ($null -eq $npm) { Fail 'npm_runtime_missing' }
$npmPath = if ($npm.PSObject.Properties.Name -contains 'FullName') { $npm.FullName } else { $npm.Source }
$oldPreference = $ErrorActionPreference
Push-Location (Join-Path $repo 'frontend')
try {
    $ErrorActionPreference = 'Continue'
    $emptyOutput = @(& $npmPath exec -- vitest run src/foundation/does-not-exist.test.tsx 2>&1)
    $emptyExit = $LASTEXITCODE
    $testOutput = @(& $npmPath exec -- vitest run src/foundation/RuntimeProbe.test.tsx 2>&1)
    $testExit = $LASTEXITCODE
    if ($emptyExit -eq 0) { Fail 'empty_suite_accepted' }
    if ($testExit -ne 0) { Fail 'interaction_runtime_failed' }
}
finally { $ErrorActionPreference = $oldPreference; Pop-Location }

Write-Output 'frontend_config'
Write-Output 'accessible_interaction'
Write-Output 'FRONTEND_FOUNDATION_CONTRACT_PASS'
