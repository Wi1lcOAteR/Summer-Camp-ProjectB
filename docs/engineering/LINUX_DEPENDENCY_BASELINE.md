# Linux Dependency and OCI Base Baseline

Status: **VERIFIED STAGE-B INPUT / PRODUCT IMAGE NOT YET BUILT**

Frozen on `2026-07-25` (Asia/Shanghai). This file is deliberately separate from
`DEPENDENCY_BASELINE.md`: the standard evidence validator must continue to report
`rows=63 explicitly_blocked=2`, while this ledger closes the Linux/amd64 planning
input needed by CI and the public mock image.

## Target Closures

| Target | Runtime and resolver target | Direct input | Canonical SHA-256 | Fully hashed lock | Canonical SHA-256 | Packages | Install contract |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| CI | CPython `3.14.6`; `x86_64-manylinux_2_28` | `locks/python-3.14.6-linux-amd64-ci.in` | `16d3c9b0373e7fa9d98e3764490b64e5abc3ba461bb0756089b211f4a71cac1d` | `locks/python-3.14.6-linux-amd64-ci.lock` | `d24ddf3789ea9f276ee6ba4062634fef3c85c4572a7eb62096cbd570bfb0fc35` | 41 | `uv pip sync --python .venv/bin/python --require-hashes --only-binary :all: requirements.linux-ci.lock` |
| public mock demo | CPython `3.14.6`; `x86_64-manylinux_2_28` | `locks/python-3.14.6-linux-amd64-demo.in` | `2e479a450191ebb8ad1db4d35f1b9aae811b050c74e4b0e3e18188d990468456` | `locks/python-3.14.6-linux-amd64-demo.lock` | `09ce57726c02a090f134d4f2c25f2681dce58ebf2d8425502129d42ac2be34f7` | 14 | `python -m pip install --no-deps --require-hashes --only-binary=:all: -r requirements.linux-demo.lock` |

The locks were resolved with `uv 0.11.14` (`3fdfdc7d4`, Windows x64) and
`uv pip compile`, `--python-version 3.14`,
`--python-platform x86_64-manylinux_2_28`, `--only-binary :all:`, and the reviewed
Windows closure as an exact-version constraint. The active implementation plan
must copy these reviewed inputs under the install-contract names without changing
their canonical content.

## License Closure

The CI lock's 41 packages and the demo lock's 14 packages introduce no new Python
package/version pair. Every pair is present in the reviewed 54-row Python closure
in `DEPENDENCY_BASELINE.md`, which supplies its exact source URL and SPDX-style
license authority. `scripts/verify_linux_dependency_evidence.ps1` fails closed if
a Linux pair is absent, has a different version, lacks hashes, or the frozen files
change. This indirection avoids duplicating the full license table while preserving
mechanical traceability.

## OCI Base Ledger

| Item | Frozen value | License/authority | Evidence and remaining proof |
| --- | --- | --- | --- |
| multi-platform index | `python:3.14.6-slim-bookworm@sha256:86f975aca15cf04a40b399eebede9aea7c82eae084d1f1a0a6ef6bcaae871a30` | Docker Official Images metadata; upstream image assembly sources | Pinned first-party repo-info evidence is recorded in `DISTRIBUTION_EVIDENCE.md`. |
| linux/amd64 manifest | `sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb` | CPython under `PSF-2.0`; Debian components retain package-specific licenses | The manifest is 44,765,139 compressed bytes according to the pinned official metadata. |
| frontend builder | `node:24.18.0-bookworm-slim@sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6` for `linux/amd64` | Node.js `MIT` plus bundled notices; Debian components retain package-specific licenses | Source target is the Docker Library repo-info snapshot at commit `99919ada7d519a93bfafcd36ddab30df211ecdb9`; a live recheck was unavailable on 2026-07-25, so DIST-02 must re-resolve the immutable manifest before build. |
| image license closure | same immutable amd64 manifest | `PSF-2.0` plus Debian package-specific copyright files | `DIST-02` must generate an SPDX/CycloneDX SBOM, retain Python/Debian notices, scan licenses, and inspect the final image before distribution can be called verified. |

The base-image digest and license authorities are frozen planning inputs. They are
not a claim that a ProjectB image has been built. A direct anonymous registry
recheck on `2026-07-25` failed during TLS receive in this environment, so no layer
or runtime evidence was invented; the existing commit-pinned Docker Library
repo-info snapshot remains the authority until `DIST-02` performs the real pull,
build, SBOM, notice, and smoke checks.

## Reproduction

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_linux_dependency_evidence.ps1
```

Expected Stage-B result:

```text
LINUX_EVIDENCE_PASS ci_packages=41 demo_packages=14 license_rows=41
```

This verifier is additive. Do not fold these rows into
`scripts/verify_evidence.ps1`; its established standard result remains
`rows=63 explicitly_blocked=2`.
