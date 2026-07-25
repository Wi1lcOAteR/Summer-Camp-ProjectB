# T-01 Reproducible Project and Test Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the smallest reproducible ProjectB backend/frontend scaffold, a canonical fail-closed test entry, and a strict redacting secret scanner from the exact G-02A dependency closure.

**Architecture:** FastAPI exposes one profile-labelled loopback health contract and React/Vite proves the WebUI test/build toolchain. Focused helper modules make raw lock verification, frontend contract enforcement, secret scanning, gate-state resolution, and command execution independently testable. `python scripts/test_all.py` consumes one formal registry for both `--list` and the final summary, so a deferred owner is either explicitly unavailable, fully active, or a hard failure.

**Tech Stack:** CPython 3.14.6, FastAPI 0.139.2, Pydantic 2.13.4, pytest 9.1.1, Ruff 0.15.22, mypy 2.3.0, Node.js 24.18.0, npm 11.16.0, React and React DOM 19.2.7, Vite 8.1.5, TypeScript 7.0.2, Vitest 4.1.10, Testing Library React 16.3.2, JSDOM 29.1.1, and Windows PowerShell 5.1 or PowerShell 7.

---

## Status, Scope, And Preconditions

This file is a **draft/unreviewed implementation-plan fragment** for Task T-01. It does not authorize implementation and does not claim that any code, test, build, scan, review, or commit below has run.

Dispatch starts only after all course gates are satisfied: G-01 PASS, G-02A PASS, G-03 cold-start validation plus explicit student implementation approval, and G-04 worktree creation/validation. The worker must then invoke `superpowers:using-git-worktrees`, `superpowers:subagent-driven-development` or `superpowers:executing-plans`, `superpowers:test-driven-development`, both review skills, and `superpowers:verification-before-completion` as required by `AGENTS.md`.

The implementation worker must use exact CPython 3.14.6 and Node.js 24.18.0 runtimes. It must not resolve a new dependency version, contact a model/provider, create an Open Design artifact, consume private courseware, create a remote resource, or treat G-02C/D-025 as a T-01 prerequisite.

The two production locks have separate, byte-exact proofs:

- `backend/requirements-windows-x64.lock` is a raw-byte copy of `docs/engineering/locks/python-3.14.6-windows-x64.lock`. The evidence file's current raw-byte SHA-256 is `246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6`.
- `frontend/package-lock.json` is generated into its production path only by `node scripts/materialize_frontend_lock.mjs --write`. `--check` independently rematerializes the complete expected bytes in memory and compares them with the production file. The G-02A source lock's current raw-byte SHA-256 is `071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f`.
- Line-ending normalization is forbidden in both proofs. A CRLF/LF change changes the raw digest and fails.

## File And Responsibility Map

| Path | Responsibility |
| --- | --- |
| `.gitignore` | Exact editable-install metadata ignore increment |
| `backend/pyproject.toml` | Exact Python project pins and pytest/Ruff/mypy configuration |
| `backend/requirements-windows-x64.lock` | Raw-byte copy of the 54-package Windows x64 closure |
| `backend/src/projectb/__init__.py` | Package version export |
| `backend/src/projectb/api/__init__.py` | HTTP package marker |
| `backend/src/projectb/api/app.py` | FastAPI factory, module app, and typed health response |
| `backend/tests/unit/test_health.py` | Health endpoint TDD contract |
| `backend/tests/unit/test_frontend_lock_materializer.py` | Write/check/rematerialization and raw-source mutation tests |
| `backend/tests/unit/test_secret_scanner.py` | UTF-8/UTF-16, malformed encoding, read failure, and redaction tests |
| `backend/tests/unit/test_runner_contracts.py` | No-op package-script and weakened Vitest-config rejection tests |
| `backend/tests/unit/test_runner_locks.py` | Raw-byte hash/copy tests |
| `backend/tests/unit/test_runner_runtime.py` | Exact runtime-version rejection test |
| `backend/tests/unit/test_runner_gates.py` | Deferred, active, and activated-but-missing state tests |
| `backend/tests/unit/test_runner_registry.py` | Complete formal registry ownership test |
| `backend/tests/unit/test_runner_cli.py` | `--list`/summary parity and fail-fast execution tests |
| `frontend/package.json` | Exact npm dependencies and non-no-op commands |
| `frontend/package-lock.json` | Complete materialized G-02A npm closure |
| `frontend/.npmrc` | Exact-engine and no-lifecycle-script install policy |
| `frontend/tsconfig.json` | Strict TypeScript compiler contract |
| `frontend/vitest.contract.json` | Machine-readable exact Vitest environment/include contract |
| `frontend/vite.config.ts` | Vite loopback config wired directly to the test contract |
| `frontend/index.html` | Vite application entry document |
| `frontend/src/app/App.tsx` | Minimal ProjectB application root |
| `frontend/src/app/App.test.tsx` | Frontend rendering TDD contract |
| `frontend/src/main.tsx` | React DOM bootstrap |
| `scripts/frontend_lock_contract.mjs` | Pure raw-hash validation and deterministic lock transformation |
| `scripts/materialize_frontend_lock.mjs` | Argument-safe `--write`/`--check` lock CLI |
| `scripts/secret_scan/Encoding.ps1` | BOM-aware strict UTF-8/UTF-16 decoder |
| `scripts/secret_scan/Inventory.ps1` | Allowed-text inventory and containment checks |
| `scripts/secret_scan/Rules.ps1` | Synthetic and credential-pattern rule IDs without value output |
| `scripts/scan_secrets.ps1` | Fail-closed scanner orchestration and exit-code contract |
| `scripts/projectb_test_runner/contracts.py` | Exact package-script/Vitest/Vite-wiring validation |
| `scripts/projectb_test_runner/locks.py` | Raw lock hash and byte-identity validation |
| `scripts/projectb_test_runner/runtime.py` | Exact Python/Node/npm checks |
| `scripts/projectb_test_runner/gate_model.py` | Gate datatypes and three-state resolution |
| `scripts/projectb_test_runner/gate_run.py` | Inventory, execution, and rendering from one registry |
| `scripts/projectb_test_runner/core_registry.py` | Always-active G-02A/G-02B/T-01 gate definitions |
| `scripts/projectb_test_runner/deferred_registry.py` | G-02C/QA/DIST/CI owner-activation definitions |
| `scripts/projectb_test_runner/registry.py` | Duplicate-checked formal registry composition |
| `scripts/projectb_test_runner/runner.py` | Preflight, `--list`, fail-fast run, and full summary CLI |
| `scripts/projectb_test_runner/__init__.py` | Runner package marker |
| `scripts/test_all.py` | Stable canonical entry shim |

## Formal Gate Registry Contract

Every gate is declared once and both `--list` and execution consume that same ordered tuple. Core gates have no activation paths and missing requirements are immediate errors. Deferred gates use these rules:

1. None of a gate's owner-specific activation paths exists: emit `not_available_until:` followed immediately by the literal owner task ID, such as `not_available_until:G-02C`, in both listing and final summary, and do not run its command.
2. At least one activation path exists: the owner is activated. Every required path must now exist; any missing path is a hard contract error with exit 2, including under `--list`.
3. All required paths exist: run the declared command. A nonzero child result is a gate failure; it is never relabelled unavailable.

| Gate | Owner | Activation contract | Active command |
| --- | --- | --- | --- |
| `evidence-baseline` | `G-02A` | Core prerequisite | `powershell -File scripts/verify_evidence.ps1` |
| `evidence-provider` | `G-02B` | Core prerequisite | same validator with `-RequireProviderReady` |
| `frontend-lock-materialization` | `T-01` | Core | materializer `--check` |
| `backend-tests` / `backend-ruff` / `backend-mypy` | `T-01` | Core | exact Python module commands |
| `frontend-tests` / `frontend-build` | `T-01` | Core | exact npm scripts validated before dispatch |
| `secret-scan` | `T-01` | Core | strict PowerShell scanner |
| `evidence-distribution` | `G-02C` | `docs/engineering/gates/G-02C.ready` | strict distribution evidence validator |
| `browser-e2e` | `QA-01A` | any QA-01A Playwright config/core spec path | `npm --prefix frontend run e2e` |
| `artifact-redaction` | `QA-01C` | any QA-01C matrix/redaction path | artifact redaction verifier |
| `windows-distribution-contract` | `DIST-01` | any DIST-01 packaging/contract path | focused Windows contract test |
| `oci-distribution-contract` | `DIST-02` | any DIST-02 packaging/contract path | focused OCI contract test |
| `license-scan` / `ci-contract` | `CI-01` | any CI-01 script/YAML/contract path | strict license and CI contract checks |

`docs/engineering/gates/G-02C.ready` is not created by T-01. The G-02C owner may create that exact marker only after `-RequireDistributionReady` passes and both G-02C reviews have no unresolved Critical issue. Its premature presence activates the strict gate and therefore fails rather than fabricating readiness.

## Task T-01: Create The Reproducible Project And Test Scaffold

**Dependencies / parallelism:** G-01 PASS, G-02A PASS, G-03 implementation approval, and G-04 are hard prerequisites. This dispatch owns every path in the map and runs serially because manifests, generated locks, scanner helpers, runner registry, and their tests form one reproducibility contract.

**Acceptance:** `create_app("local")` returns a FastAPI app; `GET /api/health` returns status 200 with `{"status":"ok","profile":"local"}`. The materializer compares complete raw output. The scanner exits 0/1/2 for clean/finding/operational-or-encoding-error without printing a matched value. The runner rejects weakened scripts/config, reports every deferred owner truthfully, runs every activated gate, and produces list/summary entries from the same registry.

- [ ] **Step 1: Add the exact editable-install ignore rule**

Append only this block to `.gitignore` after confirming it is absent:

~~~gitignore
# Python editable-install metadata
*.egg-info/
~~~

Run: `rg -n "^\*\.egg-info/$" .gitignore`

Expected: exactly one matching line. G-04 separately owns `.worktrees/`.

- [ ] **Step 2: Create the exact backend manifest**

Create `backend/pyproject.toml`:

~~~toml
[build-system]
requires = ["setuptools==83.0.0"]
build-backend = "setuptools.build_meta"

[project]
name = "projectb"
version = "0.1.0"
description = "Local-first course learning workbench"
requires-python = "==3.14.*"
dependencies = [
    "fastapi==0.139.2",
    "uvicorn==0.51.0",
    "pydantic==2.13.4",
    "httpx==0.28.1",
    "openai==2.46.0",
    "pypdf==6.14.2",
    "pypdfium2==5.12.1",
    "Pillow==12.3.0",
    "keyring==25.7.0",
    "tzdata==2026.3",
    "python-multipart==0.0.32",
    "psutil==7.2.2",
]

