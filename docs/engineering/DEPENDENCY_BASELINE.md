# Dependency Baseline

Status: **READY FOR COMMIT - G-02A exact dependency and license evidence verified**

Verification date: `2026-07-21` (Asia/Shanghai)

This is an implementation-input evidence ledger, not the production manifest. The two lock artifacts under `docs/engineering/locks/` were resolved and smoke-tested in disposable runtimes and are consumed by T-01 when it creates the real project manifests. They must not be presented as an installed application or clean-machine distribution.

## Selected Direct Dependencies

| ID | Item | Version/term | Source URL | License/authority | Verified | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| python-runtime | CPython Windows x64 | 3.14.6; embed ZIP SHA-256 df901e84a896ff1ee720ad03377e0c8d8c2244fda79808aeeaff6316df1cb75c | https://www.python.org/downloads/release/python-3146/ | Python Software Foundation License | 2026-07-21 | verified | Official embeddable ZIP was checksum-verified and used without registry or PATH changes. |
| backend-fastapi | FastAPI | 0.139.2 | https://pypi.org/pypi/fastapi/0.139.2/json | MIT | 2026-07-21 | verified | Multipart and health-route smoke passed on CPython 3.14.6. |
| backend-asgi | Uvicorn | 0.51.0 | https://pypi.org/pypi/uvicorn/0.51.0/json | BSD-3-Clause | 2026-07-21 | verified | Synthetic PyInstaller one-file build and run passed. |
| backend-schema | Pydantic | 2.13.4 | https://pypi.org/pypi/pydantic/2.13.4/json | MIT | 2026-07-21 | verified | CPython 3.14 wheel/import smoke passed. |
| backend-http | HTTPX | 0.28.1 | https://pypi.org/pypi/httpx/0.28.1/json | BSD-3-Clause | 2026-07-21 | verified | Application HTTP/mock transport path; no network request was made in smoke. |
| backend-http2 | HTTPX2 test client | 2.7.0 | https://pypi.org/pypi/httpx2/2.7.0/json | BSD-3-Clause | 2026-07-21 | verified | Pydantic-maintained package required by Starlette 1.3.1 to avoid the deprecated HTTPX TestClient path. Not used for provider I/O. |
| openai-sdk | OpenAI Python SDK | 2.46.0 | https://pypi.org/pypi/openai/2.46.0/json | Apache-2.0 | 2026-07-21 | verified | Import-only smoke passed; no key, request, or paid call was used. |
| parser-pdf | pypdf | 6.14.2 | https://pypi.org/pypi/pypdf/6.14.2/json | BSD-3-Clause | 2026-07-21 | verified | Synthetic PDF write/read smoke passed. |
| renderer-pdf | pypdfium2 | 5.12.1; PDFium 152.0.7947.0 | https://pypi.org/pypi/pypdfium2/5.12.1/json | BSD-3-Clause plus Apache-2.0 and dependency notices including CC-BY-4.0 | 2026-07-21 | verified | Synthetic render and one-file DLL extraction smoke passed; all 19 wheel notice files must be retained. |
| parser-image | Pillow | 12.3.0 | https://pypi.org/pypi/Pillow/12.3.0/json | MIT-CMU | 2026-07-21 | verified | PNG, JPEG, and WebP encode/decode smoke passed. |
| keyring-windows | keyring WinVaultKeyring | 25.7.0 | https://pypi.org/pypi/keyring/25.7.0/json | MIT | 2026-07-21 | verified | WinVaultKeyring instantiated at priority 5 without storing a credential. PyInstaller must explicitly collect backend_complete.bash and backend_complete.zsh; the corrected one-file smoke passed. |
| timezone-data | tzdata | 2026.3 | https://pypi.org/pypi/tzdata/2026.3/json | Apache-2.0 | 2026-07-21 | verified | ZoneInfo Asia/Shanghai smoke passed and provides the deterministic tzdata version input. |
| upload-parser | python-multipart | 0.0.32 | https://pypi.org/pypi/python-multipart/0.0.32/json | Apache-2.0 | 2026-07-21 | verified | FastAPI multipart upload smoke passed. |
| process-metrics | psutil | 7.2.2 | https://pypi.org/pypi/psutil/7.2.2/json | BSD-3-Clause | 2026-07-21 | verified | Windows x64 RSS/process smoke passed. |
| backend-test | pytest | 9.1.1 | https://pypi.org/pypi/pytest/9.1.1/json | MIT | 2026-07-21 | verified | Warnings-as-errors functional smoke passed. |
| backend-lint | Ruff | 0.15.22 | https://pypi.org/pypi/ruff/0.15.22/json | MIT | 2026-07-21 | verified | Exact CLI version smoke passed. |
| backend-type | mypy | 2.3.0 | https://pypi.org/pypi/mypy/2.3.0/json | MIT | 2026-07-21 | verified | Exact CLI/import smoke passed. |
| backend-type-psutil | types-psutil | 7.2.2.20260518 | https://pypi.org/pypi/types-psutil/7.2.2.20260518/json | Apache-2.0 | 2026-07-21 | verified | Exact stub package is part of the Python lock. |
| frontend-runtime | Node.js LTS and npm | Node 24.18.0 Krypton; npm 11.16.0; win-x64 ZIP SHA-256 0ae68406b42d7725661da979b1403ec9926da205c6770827f33aac9d8f26e821 | https://nodejs.org/dist/v24.18.0/SHASUMS256.txt | Node.js MIT plus bundled notices; npm Artistic-2.0 | 2026-07-21 | verified | Official ZIP checksum passed; npm ci used engine-strict and ignore-scripts in a disposable directory. |
| frontend-react | React | 19.2.7 | https://registry.npmjs.org/react/19.2.7 | MIT | 2026-07-21 | verified | Exact import smoke passed. |
| frontend-react-dom | React DOM | 19.2.7 | https://registry.npmjs.org/react-dom/19.2.7 | MIT | 2026-07-21 | verified | Exact import smoke passed. |
| frontend-icons | lucide-react | 1.25.0 | https://registry.npmjs.org/lucide-react/1.25.0 | ISC | 2026-07-21 | verified | Selected icon library; retain ISC notice. |
| frontend-build | Vite | 8.1.5 | https://registry.npmjs.org/vite/8.1.5 | MIT | 2026-07-21 | verified | Node engine and CLI smoke passed. |
| frontend-build-react | Vite React plugin | 6.0.3 | https://registry.npmjs.org/@vitejs%2Fplugin-react/6.0.3 | MIT | 2026-07-21 | verified | Node engine/import smoke passed. |
| frontend-typescript | TypeScript | 7.0.2 | https://registry.npmjs.org/typescript/7.0.2 | Apache-2.0 | 2026-07-21 | verified | tsc CLI smoke passed; retain NOTICE. |
| frontend-test | Vitest | 4.1.10 | https://registry.npmjs.org/vitest/4.1.10 | MIT | 2026-07-21 | verified | Node engine and CLI smoke passed. |
| frontend-testing-dom | Testing Library DOM | 10.4.1 | https://registry.npmjs.org/@testing-library%2Fdom/10.4.1 | MIT | 2026-07-21 | verified | JSDOM role-query smoke passed. |
| frontend-testing-react | Testing Library React | 16.3.2 | https://registry.npmjs.org/@testing-library%2Freact/16.3.2 | MIT | 2026-07-21 | verified | Exact import smoke passed. |
| frontend-testing-user | Testing Library user-event | 14.6.1 | https://registry.npmjs.org/@testing-library%2Fuser-event/14.6.1 | MIT | 2026-07-21 | verified | Exact import smoke passed. |
| frontend-jsdom | JSDOM | 29.1.1 | https://registry.npmjs.org/jsdom/29.1.1 | MIT | 2026-07-21 | verified | DOM construction and accessible role query passed. |
| browser-test | Playwright Test | 1.61.1 | https://registry.npmjs.org/@playwright%2Ftest/1.61.1 | Apache-2.0 | 2026-07-21 | verified | Package and CLI smoke passed. Browser binaries remain QA-01 evidence, not G-02A. |
| browser-a11y | axe Playwright integration | 4.12.1 | https://registry.npmjs.org/@axe-core%2Fplaywright/4.12.1 | MPL-2.0 | 2026-07-21 | verified | Exact import smoke passed; retain axe third-party notices and MPL covered-file obligations. |
| frontend-types-react | React type definitions | 19.2.17 | https://registry.npmjs.org/@types%2Freact/19.2.17 | MIT | 2026-07-21 | verified | Exact lock entry. |
| frontend-types-react-dom | React DOM type definitions | 19.2.3 | https://registry.npmjs.org/@types%2Freact-dom/19.2.3 | MIT | 2026-07-21 | verified | Exact lock entry. |
| frontend-types-node | Node type definitions | 24.13.3 | https://registry.npmjs.org/@types%2Fnode/24.13.3 | MIT | 2026-07-21 | verified | Exact lock entry compatible with the Node 24 line. |
| windows-freezer | PyInstaller | 6.21.0 | https://pypi.org/pypi/pyinstaller/6.21.0/json | GPL-2.0-or-later WITH Bootloader-exception; runtime hooks Apache-2.0 | 2026-07-21 | verified | Supports Python below 3.16 and publishes a win_amd64 wheel. Full application clean-machine evidence remains DIST-01. |
| python-lock-closure | Hashed Windows x64 Python closure | 54 exact pins; canonical-LF SHA-256 246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6 | https://pypi.org/simple/ | Exact PyPI metadata and wheel license files | 2026-07-21 | verified | Stored at docs/engineering/locks/python-3.14.6-windows-x64.lock; validator normalizes text line endings before hashing and cross-checks every pin/direct dependency against the table below. |
| npm-lock-closure | npm lockfile v3 closure | 166 exact package entries; 115 installed on win-x64; canonical-LF SHA-256 071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f | https://registry.npmjs.org/ | Exact registry URLs, integrity hashes, and package license fields | 2026-07-21 | verified | Stored at docs/engineering/locks/frontend-package-lock.json; 54 optional cross-platform packages remain locked. Validator compares all 16 root direct dependencies and the reviewed license set; npm audit reported zero current findings. |
| dependency-transitive | Direct and transitive license closure | Python 54 packages and npm 166 entries | https://packaging.python.org/en/latest/guides/repeatable-installs/ | Machine-checked exact pins, hashes, licenses, and notice obligations | 2026-07-21 | verified | Production manifests and the CI license scanner are created later by T-01 and CI-01 from these evidence inputs. |

