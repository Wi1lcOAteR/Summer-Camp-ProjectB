param(
    [Parameter(Mandatory = $true)][string]$Container,
    [Parameter(Mandatory = $true)][string]$Image,
    [string]$BaseUrl = "http://127.0.0.1:7860"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Docker([string[]]$Arguments) {
    $result = @(& docker @Arguments 2>&1)
    if ($LASTEXITCODE -ne 0) { throw ("docker_failed:{0}" -f ($Arguments -join " ")) }
    return $result
}

function Get-HttpStatus([string]$Uri) {
    try {
        return [int](Invoke-WebRequest -UseBasicParsing -Uri $Uri -TimeoutSec 2).StatusCode
    } catch {
        if ($null -ne $_.Exception.Response) { return [int]$_.Exception.Response.StatusCode.value__ }
        throw
    }
}

function Wait-ContainerReady([string]$Name, [string]$Uri) {
    for ($attempt = 0; $attempt -lt 60; $attempt++) {
        $running = ((Invoke-Docker @("inspect", "--format", "{{.State.Running}}", $Name)) -join "").Trim()
        if ($running -eq "true") {
            try {
                $response = Invoke-WebRequest -UseBasicParsing -Uri $Uri -TimeoutSec 2
                if ($response.StatusCode -eq 200) { return $response.Content }
            } catch {
                # A running container can need a short startup window before HTTP is ready.
            }
        }
        Start-Sleep -Milliseconds 500
    }
    throw "oci_restart_not_running"
}

$imageArchitecture = ((Invoke-Docker @("image", "inspect", "--format", "{{.Architecture}}", $Image)) -join "").Trim()
$imageOs = ((Invoke-Docker @("image", "inspect", "--format", "{{.Os}}", $Image)) -join "").Trim()
$imageUser = ((Invoke-Docker @("image", "inspect", "--format", "{{.Config.User}}", $Image)) -join "").Trim()
if ($imageArchitecture -ne "amd64" -or $imageOs -ne "linux") { throw "oci_architecture_invalid" }
if ($imageUser -ne "10001:10001") { throw "oci_user_invalid" }
$history = ((Invoke-Docker @("history", "--no-trunc", "--format", "{{.CreatedBy}}", $Image)) -join "`n").ToLowerInvariant()
if ($history -match "--mount=type=secret|arg\s+(api[_-]?key|token|password|secret)") { throw "oci_history_secret" }
$resourceProbe = Invoke-Docker @(
    "run", "--rm", "--entrypoint", "/bin/sh", $Image,
    "-c", "test -s /opt/projectb/licenses/sbom.spdx.json && test -s /opt/projectb/licenses/THIRD_PARTY_NOTICES.md && test -s /opt/projectb/licenses/OCI_THIRD_PARTY_NOTICES.md && test -s /opt/projectb/licenses/debian-packages.tsv"
)

$readonlyRoot = ((Invoke-Docker @("inspect", "--format", "{{.HostConfig.ReadonlyRootfs}}", $Container)) -join "").Trim()
if ($readonlyRoot -ne "true") { throw "oci_readonly_root_invalid" }
$tmpfs = ((Invoke-Docker @("inspect", "--format", "{{json .HostConfig.Tmpfs}}", $Container)) -join "`n").Trim()
if ($tmpfs -notmatch '"/tmp/projectb-demo"' -or $tmpfs -notmatch "rw") { throw "oci_tmpfs_invalid" }
if (((Invoke-Docker @("exec", $Container, "id", "-u")) -join "").Trim() -ne "10001") { throw "oci_runtime_uid_invalid" }
if (((Invoke-Docker @("exec", $Container, "id", "-g")) -join "").Trim() -ne "10001") { throw "oci_runtime_gid_invalid" }

$health = ((Invoke-Docker @("inspect", "--format", "{{json .State.Health.Status}}", $Container)) -join "").Trim('"', "`r", "`n")
if ($health -notin @("healthy", "starting")) { throw "oci_health_invalid" }
$settingsUri = $BaseUrl.TrimEnd('/') + "/api/settings"
$body = Wait-ContainerReady $Container $settingsUri | ConvertFrom-Json
if ($body.profile -ne "demo" -or $body.bind_host -ne "0.0.0.0" -or $body.provider_mode -ne "L") { throw "oci_profile_failed" }
if ((Get-HttpStatus ($BaseUrl.TrimEnd('/') + "/")) -ne 200) { throw "oci_webui_failed" }
if ((Get-HttpStatus ($BaseUrl.TrimEnd('/') + "/api/demo/fixture-explanation")) -ne 200) { throw "oci_fixture_failed" }

foreach ($route in @(
    "/api/courses/probe/materials/import",
    "/api/providers/execute",
    "/api/credentials/provider"
)) {
    if ((Get-HttpStatus ($BaseUrl.TrimEnd('/') + $route)) -ne 404) { throw "oci_capability_leak:$route" }
}

$marker = "/tmp/projectb-demo/dist02-restart-marker"
Invoke-Docker @("exec", $Container, "sh", "-c", ("touch {0}" -f $marker)) | Out-Null
Invoke-Docker @("restart", $Container) | Out-Null
Wait-ContainerReady $Container $settingsUri | Out-Null
Invoke-Docker @("exec", $Container, "sh", "-c", ("test ! -e {0}" -f $marker)) | Out-Null

$egressCode = @'
import socket
from projectb.profiles.demo import DemoEgressDenied, install_demo_egress_guard

install_demo_egress_guard()
try:
    socket.getaddrinfo('example.com', 443)
except DemoEgressDenied:
    print("OCI_EGRESS_DENIED")
else:
    raise SystemExit("egress_not_denied")
'@
$egressResult = @($egressCode | & docker exec -i $Container /usr/local/bin/python - 2>&1)
if ($LASTEXITCODE -ne 0) { throw "docker_failed:exec egress_probe" }
$egressProbe = $egressResult -join "`n"
if ($egressProbe.Trim() -ne "OCI_EGRESS_DENIED") { throw "oci_egress_guard_unverified" }

$networkCode = @'
import os
from pathlib import Path

service_port = int(os.environ["PROJECTB_PORT"])
count = sum(
    1
    for table in (Path("/proc/1/net/tcp"), Path("/proc/1/net/tcp6"))
    for line in table.read_text(encoding="ascii").splitlines()[1:]
    if line.split()[3] == "01"
    and int(line.split()[1].rsplit(":", 1)[1], 16) != service_port
)
print(f"OCI_NETWORK_COUNT={count}")
if count:
    raise SystemExit("network_count_nonzero")
'@
$networkResult = @($networkCode | & docker exec -i $Container /usr/local/bin/python - 2>&1)
if ($LASTEXITCODE -ne 0) { throw "docker_failed:exec network_count_probe" }
$networkProbe = ($networkResult -join "`n").Trim()
if ($networkProbe -ne "OCI_NETWORK_COUNT=0") { throw ("oci_network_count_unverified:{0}" -f $networkProbe) }
Write-Output $networkProbe

Write-Output "OCI_SMOKE_PASS profile=demo user=10001:10001 readonly=true tmpfs=true"