[project.optional-dependencies]
test = ["httpx2==2.7.0", "pytest==9.1.1"]
quality = ["ruff==0.15.22", "mypy==2.3.0", "types-psutil==7.2.2.20260518"]
build = ["pyinstaller==6.21.0"]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
addopts = "-W error --strict-config --strict-markers"
testpaths = ["tests"]

[tool.ruff]
target-version = "py314"
line-length = 100
src = ["src"]

[tool.ruff.lint]
select = ["B", "E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.14"
strict = true
warn_unreachable = true
~~~

- [ ] **Step 3: Copy the Python lock as raw bytes**

Run:

~~~powershell
New-Item -ItemType Directory -Force backend | Out-Null
[IO.File]::WriteAllBytes(
    (Join-Path (Resolve-Path .) "backend/requirements-windows-x64.lock"),
    [IO.File]::ReadAllBytes(
        (Resolve-Path "docs/engineering/locks/python-3.14.6-windows-x64.lock")
    )
)
~~~

Expected: the production file is created without text decoding or newline conversion.

- [ ] **Step 4: Prove the Python lock is byte-identical**

Run:

~~~powershell
$source = [IO.File]::ReadAllBytes(
    (Resolve-Path "docs/engineering/locks/python-3.14.6-windows-x64.lock")
)
$target = [IO.File]::ReadAllBytes(
    (Resolve-Path "backend/requirements-windows-x64.lock")
)
$sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    "docs/engineering/locks/python-3.14.6-windows-x64.lock").Hash.ToLowerInvariant()
$targetHash = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    "backend/requirements-windows-x64.lock").Hash.ToLowerInvariant()
if ($sourceHash -ne "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6") {
    throw "G-02A Python lock raw SHA-256 mismatch"
}
if ($sourceHash -ne $targetHash -or
    [Convert]::ToBase64String($source) -ne [Convert]::ToBase64String($target)) {
    throw "Production Python lock is not a raw-byte copy"
}
~~~

Expected: exit 0. No canonical-line-ending hash is used.

- [ ] **Step 5: Create the backend package markers**

Create `backend/src/projectb/__init__.py`:

~~~python
__version__ = "0.1.0"
~~~

Create `backend/src/projectb/api/__init__.py`:

~~~python
"""ProjectB HTTP boundary."""
~~~

- [ ] **Step 6: Install the exact Python closure**

Run:

~~~powershell
python -m pip install --require-hashes -r backend/requirements-windows-x64.lock
python -m pip install --no-deps -e "backend[test,quality,build]"
~~~

Expected: both commands exit 0 without resolving an unpinned dependency.

- [ ] **Step 7: Write the failing health test**

Create `backend/tests/unit/test_health.py`:

~~~python
from fastapi.testclient import TestClient

from projectb.api.app import create_app


def test_health_reports_local_profile() -> None:
    response = TestClient(create_app("local")).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "profile": "local"}
~~~

- [ ] **Step 8: Run the health test and preserve red evidence**

Run: `python -m pytest backend/tests/unit/test_health.py -q`

Expected: FAIL because `projectb.api.app` is absent. A dependency/runtime failure is an environment blocker, not acceptable red evidence.

- [ ] **Step 9: Add the minimal health implementation**

Create `backend/src/projectb/api/app.py`:

~~~python
from fastapi import FastAPI


def create_app(profile: str = "local") -> FastAPI:
    app = FastAPI()

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "profile": profile}

    return app


app = create_app()
~~~

- [ ] **Step 10: Run the focused health test to green**

Run: `python -m pytest backend/tests/unit/test_health.py -q`

Expected: `1 passed` and exit 0.

- [ ] **Step 11: Refactor the health response to an explicit schema**

Replace `backend/src/projectb/api/app.py` with:

~~~python
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    profile: str


def create_app(profile: str = "local") -> FastAPI:
    app = FastAPI()

    @app.get("/api/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", profile=profile)

    return app


app = create_app()
~~~

- [ ] **Step 12: Verify the health refactor**

Run:

~~~powershell
python -m pytest backend/tests/unit/test_health.py -q
python -m ruff check backend/src/projectb/api/app.py backend/tests/unit/test_health.py
python -m mypy backend/src/projectb
~~~

Expected: all three commands exit 0.

- [ ] **Step 13: Create the exact frontend package manifest**

Create `frontend/package.json`:

~~~json
{
  "name": "projectb-web",
  "version": "0.1.0",
  "private": true,
  "license": "UNLICENSED",
  "type": "module",
  "packageManager": "npm@11.16.0",
  "engines": {
    "node": "24.18.0",
    "npm": "11.16.0"
  },
  "scripts": {
    "dev": "vite --host 127.0.0.1",
    "test": "vitest run",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview --host 127.0.0.1"
  },
  "dependencies": {
    "lucide-react": "1.25.0",
    "react": "19.2.7",
    "react-dom": "19.2.7"
  },
  "devDependencies": {
    "@axe-core/playwright": "4.12.1",
    "@playwright/test": "1.61.1",
    "@testing-library/dom": "10.4.1",
    "@testing-library/react": "16.3.2",
    "@testing-library/user-event": "14.6.1",
    "@types/node": "24.13.3",
    "@types/react": "19.2.17",
    "@types/react-dom": "19.2.3",
    "@vitejs/plugin-react": "6.0.3",
    "jsdom": "29.1.1",
    "typescript": "7.0.2",
    "vite": "8.1.5",
    "vitest": "4.1.10"
  }
}
~~~

- [ ] **Step 14: Create the npm install policy**

Create `frontend/.npmrc`:

~~~ini
engine-strict=true
ignore-scripts=true
audit=true
fund=false
save-exact=true
package-lock=true
~~~

- [ ] **Step 15: Write the failing lock-materializer tests**

Create `backend/tests/unit/test_frontend_lock_materializer.py`:

~~~python
import shutil
import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPOSITORY_ROOT / "scripts" / "materialize_frontend_lock.mjs"
SOURCE = REPOSITORY_ROOT / "docs" / "engineering" / "locks" / "frontend-package-lock.json"
MANIFEST = REPOSITORY_ROOT / "frontend" / "package.json"
NODE = shutil.which("node")


def run_materializer(mode: str, source: Path, output: Path) -> subprocess.CompletedProcess[str]:
    assert NODE is not None, "Node.js 24.18.0 is required"
    return subprocess.run(
        [
            NODE,
            str(SCRIPT),
            mode,
            "--source",
            str(source),
            "--manifest",
            str(MANIFEST),
            "--output",
            str(output),
        ],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_write_then_check_compares_complete_materialized_bytes(tmp_path: Path) -> None:
    output = tmp_path / "package-lock.json"

    written = run_materializer("--write", SOURCE, output)
    assert written.returncode == 0, written.stderr
    expected = output.read_bytes()

    checked = run_materializer("--check", SOURCE, output)
    assert checked.returncode == 0, checked.stderr

    output.write_bytes(expected + b" ")
    changed = run_materializer("--check", SOURCE, output)
    assert changed.returncode == 2


def test_changed_source_raw_bytes_are_rejected(tmp_path: Path) -> None:
    changed_source = tmp_path / "source.json"
    changed_source.write_bytes(SOURCE.read_bytes() + b"\n")

    result = run_materializer("--write", changed_source, tmp_path / "output.json")

    assert result.returncode == 2
    assert "raw SHA-256 mismatch" in result.stderr
~~~

- [ ] **Step 16: Run the materializer tests and preserve red evidence**

Run: `python -m pytest backend/tests/unit/test_frontend_lock_materializer.py -q`

Expected: FAIL because both JavaScript modules are absent. A missing Node runtime is an environment blocker.

- [ ] **Step 17: Implement the pure frontend lock contract**

Create `scripts/frontend_lock_contract.mjs`:

~~~javascript
import { createHash } from "node:crypto";
import { TextDecoder } from "node:util";

export const EXPECTED_SOURCE_SHA256 =
  "071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f";
export const EXPECTED_NON_ROOT_PACKAGES = 166;

export function rawSha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function parseStrictJson(bytes, label) {
  let text;
  try {
    text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch (error) {
    throw new Error(`${label} is not strict UTF-8: ${error.message}`);
  }
  return JSON.parse(text);
}

function sortedRecord(record) {
  if (record === undefined || record === null || Array.isArray(record)) {
    throw new Error("dependency record is missing or invalid");
  }
  return Object.fromEntries(
    Object.entries(record).sort(([left], [right]) => left.localeCompare(right)),
  );
}

function assertSameRecord(label, actual, expected) {
  if (JSON.stringify(sortedRecord(actual)) !== JSON.stringify(sortedRecord(expected))) {
    throw new Error(`${label} differs from the G-02A root dependency record`);
  }
}

export function materializeLock(sourceBytes, manifestBytes) {
  if (rawSha256(sourceBytes) !== EXPECTED_SOURCE_SHA256) {
    throw new Error("G-02A frontend lock raw SHA-256 mismatch");
  }

  const sourceLock = parseStrictJson(sourceBytes, "source lock");
  const manifest = parseStrictJson(manifestBytes, "frontend manifest");
  const sourceRoot = sourceLock.packages?.[""];
  if (sourceRoot === undefined) {
    throw new Error("G-02A frontend lock has no root package record");
  }

  assertSameRecord("dependencies", manifest.dependencies, sourceRoot.dependencies);
  assertSameRecord("devDependencies", manifest.devDependencies, sourceRoot.devDependencies);

  const productionLock = structuredClone(sourceLock);
  productionLock.name = manifest.name;
  productionLock.version = manifest.version;
  productionLock.packages[""].name = manifest.name;
  productionLock.packages[""].version = manifest.version;
  productionLock.packages[""].license = manifest.license;

  const nonRootCount = Object.keys(productionLock.packages).filter(
    (key) => key !== "",
  ).length;
  if (nonRootCount !== EXPECTED_NON_ROOT_PACKAGES) {
    throw new Error("G-02A frontend closure package count mismatch");
  }

  const bytes = Buffer.from(`${JSON.stringify(productionLock, null, 2)}\n`, "utf8");
  return { bytes, nonRootCount, sha256: rawSha256(bytes) };
}
~~~

- [ ] **Step 18: Implement the materializer `--write`/`--check` CLI**

Create `scripts/materialize_frontend_lock.mjs`:

~~~javascript
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { materializeLock } from "./frontend_lock_contract.mjs";

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = resolve(scriptDirectory, "..");

function parseArguments(argv) {
  const options = {
    mode: null,
    source: resolve(repositoryRoot, "docs/engineering/locks/frontend-package-lock.json"),
    manifest: resolve(repositoryRoot, "frontend/package.json"),
    output: resolve(repositoryRoot, "frontend/package-lock.json"),
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--write" || argument === "--check") {
      if (options.mode !== null) {
        throw new Error("choose exactly one of --write or --check");
      }
      options.mode = argument;
      continue;
    }
    if (["--source", "--manifest", "--output"].includes(argument)) {
      const value = argv[index + 1];
      if (value === undefined) {
        throw new Error(`${argument} requires a path`);
      }
      options[argument.slice(2)] = resolve(value);
      index += 1;
      continue;
    }
    throw new Error(`unknown argument: ${argument}`);
  }
  if (options.mode === null) {
    throw new Error("choose exactly one of --write or --check");
  }
  return options;
}

function main() {
  const options = parseArguments(process.argv.slice(2));
  const materialized = materializeLock(
    readFileSync(options.source),
    readFileSync(options.manifest),
  );
  if (options.mode === "--write") {
    writeFileSync(options.output, materialized.bytes);
    if (!readFileSync(options.output).equals(materialized.bytes)) {
      throw new Error("written lock differs from materialized bytes");
    }
  } else {
    let actual;
    try {
      actual = readFileSync(options.output);
    } catch {
      throw new Error("materialized output is missing or unreadable");
    }
    if (!actual.equals(materialized.bytes)) {
      throw new Error("materialized output raw bytes differ");
    }
  }
  process.stdout.write(
    `FRONTEND_LOCK_OK mode=${options.mode.slice(2)} packages=${materialized.nonRootCount} sha256=${materialized.sha256}\n`,
  );
}

try {
  main();
} catch (error) {
  process.stderr.write(`FRONTEND_LOCK_ERROR ${error.message}\n`);
  process.exitCode = 2;
}
~~~

- [ ] **Step 19: Run the materializer tests to green**

Run: `python -m pytest backend/tests/unit/test_frontend_lock_materializer.py -q`

Expected: `2 passed` and exit 0.

- [ ] **Step 20: Materialize and independently check the production npm lock**

Run:

~~~powershell
node scripts/materialize_frontend_lock.mjs --write
$before = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    "frontend/package-lock.json").Hash.ToLowerInvariant()
node scripts/materialize_frontend_lock.mjs --check
$after = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    "frontend/package-lock.json").Hash.ToLowerInvariant()
if ($before -ne $after) {
    throw "--check modified the production npm lock"
}
~~~