## Python License Closure

The validator requires exactly the same 54 normalized name/version pairs in this table and in the hashed Python lock.

| Ecosystem | Package | Version | License | Source | Role |
| --- | --- | --- | --- | --- | --- |
| python | altgraph | 0.17.5 | MIT | https://pypi.org/pypi/altgraph/0.17.5/json | transitive |
| python | annotated-doc | 0.0.4 | MIT | https://pypi.org/pypi/annotated-doc/0.0.4/json | transitive |
| python | annotated-types | 0.7.0 | MIT | https://pypi.org/pypi/annotated-types/0.7.0/json | transitive |
| python | anyio | 4.14.2 | MIT | https://pypi.org/pypi/anyio/4.14.2/json | transitive |
| python | ast-serialize | 0.6.0 | MIT | https://pypi.org/pypi/ast-serialize/0.6.0/json | transitive |
| python | certifi | 2026.6.17 | MPL-2.0 | https://pypi.org/pypi/certifi/2026.6.17/json | transitive |
| python | click | 8.4.2 | BSD-3-Clause | https://pypi.org/pypi/click/8.4.2/json | transitive |
| python | colorama | 0.4.6 | BSD-3-Clause | https://pypi.org/pypi/colorama/0.4.6/json | transitive |
| python | distro | 1.9.0 | Apache-2.0 | https://pypi.org/pypi/distro/1.9.0/json | transitive |
| python | fastapi | 0.139.2 | MIT | https://pypi.org/pypi/fastapi/0.139.2/json | direct |
| python | h11 | 0.16.0 | MIT | https://pypi.org/pypi/h11/0.16.0/json | transitive |
| python | httpcore | 1.0.9 | BSD-3-Clause | https://pypi.org/pypi/httpcore/1.0.9/json | transitive |
| python | httpcore2 | 2.7.0 | BSD-3-Clause | https://pypi.org/pypi/httpcore2/2.7.0/json | transitive |
| python | httpx | 0.28.1 | BSD-3-Clause | https://pypi.org/pypi/httpx/0.28.1/json | direct |
| python | httpx2 | 2.7.0 | BSD-3-Clause | https://pypi.org/pypi/httpx2/2.7.0/json | direct-test |
| python | idna | 3.18 | BSD-3-Clause | https://pypi.org/pypi/idna/3.18/json | transitive |
| python | iniconfig | 2.3.0 | MIT | https://pypi.org/pypi/iniconfig/2.3.0/json | transitive |
| python | jaraco.classes | 3.4.0 | MIT | https://pypi.org/pypi/jaraco.classes/3.4.0/json | transitive |
| python | jaraco.context | 6.1.2 | MIT | https://pypi.org/pypi/jaraco.context/6.1.2/json | transitive |
| python | jaraco.functools | 4.6.0 | MIT | https://pypi.org/pypi/jaraco.functools/4.6.0/json | transitive |
| python | jiter | 0.16.0 | MIT | https://pypi.org/pypi/jiter/0.16.0/json | transitive |
| python | keyring | 25.7.0 | MIT | https://pypi.org/pypi/keyring/25.7.0/json | direct |
| python | librt | 0.13.0 | MIT | https://pypi.org/pypi/librt/0.13.0/json | transitive |
| python | more-itertools | 11.1.0 | MIT | https://pypi.org/pypi/more-itertools/11.1.0/json | transitive |
| python | mypy | 2.3.0 | MIT | https://pypi.org/pypi/mypy/2.3.0/json | direct-dev |
| python | mypy-extensions | 1.1.0 | MIT | https://pypi.org/pypi/mypy-extensions/1.1.0/json | transitive |
| python | openai | 2.46.0 | Apache-2.0 | https://pypi.org/pypi/openai/2.46.0/json | direct |
| python | packaging | 26.2 | Apache-2.0 OR BSD-2-Clause | https://pypi.org/pypi/packaging/26.2/json | transitive |
| python | pathspec | 1.1.1 | MPL-2.0 | https://pypi.org/pypi/pathspec/1.1.1/json | transitive |
| python | pefile | 2024.8.26 | MIT | https://pypi.org/pypi/pefile/2024.8.26/json | transitive |
| python | Pillow | 12.3.0 | MIT-CMU | https://pypi.org/pypi/Pillow/12.3.0/json | direct |
| python | pluggy | 1.6.0 | MIT | https://pypi.org/pypi/pluggy/1.6.0/json | transitive |
| python | psutil | 7.2.2 | BSD-3-Clause | https://pypi.org/pypi/psutil/7.2.2/json | direct |
| python | pydantic | 2.13.4 | MIT | https://pypi.org/pypi/pydantic/2.13.4/json | direct |
| python | pydantic-core | 2.46.4 | MIT | https://pypi.org/pypi/pydantic-core/2.46.4/json | transitive |
| python | Pygments | 2.20.0 | BSD-2-Clause | https://pypi.org/pypi/Pygments/2.20.0/json | transitive |
| python | pyinstaller | 6.21.0 | GPL-2.0-or-later WITH Bootloader-exception | https://pypi.org/pypi/pyinstaller/6.21.0/json | direct-build |
| python | pyinstaller-hooks-contrib | 2026.6 | GPL-2.0-or-later standard hooks; Apache-2.0 runtime hooks | https://pypi.org/pypi/pyinstaller-hooks-contrib/2026.6/json | transitive-build |
| python | pypdf | 6.14.2 | BSD-3-Clause | https://pypi.org/pypi/pypdf/6.14.2/json | direct |
| python | pypdfium2 | 5.12.1 | BSD-3-Clause plus Apache-2.0 and dependency notices including CC-BY-4.0 | https://pypi.org/pypi/pypdfium2/5.12.1/json | direct |
| python | pytest | 9.1.1 | MIT | https://pypi.org/pypi/pytest/9.1.1/json | direct-dev |
| python | python-multipart | 0.0.32 | Apache-2.0 | https://pypi.org/pypi/python-multipart/0.0.32/json | direct |
| python | pywin32-ctypes | 0.2.3 | BSD-3-Clause | https://pypi.org/pypi/pywin32-ctypes/0.2.3/json | transitive |
| python | ruff | 0.15.22 | MIT | https://pypi.org/pypi/ruff/0.15.22/json | direct-dev |
| python | setuptools | 83.0.0 | MIT plus bundled vendor notices | https://pypi.org/pypi/setuptools/83.0.0/json | transitive-build |
| python | sniffio | 1.3.1 | MIT OR Apache-2.0 | https://pypi.org/pypi/sniffio/1.3.1/json | transitive |
| python | starlette | 1.3.1 | BSD-3-Clause | https://pypi.org/pypi/starlette/1.3.1/json | transitive |
| python | tqdm | 4.69.0 | MPL-2.0 AND MIT | https://pypi.org/pypi/tqdm/4.69.0/json | transitive |
| python | truststore | 0.10.4 | MIT | https://pypi.org/pypi/truststore/0.10.4/json | transitive |
| python | types-psutil | 7.2.2.20260518 | Apache-2.0 | https://pypi.org/pypi/types-psutil/7.2.2.20260518/json | direct-dev |
| python | typing-extensions | 4.16.0 | PSF-2.0 | https://pypi.org/pypi/typing-extensions/4.16.0/json | transitive |
| python | typing-inspection | 0.4.2 | MIT | https://pypi.org/pypi/typing-inspection/0.4.2/json | transitive |
| python | tzdata | 2026.3 | Apache-2.0 | https://pypi.org/pypi/tzdata/2026.3/json | direct |
| python | uvicorn | 0.51.0 | BSD-3-Clause | https://pypi.org/pypi/uvicorn/0.51.0/json | direct |

