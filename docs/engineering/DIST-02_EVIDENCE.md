# DIST-02 Evidence

Status: local OCI runtime closure is complete. Remote CI, registry push, and
public deployment were not executed; public URL/deployment are explicitly waived
for this local-only project.

```json
{
  "task": "DIST-02",
  "implementationCommit": "5145fea",
  "image": {"status": "pass", "command": "docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:local .", "engine": "29.1.2 linux/amd64", "builder": "ephemeral docker-container BuildKit with docker.m.daocloud.io mirror; exact pinned base digests unchanged", "id": "sha256:895b7df70ba3622c91d186c8856d9e97414a94bedc2e4d626791a7340d77d234", "size": 50910779, "platform": "linux/amd64", "user": "10001:10001"},
  "localSmoke": {"status": "pass", "runCommand": "docker run -d --rm --name projectb-demo-smoke --read-only --tmpfs /tmp/projectb-demo:rw,size=64m -e PROJECTB_DEMO_LOCAL_SMOKE=1 -p 127.0.0.1:7860:7860 projectb-demo:local", "smokeCommand": "powershell -NoProfile -ExecutionPolicy Bypass -File packaging/oci/smoke_test.ps1 -Container projectb-demo-smoke -Image projectb-demo:local -BaseUrl http://127.0.0.1:7860", "finallyCommand": "docker rm -f projectb-demo-smoke", "receipt": "OCI_NETWORK_COUNT=0; OCI_SMOKE_PASS profile=demo user=10001:10001 readonly=true tmpfs=true; OCI_CONTAINER_CLEANUP_DONE name=projectb-demo-smoke"},
  "localBrowser": {"status": "pass", "receipt": "DIST02_BROWSER_PASS chrome=system desktop=1440x900 mobile=360x800 routes=import,learning,settings"},
  "publicUrl": {"status": "waived", "decision": "student_confirmed_local_only"},
  "deployment": {"status": "waived", "decision": "student_confirmed_local_only"},
  "registryPush": {"status": "not_executed"},
  "remoteCI": {"status": "not_executed", "reason": "external Docker/GitLab runner evidence remains downstream"}
}
```

The static OCI contract (`7 passed`) plus the focused demo/OCI regression suite
(`17 passed` combined) lock the reviewed linux/amd64 Node and Python digests, the hashed
`requirements.linux-demo.lock`, demo-only mock provider settings, non-root UID/GID
`10001:10001`, read-only runtime plus tmpfs data root, healthcheck, a deterministic
185-component/185-relationship SPDX graph, complete notice bundle, and
push-triggered GitHub/GitLab OCI jobs.

`scripts/test_all.py --all` passed with backend `256 passed`, frontend `60 passed`,
Ruff, mypy, Vite, credential scan (`files=508`), and license verification. The
local smoke verified image history/resources, actual UID/GID, read-only root,
tmpfs reset, demo settings, exact forbidden upload/provider/credential routes,
mock fixture execution, process-level egress denial, zero established outbound
PID 1 sockets after the probes, and cleanup of the exact named container. The
egress and network-count probes are passed through stdin to Python so Windows
CLI quoting cannot rewrite the tests. System Chrome then verified the real demo
at desktop and mobile viewports across Import, Learning, and Settings.

The initial direct Docker Hub attempts failed at `auth.docker.io` anonymous-token
authorization. With approval, the coordinator used a disposable BuildKit registry
mirror only for transport; the Dockerfile's exact base-image digests and lock
files were unchanged. No registry login, image push, or public deployment was
performed.
