Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:Failures = [Collections.Generic.List[string]]::new()

function Add-Failure {
    param([string]$Category, [string]$Detail)
    [void]$script:Failures.Add("$Category $Detail")
}

function Get-CanonicalLfHash {
    param([string]$Path)

    try {
        $text = [IO.File]::ReadAllText($Path, [Text.UTF8Encoding]::new($false, $true))
        $text = $text.Replace("`r`n", "`n").Replace("`r", "`n")
        $bytes = [Text.UTF8Encoding]::new($false).GetBytes($text)
        $sha = [Security.Cryptography.SHA256]::Create()
        try {
            return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
        }
        finally {
            $sha.Dispose()
        }
    }
    catch {
        Add-Failure 'hash' ([IO.Path]::GetFileName($Path))
        return ''
    }
}

function Test-RawParity {
    param([string]$Actual, [string]$Authority, [string]$Label)

    if (-not (Test-Path -LiteralPath $Actual -PathType Leaf)) {
        Add-Failure 'raw_lock_parity' "$Label missing"
        return
    }
    $left = [IO.File]::ReadAllBytes($Actual)
    $right = [IO.File]::ReadAllBytes($Authority)
    if ($left.Length -ne $right.Length -or -not [Collections.StructuralComparisons]::StructuralEqualityComparer.Equals($left, $right)) {
        Add-Failure 'raw_lock_parity' "$Label differs"
    }
}

