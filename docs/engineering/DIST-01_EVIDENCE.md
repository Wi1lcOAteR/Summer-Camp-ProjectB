# DIST-01 Evidence

## Review-enabled release closure (2026-08-12)

- The release WebUI no longer uses the former hard-coded Review fixture. It consumes the existing persisted review revision/task API and exposes working generate, complete, skip, and recover actions.
- Frontend verification before the final artifact rebuild: Review focused Vitest `3 passed`; complete frontend gate `8 files passed, 59 tests passed`; TypeScript unused checks and Vite production build passed.
- Pinned PyInstaller `6.21.0` rebuilt the same source bytes successfully. Final `ProjectB.exe`: `29,225,145` bytes; SHA-256 `CB463E179FE2D3367ED0BA96B0621A5E32CF01319F39DB0AB74FC9FCC237F6A3`.
- Disposable-data smoke returned `WINDOWS_SMOKE_PASS profile=local credential_configured=False`. The retained local course then generated a real five-task revision. Browser acceptance executed start, skip, and recover and returned to five pending/zero skipped tasks, so persistence was exercised without consuming student progress.
- The older artifact receipt below remains historical evidence and must not be presented as the final review-enabled binary.

Status: current optimized artifact passes local development verification; exact-artifact clean-host performance retest was waived by student decision D-026.

The Windows package is a single `ProjectB.exe` produced by the pinned
PyInstaller recipe. The executable embeds the Vite build and the complete
third-party notice bundle, writes SQLite/content below the explicit data root
(`%LOCALAPPDATA%\\ProjectB` by default), and binds the local profile to
`127.0.0.1` only. The smoke script checks value-free credential status through
the application endpoint and never prints a credential value.

The clean Windows 11 x64 environment was created and exercised with the prior
artifact, but the readiness measurement did not meet the former `<=10.0`
second threshold. The student explicitly waived copying the current smaller
artifact into that guest for another timing run. The WinVault lifecycle is not
represented as a clean-VM PASS; separate deterministic credential tests and
the development-host lifecycle remain the available evidence.

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
| Development smoke | `WINDOWS_SMOKE_PASS profile=local credential_configured=False` on `127.0.0.1`; WebUI root, SQLite migrations/data root, `/api/courses`, and credential-status checks passed |
| Cleanup | smoke left no owned `ProjectB` process or listener on the test port and removed only its disposable `tmp` run directory; a pre-existing exact-artifact process is rejected and retained |
| Full local gate | backend `246 passed`; frontend `60 passed`; `TEST_ALL_PASS mode=all`; license and credential gates passed |

The freezer also checks Python 3.14.6 x64, PyInstaller 6.21.0, Node 24.18.0,
npm 11.16.0, and rejects reparse points before recursive cleanup. The generated
`PKG-00.toc` was checked for the WebUI HTML/assets, third-party notices,
PDFium DLL, and keyring resources.

The GitHub `windows-package` job is push-triggered, pins the Windows runner,
Python/Node/action revisions, runs the same contract/build, scans the local
artifact, and prints its hash. It does not upload or publish the executable.
## Clean Windows VM attempt (2026-08-11)

The coordinator rebuilt the release worktree with Python 3.14.6 and
PyInstaller 6.21.0. The artifact measured in this attempt was `36,640,080` bytes with SHA-256
`DAC2D69B27D85C65BBC32F068EA7D55AD8876237CFC177ACBB40D5F3584F09AB`.

The test guest was Windows 11 Enterprise Evaluation x64 build 26200 with 2
logical processors, 8 GiB RAM, an 80 GiB virtual disk reported by Windows as
SSD, and no installed Python, Node.js, or Docker runtime. Python Store aliases
were excluded only after confirming they reported version `0.0.0.0` and were
located under `Microsoft\WindowsApps`.

Observed readiness measurements included `23.554`, `14.664`, and `11.487`
seconds; strict ten-second runs also returned `startup_timeout`. Windows Update
and VirtualBox Guest Control load were isolated, and the same artifact was
rerun from a background guest process, but the threshold still did not pass.
An AHCI experiment booted once but later became unresponsive during shutdown;
the VM was returned to its retained IDE attachment and powered off. No product
or credential file was removed.

Because readiness failed, the script's real WinVault set/status/clear section
was not counted as a completed receipt. SmartScreen was not interactively
observed, so no warning-free claim is made. On 2026-08-11 the student closed
`DIST-01-VM-CLOSE` by waiver D-026 rather than by a current-artifact performance
PASS; the historical measurements remain evidence, not a successful threshold.

## Current optimized artifact (2026-08-11)

Archive inspection showed that optional Pillow image extensions occupied about
7.4 MB of the single-file package even though the production PDF validator only
opens `pypdfium2.PdfDocument` to count pages. With every `PIL` import blocked,
the real two-page PDF fixture still returned page count 2 and loaded no Pillow
module. A new packaging contract first failed because `PIL` was absent from the
PyInstaller exclusion list; after the minimal exclusion, the Windows contract
and PDF extraction tests returned `7 passed`.

The rebuilt current artifact is `29,215,426` bytes with SHA-256
`6A6A6C890EDD434798A0CB016A13463B2B4414ED4035230683A979B872704A98`.

## 2026-08-12 frozen material-worker repair

The student-preview run exposed that the one-file executable launched itself with the source module path when parsing an imported material. The launcher did not recognize that worker invocation, so every frozen TXT/PDF import ended as `content_unreadable` even though source-mode tests passed. A frozen-mode regression test now binds the executable command to `--material-worker`; the launcher handles that private entry point without starting the WebUI server.

Focused material and Windows distribution tests returned `9 passed`; scoped Ruff passed. PyInstaller `6.21.0` returned `WINDOWS_BUILD_PASS`. A fresh disposable-data instance of the rebuilt executable imported the synthetic TXT fixture with `status=imported`, and Edge acceptance then completed import, confirmed source mapping, deterministic mutex evaluation, and evidence creation. The current artifact is `29,223,634` bytes with SHA-256 `8B89717EDCA32720009750783B918130EA27A9BDE62CE159C11BE9721458047E`.
The first browser handoff exposed a real frozen-package failure:
`GET /api/courses` returned 500 because the PyInstaller archive omitted
`001_core.sql` and `002_learning.sql`. The RED distribution contract returned
`2 failed`; terminal repair `e06a863` adds both migrations to `datas`, makes
`build.ps1` verify both exact `PKG-00.toc` paths, and makes the smoke call
`/api/courses`. The rebuilt archive lists both SQL files, the focused contract
returns `2 passed`, and the development smoke returns
`WINDOWS_SMOKE_PASS profile=local credential_configured=False`. Browser
revalidation shows no alert and an empty usable material list.
No clean-VM startup, SmartScreen, WinVault, or `<=10` second PASS is claimed for
this rebuilt artifact. D-026 makes that exact rerun non-blocking for the local
submission package.
