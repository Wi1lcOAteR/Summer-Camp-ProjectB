# Dependency Baseline

Status: **BLOCKED - no project lockfile exists yet**

Verification date: `2026-07-21` (Asia/Shanghai)

This is an evidence ledger, not an install manifest. `explicitly-blocked` means the row is present and the reason is recorded, but downstream implementation must not consume it. Host and Codex-bundled packages are evidence of an environment only; they are not project dependencies.

| ID | Item | Version/term | Source URL | License/authority | Verified | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| python-runtime | Project Python runtime | host observed CPython 3.14.3; project version unlocked | https://www.python.org/downloads/windows/ | Python Software Foundation; project compatibility not tested | 2026-07-21 | explicitly-blocked | `py` 3.13 launcher points to a missing installation; no project manifest or lockfile. |
| backend-fastapi | FastAPI | exact version not verified | https://fastapi.tiangolo.com/ | official FastAPI docs; package/license not retrieved in this environment | 2026-07-21 | explicitly-blocked | Required by SPEC, but not installed or locked. |
| backend-asgi | Uvicorn | exact version not verified | https://www.uvicorn.org/ | official Uvicorn docs; package/license not retrieved in this environment | 2026-07-21 | explicitly-blocked | ASGI server choice is still an evidence-gated candidate. |
| backend-schema | Pydantic | exact version not verified | https://docs.pydantic.dev/latest/ | official Pydantic docs; package/license not retrieved in this environment | 2026-07-21 | explicitly-blocked | Schema dependency cannot be consumed until a lock and license row exist. |
| backend-http | HTTP client | exact client/version not verified | https://www.python-httpx.org/ | official HTTPX docs; package/license not retrieved in this environment | 2026-07-21 | explicitly-blocked | HTTPX is a candidate only; no install or lockfile. |
| openai-sdk | OpenAI Python SDK | exact version/license not verified | https://github.com/openai/openai-python | official upstream repository; release and license not retrieved in this environment | 2026-07-21 | explicitly-blocked | Adapter may use a verified HTTP client instead, but that is a later documented choice. |
| parser-pdf | pypdf | host observed 6.10.2; project version unlocked | https://pypi.org/project/pypdf/ | local METADATA: BSD-3-Clause; project lock absent | 2026-07-21 | explicitly-blocked | Only package found in the host project Python; no project install was performed. |
| renderer-pdf | pypdfium2 | Codex bundle observed 5.11.0; project version unlocked | https://pypi.org/project/pypdfium2/ | bundled notices include BSD-3-Clause/Apache-2.0 and dependency notices; project lock absent | 2026-07-21 | explicitly-blocked | Bundled runtime is not a project dependency and was not copied into the repository. |
| keyring-windows | keyring Windows Credential Manager backend | exact package/backend/version not verified | https://pypi.org/project/keyring/ | official PyPI target; Windows backend behavior/license not retrieved | 2026-07-21 | explicitly-blocked | Credential storage is a hard security boundary and cannot be guessed. |
| backend-test | pytest and backend test tools | exact versions/licenses not verified | https://docs.pytest.org/en/stable/ | official pytest docs; package/license not retrieved | 2026-07-21 | explicitly-blocked | No project test dependency is installed or locked. |
| frontend-runtime | Node.js and npm | host observed Node 24.14.0 / npm 11.9.0; project version unlocked | https://nodejs.org/en/about/previous-releases | Node.js release policy; project lock absent | 2026-07-21 | explicitly-blocked | Host runtime cannot substitute for a reproducible project toolchain. |
| frontend-react | React | exact version/license not verified | https://react.dev/ | official React docs; package/license not retrieved | 2026-07-21 | explicitly-blocked | Required by SPEC but not installed or locked. |
| frontend-build | Vite | exact version/license not verified | https://vite.dev/ | official Vite docs; package/license not retrieved | 2026-07-21 | explicitly-blocked | Build tool choice remains evidence-gated. |
| frontend-test | Vitest | exact version/license not verified | https://vitest.dev/ | official Vitest docs; package/license not retrieved | 2026-07-21 | explicitly-blocked | Frontend test tool is not installed or locked. |
| browser-test | Playwright | Codex bundle observed 1.61.1; project version unlocked | https://playwright.dev/ | bundled Apache-2.0 LICENSE/NOTICE/ThirdPartyNotices; project lock absent | 2026-07-21 | explicitly-blocked | Bundled browser tooling is evidence-only; browser binaries and project install remain unverified. |
| windows-freezer | PyInstaller or Nuitka | candidate not selected; exact version/license not verified | https://pyinstaller.org/en/stable/license.html | official freezer license page; clean-machine behavior not verified | 2026-07-21 | explicitly-blocked | G-02C also depends on this row; no freezer is installed. |
| dependency-transitive | Direct/transitive license closure | no lockfile, therefore closure unavailable | https://packaging.python.org/en/latest/guides/writing-pyproject-toml/ | Python Packaging User Guide; closure requires a project lock | 2026-07-21 | explicitly-blocked | A license table without a resolved lock would be incomplete evidence. |

## Environment observations

- Host commands observed: Python `3.14.3`, Node `v24.14.0`, npm `11.9.0`, SQLite CLI `3.51.2`, Docker CLI `29.1.2`.
- The host Python contained only `pypdf 6.10.2`; the local metadata reports BSD-3-Clause and `Requires-Python >=3.9`.
- Codex-bundled Python and Node packages were inspected only to understand available tooling. They are not installed into this repository and must not be used as project lock evidence.
- Network access to PyPI/npm was unavailable during this audit (connection closed / cache permission failures), so no current registry version was promoted to `verified`.

## Gate

G-02A remains pending. Before T-01, select exact packages, create project manifests and lockfiles, verify direct/transitive licenses, and rerun this ledger from a reachable authoritative source.