Expected: both Node commands print `FRONTEND_LOCK_OK`, hashes match, and `--check` performs no write.

- [ ] **Step 21: Install the exact npm closure**

Run: `npm --prefix frontend ci --engine-strict --ignore-scripts`

Expected: exit 0 with no lock mutation. T-01 does not install Playwright browser binaries.

- [ ] **Step 22: Create strict TypeScript configuration**

Create `frontend/tsconfig.json`:

~~~json
{
  "compilerOptions": {
    "target": "ES2023",
    "useDefineForClassFields": true,
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "allowJs": false,
    "skipLibCheck": false,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "types": ["node"]
  },
  "include": ["src", "vite.config.ts"]
}
~~~

- [ ] **Step 23: Create the machine-readable Vitest contract**

Create `frontend/vitest.contract.json`:

~~~json
{
  "environment": "jsdom",
  "globals": true,
  "include": ["src/**/*.test.ts", "src/**/*.test.tsx"]
}
~~~

- [ ] **Step 24: Wire Vite directly to the Vitest contract**

Create `frontend/vite.config.ts`:

~~~typescript
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

import testContract from "./vitest.contract.json";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
  },
  preview: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true,
  },
  test: testContract,
});
~~~

- [ ] **Step 25: Write the failing frontend render test**

Create `frontend/src/app/App.test.tsx`:

~~~tsx
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { App } from "./App";

afterEach(() => {
  cleanup();
});

describe("App", () => {
  it("renders the ProjectB product name", () => {
    render(<App />);
    expect(screen.getByRole("heading", { level: 1, name: "ProjectB" })).toBeTruthy();
  });
});
~~~

- [ ] **Step 26: Run the frontend render test and preserve red evidence**

Run: `npm --prefix frontend run test -- src/app/App.test.tsx`

Expected: FAIL because `frontend/src/app/App.tsx` is absent.

- [ ] **Step 27: Add the minimal React application root**

Create `frontend/src/app/App.tsx`:

~~~tsx
export function App() {
  return (
    <main>
      <h1>ProjectB</h1>
    </main>
  );
}
~~~

- [ ] **Step 28: Run the frontend render test to green**

Run: `npm --prefix frontend run test -- src/app/App.test.tsx`

Expected: one test file and one test pass.

- [ ] **Step 29: Run the frontend build and preserve entry-point red evidence**

Run: `npm --prefix frontend run build`

Expected: FAIL because `frontend/index.html` is absent. A TypeScript/config failure must be fixed before accepting this red result.

- [ ] **Step 30: Create the Vite entry document**

Create `frontend/index.html`:

~~~html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ProjectB</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
~~~

- [ ] **Step 31: Create the React DOM bootstrap**

Create `frontend/src/main.tsx`:

~~~tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "./app/App";

const rootElement = document.getElementById("root");
if (rootElement === null) {
  throw new Error("ProjectB root element is missing");
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
~~~

- [ ] **Step 32: Run the frontend build to green**

Run: `npm --prefix frontend run build`

Expected: TypeScript checking and Vite production build both exit 0.

- [ ] **Step 33: Write the failing secret-scanner encoding and redaction tests**

Create `backend/tests/unit/test_secret_scanner.py`:

~~~python
import shutil
import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCANNER = REPOSITORY_ROOT / "scripts" / "scan_secrets.ps1"
POWERSHELL = shutil.which("powershell") or shutil.which("pwsh")


def run_scanner(root: Path, candidate: Path | None = None) -> subprocess.CompletedProcess[str]:
    assert POWERSHELL is not None, "Windows PowerShell 5.1 or PowerShell 7 is required"
    command = [
        POWERSHELL,
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(SCANNER),
        "-Root",
        str(root),
    ]
    if candidate is not None:
        command.extend(["-CandidatePath", str(candidate)])
    return subprocess.run(command, capture_output=True, text=True, check=False)


def output_of(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout + result.stderr


def synthetic_marker() -> str:
    return "PROJECTB_SYNTHETIC_" + "CREDENTIAL_MARKER"


def test_clean_utf8_text_exits_zero(tmp_path: Path) -> None:
    (tmp_path / "clean.txt").write_text("ordinary project text", encoding="utf-8")

    result = run_scanner(tmp_path)

    assert result.returncode == 0, output_of(result)


def test_utf8_marker_is_redacted_and_exits_one(tmp_path: Path) -> None:
    marker = synthetic_marker()
    (tmp_path / "finding.py").write_text(marker, encoding="utf-8")

    result = run_scanner(tmp_path)

    assert result.returncode == 1
    assert "rule=synthetic-marker" in output_of(result)
    assert marker not in output_of(result)


def test_utf16_marker_is_detected_without_value_output(tmp_path: Path) -> None:
    marker = synthetic_marker()
    (tmp_path / "finding.txt").write_text(marker, encoding="utf-16")

    result = run_scanner(tmp_path)

    assert result.returncode == 1
    assert "rule=synthetic-marker" in output_of(result)
    assert marker not in output_of(result)


def test_malformed_allowed_text_encoding_exits_two(tmp_path: Path) -> None:
    (tmp_path / "malformed.txt").write_bytes(b"\x80")

    result = run_scanner(tmp_path)

    assert result.returncode == 2
    assert "kind=invalid_encoding" in output_of(result)


def test_explicit_unreadable_candidate_exits_two(tmp_path: Path) -> None:
    unreadable = tmp_path / "unreadable.txt"
    unreadable.mkdir()

    result = run_scanner(tmp_path, unreadable)

    assert result.returncode == 2
    assert "kind=read_failure" in output_of(result)
~~~

- [ ] **Step 34: Run the scanner tests and preserve red evidence**

Run: `python -m pytest backend/tests/unit/test_secret_scanner.py -q`

Expected: all five tests FAIL because `scripts/scan_secrets.ps1` and its helpers are absent. A missing PowerShell runtime is an environment blocker.

- [ ] **Step 35: Implement BOM-aware strict text decoding**

Create `scripts/secret_scan/Encoding.ps1`:

~~~powershell
Set-StrictMode -Version Latest

function Read-ProjectTextStrict {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Path)

    [byte[]]$bytes = [IO.File]::ReadAllBytes($Path)
    $offset = 0
    $encoding = $null

    if ($bytes.Length -ge 4 -and
        $bytes[0] -eq 0xFF -and $bytes[1] -eq 0xFE -and
        $bytes[2] -eq 0x00 -and $bytes[3] -eq 0x00) {
        throw [IO.InvalidDataException]::new("unsupported_encoding:utf32le")
    }
    if ($bytes.Length -ge 4 -and
        $bytes[0] -eq 0x00 -and $bytes[1] -eq 0x00 -and
        $bytes[2] -eq 0xFE -and $bytes[3] -eq 0xFF) {
        throw [IO.InvalidDataException]::new("unsupported_encoding:utf32be")
    }
    if ($bytes.Length -ge 3 -and
        $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        $encoding = [Text.UTF8Encoding]::new($false, $true)
        $offset = 3
    } elseif ($bytes.Length -ge 2 -and $bytes[0] -eq 0xFF -and $bytes[1] -eq 0xFE) {
        $encoding = [Text.UnicodeEncoding]::new($false, $false, $true)
        $offset = 2
    } elseif ($bytes.Length -ge 2 -and $bytes[0] -eq 0xFE -and $bytes[1] -eq 0xFF) {
        $encoding = [Text.UnicodeEncoding]::new($true, $false, $true)
        $offset = 2
    } else {
        $encoding = [Text.UTF8Encoding]::new($false, $true)
    }

    try {
        return $encoding.GetString($bytes, $offset, $bytes.Length - $offset)
    } catch [Text.DecoderFallbackException] {
        throw [IO.InvalidDataException]::new("invalid_encoding", $_.Exception)
    }
}
~~~

- [ ] **Step 36: Implement the allowed-text candidate inventory**

Create `scripts/secret_scan/Inventory.ps1`:

~~~powershell
Set-StrictMode -Version Latest

$script:AllowedTextExtensions = [Collections.Generic.HashSet[string]]::new(
    [StringComparer]::OrdinalIgnoreCase
)
@(
    ".cfg", ".css", ".csv", ".html", ".ini", ".js", ".json", ".jsx",
    ".md", ".mjs", ".ps1", ".psm1", ".py", ".toml", ".ts", ".tsx",
    ".txt", ".xml", ".yaml", ".yml"
) | ForEach-Object { [void]$script:AllowedTextExtensions.Add($_) }

$script:AllowedTextNames = [Collections.Generic.HashSet[string]]::new(
    [StringComparer]::OrdinalIgnoreCase
)
@(
    ".dockerignore", ".env.example", ".gitignore", ".npmrc", "Dockerfile",
    "LICENSE", "Makefile", "NOTICE"
) | ForEach-Object { [void]$script:AllowedTextNames.Add($_) }

function Test-ProjectTextPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    $name = [IO.Path]::GetFileName($Path)
    $extension = [IO.Path]::GetExtension($Path)
    return $script:AllowedTextNames.Contains($name) -or
        $script:AllowedTextExtensions.Contains($extension)
}

