from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OCI = ROOT / "packaging" / "oci"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_oci_files_and_evidence_exist() -> None:
    for path in (
        OCI / "Dockerfile",
        OCI / "Dockerfile.dockerignore",
        OCI / "entrypoint.sh",
        OCI / ".dockerignore",
        OCI / "smoke_test.ps1",
        OCI / "sbom.spdx.json",
        OCI / "THIRD_PARTY_NOTICES.md",
        ROOT / "backend/tests/distribution/test_oci_contract.py",
        ROOT / "docs/engineering/DIST-02_EVIDENCE.md",
    ):
        assert path.is_file(), path


def test_dockerfile_is_digest_pinned_and_uses_demo_lock() -> None:
    text = read_text(OCI / "Dockerfile")
    assert "node:24.18.0-bookworm-slim@sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6" in text
    assert "python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb" in text
    assert "requirements.linux-demo.lock" in text
    assert "requirements-windows-x64.lock" not in text
    assert re.search(r"pip\s+install[^\n]*--require-hashes", text)
    assert "pip install -r" not in text
    for source in re.findall(r"^FROM\s+(?:--platform=[^\s]+\s+)?([^\s]+)", text, flags=re.MULTILINE):
        assert re.search(r"@sha256:[0-9a-f]{64}$", source), source
    assert "ADD http" not in text.lower()
    assert "ARG API_KEY" not in text and "ARG TOKEN" not in text


def test_runtime_is_non_root_demo_only_and_health_checked() -> None:
    dockerfile = read_text(OCI / "Dockerfile")
    entrypoint = read_text(OCI / "entrypoint.sh")
    assert re.search(r"USER\s+10001:10001", dockerfile)
    assert "HEALTHCHECK" in dockerfile
    for literal in ("PROJECTB_PROFILE=demo", "PROJECTB_PROVIDER_ADAPTER=deterministic.mock", "PROJECTB_EGRESS_POLICY=deny", "PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring"):
        assert literal in dockerfile
        assert literal.split("=", 1)[0] in entrypoint
    assert "socket.getaddrinfo" in dockerfile and "socket.connect" in dockerfile
    assert "exec" in entrypoint
    assert "set -eu" in entrypoint or "set -euo pipefail" in entrypoint
    for literal in (
        '"$#" -eq 0',
        '"$(id -u)" = "10001"',
        '"$(id -g)" = "10001"',
        '"$PYTHON_KEYRING_BACKEND" = "keyring.backends.null.Keyring"',
        '"$PROJECTB_DATA_ROOT" = "/tmp/projectb-demo"',
        '"${PROJECTB_BIND_HOST:-}" = "0.0.0.0"',
        '"$PROJECTB_PORT" = "7860"',
    ):
        assert literal in entrypoint


def test_context_and_evidence_are_closed() -> None:
    context = read_text(OCI / ".dockerignore")
    assert read_text(OCI / "Dockerfile.dockerignore") == context
    for pattern in (".env", ".env.*", "**/*.sqlite*", "**/*.db", "**/*.pem", "**/*.key", "**/__pycache__", "**/*.py[cod]", "**/.mypy_cache", "**/.pytest_cache", "frontend/node_modules", "backend/tests"):
        assert pattern in context
    sbom = json.loads(read_text(OCI / "sbom.spdx.json"))
    assert sbom["spdxVersion"] == "SPDX-2.3"
    assert sbom["name"] == "ProjectB-demo-oci"
    packages = {package["SPDXID"]: package for package in sbom["packages"]}
    assert len(packages) >= 180
    assert "SPDXRef-Package-NpmLock" not in packages
    assert "SPDXRef-Package-Debian" not in packages
    relationships = {(row["spdxElementId"], row["relationshipType"], row["relatedSpdxElement"]) for row in sbom["relationships"]}
    assert ("SPDXRef-DOCUMENT", "DESCRIBES", "SPDXRef-Package-ProjectB") in relationships
    assert any(row["relationshipType"] == "DEPENDS_ON" and row["spdxElementId"] == "SPDXRef-Package-ProjectB" for row in sbom["relationships"])
    assert any(package["name"] == "debian-base-bookworm" for package in packages.values())
    assert all(package["licenseDeclared"] != "DFSG-compiled" for package in packages.values())
    dockerfile = read_text(OCI / "Dockerfile")
    assert "dpkg-query" in dockerfile
    assert "frontend-package-lock.json" in dockerfile
    evidence = read_text(ROOT / "docs/engineering/DIST-02_EVIDENCE.md")
    assert '"publicUrl": {"status": "not_executed"}' in evidence
    assert '"deployment": {"status": "not_executed"}' in evidence
    assert "api_key" not in evidence.lower()


def test_both_push_ci_files_contain_oci_contract() -> None:
    github = read_text(ROOT / ".github/workflows/ci.yml")
    gitlab = read_text(ROOT / ".gitlab-ci.yml")
    for text in (github, gitlab):
        assert "docker build --platform linux/amd64" in text
        assert "packaging/oci/Dockerfile" in text
        assert "projectb-docker-linux-amd64" in text or "ubuntu-24.04" in text
        assert "sbom.spdx.json" in text and "THIRD_PARTY_NOTICES.md" in text
        assert "docker push" not in text
    assert "docker buildx version" in gitlab
    assert "name=seccomp" in gitlab
    assert "/host/etc/shadow" in gitlab
    assert "PROJECTB_RUNNER_PRIVILEGED" in gitlab
    assert "PROJECTB_RUNNER_HOST_MOUNTS" in gitlab
    assert 'CONTAINER_NAME="projectb-demo-ci-${CI_JOB_ID}"' in gitlab
    assert 'HOST_PORT="$((20000 + CI_JOB_ID % 10000))"' in gitlab
    assert 'IMAGE_TAG="projectb-demo:${CI_COMMIT_SHA}-${CI_JOB_ID}"' in gitlab
    assert "--name projectb-demo-ci " not in gitlab


def test_smoke_inspects_image_runtime_and_exact_forbidden_routes() -> None:
    smoke = read_text(OCI / "smoke_test.ps1")
    for literal in (
        '"image", "inspect"',
        "$Image",
        "ReadonlyRootfs",
        "Tmpfs",
        "sbom.spdx.json",
        "THIRD_PARTY_NOTICES.md",
        "/api/courses/probe/materials/import",
        "/api/providers/execute",
        "/api/credentials/provider",
    ):
        assert literal in smoke
    assert "@(404, 405, 422)" not in smoke
    assert "oci_restart_not_running" in smoke
    assert "OCI_EGRESS_DENIED" in smoke
    assert "@(& docker exec" not in smoke


def test_demo_import_graph_does_not_require_local_only_packages() -> None:
    code = f"""
import builtins
import sys
sys.path.insert(0, {str(ROOT / 'backend')!r})
blocked = {{'httpx', 'multipart', 'openai', 'psutil', 'pypdf', 'pypdfium2'}}
original = builtins.__import__
def guarded(name, globals=None, locals=None, fromlist=(), level=0):
    if name.split('.', 1)[0] in blocked:
        raise ModuleNotFoundError(name)
    return original(name, globals, locals, fromlist, level)
builtins.__import__ = guarded
import projectb.profiles.demo
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr
