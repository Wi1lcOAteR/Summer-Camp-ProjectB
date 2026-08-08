param([Parameter(Mandatory = $true)][string]$Root)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath $Root).Path
$fixture = Join-Path $repoRoot ("tmp/cleanup-contract-" + [guid]::NewGuid().ToString('N'))

function Assert-Equal($Actual, $Expected, [string]$Message) {
    if ($Actual -ne $Expected) { throw "$Message expected=$Expected actual=$Actual" }
}

try {
    New-Item -ItemType Directory -Force -Path $fixture | Out-Null
    & git -C $fixture init -q
    Set-Content -LiteralPath (Join-Path $fixture '.gitignore') -Value ".mypy_cache/`n.pytest_cache/`n.ruff_cache/`ntmp/`ninventory.json`ndecisions.json" -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $fixture 'tracked-reference.md') -Value 'no cleanup reference' -Encoding utf8NoBOM
    & git -C $fixture add .gitignore
    & git -C $fixture add tracked-reference.md
    if ($LASTEXITCODE -ne 0) { throw 'fixture git add failed' }
    New-Item -ItemType Directory -Force -Path @(
        (Join-Path $fixture '.mypy_cache'),
        (Join-Path $fixture '.pytest_cache'),
        (Join-Path $fixture '.ruff_cache'),
        (Join-Path $fixture 'junction-target'),
        (Join-Path $fixture 'tmp/run-123'),
        (Join-Path $fixture 'tmp/not-approved'),
        (Join-Path $fixture 'tmp/stage-b-archive-20260725'),
        (Join-Path $fixture 'tmp/toolchains'),
        (Join-Path $fixture '.worktrees/active')
    ) | Out-Null
    Set-Content -LiteralPath (Join-Path $fixture '.pytest_cache/cache.txt') -Value 'synthetic cache' -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $fixture '.ruff_cache/cache.txt') -Value ('gho_' + ('A' * 30)) -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $fixture 'tmp/run-123/result.txt') -Value 'synthetic result' -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $fixture 'tracked-reference.md') -Value 'active reference: .ruff_cache' -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $fixture 'untracked-reference.md') -Value 'active reference: .mypy_cache' -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $fixture 'junction-target/sentinel.txt') -Value 'retain me' -Encoding utf8NoBOM
    New-Item -ItemType Junction -Path (Join-Path $fixture '.pytest_cache/nested-link') -Target (Join-Path $fixture 'junction-target') | Out-Null

    $records = @(
        @{ path = '.'; kind = 'coordination_root' },
        @{ path = '.git'; kind = 'excluded_tree' },
        @{ path = '.mypy_cache'; kind = 'excluded_tree' },
        @{ path = '.pytest_cache'; kind = 'excluded_tree' },
        @{ path = '.ruff_cache'; kind = 'excluded_tree' },
        @{ path = 'tmp/run-123'; kind = 'directory_candidate' },
        @{ path = 'tmp/not-approved'; kind = 'directory_candidate' },
        @{ path = 'tmp/stage-b-archive-20260725'; kind = 'directory_candidate' },
        @{ path = 'tmp/toolchains'; kind = 'symlink' },
        @{ path = '.worktrees/active'; kind = 'worktree' },
        @{ path = 'tmp/duplicate'; kind = 'directory_candidate'; duplicate_group = 'sha256:test'; duplicate_proof = @{ owner = 'unknown'; reference_scan = 'unknown'; basis = 'unproven' } }
    )
    $inventory = @{ schema_version = 1; checkout_root = '.'; records = $records }
    $inventoryPath = Join-Path $fixture 'inventory.json'
    $outputPath = Join-Path $fixture 'decisions.json'
    $inventory | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $inventoryPath -Encoding utf8NoBOM

    & (Join-Path $repoRoot 'scripts/audit_cleanup_paths.ps1') -Root $fixture -Inventory $inventoryPath -Output $outputPath -DisposableTmpRun @('run-123')
    if ($LASTEXITCODE -ne 0) { throw "cleanup audit failed exit=$LASTEXITCODE" }
    $decisions = (Get-Content -Raw -LiteralPath $outputPath | ConvertFrom-Json).decisions
    $byPath = @{}
    foreach ($decision in $decisions) { $byPath[$decision.path] = $decision }

    Assert-Equal $byPath['.pytest_cache'].decision 'retain' 'nested junction cache'
    Assert-Equal $byPath['.pytest_cache'].reason 'symlink_or_reparse_point' 'nested junction reason'
    Assert-Equal $byPath['.mypy_cache'].decision 'retain' 'untracked reference cache'
    Assert-Equal $byPath['.mypy_cache'].checks.reference_scan 'fail' 'untracked reference check'
    Assert-Equal $byPath['.ruff_cache'].decision 'retain' 'unstaged tracked reference cache'
    Assert-Equal $byPath['.ruff_cache'].checks.reference_scan 'fail' 'unstaged tracked reference check'
    Assert-Equal $byPath['.ruff_cache'].checks.credential_scan 'fail' 'canonical credential scanner check'
    Assert-Equal $byPath['tmp/run-123'].decision 'retain' "named tmp decision reason=$($byPath['tmp/run-123'].reason) checks=$($byPath['tmp/run-123'].checks | ConvertTo-Json -Compress)"
    foreach ($retained in @('.', '.git', 'tmp/not-approved', 'tmp/stage-b-archive-20260725', 'tmp/toolchains', '.worktrees/active', 'tmp/duplicate')) {
        Assert-Equal $byPath[$retained].decision 'retain' "retain $retained"
    }
    foreach ($check in @('containment', 'reference_scan', 'credential_scan', 'ownership')) {
        Assert-Equal $byPath['tmp/run-123'].checks.$check 'pass' "tmp check $check"
    }
    Assert-Equal $byPath['tmp/run-123'].checks.process_use 'unknown' 'process use fails closed'
    if (-not (Test-Path -LiteralPath (Join-Path $fixture 'junction-target/sentinel.txt'))) { throw 'audit followed nested junction' }
    if (-not (Test-Path -LiteralPath (Join-Path $fixture 'tmp/run-123/result.txt'))) { throw 'audit deleted tmp content' }

    New-Item -ItemType Junction -Path (Join-Path $fixture 'untracked-link') -Target (Join-Path $fixture 'junction-target') | Out-Null
    & (Join-Path $repoRoot 'scripts/audit_cleanup_paths.ps1') -Root $fixture -Inventory $inventoryPath -Output $outputPath -DisposableTmpRun @('run-123')
    if ($LASTEXITCODE -ne 0) { throw "symlink audit failed exit=$LASTEXITCODE" }
    $symlinkDecisions = (Get-Content -Raw -LiteralPath $outputPath | ConvertFrom-Json).decisions
    $symlinkByPath = @{}
    foreach ($decision in $symlinkDecisions) { $symlinkByPath[$decision.path] = $decision }
    Assert-Equal $symlinkByPath['tmp/run-123'].checks.reference_scan 'unknown' 'untracked symlink fail closed'
    Write-Output 'CLEANUP_PATH_CONTRACT_PASS'
}
finally {
    if (Test-Path -LiteralPath $fixture) { Remove-Item -LiteralPath $fixture -Recurse -Force }
}