function Resolve-ContainedCandidate {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$Candidate
    )
    $rootFull = [IO.Path]::GetFullPath($Root).TrimEnd('\', '/')
    $full = if ([IO.Path]::IsPathRooted($Candidate)) {
        [IO.Path]::GetFullPath($Candidate)
    } else {
        [IO.Path]::GetFullPath((Join-Path $rootFull $Candidate))
    }
    $prefix = $rootFull + [IO.Path]::DirectorySeparatorChar
    if ($full -ne $rootFull -and
        -not $full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw [IO.InvalidDataException]::new("candidate_outside_root")
    }
    return $full
}

function Get-GitProjectPaths {
    param([Parameter(Mandatory = $true)][string]$Root)
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = "git"
    $start.Arguments = "-c core.quotepath=false ls-files -z --cached --others --exclude-standard"
    $start.WorkingDirectory = $Root
    $start.UseShellExecute = $false
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $start.CreateNoWindow = $true
    $start.StandardOutputEncoding = [Text.UTF8Encoding]::new($false, $true)
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    if (-not $process.Start()) {
        throw [IO.IOException]::new("git_inventory_start_failed")
    }
    $output = $process.StandardOutput.ReadToEnd()
    [void]$process.StandardError.ReadToEnd()
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) {
        throw [IO.IOException]::new("git_inventory_failed")
    }
    return @($output.Split([char]0, [StringSplitOptions]::RemoveEmptyEntries))
}

function Get-ProjectCandidatePaths {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [string[]]$CandidatePath = @()
    )
    $rootFull = [IO.Path]::GetFullPath($Root)
    $paths = if ($CandidatePath.Count -gt 0) {
        @($CandidatePath | ForEach-Object { Resolve-ContainedCandidate $rootFull $_ })
    } elseif (Test-Path -LiteralPath (Join-Path $rootFull ".git")) {
        @(Get-GitProjectPaths $rootFull | ForEach-Object {
            Resolve-ContainedCandidate $rootFull $_
        })
    } else {
        @(Get-ChildItem -LiteralPath $rootFull -Recurse -Force -File |
            ForEach-Object { $_.FullName })
    }
    return @($paths | Where-Object { Test-ProjectTextPath $_ } | Sort-Object -Unique)
}
~~~

- [ ] **Step 37: Implement redacted secret-rule matching**

Create `scripts/secret_scan/Rules.ps1`:

~~~powershell
Set-StrictMode -Version Latest

function Get-ProjectSecretRules {
    $syntheticMarker = "PROJECTB_SYNTHETIC_" + "CREDENTIAL_MARKER"
    $privateKeyMarker = "-----BEGIN " + "PRIVATE KEY-----"
    return @(
        [pscustomobject]@{
            Id = "synthetic-marker"
            Pattern = [regex]::new([regex]::Escape($syntheticMarker))
        },
        [pscustomobject]@{
            Id = "openai-key-shape"
            Pattern = [regex]::new('(?<![A-Za-z0-9])sk-(?:proj-)?[A-Za-z0-9_-]{20,}')
        },
        [pscustomobject]@{
            Id = "aws-access-key-shape"
            Pattern = [regex]::new('(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![A-Z0-9])')
        },
        [pscustomobject]@{
            Id = "private-key-header"
            Pattern = [regex]::new([regex]::Escape($privateKeyMarker))
        },
        [pscustomobject]@{
            Id = "credential-assignment"
            Pattern = [regex]::new(
                '(?i)(?:api[_-]?key|token|password|secret)\s*[:=]\s*["''][^"'']{8,}'
            )
        }
    )
}

function Find-ProjectSecretRuleIds {
    param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Text)
    return @(Get-ProjectSecretRules | Where-Object { $_.Pattern.IsMatch($Text) } |
        ForEach-Object { $_.Id })
}
~~~

- [ ] **Step 38: Implement fail-closed scanner orchestration**

Create `scripts/scan_secrets.ps1`:

~~~powershell
[CmdletBinding()]
param(
    [string]$Root = (Join-Path $PSScriptRoot ".."),
    [string[]]$CandidatePath = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "secret_scan/Encoding.ps1")
. (Join-Path $PSScriptRoot "secret_scan/Inventory.ps1")
. (Join-Path $PSScriptRoot "secret_scan/Rules.ps1")

function Get-PathFingerprint {
    param([Parameter(Mandatory = $true)][string]$Path)
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes([IO.Path]::GetFullPath($Path))
        return -join ($algorithm.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") })
    } finally {
        $algorithm.Dispose()
    }
}

$hasFinding = $false
$hasError = $false
try {
    $rootFull = [IO.Path]::GetFullPath($Root)
    $paths = @(Get-ProjectCandidatePaths -Root $rootFull -CandidatePath $CandidatePath)
} catch {
    Write-Output "SECRET_SCAN_ERROR kind=inventory_failure"
    exit 2
}

foreach ($path in $paths) {
    $fingerprint = Get-PathFingerprint $path
    try {
        $text = Read-ProjectTextStrict $path
    } catch [IO.InvalidDataException] {
        $kind = if ($_.Exception.Message.StartsWith("invalid_encoding") -or
            $_.Exception.Message.StartsWith("unsupported_encoding")) {
            "invalid_encoding"
        } else {
            "read_failure"
        }
        Write-Output "SECRET_SCAN_ERROR kind=$kind path_sha256=$fingerprint"
        $hasError = $true
        continue
    } catch {
        Write-Output "SECRET_SCAN_ERROR kind=read_failure path_sha256=$fingerprint"
        $hasError = $true
        continue
    }

    foreach ($ruleId in @(Find-ProjectSecretRuleIds -Text $text)) {
        Write-Output "SECRET_SCAN_FINDING rule=$ruleId path_sha256=$fingerprint"
        $hasFinding = $true
    }
}

if ($hasError) {
    exit 2
}
if ($hasFinding) {
    exit 1
}
Write-Output "SECRET_SCAN_OK files=$($paths.Count)"
exit 0
~~~

- [ ] **Step 39: Run all scanner tests to green**

Run: `python -m pytest backend/tests/unit/test_secret_scanner.py -q`

Expected: `5 passed` and exit 0. The two finding tests' combined output contains rule IDs but not the synthetic marker.

- [ ] **Step 40: Run the scanner on the actual worktree**