## npm Closure and Notices

The lock contains 166 non-root package entries: 112 non-optional and 54 optional cross-platform entries. All have an exact version, npm registry tarball URL, integrity hash, and license field. License counts are MIT 111, Apache-2.0 28, MPL-2.0 14, ISC 4, BSD-2-Clause 2, BSD-3-Clause 2, MIT-0 2, 0BSD 1, BlueOak-1.0.0 1, and CC0-1.0 1. No blank, GPL, AGPL, or SSPL license entry was observed.

Distribution must retain the PyInstaller exception and COPYING, all pypdfium2/PDFium notices, MPL-2.0 texts and covered-file obligations, Node LICENSE and npm Artistic-2.0 terms, Playwright NOTICE/ThirdPartyNotices, axe third-party license, TypeScript NOTICE, Vite composite LICENSE, Lucide ISC notice, and setuptools vendor notices. CI-01 must regenerate this closure from the production locks and fail on a new unknown or incompatible license.

## Functional Evidence and Residual Boundaries

- Exact CPython 3.14.6 smoke passed for FastAPI multipart/TestClient with warnings as errors, HTTP mock transport, tzdata, Pillow, pypdf, pypdfium2, WinVaultKeyring instantiation, psutil, and OpenAI import without network.
- Exact Node 24.18.0 smoke passed for `npm ci --engine-strict --ignore-scripts`, 13 core imports, a JSDOM role query, and Vite/Vitest/Playwright/tsc CLI versions.
- PyInstaller one-file smoke passed for Uvicorn, pypdfium2/PDFium, and keyring after explicitly collecting the two completion resources. The initial missing-resource failure is a required regression case for DIST-01.
- Playwright browser binaries, full application one-file behavior, Credential Manager set/get/delete, OCI build/run, clean-machine launch, and production dependency/license regeneration remain their later PLAN tasks. This PASS does not claim those outcomes.

