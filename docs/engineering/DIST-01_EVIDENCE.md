# DIST-01 Evidence

Status: local development verification complete; clean-host close remains separate.

The Windows package is a single `ProjectB.exe` produced by the pinned
PyInstaller recipe. The executable embeds the Vite build and the complete
third-party notice bundle, writes SQLite/content below the explicit data root
(`%LOCALAPPDATA%\\ProjectB` by default), and binds the local profile to
`127.0.0.1` only. The smoke script checks value-free credential status through
the application endpoint and never prints a credential value.

The clean Windows 11 x64 / WinVault lifecycle gate is owned by
`DIST-01-VM-CLOSE` and remains `not executed` until that environment is
available.

## Development receipt (2026-08-10)

The reviewed commands were run from the DIST-01 worktree with the pinned
CPython runtime and a worktree-local temporary root:

| Check | Receipt |
| --- | --- |
| Contract tests | `backend/tests/distribution/test_windows_contract.py`: `2 passed` |
| Push-CI seed contract | `CI_SEED_CONTRACT_PASS` |
| Frontend build consumed by freezer | Vite `8.1.5`, build passed |
| Freezer | PyInstaller `6.21.0`, `WINDOWS_BUILD_PASS` |
| Artifact | `dist/ProjectB.exe`, 36,634,645 bytes |
| Artifact SHA-256 | `1E256C07B675F8C4F5B434452FED0AA9B1969E5ED932C3CCB5BC1BB9D9ABF64B` |
| Artifact credential scan | `CREDENTIAL_SCAN_PASS files=0` (the canonical scanner intentionally skips `.exe`; this is not an embedded-binary string scan) |
| Development smoke | `WINDOWS_SMOKE_PASS profile=local credential_configured=False` on `127.0.0.1`; WebUI root and SQLite data-root checks passed |
| Cleanup | smoke left no owned `ProjectB` process or listener on the test port and removed only its disposable `tmp` run directory; a pre-existing exact-artifact process is rejected and retained |
| Full local gate | backend `246 passed`; frontend `60 passed`; `TEST_ALL_PASS mode=all`; license and credential gates passed |

The freezer also checks Python 3.14.6 x64, PyInstaller 6.21.0, Node 24.18.0,
npm 11.16.0, and rejects reparse points before recursive cleanup. The generated
`PKG-00.toc` was checked for the WebUI HTML/assets, third-party notices,
PDFium DLL, and keyring resources.

The GitHub `windows-package` job is push-triggered, pins the Windows runner,
Python/Node/action revisions, runs the same contract/build, scans the local
artifact, and prints its hash. It does not upload or publish the executable.
The clean Windows 11 x64 / WinVault lifecycle gate remains
`DIST-01-VM-CLOSE: not executed`; no clean-host or SmartScreen claim is made.