Run: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_secrets.ps1`

Expected: `SECRET_SCAN_OK` with a positive decimal `files` count and exit 0. Exit 1 stops for a redacted finding; exit 2 stops for inventory, decoding, or read failure.

- [ ] **Step 41: Write failing package-script and Vitest-contract tests**

Create `backend/tests/unit/test_runner_contracts.py`:

~~~python
import json
from pathlib import Path

import pytest

from scripts.projectb_test_runner.contracts import ContractError, verify_frontend_contract

EXACT_SCRIPTS = {
    "dev": "vite --host 127.0.0.1",
    "test": "vitest run",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview --host 127.0.0.1",
}
EXACT_TEST_CONTRACT = {
    "environment": "jsdom",
    "globals": True,
    "include": ["src/**/*.test.ts", "src/**/*.test.tsx"],
}
EXACT_VITE_CONFIG = """import testContract from \"./vitest.contract.json\";
export default defineConfig({ test: testContract });
"""


def write_frontend_contract(root: Path) -> None:
    frontend = root / "frontend"
    frontend.mkdir()
    (frontend / "package.json").write_text(
        json.dumps({"scripts": EXACT_SCRIPTS}), encoding="utf-8"
    )
    (frontend / "vitest.contract.json").write_text(
        json.dumps(EXACT_TEST_CONTRACT), encoding="utf-8"
    )
    (frontend / "vite.config.ts").write_text(EXACT_VITE_CONFIG, encoding="utf-8")


def test_exact_frontend_contract_passes(tmp_path: Path) -> None:
    write_frontend_contract(tmp_path)

    verify_frontend_contract(tmp_path)


def test_no_op_test_script_is_rejected(tmp_path: Path) -> None:
    write_frontend_contract(tmp_path)
    manifest_path = tmp_path / "frontend" / "package.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["scripts"]["test"] = "node -e \"process.exit(0)\""
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(ContractError, match="script:test"):
        verify_frontend_contract(tmp_path)


def test_weakened_vite_wiring_is_rejected(tmp_path: Path) -> None:
    write_frontend_contract(tmp_path)
    (tmp_path / "frontend" / "vite.config.ts").write_text(
        'export default defineConfig({ test: { environment: "node" } });',
        encoding="utf-8",
    )

    with pytest.raises(ContractError, match="Vite test wiring"):
        verify_frontend_contract(tmp_path)


def test_omitting_plain_typescript_tests_is_rejected(tmp_path: Path) -> None:
    write_frontend_contract(tmp_path)
    contract_path = tmp_path / "frontend" / "vitest.contract.json"
    weakened = dict(EXACT_TEST_CONTRACT)
    weakened["include"] = ["src/**/*.test.tsx"]
    contract_path.write_text(json.dumps(weakened), encoding="utf-8")

    with pytest.raises(ContractError, match="Vitest contract"):
        verify_frontend_contract(tmp_path)
~~~

- [ ] **Step 42: Run frontend-contract tests and preserve red evidence**

Run: `python -m pytest backend/tests/unit/test_runner_contracts.py -q`

Expected: FAIL during import because `scripts.projectb_test_runner.contracts` is absent.

- [ ] **Step 43: Create the runner package marker**

Create `scripts/projectb_test_runner/__init__.py`:

~~~python
"""Fail-closed ProjectB test-runner support."""
~~~

- [ ] **Step 44: Implement exact package and Vitest contract validation**

Create `scripts/projectb_test_runner/contracts.py`:

~~~python
import json
import re
from pathlib import Path
from typing import Any


class ContractError(RuntimeError):
    """A checked-in verification contract is missing or weakened."""


EXPECTED_PACKAGE_SCRIPTS = {
    "dev": "vite --host 127.0.0.1",
    "test": "vitest run",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview --host 127.0.0.1",
}
EXPECTED_VITEST_CONTRACT = {
    "environment": "jsdom",
    "globals": True,
    "include": ["src/**/*.test.ts", "src/**/*.test.tsx"],
}


def load_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ContractError(f"invalid JSON contract: {path.name}") from error
    if not isinstance(value, dict):
        raise ContractError(f"JSON contract is not an object: {path.name}")
    return value


def verify_package_scripts(path: Path) -> None:
    manifest = load_json_object(path)
    scripts = manifest.get("scripts")
    if not isinstance(scripts, dict):
        raise ContractError("frontend package scripts are missing")
    for name, expected in EXPECTED_PACKAGE_SCRIPTS.items():
        if scripts.get(name) != expected:
            raise ContractError(f"script:{name} differs from the canonical command")


def verify_vitest_contract(path: Path) -> None:
    if load_json_object(path) != EXPECTED_VITEST_CONTRACT:
        raise ContractError("Vitest contract is missing or weakened")


def verify_vite_wiring(path: Path) -> None:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise ContractError("Vite config is unreadable") from error
    compact = re.sub(r"\s+", "", text)
    required_import = 'importtestContractfrom"./vitest.contract.json";'
    if required_import not in compact:
        raise ContractError("Vite test wiring does not import the exact contract")
    if compact.count("test:") != 1 or compact.count("test:testContract") != 1:
        raise ContractError("Vite test wiring does not use the exact contract once")


def verify_frontend_contract(repository_root: Path) -> None:
    frontend = repository_root / "frontend"
    verify_package_scripts(frontend / "package.json")
    verify_vitest_contract(frontend / "vitest.contract.json")
    verify_vite_wiring(frontend / "vite.config.ts")
~~~

- [ ] **Step 45: Run frontend-contract tests to green**

Run: `python -m pytest backend/tests/unit/test_runner_contracts.py -q`

Expected: `4 passed` and exit 0. The three negative fixtures fail only inside their `pytest.raises` assertions.

- [ ] **Step 46: Write failing raw lock-proof tests**

Create `backend/tests/unit/test_runner_locks.py`:

~~~python
from hashlib import sha256
from pathlib import Path

import pytest

from scripts.projectb_test_runner.contracts import ContractError
from scripts.projectb_test_runner.locks import (
    EXPECTED_NPM_SOURCE_SHA256,
    EXPECTED_PYTHON_LOCK_SHA256,
    assert_raw_copy,
    raw_sha256,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def test_raw_copy_accepts_identical_bytes(tmp_path: Path) -> None:
    source = tmp_path / "source.lock"
    target = tmp_path / "target.lock"
    source.write_bytes(b"one\ntwo\n")
    target.write_bytes(source.read_bytes())

    assert_raw_copy(source, target, sha256(source.read_bytes()).hexdigest())


def test_raw_copy_rejects_line_ending_change(tmp_path: Path) -> None:
    source = tmp_path / "source.lock"
    target = tmp_path / "target.lock"
    source.write_bytes(b"one\ntwo\n")
    target.write_bytes(b"one\r\ntwo\r\n")

    with pytest.raises(ContractError, match="raw bytes"):
        assert_raw_copy(source, target, sha256(source.read_bytes()).hexdigest())


def test_checked_in_evidence_has_expected_raw_hashes() -> None:
    python_lock = REPOSITORY_ROOT / "docs/engineering/locks/python-3.14.6-windows-x64.lock"
    npm_lock = REPOSITORY_ROOT / "docs/engineering/locks/frontend-package-lock.json"

    assert raw_sha256(python_lock) == EXPECTED_PYTHON_LOCK_SHA256
    assert raw_sha256(npm_lock) == EXPECTED_NPM_SOURCE_SHA256
~~~

- [ ] **Step 47: Run lock-proof tests and preserve red evidence**

Run: `python -m pytest backend/tests/unit/test_runner_locks.py -q`

Expected: FAIL during import because `scripts.projectb_test_runner.locks` is absent.

- [ ] **Step 48: Implement raw lock proof**

Create `scripts/projectb_test_runner/locks.py`:

~~~python
from hashlib import sha256
from pathlib import Path

from .contracts import ContractError

EXPECTED_PYTHON_LOCK_SHA256 = (
    "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6"
)
EXPECTED_NPM_SOURCE_SHA256 = (
    "071826d575cbcc472020a7df984e2e8f2410a75c1782550c5ddfeed268af3c2f"
)


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise ContractError(f"required lock is unreadable: {path.name}") from error


def raw_sha256(path: Path) -> str:
    return sha256(read_bytes(path)).hexdigest()


def assert_raw_copy(source: Path, target: Path, expected_source_hash: str) -> None:
    source_bytes = read_bytes(source)
    target_bytes = read_bytes(target)
    if sha256(source_bytes).hexdigest() != expected_source_hash:
        raise ContractError(f"source lock raw SHA-256 mismatch: {source.name}")
    if source_bytes != target_bytes:
        raise ContractError(f"production lock raw bytes differ: {target.name}")


def verify_lock_contract(repository_root: Path) -> None:
    python_source = (
        repository_root / "docs/engineering/locks/python-3.14.6-windows-x64.lock"
    )
    python_target = repository_root / "backend/requirements-windows-x64.lock"
    npm_source = repository_root / "docs/engineering/locks/frontend-package-lock.json"
    npm_target = repository_root / "frontend/package-lock.json"
    materializer = repository_root / "scripts/materialize_frontend_lock.mjs"
    materializer_contract = repository_root / "scripts/frontend_lock_contract.mjs"

    assert_raw_copy(python_source, python_target, EXPECTED_PYTHON_LOCK_SHA256)
    if raw_sha256(npm_source) != EXPECTED_NPM_SOURCE_SHA256:
        raise ContractError("G-02A npm source lock raw SHA-256 mismatch")
    for required in (npm_target, materializer, materializer_contract):
        if not required.is_file():
            raise ContractError(f"required lock artifact is missing: {required.name}")
~~~

- [ ] **Step 49: Run lock-proof tests to green**

Run: `python -m pytest backend/tests/unit/test_runner_locks.py -q`

Expected: `3 passed` and exit 0.

- [ ] **Step 50: Write the failing exact-runtime test**

Create `backend/tests/unit/test_runner_runtime.py`:

~~~python
import pytest

from scripts.projectb_test_runner.contracts import ContractError
from scripts.projectb_test_runner.runtime import assert_exact_version


def test_exact_version_accepts_only_the_declared_value() -> None:
    assert_exact_version("Node.js", "v24.18.0", "v24.18.0")

    with pytest.raises(ContractError, match="Node.js"):
        assert_exact_version("Node.js", "v24.18.1", "v24.18.0")
~~~

- [ ] **Step 51: Run the runtime test and preserve red evidence**

Run: `python -m pytest backend/tests/unit/test_runner_runtime.py -q`

Expected: FAIL during import because `scripts.projectb_test_runner.runtime` is absent.

- [ ] **Step 52: Implement exact Python, Node, and npm runtime checks**

Create `scripts/projectb_test_runner/runtime.py`:

~~~python
import subprocess
import sys
from collections.abc import Sequence

from .contracts import ContractError


def assert_exact_version(label: str, observed: str, expected: str) -> None:
    if observed.strip() != expected:
        raise ContractError(f"{label} must be exactly {expected}; observed {observed.strip()}")


def capture_version(command: Sequence[str]) -> str:
    try:
        result = subprocess.run(
            list(command), capture_output=True, text=True, encoding="utf-8", check=False
        )
    except OSError as error:
        raise ContractError(f"runtime command is unavailable: {command[0]}") from error
    if result.returncode != 0:
        raise ContractError(f"runtime command failed: {command[0]}")
    return result.stdout.strip()


def verify_exact_runtimes() -> None:
    python_version = ".".join(str(part) for part in sys.version_info[:3])
    assert_exact_version("CPython", python_version, "3.14.6")
    assert_exact_version("Node.js", capture_version(("node", "--version")), "v24.18.0")
    assert_exact_version("npm", capture_version(("npm", "--version")), "11.16.0")
~~~

- [ ] **Step 53: Run the runtime test to green**

Run: `python -m pytest backend/tests/unit/test_runner_runtime.py -q`

Expected: `1 passed` and exit 0.

- [ ] **Step 54: Write failing three-state gate tests**

Create `backend/tests/unit/test_runner_gates.py`:

~~~python
import sys
from pathlib import Path

import pytest

from scripts.projectb_test_runner.gate_model import (
    GateContractError,
    GateSpec,
    resolve_gate,
)
from scripts.projectb_test_runner.gate_run import execute_inventory, inventory_registry


def deferred_gate(tmp_path: Path) -> GateSpec:
    sentinel = tmp_path / "ran.txt"
    return GateSpec(
        name="future-check",
        owner="OWNER-01",
        command=(
            sys.executable,
            "-c",
            f"from pathlib import Path; Path({str(sentinel)!r}).write_text('ran')",
        ),
        activation_paths=("owner/ready.marker",),
        required_paths=("owner/ready.marker", "owner/check.py"),
    )


def test_scaffold_gate_is_explicitly_unavailable(tmp_path: Path) -> None:
    gate = deferred_gate(tmp_path)

    resolution = resolve_gate(tmp_path, gate)

    assert resolution.status == "not_available_until:OWNER-01"


def test_activated_gate_with_missing_requirement_is_hard_failure(tmp_path: Path) -> None:
    gate = deferred_gate(tmp_path)
    marker = tmp_path / "owner" / "ready.marker"
    marker.parent.mkdir()
    marker.write_text("active", encoding="utf-8")

    with pytest.raises(GateContractError, match="owner/check.py"):
        resolve_gate(tmp_path, gate)


def test_fully_activated_gate_runs_its_command(tmp_path: Path) -> None:
    gate = deferred_gate(tmp_path)
    owner = tmp_path / "owner"
    owner.mkdir()
    (owner / "ready.marker").write_text("active", encoding="utf-8")
    (owner / "check.py").write_text("# owner command", encoding="utf-8")
    inventory = inventory_registry(tmp_path, (gate,))

    exit_code, results = execute_inventory(tmp_path, inventory)

    assert exit_code == 0
    assert results[0].status == "pass"
    assert (tmp_path / "ran.txt").read_text(encoding="utf-8") == "ran"
~~~

- [ ] **Step 55: Run gate-state tests and preserve red evidence**

Run: `python -m pytest backend/tests/unit/test_runner_gates.py -q`

Expected: FAIL during import because `gate_model.py` and `gate_run.py` are absent.

- [ ] **Step 56: Implement gate datatypes and three-state resolution**

Create `scripts/projectb_test_runner/gate_model.py`:

~~~python
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


class GateContractError(RuntimeError):
    """A gate owner is active but its executable contract is incomplete."""


@dataclass(frozen=True)
class GateSpec:
    name: str
    owner: str
    command: tuple[str, ...]
    required_paths: tuple[str, ...]
    activation_paths: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name or not self.owner or not self.command:
            raise ValueError("gate name, owner, and command are required")
        if not self.required_paths:
            raise ValueError("every gate must declare required paths")


@dataclass(frozen=True)
class GateResolution:
    spec: GateSpec
    status: str

    @property
    def active(self) -> bool:
        return self.status == "active"


def contract_path(repository_root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts:
        raise GateContractError(f"invalid gate path: {relative}")
    return repository_root.joinpath(*path.parts)


def resolve_gate(repository_root: Path, spec: GateSpec) -> GateResolution:
    activation_exists = [
        contract_path(repository_root, relative).exists()
        for relative in spec.activation_paths
    ]
    if spec.activation_paths and not any(activation_exists):
        return GateResolution(spec, f"not_available_until:{spec.owner}")

    missing = [
        relative
        for relative in spec.required_paths
        if not contract_path(repository_root, relative).is_file()
    ]
    if missing:
        joined = ",".join(missing)
        raise GateContractError(
            f"gate={spec.name} owner={spec.owner} activated-but-missing={joined}"
        )
    return GateResolution(spec, "active")
~~~

- [ ] **Step 57: Implement inventory, execution, and shared rendering**

Create `scripts/projectb_test_runner/gate_run.py`:

~~~python
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from .gate_model import GateResolution, GateSpec, resolve_gate

CommandRunner = Callable[[Sequence[str], Path], int]


@dataclass(frozen=True)
class GateResult:
    name: str
    owner: str
    status: str


def inventory_registry(
    repository_root: Path, registry: tuple[GateSpec, ...]
) -> tuple[GateResolution, ...]:
    return tuple(resolve_gate(repository_root, spec) for spec in registry)


def run_subprocess(command: Sequence[str], repository_root: Path) -> int:
    print(f"RUN command={subprocess.list2cmdline(list(command))}")
    try:
        return subprocess.run(list(command), cwd=repository_root, check=False).returncode
    except OSError:
        return 127


def execute_inventory(
    repository_root: Path,
    inventory: tuple[GateResolution, ...],
    command_runner: CommandRunner = run_subprocess,
) -> tuple[int, tuple[GateResult, ...]]:
    results: list[GateResult] = []
    failed_name: str | None = None
    failed_code = 0
    for resolution in inventory:
        spec = resolution.spec
        if not resolution.active:
            results.append(GateResult(spec.name, spec.owner, resolution.status))
            continue
        if failed_name is not None:
            results.append(
                GateResult(spec.name, spec.owner, f"not_run_after_failure:{failed_name}")
            )
            continue
        return_code = command_runner(spec.command, repository_root)
        if return_code == 0:
            results.append(GateResult(spec.name, spec.owner, "pass"))
        else:
            failed_name = spec.name
            failed_code = return_code
            results.append(GateResult(spec.name, spec.owner, f"failed:{return_code}"))
    return failed_code, tuple(results)


def list_lines(inventory: tuple[GateResolution, ...]) -> tuple[str, ...]:
    return tuple(
        f"LIST gate={item.spec.name} owner={item.spec.owner} status={item.status}"
        for item in inventory
    )


def summary_lines(results: tuple[GateResult, ...]) -> tuple[str, ...]:
    return tuple(
        f"SUMMARY gate={item.name} owner={item.owner} status={item.status}"
        for item in results
    )
~~~

- [ ] **Step 58: Run gate-state tests to green**

Run: `python -m pytest backend/tests/unit/test_runner_gates.py -q`

Expected: `3 passed` and exit 0.

- [ ] **Step 59: Write the failing complete-registry ownership test**

Create `backend/tests/unit/test_runner_registry.py`:

~~~python
from scripts.projectb_test_runner.registry import build_registry

EXPECTED_GATE_OWNERS = (
    ("evidence-baseline", "G-02A"),
    ("evidence-provider", "G-02B"),
    ("frontend-lock-materialization", "T-01"),
    ("backend-tests", "T-01"),
    ("backend-ruff", "T-01"),
    ("backend-mypy", "T-01"),
    ("frontend-tests", "T-01"),
    ("frontend-build", "T-01"),
    ("secret-scan", "T-01"),
    ("evidence-distribution", "G-02C"),
    ("browser-e2e", "QA-01A"),
    ("artifact-redaction", "QA-01C"),
    ("windows-distribution-contract", "DIST-01"),
    ("oci-distribution-contract", "DIST-02"),
    ("license-scan", "CI-01"),
    ("ci-contract", "CI-01"),
)


def test_formal_registry_has_every_declared_gate_once() -> None:
    registry = build_registry(python="python", powershell="powershell", npm="npm", node="node")

    observed = tuple((gate.name, gate.owner) for gate in registry)

    assert observed == EXPECTED_GATE_OWNERS
    assert len({gate.name for gate in registry}) == len(registry)
~~~

- [ ] **Step 60: Run the registry test and preserve red evidence**

Run: `python -m pytest backend/tests/unit/test_runner_registry.py -q`

Expected: FAIL during import because the three registry modules are absent.

- [ ] **Step 61: Define the always-active core registry**

Create `scripts/projectb_test_runner/core_registry.py`:

~~~python
from .gate_model import GateSpec


def core_gates(
    *, python: str, powershell: str, npm: str, node: str
) -> tuple[GateSpec, ...]:
    return (
        GateSpec(
            "evidence-baseline",
            "G-02A",
            (
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/verify_evidence.ps1",
            ),
            ("scripts/verify_evidence.ps1",),
        ),
        GateSpec(
            "evidence-provider",
            "G-02B",
            (
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/verify_evidence.ps1",
                "-RequireProviderReady",
            ),
            ("scripts/verify_evidence.ps1",),
        ),
        GateSpec(
            "frontend-lock-materialization",
            "T-01",
            (node, "scripts/materialize_frontend_lock.mjs", "--check"),
            (
                "scripts/frontend_lock_contract.mjs",
                "scripts/materialize_frontend_lock.mjs",
                "docs/engineering/locks/frontend-package-lock.json",
                "frontend/package.json",
                "frontend/package-lock.json",
            ),
        ),
        GateSpec(
            "backend-tests",
            "T-01",
            (python, "-m", "pytest", "backend/tests", "-q"),
            ("backend/pyproject.toml", "backend/tests/unit/test_health.py"),
        ),
        GateSpec(
            "backend-ruff",
            "T-01",
            (python, "-m", "ruff", "check", "backend/src", "backend/tests", "scripts"),
            ("backend/pyproject.toml", "backend/src/projectb/api/app.py"),
        ),
        GateSpec(
            "backend-mypy",
            "T-01",
            (python, "-m", "mypy", "backend/src", "scripts/projectb_test_runner"),
            ("backend/pyproject.toml", "backend/src/projectb/api/app.py"),
        ),
        GateSpec(
            "frontend-tests",
            "T-01",
            (npm, "--prefix", "frontend", "run", "test"),
            (
                "frontend/package.json",
                "frontend/vitest.contract.json",
                "frontend/vite.config.ts",
                "frontend/src/app/App.test.tsx",
            ),
        ),
        GateSpec(
            "frontend-build",
            "T-01",
            (npm, "--prefix", "frontend", "run", "build"),
            ("frontend/package.json", "frontend/tsconfig.json", "frontend/index.html"),
        ),
        GateSpec(
            "secret-scan",
            "T-01",
            (
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/scan_secrets.ps1",
            ),
            (
                "scripts/scan_secrets.ps1",
                "scripts/secret_scan/Encoding.ps1",
                "scripts/secret_scan/Inventory.ps1",
                "scripts/secret_scan/Rules.ps1",
            ),
        ),
    )
~~~

- [ ] **Step 62: Define deferred owner-activation paths and commands**

Create `scripts/projectb_test_runner/deferred_registry.py`:

~~~python
from .gate_model import GateSpec


def deferred_gates(
    *, python: str, powershell: str, npm: str
) -> tuple[GateSpec, ...]:
    qa01a = (
        "frontend/playwright.config.ts",
        "frontend/e2e/core_workflow.spec.ts",
        "frontend/e2e/responsive.spec.ts",
    )
    qa01c = (
        "scripts/check_artifact_redaction.py",
        "backend/tests/integration/test_input_fixture_matrix.py",
        "backend/tests/fixtures/input_matrix/manifest.json",
        "backend/tests/fixtures/input_matrix/build_fixtures.py",
    )
    dist01 = (
        "packaging/windows/build.ps1",
        "packaging/windows/freezer-manifest.json",
        "packaging/windows/smoke_test.ps1",
        "backend/tests/integration/test_windows_distribution_contract.py",
        "docs/engineering/DIST-01_EVIDENCE.md",
    )
    dist02 = (
        "packaging/oci/Dockerfile",
        "packaging/oci/entrypoint.sh",
        "packaging/oci/smoke_test.ps1",
        "backend/tests/integration/test_oci_distribution_contract.py",
        "docs/engineering/DIST-02_EVIDENCE.md",
    )
    ci01 = (
        "scripts/scan_secrets.py",
        "scripts/verify_licenses.py",
        "scripts/verify_ci_contract.py",
        "backend/tests/integration/test_ci_contract.py",
        ".gitlab-ci.yml",
        ".github/workflows/ci.yml",
        "docs/engineering/CI-01_EVIDENCE.md",
    )
    return (
        GateSpec(
            "evidence-distribution",
            "G-02C",
            (
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/verify_evidence.ps1",
                "-RequireDistributionReady",
            ),
            ("docs/engineering/gates/G-02C.ready", "scripts/verify_evidence.ps1"),
            ("docs/engineering/gates/G-02C.ready",),
        ),
        GateSpec(
            "browser-e2e",
            "QA-01A",
            (npm, "--prefix", "frontend", "run", "e2e"),
            ("frontend/package.json", *qa01a),
            qa01a,
        ),
        GateSpec(
            "artifact-redaction",
            "QA-01C",
            (python, "scripts/check_artifact_redaction.py", "artifacts/qa"),
            qa01c,
            qa01c,
        ),
        GateSpec(
            "windows-distribution-contract",
            "DIST-01",
            (
                python,
                "-m",
                "pytest",
                "backend/tests/integration/test_windows_distribution_contract.py",
                "-q",
            ),
            dist01,
            dist01,
        ),
        GateSpec(
            "oci-distribution-contract",
            "DIST-02",
            (
                python,
                "-m",
                "pytest",
                "backend/tests/integration/test_oci_distribution_contract.py",
                "-q",
            ),
            dist02,
            dist02,
        ),
        GateSpec(
            "license-scan",
            "CI-01",
            (python, "scripts/verify_licenses.py", "--strict"),
            ("scripts/verify_licenses.py",),
            ci01,
        ),
        GateSpec(
            "ci-contract",
            "CI-01",
            (python, "scripts/verify_ci_contract.py"),
            ci01,
            ci01,
        ),
    )
~~~

- [ ] **Step 63: Compose and duplicate-check the formal registry**

Create `scripts/projectb_test_runner/registry.py`:

~~~python
import sys

from .core_registry import core_gates
from .deferred_registry import deferred_gates
from .gate_model import GateSpec


def build_registry(
    *,
    python: str = sys.executable,
    powershell: str = "powershell",
    npm: str = "npm",
    node: str = "node",
) -> tuple[GateSpec, ...]:
    registry = core_gates(
        python=python, powershell=powershell, npm=npm, node=node
    ) + deferred_gates(python=python, powershell=powershell, npm=npm)
    names = [gate.name for gate in registry]
    if len(names) != len(set(names)):
        raise RuntimeError("formal gate registry contains a duplicate name")
    return registry
~~~

- [ ] **Step 64: Run the registry test to green**

Run: `python -m pytest backend/tests/unit/test_runner_registry.py -q`

Expected: `1 passed` and exit 0, with exactly 16 ordered gates.

- [ ] **Step 65: Write failing runner CLI parity and fail-fast tests**

Create `backend/tests/unit/test_runner_cli.py`:

~~~python
from pathlib import Path

from scripts.projectb_test_runner.gate_model import GateSpec
from scripts.projectb_test_runner.runner import main


def row_keys(output: str, prefix: str) -> tuple[tuple[str, str], ...]:
    rows: list[tuple[str, str]] = []
    for line in output.splitlines():
        if not line.startswith(prefix):
            continue
        fields = dict(field.split("=", 1) for field in line.split()[1:])
        rows.append((fields["gate"], fields["owner"]))
    return tuple(rows)


def test_list_and_summary_use_the_same_ordered_registry(
    tmp_path: Path, capsys: object
) -> None:
    (tmp_path / "core.txt").write_text("ready", encoding="utf-8")
    registry = (
        GateSpec("core", "T-01", ("core-command",), ("core.txt",)),
        GateSpec(
            "future",
            "OWNER-02",
            ("future-command",),
            ("future/ready", "future/check"),
            ("future/ready",),
        ),
    )
    def no_preflight(root: Path) -> None:
        del root

    assert main(
        ["--list"],
        repository_root=tmp_path,
        registry=registry,
        preflight=no_preflight,
    ) == 0
    listed = capsys.readouterr().out  # type: ignore[attr-defined]

    assert main(
        [],
        repository_root=tmp_path,
        registry=registry,
        preflight=no_preflight,
        command_runner=lambda command, root: 0,
    ) == 0
    summarized = capsys.readouterr().out  # type: ignore[attr-defined]

    assert row_keys(listed, "LIST ") == row_keys(summarized, "SUMMARY ")
    assert "status=not_available_until:OWNER-02" in listed
    assert "status=not_available_until:OWNER-02" in summarized


def test_first_failed_gate_prevents_later_active_command(
    tmp_path: Path, capsys: object
) -> None:
    (tmp_path / "first.txt").write_text("ready", encoding="utf-8")
    (tmp_path / "second.txt").write_text("ready", encoding="utf-8")
    registry = (
        GateSpec("first", "T-01", ("first-command",), ("first.txt",)),
        GateSpec("second", "T-01", ("second-command",), ("second.txt",)),
    )
    called: list[str] = []

    def fail_first(command: tuple[str, ...], root: Path) -> int:
        del root
        called.append(command[0])
        return 7

    code = main(
        [],
        repository_root=tmp_path,
        registry=registry,
        preflight=lambda root: None,
        command_runner=fail_first,
    )
    output = capsys.readouterr().out  # type: ignore[attr-defined]

    assert code == 7
    assert called == ["first-command"]
    assert "gate=first owner=T-01 status=failed:7" in output
    assert "gate=second owner=T-01 status=not_run_after_failure:first" in output
~~~

- [ ] **Step 66: Run runner CLI tests and preserve red evidence**

Run: `python -m pytest backend/tests/unit/test_runner_cli.py -q`

Expected: FAIL during import because `scripts.projectb_test_runner.runner` is absent.

- [ ] **Step 67: Implement preflight, listing, execution, and full summary**

Create `scripts/projectb_test_runner/runner.py`:

~~~python
import argparse
from collections.abc import Callable, Sequence
from pathlib import Path

from .contracts import ContractError, verify_frontend_contract
from .gate_model import GateContractError, GateSpec
from .gate_run import (
    CommandRunner,
    execute_inventory,
    inventory_registry,
    list_lines,
    run_subprocess,
    summary_lines,
)
from .locks import verify_lock_contract
from .registry import build_registry
from .runtime import verify_exact_runtimes

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
Preflight = Callable[[Path], None]


def perform_preflight(repository_root: Path) -> None:
    verify_exact_runtimes()
    verify_frontend_contract(repository_root)
    verify_lock_contract(repository_root)


def parse_arguments(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the canonical ProjectB gates")
    parser.add_argument(
        "--list", action="store_true", help="list resolved gates without running commands"
    )
    return parser.parse_args(argv)


def main(
    argv: Sequence[str] | None = None,
    *,
    repository_root: Path = REPOSITORY_ROOT,
    registry: tuple[GateSpec, ...] | None = None,
    preflight: Preflight = perform_preflight,
    command_runner: CommandRunner = run_subprocess,
) -> int:
    arguments = parse_arguments(argv)
    selected_registry = build_registry() if registry is None else registry
    try:
        preflight(repository_root)
        inventory = inventory_registry(repository_root, selected_registry)
    except (ContractError, GateContractError, OSError, ValueError) as error:
        print(f"TEST_ALL_CONTRACT_ERROR {error}")
        return 2

    if arguments.list:
        for line in list_lines(inventory):
            print(line)
        return 0

    exit_code, results = execute_inventory(
        repository_root, inventory, command_runner=command_runner
    )
    for line in summary_lines(results):
        print(line)
    if exit_code != 0:
        print(f"TEST_ALL_FAIL code={exit_code}")
        return exit_code
    print("TEST_ALL_PASS")
    return 0
~~~

- [ ] **Step 68: Create the stable canonical entry shim**

Create `scripts/test_all.py`:

~~~python
import sys
from importlib import import_module
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

main = import_module("scripts.projectb_test_runner.runner").main


if __name__ == "__main__":
    raise SystemExit(main())
~~~

- [ ] **Step 69: Run runner CLI tests to green**

Run: `python -m pytest backend/tests/unit/test_runner_cli.py -q`

Expected: `2 passed` and exit 0. The fail-fast fixture records only the first command while still emitting both summary rows.

- [ ] **Step 70: Run all focused runner tests together**

Run:

~~~powershell
python -m pytest `
    backend/tests/unit/test_runner_contracts.py `
    backend/tests/unit/test_runner_locks.py `
    backend/tests/unit/test_runner_runtime.py `
    backend/tests/unit/test_runner_gates.py `
    backend/tests/unit/test_runner_registry.py `
    backend/tests/unit/test_runner_cli.py -q
~~~

Expected: `14 passed` and exit 0: 4 contract, 3 lock, 1 runtime, 3 gate-state, 1 registry, and 2 CLI tests.

- [ ] **Step 71: Verify the actual registry listing before command execution**

Run: `python scripts/test_all.py --list`

Expected: exactly 16 `LIST` rows in the registry order. The nine G-02A/G-02B/T-01 rows are `active`; every absent deferred owner is reported with its literal task ID, for example `not_available_until:QA-01A`. If any future-owner path already exists, that gate is active only when all its required paths exist; a partial owner exits 2.

- [ ] **Step 72: Run the complete canonical T-01 regression entry**

Run: `python scripts/test_all.py`

Expected: all active gates pass, all truly absent owner gates retain their exact unavailable state, all 16 gates appear once in `SUMMARY`, and the final line is `TEST_ALL_PASS`. A nonzero active child code is propagated and later active commands are not run.

- [ ] **Step 73: Reprove generated locks without relying on Git tracking state**

Run:

~~~powershell
$pythonSource = [IO.File]::ReadAllBytes(
    (Resolve-Path "docs/engineering/locks/python-3.14.6-windows-x64.lock")
)
$pythonTarget = [IO.File]::ReadAllBytes(
    (Resolve-Path "backend/requirements-windows-x64.lock")
)
if ([Convert]::ToBase64String($pythonSource) -ne
    [Convert]::ToBase64String($pythonTarget)) {
    throw "Python lock raw bytes changed"
}
$npmBefore = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    "frontend/package-lock.json").Hash.ToLowerInvariant()
node scripts/materialize_frontend_lock.mjs --check
$npmAfter = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    "frontend/package-lock.json").Hash.ToLowerInvariant()
if ($npmBefore -ne $npmAfter) {
    throw "npm lock check modified the file"
}
~~~

Expected: exit 0. This proof works for untracked, staged, or committed locks and never uses `git diff` as a generation check.

- [ ] **Step 74: Dispatch the independent SPEC-compliance review**

Use `superpowers:requesting-code-review` with a fresh reviewer that did not implement T-01. Give it only `SPEC.md`, the formal T-01 section of `PLAN.md`, this T-01 fragment, and the T-01 working-tree diff. Use this exact review request:

~~~text
Review T-01 for SPEC and PLAN compliance only. Check AC-10, the local/demo profile boundary, exact G-02A dependency consumption, one-command verification, raw lock reproducibility, the formal deferred-gate states, scanner 0/1/2 semantics, and every T-01 acceptance statement. Report findings first with Critical/Major/Minor severity and exact file:line references. Do not edit files. A missing executed test or ambiguous owner activation is a finding, never an inferred pass.
~~~

Expected: a written finding list and a canonical reviewer identity. Record that identity in `PROJECTB_SPEC_REVIEW_ID`. Any Critical finding stops the task and returns to the relevant red-green step.

- [ ] **Step 75: Resolve and reverify every SPEC-review finding**

For each accepted finding, add or strengthen the smallest failing focused test, run it red for the stated reason, make the minimum correction, rerun it green, then rerun Steps 70–73. Do not weaken, skip, or delete an assertion. Re-dispatch the same reviewer only to verify its own findings are resolved.

Expected: the SPEC reviewer reports no unresolved Critical issue and every correction has fresh red/green evidence.

- [ ] **Step 76: Dispatch a different quality/security/test/license review**

Use `superpowers:requesting-code-review` with a second fresh reviewer. It must differ from both the worker and the Step 74 reviewer. Give it the same scoped files plus the recorded red/green outputs. Use this exact request:

~~~text
Review T-01 for correctness, maintainability, security, test quality, reproducibility, and license discipline. Focus on raw-byte lock comparison, complete npm rematerialization, no-op script/config bypasses, UTF-8/UTF-16 strict decoding, path containment, scanner redaction, gate activation races, fail-fast propagation, list/summary parity, command quoting, and exact dependency/license evidence. Report findings first with Critical/Major/Minor severity and exact file:line references. Do not edit files and do not reuse the SPEC review as evidence.
~~~

Expected: a written finding list and a distinct canonical identity in `PROJECTB_QUALITY_REVIEW_ID`. Resolve accepted findings through the same red-green-reverify loop. Any unresolved Critical issue blocks staging.

- [ ] **Step 77: Run the final focused and full local verification after reviews**

Run:

~~~powershell
python -m pytest backend/tests/unit/test_health.py -q
python -m pytest backend/tests/unit/test_frontend_lock_materializer.py -q
python -m pytest backend/tests/unit/test_secret_scanner.py -q
python -m pytest `
    backend/tests/unit/test_runner_contracts.py `
    backend/tests/unit/test_runner_locks.py `
    backend/tests/unit/test_runner_runtime.py `
    backend/tests/unit/test_runner_gates.py `
    backend/tests/unit/test_runner_registry.py `
    backend/tests/unit/test_runner_cli.py -q
npm --prefix frontend run test -- src/app/App.test.tsx
npm --prefix frontend run build
python scripts/test_all.py --list
python scripts/test_all.py
~~~

Expected: every command exits 0; the runner suite reports 14 passes; the registry list and summary each cover the same 16 gates; no absent future-owner gate is labelled PASS.

- [ ] **Step 78: Run the final credential scan**

Run: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_secrets.ps1`