The following commands were rerun on 2026-07-21 after review. `$PY314`, `$PY314_SITE`, `$NODE2418`, and `$NPM_WORKSPACE` referred only to disposable directories; no credential was read or stored and the provider call count was zero.

```powershell
$PY314 = "C:\\Users\\22078\\AppData\\Local\\Temp\\projectb-python-3.14.6-embed-8e64553c825748e68498b5012f3c227c\\python.exe"
$PY314_SITE = "C:\\Users\\22078\\AppData\\Local\\Temp\\projectb-python-3.14.6-embed-8e64553c825748e68498b5012f3c227c\\Lib\\site-packages"
$NODE2418 = "C:\\Users\\22078\\AppData\\Local\\Temp\\projectb-node-24.18.0-3a77503f8d2a45dd9851799814318219\\node-v24.18.0-win-x64\\node.exe"
$NODE2418_DIR = Split-Path $NODE2418
$NPM_WORKSPACE = "C:\\Users\\22078\\AppData\\Local\\Temp\\projectb-g02a-npm-node2418-lock-437c55099dde442b96c534c5e5f4233d"
$env:PROJECTB_G02A_SITE_PACKAGES = $PY314_SITE
& $PY314 -W error scripts/evidence/g02a_python_smoke.py
# PYTHON_SMOKE_PASS packages=16 fastapi=health+multipart image=png+jpeg+webp pdf=read+render keyring=instantiate-only provider_network=0

Copy-Item scripts/evidence/g02a_node_smoke.mjs "$NPM_WORKSPACE/g02a_node_smoke.mjs"
$env:PATH = "$NODE2418_DIR;$env:PATH"
& $NODE2418 "$NPM_WORKSPACE/g02a_node_smoke.mjs"
# NODE_SMOKE_PASS modules=13 jsdom_role_query=pass node=v24.18.0

& "$NPM_WORKSPACE/node_modules/.bin/vite.cmd" --version
& "$NPM_WORKSPACE/node_modules/.bin/vitest.cmd" --version
& "$NPM_WORKSPACE/node_modules/.bin/playwright.cmd" --version
& "$NPM_WORKSPACE/node_modules/.bin/tsc.cmd" --version
# vite/8.1.5 and vitest/4.1.10 on node-v24.18.0; Playwright 1.61.1; TypeScript 7.0.2
```

The already-built one-file evidence binaries were also rerun: Uvicorn reported `0.51.0` on CPython `3.14.6`; pypdfium2 reported `5.12.1` with PDFium `152.0.7947.0` extracted under `_MEI*`; and the corrected keyring binary listed `WinVaultKeyring (priority: 5)`. These are component smokes, not a substitute for DIST-01's committed build recipe and clean-machine application test.

Validator regression fixtures also passed: converting both committed lock copies to CRLF still produced `EVIDENCE_VALIDATION_PASS rows=63 explicitly_blocked=2 python_pins=54 npm_packages=166`; changing the documented React version to `19.2.6` failed with `Direct npm evidence row 'frontend-react' does not match react@19.2.7`; and changing one Python license to `UNKNOWN` failed with `Unreviewed Python license 'UNKNOWN' for 'altgraph'`.

## Gate

G-02A evidence is ready for the reviewed task commit. The coordinator marks the task PASS only after recording that commit in `PLAN.md` and `AGENT_LOG.md`. T-01 must consume these exact selections, create production manifests/locks, rerun compatibility and license checks, and record any required change as a reviewed evidence update rather than silently drifting versions.
