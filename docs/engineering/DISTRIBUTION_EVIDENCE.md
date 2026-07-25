# Distribution and Hosting Evidence

Status: **BLOCKED - G-02C found a confirmed paid-plan conflict requiring D-025**

Verification date: `2026-07-21` for the selected HF/freezer/base rows; alternative-host research refreshed `2026-07-22` (Asia/Shanghai). No deployment, account action, payment method, student credit use, Docker build, registry push, or paid resource was created.

The freezer and OCI base can now be selected exactly. The previously selected Hugging Face Docker Space direction cannot satisfy the current no-paid-resource boundary: Hugging Face's current official docs explicitly require a paid plan to create a Gradio or Docker Space even though CPU Basic has no hourly hardware charge. No alternative host is selected silently.

| ID | Item | Version/term | Source URL | License/authority | Verified | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| windows-freezer | Windows x64 single-file freezer | PyInstaller 6.21.0; Python >=3.8 and <3.16; win_amd64 wheel SHA-256 7fae06c494ce0ebfe6bd3055c0e409def884f63af2e3705d06bd431ad9237fc7 | https://pyinstaller.org/en/stable/license.html | GPL-2.0-or-later WITH Bootloader-exception; runtime hooks Apache-2.0 | 2026-07-21 | verified | One-file Uvicorn and PDFium smoke passed on CPython 3.14.6. keyring requires explicit collection of backend_complete.bash and backend_complete.zsh; corrected smoke exposed WinVaultKeyring priority 5. Full app/clean-machine proof remains DIST-01. |
| oci-base | OCI base image for linux/amd64 | python:3.14.6-slim-bookworm index sha256:86f975aca15cf04a40b399eebede9aea7c82eae084d1f1a0a6ef6bcaae871a30; amd64 manifest sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb | https://github.com/docker-library/repo-info/blob/99919ada7d519a93bfafcd36ddab30df211ecdb9/repos/python/remote/3.14.6-slim-bookworm.md | Docker Official Images metadata; PSF Python plus Debian package-specific licenses | 2026-07-21 | verified | Exact amd64 image is 44,765,139 compressed bytes and uses Python 3.14.6. DIST-02 must generate an SBOM and retain Debian/Python notices; a digest does not prove project image behavior. |
| host-runtime | Hugging Face Docker Spaces runtime | Docker SDK supports a Dockerfile, sdk: docker, default app_port 7860, and containers running as UID 1000 | https://github.com/huggingface/hub-docs/blob/86be61b3d86b7df41ba4500e6b93de7a41f1d1fb/docs/hub/spaces-sdks-docker.md | Hugging Face official hub-docs; Apache-2.0 | 2026-07-21 | verified | Technical runtime is compatible with FastAPI/React, but creation is commercially incompatible with the current no-paid boundary. |
| host-https | Public HTTPS access | public/protected running app uses https://<space-subdomain>.hf.space; public source and app are visible | https://github.com/huggingface/hub-docs/blob/86be61b3d86b7df41ba4500e6b93de7a41f1d1fb/docs/hub/spaces-overview.md | Hugging Face official hub-docs; Apache-2.0 | 2026-07-21 | verified | This is documentation evidence only; no URL or external browser acceptance evidence exists. |
| host-storage | Host storage and persistence | default 50 GB disk is not persistent; Space disk is ephemeral and lost on restart/stop | https://github.com/huggingface/hub-docs/blob/86be61b3d86b7df41ba4500e6b93de7a41f1d1fb/docs/hub/spaces-storage.md | Hugging Face official hub-docs; Apache-2.0 | 2026-07-21 | verified | The demo already requires disposable state and must not attach a storage bucket or persist private/user material. |
| host-sleep | Idle sleep and restart | CPU Basic sleeps after 48 hours inactive; a visitor restarts it; indefinite/custom sleep requires paid hardware | https://github.com/huggingface/hub-docs/blob/86be61b3d86b7df41ba4500e6b93de7a41f1d1fb/docs/hub/spaces-gpus.md | Hugging Face official hub-docs; Apache-2.0 | 2026-07-21 | verified | Project session TTL remains separate from host sleep/wake behavior. |
| host-quota | CPU, memory, and ephemeral disk | CPU Basic 2 vCPU, 16 GB RAM, 50 GB disk; outbound network limited to standard HTTP/HTTPS ports plus 8080 | https://github.com/huggingface/hub-docs/blob/86be61b3d86b7df41ba4500e6b93de7a41f1d1fb/docs/hub/spaces-overview.md | Hugging Face official hub-docs; Apache-2.0 | 2026-07-21 | verified | Project limits must be lower and reproducible; no runtime benchmark has been performed. |
| host-cost | Hosting cost boundary | CPU Basic hardware has no hourly charge, but creating a new Docker/Gradio compute Space requires a paid PRO, Team, or Enterprise plan | https://github.com/huggingface/hub-docs/blob/86be61b3d86b7df41ba4500e6b93de7a41f1d1fb/docs/hub/spaces-overview.md | Hugging Face official hub-docs at commit 86be61b3; paid-plan requirement | 2026-07-21 | explicitly-blocked | This contradicts the confirmed no-paid-resource boundary and current authorization. ZeroGPU's free exception is for Gradio, not the selected Docker SDK. |
| host-account | Account and plan authorization | Docker Space creation requires an eligible paid personal or organization plan | https://github.com/huggingface/hub-docs/blob/86be61b3d86b7df41ba4500e6b93de7a41f1d1fb/docs/hub/spaces-overview.md | Hugging Face official account/plan requirement | 2026-07-21 | explicitly-blocked | No account, payment method, subscription, or terms acceptance is authorized. The student must choose D-025 before any platform action. |
| fallback | No-silent-substitution boundary | selected host conflict requires explicit student choice and SPEC diff; preserve OCI/same-contract/HTTPS/mock/isolation requirements | https://github.com/huggingface/hub-docs/blob/86be61b3d86b7df41ba4500e6b93de7a41f1d1fb/docs/hub/spaces-overview.md | ProjectB SPEC and current official host facts | 2026-07-22 | verified | First-party candidate research now exists in `docs/research/PUBLIC_HOSTING_ALTERNATIVES.md`, but no route is selected. Render and Koyeb remain excluded by the prior browser security decision. |