Expected: `SECRET_SCAN_OK` and exit 0. A finding or operational/encoding error stops staging; never print or copy a matched value into review evidence.

- [ ] **Step 79: Stage exactly the T-01-owned paths**

Run:

~~~powershell
$paths = @(
    ".gitignore",
    "backend/pyproject.toml",
    "backend/requirements-windows-x64.lock",
    "backend/src/projectb/__init__.py",
    "backend/src/projectb/api/__init__.py",
    "backend/src/projectb/api/app.py",
    "backend/tests/unit/test_health.py",
    "backend/tests/unit/test_frontend_lock_materializer.py",
    "backend/tests/unit/test_secret_scanner.py",
    "backend/tests/unit/test_runner_contracts.py",
    "backend/tests/unit/test_runner_locks.py",
    "backend/tests/unit/test_runner_runtime.py",
    "backend/tests/unit/test_runner_gates.py",
    "backend/tests/unit/test_runner_registry.py",
    "backend/tests/unit/test_runner_cli.py",
    "frontend/package.json",
    "frontend/package-lock.json",
    "frontend/.npmrc",
    "frontend/tsconfig.json",
    "frontend/vitest.contract.json",
    "frontend/vite.config.ts",
    "frontend/index.html",
    "frontend/src/app/App.tsx",
    "frontend/src/app/App.test.tsx",
    "frontend/src/main.tsx",
    "scripts/frontend_lock_contract.mjs",
    "scripts/materialize_frontend_lock.mjs",
    "scripts/secret_scan/Encoding.ps1",
    "scripts/secret_scan/Inventory.ps1",
    "scripts/secret_scan/Rules.ps1",
    "scripts/scan_secrets.ps1",
    "scripts/projectb_test_runner/__init__.py",
    "scripts/projectb_test_runner/contracts.py",
    "scripts/projectb_test_runner/locks.py",
    "scripts/projectb_test_runner/runtime.py",
    "scripts/projectb_test_runner/gate_model.py",
    "scripts/projectb_test_runner/gate_run.py",
    "scripts/projectb_test_runner/core_registry.py",
    "scripts/projectb_test_runner/deferred_registry.py",
    "scripts/projectb_test_runner/registry.py",
    "scripts/projectb_test_runner/runner.py",
    "scripts/test_all.py"
)
git add -- $paths
~~~