function Get-EnvironmentSnapshot {
    $userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    $machinePath = [Environment]::GetEnvironmentVariable('PATH', 'Machine')
    $userRegistry = if (Test-Path -LiteralPath 'HKCU:\Environment') {
        (Get-ItemProperty -LiteralPath 'HKCU:\Environment' | Out-String)
    }
    else { '' }
    $machineRegistry = if (Test-Path -LiteralPath 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment') {
        (Get-ItemProperty -LiteralPath 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment' | Out-String)
    }
    else { '' }
    return "$($env:PATH)`0$userPath`0$machinePath`0$userRegistry`0$machineRegistry"
}

function Test-ExactMap {
    param($Actual, [hashtable]$Expected, [string]$Label)

    $properties = @($Actual.PSObject.Properties)
    if ($properties.Count -ne $Expected.Count) {
        Add-Failure 'manifest' "$Label count"
        return
    }
    foreach ($entry in $Expected.GetEnumerator()) {
        $property = $Actual.PSObject.Properties[$entry.Key]
        if (-not $property -or $property.Value -cne $entry.Value) {
            Add-Failure 'manifest' "$Label $($entry.Key)"
        }
    }
}

$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
Push-Location $repo
try {
    $artifacts = @(
        '.python-version',
        'pyproject.toml',
        'backend/requirements-windows-x64.lock',
        'requirements.linux-ci.lock',
        'packaging/oci/requirements.linux-demo.lock',
        'frontend/package.json',
        'frontend/package-lock.json',
        'frontend/.npmrc',
        'scripts/bootstrap.ps1'
    )
    foreach ($artifact in $artifacts) {
        if (-not (Test-Path -LiteralPath $artifact -PathType Leaf)) {
            Add-Failure 'missing_artifact' $artifact
        }
    }

    $locks = @(
        @('backend/requirements-windows-x64.lock', 'docs/engineering/locks/python-3.14.6-windows-x64.lock', '246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6', 'windows'),
        @('requirements.linux-ci.lock', 'docs/engineering/locks/python-3.14.6-linux-amd64-ci.lock', 'd24ddf3789ea9f276ee6ba4062634fef3c85c4572a7eb62096cbd570bfb0fc35', 'linux-ci'),
        @('packaging/oci/requirements.linux-demo.lock', 'docs/engineering/locks/python-3.14.6-linux-amd64-demo.lock', '09ce57726c02a090f134d4f2c25f2681dce58ebf2d8425502129d42ac2be34f7', 'linux-demo'),
        @('frontend/package-lock.json', 'docs/engineering/locks/frontend-package-lock.json', '071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f', 'npm')
    )
    foreach ($lock in $locks) {
        $authorityHash = Get-CanonicalLfHash (Join-Path $repo $lock[1])
        if ($authorityHash -cne $lock[2]) { Add-Failure 'hash' "$($lock[3]) authority" }
        if (Test-Path -LiteralPath $lock[0] -PathType Leaf) {
            $actualHash = Get-CanonicalLfHash (Join-Path $repo $lock[0])
            if ($actualHash -cne $lock[2]) { Add-Failure 'hash' "$($lock[3]) production" }
        }
        else {
            Add-Failure 'hash' "$($lock[3]) production missing"
        }
        Test-RawParity (Join-Path $repo $lock[0]) (Join-Path $repo $lock[1]) $lock[3]
    }

    if (Test-Path -LiteralPath '.python-version') {
        $pythonVersion = [IO.File]::ReadAllText((Join-Path $repo '.python-version'), [Text.UTF8Encoding]::new($false, $true)).Trim()
        if ($pythonVersion -cne '3.14.6') { Add-Failure 'version_drift' '.python-version' }
    }
    else { Add-Failure 'version_drift' '.python-version missing' }

    if (Test-Path -LiteralPath 'pyproject.toml') {
        $pyproject = [IO.File]::ReadAllText((Join-Path $repo 'pyproject.toml'), [Text.UTF8Encoding]::new($false, $true))
        $pythonPins = @(
            'fastapi==0.139.2', 'uvicorn==0.51.0', 'pydantic==2.13.4', 'httpx==0.28.1',
            'httpx2==2.7.0', 'openai==2.46.0', 'pypdf==6.14.2', 'pypdfium2==5.12.1',
            'Pillow==12.3.0', 'keyring==25.7.0', 'tzdata==2026.3', 'python-multipart==0.0.32',
            'psutil==7.2.2', 'pytest==9.1.1', 'ruff==0.15.22', 'mypy==2.3.0',
            'types-psutil==7.2.2.20260518', 'pyinstaller==6.21.0'
        )
        if ($pyproject -notmatch 'requires-python\s*=\s*"==3\.14\.\*"') { Add-Failure 'manifest' 'requires-python' }
        foreach ($pin in $pythonPins) {
            if ($pyproject -notmatch [regex]::Escape('"' + $pin + '"')) { Add-Failure 'manifest' "python $pin" }
        }
    }
    else { Add-Failure 'manifest' 'pyproject missing' }

    if (Test-Path -LiteralPath 'frontend/package.json') {
        try {
            $package = Get-Content -Raw -Encoding utf8 frontend/package.json | ConvertFrom-Json
            if ($package.name -cne 'projectb-g02a-npm-985d41ddbb004457b9e80e09f77cef91' -or $package.version -cne '1.0.0' -or -not $package.private) {
                Add-Failure 'manifest' 'npm identity'
            }
            Test-ExactMap $package.dependencies @{
                'react' = '19.2.7'; 'react-dom' = '19.2.7'; 'lucide-react' = '1.25.0'
            } 'dependencies'
            Test-ExactMap $package.devDependencies @{
                'vite' = '8.1.5'; '@vitejs/plugin-react' = '6.0.3'; 'typescript' = '7.0.2';
                'vitest' = '4.1.10'; '@testing-library/dom' = '10.4.1';
                '@testing-library/react' = '16.3.2'; '@testing-library/user-event' = '14.6.1';
                'jsdom' = '29.1.1'; '@playwright/test' = '1.61.1';
                '@axe-core/playwright' = '4.12.1'; '@types/react' = '19.2.17';
                '@types/react-dom' = '19.2.3'; '@types/node' = '24.13.3'
            } 'devDependencies'
        }
        catch { Add-Failure 'manifest' 'package.json invalid' }
    }
    else { Add-Failure 'manifest' 'package.json missing' }

    if (Test-Path -LiteralPath 'frontend/.npmrc') {
        $npmrc = @(Get-Content -Encoding utf8 frontend/.npmrc | Where-Object { $_ })
        if ($npmrc.Count -ne 2 -or 'engine-strict=true' -notin $npmrc -or 'ignore-scripts=true' -notin $npmrc) {
            Add-Failure 'manifest' '.npmrc policy'
        }
    }
    else { Add-Failure 'manifest' '.npmrc missing' }

    $bootstrap = Join-Path $repo 'scripts/bootstrap.ps1'
    if (Test-Path -LiteralPath $bootstrap -PathType Leaf) {
        $source = [IO.File]::ReadAllText($bootstrap, [Text.UTF8Encoding]::new($false, $true))
        if ($source -notmatch 'npm\.cmd' -or $source -notmatch 'npm_ps1_blocked') {
            Add-Failure 'blocked_npm_ps1' 'guard missing'
        }
        if ($source -notmatch 'runtime_root_outside_project') {
            Add-Failure 'system_mutation' 'runtime root guard missing'
        }
        if ($source -match '(?i)SetEnvironmentVariable|\bsetx(?:\.exe)?\b|HKCU:|HKLM:|\$env:PATH\s*=') {
            Add-Failure 'system_mutation' 'forbidden API'
        }

        $sandbox = Join-Path $repo 'tmp/f01a-runtime-contract'
        try {
            if (Test-Path -LiteralPath $sandbox) { Remove-Item -LiteralPath $sandbox -Recurse -Force }
            [void](New-Item -ItemType Directory -Path (Join-Path $sandbox 'corrupt/downloads') -Force)
            [IO.File]::WriteAllBytes((Join-Path $sandbox 'corrupt/downloads/python-3.14.6-embed-amd64.zip'), [byte[]](1, 2, 3, 4))
            $before = Get-EnvironmentSnapshot
            try {
                $null = & $bootstrap -RuntimeRoot (Join-Path $sandbox 'corrupt') -Offline
                Add-Failure 'corrupt_download' 'accepted'
            }
            catch {
                if ($_.Exception.Message -notmatch '^BOOTSTRAP_ERROR artifact_hash_mismatch python$') {
                    Add-Failure 'corrupt_download' 'wrong error'
                }
            }
            $after = Get-EnvironmentSnapshot
            if ($before -cne $after) { Add-Failure 'system_mutation' 'environment changed' }

            $driftRoot = Join-Path $sandbox 'drift'
            $driftPython = Join-Path $driftRoot 'runtimes/python-3.14.6'
            [void](New-Item -ItemType Directory -Path $driftPython -Force)
            $systemPython = (Get-Command python.exe -CommandType Application | Select-Object -First 1).Source
            Copy-Item -LiteralPath $systemPython -Destination (Join-Path $driftPython 'python.exe')
            $pythonDll = Join-Path (Split-Path $systemPython) 'python313.dll'
            if (Test-Path -LiteralPath $pythonDll) { Copy-Item -LiteralPath $pythonDll -Destination $driftPython }
            [IO.File]::WriteAllText((Join-Path $driftPython 'python314._pth'), ".`nimport site`n", [Text.UTF8Encoding]::new($false))
            try {
                $null = & $bootstrap -RuntimeRoot $driftRoot -Offline
                Add-Failure 'version_drift' 'accepted'
            }
            catch {
                if ($_.Exception.Message -notmatch '^BOOTSTRAP_ERROR python_version_mismatch$') {
                    Add-Failure 'version_drift' 'wrong error'
                }
            }
        }
        catch { Add-Failure 'runtime_negative' $_.Exception.GetType().Name }
        finally {
            if (Test-Path -LiteralPath $sandbox) { Remove-Item -LiteralPath $sandbox -Recurse -Force }
        }

        if ($script:Failures.Count -eq 0) {
            try {
                $tools = & $bootstrap
                if (-not [IO.Path]::IsPathRooted($tools.Py) -or [IO.Path]::GetExtension($tools.Py) -cne '.exe') {
                    Add-Failure 'runtime' 'python path'
                }
                if (-not [IO.Path]::IsPathRooted($tools.Npm) -or [IO.Path]::GetFileName($tools.Npm) -cne 'npm.cmd') {
                    Add-Failure 'blocked_npm_ps1' 'npm command'
                }
                $pyVersion = (& $tools.Py --version 2>&1 | Out-String).Trim()
                $nodeVersion = (& $tools.Node --version 2>&1 | Out-String).Trim()
                $npmVersion = (& $tools.Npm --version 2>&1 | Out-String).Trim()
                $uvVersion = (& $tools.Uv --version 2>&1 | Out-String).Trim()
                if ($pyVersion -cne 'Python 3.14.6') { Add-Failure 'version_drift' 'python runtime' }
                if ($nodeVersion -cne 'v24.18.0') { Add-Failure 'version_drift' 'node runtime' }
                if ($npmVersion -cne '11.16.0') { Add-Failure 'version_drift' 'npm runtime' }
                if ($uvVersion -notmatch '^uv 0\.11\.14(?: |$)') { Add-Failure 'version_drift' 'uv runtime' }
                $pathConfig = [IO.File]::ReadAllText((Join-Path (Split-Path $tools.Py) 'python314._pth'), [Text.UTF8Encoding]::new($false, $true))
                if ($pathConfig -notmatch '(?m)^import site\s*$') { Add-Failure 'runtime_import' 'site-packages' }

                $uvBackup = "$($tools.Uv).contract-backup"
                try {
                    Move-Item -LiteralPath $tools.Uv -Destination $uvBackup
                    Copy-Item -LiteralPath $tools.Node -Destination $tools.Uv
                    try {
                        $null = & $bootstrap -RuntimeRoot $tools.RuntimeRoot -Offline
                        Add-Failure 'version_drift' 'uv accepted'
                    }
                    catch {
                        if ($_.Exception.Message -notmatch '^BOOTSTRAP_ERROR uv_version_mismatch$') {
                            Add-Failure 'version_drift' 'uv wrong error'
                        }
                    }
                }
                finally {
                    if (Test-Path -LiteralPath $tools.Uv) { Remove-Item -LiteralPath $tools.Uv -Force }
                    if (Test-Path -LiteralPath $uvBackup) { Move-Item -LiteralPath $uvBackup -Destination $tools.Uv }
                }
            }
            catch { Add-Failure 'runtime' $_.Exception.Message }
        }
    }
    else {
        Add-Failure 'blocked_npm_ps1' 'bootstrap missing'
        Add-Failure 'corrupt_download' 'bootstrap missing'
        Add-Failure 'system_mutation' 'bootstrap missing'
    }

    if ($script:Failures.Count) {
        $script:Failures | ForEach-Object { "CONTRACT_RED $_" }
        exit 1
    }
    'FOUNDATION_RUNTIME_CONTRACT_PASS locks=4 python=3.14.6 node=24.18.0 npm=11.16.0'
}
finally {
    Pop-Location
}