## Reproducible Source Snapshots

- Hugging Face hub-docs commit: `86be61b3d86b7df41ba4500e6b93de7a41f1d1fb`, committed `2026-07-21T12:37:28Z`; repository license Apache-2.0.
- Docker Library repo-info commit: `99919ada7d519a93bfafcd36ddab30df211ecdb9`, committed `2026-07-21T15:12:16Z`.
- PyInstaller exact PyPI release: 6.21.0, official documentation title also reports 6.21.0.

The Docker registry endpoint and Hugging Face rendered site timed out/reset in this environment. Exact first-party GitHub snapshots were used instead. Docker itself still reports no local daemon, so no image build/run evidence exists.

## Alternative-Host Research Boundary

`docs/research/PUBLIC_HOSTING_ALTERNATIVES.md` records current official evidence for two conditional alternatives without promoting either into the host evidence rows:

- an existing student/NJU-controlled x64 Docker host, optionally exposed through Tailscale Funnel when no existing HTTPS domain is available;
- Azure for Students with Azure Container Apps Consumption, subject to student eligibility, explicit account/resource approval and a no-pay-as-you-go boundary.

It also records why Cloudflare Quick Tunnel, Northflank Developer Sandbox, Oracle Always Free and static hosting are not current final-host recommendations. These facts make D-025 answerable but do not verify `host-cost` or `host-account`: those rows preserve the previously selected HF route's incompatibility evidence while the actual host remains unset pending student choice and a confirmed SPEC diff.

## D-025 Gate

The previously selected HF host is proven incompatible with the no-paid-resource rule, so the actual host is currently unset. Current first-party research supports three decision paths:

1. provide an existing student/NJU-controlled x64 Docker host; use its existing HTTPS entry point or explicitly accept Tailscale Funnel's beta/always-online boundary;
2. approve the documented Azure for Students + Container Apps SPEC diff, account/resource creation and student-credit use while forbidding pay-as-you-go upgrade;
3. explicitly authorize a paid Hugging Face plan and recurring-cost boundary, which is outside the current Goal authorization.

Until D-025 is resolved, the host-specific G-02C2/release path, final public deployment and any claim of a public WebUI URL remain blocked. It does not block reduced-SPEC confirmation, implementation-plan authoring, G-03 cold start, or host-neutral local work after implementation approval. The verified PyInstaller and base-image rows remain usable inputs, but full application and clean-environment proof still belongs to future DIST tasks.