Expected: exactly 42 T-01-owned paths are staged. No process document, evidence ledger, user file, generated `dist/`, `node_modules/`, or private material is staged.

- [ ] **Step 80: Verify the staged set and whitespace exactly**

Run:

~~~powershell
git diff --cached --check
$expected = @(
    ".gitignore",
    "backend/pyproject.toml",
    "backend/requirements-windows-x64.lock",
    "backend/src/projectb/__init__.py",
    "backend/src/projectb/api/__init__.py",
    "backend/src/projectb/api/app.py",
    "backend/tests/unit/test_health.py",
    "backend/tests/unit/test_frontend_lock_materializer.py",
    "backend/tests/unit/test_secret_scanner.py",
    "backend/tests/unit/test_runner_contracts.py",
    "backend/tests/unit/test_runner_gates.py",
    "backend/tests/unit/test_runner_locks.py",
    "backend/tests/unit/test_runner_registry.py",
    "backend/tests/unit/test_runner_runtime.py",
    "backend/tests/unit/test_runner_cli.py",
    "frontend/.npmrc",
    "frontend/index.html",
    "frontend/package-lock.json",
    "frontend/package.json",
    "frontend/src/app/App.test.tsx",
    "frontend/src/app/App.tsx",
    "frontend/src/main.tsx",
    "frontend/tsconfig.json",
    "frontend/vite.config.ts",
    "frontend/vitest.contract.json",
    "scripts/frontend_lock_contract.mjs",
    "scripts/materialize_frontend_lock.mjs",
    "scripts/projectb_test_runner/__init__.py",
    "scripts/projectb_test_runner/contracts.py",
    "scripts/projectb_test_runner/core_registry.py",
    "scripts/projectb_test_runner/deferred_registry.py",
    "scripts/projectb_test_runner/gate_model.py",
    "scripts/projectb_test_runner/gate_run.py",
    "scripts/projectb_test_runner/locks.py",
    "scripts/projectb_test_runner/registry.py",
    "scripts/projectb_test_runner/runner.py",
    "scripts/projectb_test_runner/runtime.py",
    "scripts/scan_secrets.ps1",
    "scripts/secret_scan/Encoding.ps1",
    "scripts/secret_scan/Inventory.ps1",
    "scripts/secret_scan/Rules.ps1",
    "scripts/test_all.py"
) | Sort-Object
$staged = @(git diff --cached --name-only) | Sort-Object
if (($expected -join "`n") -ne ($staged -join "`n")) {
    throw "Staged path set differs from the exact T-01 contract"
}
~~~

