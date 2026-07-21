# Distribution and Hosting Evidence

Status: **BLOCKED - current host terms, immutable base digest, and clean-machine packaging are not verified**

Verification date: `2026-07-21` (Asia/Shanghai). This audit performed no deployment, account action, Docker build, or paid resource creation.

| ID | Item | Version/term | Source URL | License/authority | Verified | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| windows-freezer | Windows x64 single-file freezer | PyInstaller candidate; exact version and target smoke not verified | https://pyinstaller.org/en/stable/license.html | PyInstaller official license/usage pages; clean-machine behavior unverified | 2026-07-21 | explicitly-blocked | Recheck the official license and usage/one-file constraints at https://pyinstaller.org/en/stable/usage.html. Nuitka is an unselected alternative; do not substitute it silently. |
| oci-base | OCI base image | `python:3.13-slim-bookworm` candidate; immutable digest and amd64 manifest not verified | https://hub.docker.com/_/python | Docker Official Image metadata; Debian/Python notices not collected | 2026-07-21 | explicitly-blocked | A mutable tag is not a reproducible image lock. |
| host-runtime | Public host runtime | Hugging Face Spaces Docker SDK candidate; current runtime requirements not retrieved | https://huggingface.co/docs/hub/spaces-sdks-docker | Hugging Face official docs; terms/current limits unavailable in this audit | 2026-07-21 | explicitly-blocked | No Space was created. |
| host-https | Public HTTPS access | generated HTTPS URL and ingress behavior not verified | https://huggingface.co/docs/hub/spaces-overview | Hugging Face official docs; current deployment behavior unavailable | 2026-07-21 | explicitly-blocked | AC-47 requires an externally reachable URL and evidence. |
| host-storage | Host storage and persistence | ephemeral/persistent storage behavior and quotas not verified | https://huggingface.co/docs/hub/spaces-overview | Hugging Face official docs; current storage terms unavailable | 2026-07-21 | explicitly-blocked | Demo state must remain disposable even if host storage exists. |
| host-sleep | Idle sleep and restart | idle sleep/restart policy not verified | https://huggingface.co/docs/hub/spaces-overview | Hugging Face official docs; current lifecycle terms unavailable | 2026-07-21 | explicitly-blocked | Project session TTL is not a substitute for host lifecycle evidence. |
| host-quota | CPU, memory, request and storage quota | current free-tier/hardware quota not verified | https://huggingface.co/docs/hub/spaces-gpus | Hugging Face official docs; current quota table unavailable | 2026-07-21 | explicitly-blocked | Do not infer historical free-tier values. |
| host-cost | Hosting cost boundary | current price/free allowance not verified | https://huggingface.co/pricing#spaces | Hugging Face pricing page; current cost not retrieved | 2026-07-21 | explicitly-blocked | No paid resource may be created without a separate execution-time authorization. |
| host-account | Account and terms | account/payment/acceptable-use terms not verified | https://huggingface.co/terms-of-service | Hugging Face official terms; current page unavailable | 2026-07-21 | explicitly-blocked | Student account ownership and external deployment remain execution-time decisions. |
| fallback | No-paid-resource fallback | if selected host violates no-paid/HTTPS/limits, require explicit SPEC change before substitution | https://huggingface.co/docs/hub/spaces-sdks-docker | ProjectB SPEC/PLAN boundary; host facts still unverified | 2026-07-21 | verified | No alternative host is selected and no deployment is authorized by this row. |

## Local observations

- Docker CLI `29.1.2` was present, but the Docker daemon was unavailable (`docker_engine` named pipe missing), so no image build/run evidence exists.
- PyInstaller, Nuitka, and cx_Freeze were not installed or cached in the project environment.
- Network probes to the official freezer, registry, Docker Hub, and Hugging Face pages failed with connection close/timeouts during this audit. The failure is recorded rather than replaced with historical limits.

## Gate

G-02C remains pending. Recheck the first-party pages, lock an immutable OCI digest and architecture, select one freezer, and run clean-machine build/smoke tests before DIST-01/DIST-02 or a public URL claim.
