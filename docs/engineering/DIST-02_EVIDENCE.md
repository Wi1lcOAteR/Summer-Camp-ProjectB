# DIST-02 Evidence

Status: implementation and static contract are complete, but runtime closure is
blocked by Docker Hub connectivity. Docker Desktop was started with approval and
reported `29.1.2 linux/amd64`; the build then timed out while obtaining anonymous
tokens for the exact pinned Node and Python digests. No registry login, image
push, public URL, or deployment is claimed.

```json
{
  "task": "DIST-02",
  "implementationCommit": "12d709b",
  "image": {"status": "blocked_external_network", "command": "docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:local .", "engine": "29.1.2 linux/x86_64", "lastRetry": "2026-08-10T19:11:00+08:00", "blocker": "auth.docker.io anonymous-token timeout before base-image metadata"},
  "localSmoke": {"status": "not_executed", "command": "docker run -d --rm --read-only --tmpfs /tmp/projectb-demo:rw,size=64m"},
  "publicUrl": {"status": "waived", "decision": "student_confirmed_local_only"},
  "deployment": {"status": "waived", "decision": "student_confirmed_local_only"},
  "registryPush": {"status": "not_executed"}
}
```

The static contract (`7 passed`) locks the reviewed linux/amd64 Node and Python digests,
the hashed `requirements.linux-demo.lock`, demo-only mock provider settings,
non-root UID/GID `10001:10001`, read-only runtime plus tmpfs data root,
healthcheck, a deterministic 185-component/185-relationship SPDX graph, complete
notice bundle, and push-triggered GitHub/GitLab OCI jobs. `scripts/test_all.py --all`
passed with backend `254 passed`, frontend
`60 passed`, Ruff, mypy, Vite, credential scan, and license verification. The
local smoke will additionally verify image history/resources, actual UID/GID,
read-only root, tmpfs reset, demo settings, exact forbidden upload/provider/
credential routes, mock fixture execution, process-level egress denial, and
cleanup of the named container.

The coordinator retried the exact build with approved Docker access at
`2026-08-10T19:11:00+08:00`. The daemon was healthy, but both pinned Node and
Python metadata requests failed before any layer build while connecting to
`auth.docker.io`; no image, container, digest, run, or smoke receipt exists.