Expected: `git diff --cached --check` exits 0 and the exact sorted 42-path comparison succeeds.

- [ ] **Step 81: Commit with the runtime-provided worker identity**

Run:

~~~powershell
if ([string]::IsNullOrWhiteSpace($env:PROJECTB_AGENT_ID)) {
    throw "PROJECTB_AGENT_ID must contain the canonical T-01 worker identity"
}
if ([string]::IsNullOrWhiteSpace($env:PROJECTB_SPEC_REVIEW_ID) -or
    [string]::IsNullOrWhiteSpace($env:PROJECTB_QUALITY_REVIEW_ID)) {
    throw "Both canonical review identities are required"
}
if ($env:PROJECTB_AGENT_ID -eq $env:PROJECTB_SPEC_REVIEW_ID -or
    $env:PROJECTB_AGENT_ID -eq $env:PROJECTB_QUALITY_REVIEW_ID -or
    $env:PROJECTB_SPEC_REVIEW_ID -eq $env:PROJECTB_QUALITY_REVIEW_ID) {
    throw "Worker, SPEC reviewer, and quality reviewer identities must be distinct"
}
git commit -m "build(T-01): add reproducible app and test scaffold [agent: $env:PROJECTB_AGENT_ID]"
git rev-parse HEAD
~~~

Expected: one small T-01 commit is created and its actual hash is printed. No push, PR/MR, release, or deployment occurs.

- [ ] **Step 82: Emit the coordinator evidence handoff**

Run:

~~~powershell
$record = [ordered]@{
    task = "T-01"
    commit = (git rev-parse HEAD).Trim()
    worker = $env:PROJECTB_AGENT_ID
    spec_reviewer = $env:PROJECTB_SPEC_REVIEW_ID
    quality_reviewer = $env:PROJECTB_QUALITY_REVIEW_ID
    focused_tests = "executed in Step 77"
    canonical_entry = "executed in Step 77"
    credential_scan = "executed in Step 78"
    remote_actions = "not executed"
}
$record | ConvertTo-Json -Compress
~~~

Expected: one JSON object containing only observed identities/hash/statuses. The coordinator uses this output to update `PLAN.md` and `AGENT_LOG.md` immediately after the task; the worker does not edit those shared files from the T-01 worktree.

## Completion Standard

T-01 is complete only when every checkbox has current evidence, the exact raw-lock and complete rematerialization proofs pass, scanner error/finding values remain redacted, all 16 registry entries appear consistently, both distinct reviews have no unresolved Critical issue, the 42-path commit exists, and the coordinator has recorded its actual hash and evidence. Until then this fragment remains draft/unreviewed and no implementation result is claimed.
