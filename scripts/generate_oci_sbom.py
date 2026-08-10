"""Generate the deterministic SPDX package graph for the demo OCI image."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OCI = ROOT / "packaging" / "oci"


def package_id(prefix: str, name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9.-]+", "-", name).strip("-") or "unnamed"
    return f"SPDXRef-Package-{prefix}-{safe}"


def package(*, identifier: str, name: str, version: str, download: str, license_name: str) -> dict[str, object]:
    return {
        "SPDXID": identifier,
        "name": name,
        "versionInfo": version,
        "downloadLocation": download,
        "filesAnalyzed": False,
        "licenseConcluded": "NOASSERTION",
        "licenseDeclared": license_name or "NOASSERTION",
    }


def python_packages() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    pattern = re.compile(r"^([A-Za-z0-9_.-]+)==([^\\\s]+)")
    for line in (OCI / "requirements.linux-demo.lock").read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        name, version = match.groups()
        rows.append(
            package(
                identifier=package_id("Python", name),
                name=name,
                version=version,
                download=f"https://pypi.org/project/{name}/{version}/",
                license_name="NOASSERTION",
            )
        )
    return rows


def npm_packages() -> list[dict[str, object]]:
    lock = json.loads((ROOT / "frontend/package-lock.json").read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    for path, metadata in lock["packages"].items():
        if not path or not path.startswith("node_modules/"):
            continue
        name = path.rsplit("node_modules/", 1)[-1]
        version = metadata.get("version")
        if not isinstance(version, str):
            raise ValueError(f"npm lock entry has no version: {path}")
        license_name = metadata.get("license")
        if isinstance(license_name, dict):
            license_name = license_name.get("type", "NOASSERTION")
        if not isinstance(license_name, str):
            license_name = "NOASSERTION"
        rows.append(
            package(
                identifier=package_id("Npm", path),
                name=name,
                version=version,
                download=f"https://registry.npmjs.org/{name}",
                license_name=license_name,
            )
        )
    return rows


def main() -> None:
    project_id = "SPDXRef-Package-ProjectB"
    packages = [
        package(
            identifier=project_id,
            name="ProjectB",
            version="local-demo",
            download="NOASSERTION",
            license_name="NOASSERTION",
        ),
        package(
            identifier="SPDXRef-Package-NodeBase",
            name="node",
            version="24.18.0-bookworm-slim@sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6",
            download="https://hub.docker.com/_/node",
            license_name="MIT",
        ),
        package(
            identifier="SPDXRef-Package-PythonBase",
            name="python",
            version="3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb",
            download="https://hub.docker.com/_/python",
            license_name="PSF-2.0",
        ),
        package(
            identifier="SPDXRef-Package-DebianBase",
            name="debian-base-bookworm",
            version="bookworm (see debian-packages.tsv)",
            download="https://www.debian.org/releases/bookworm/",
            license_name="NOASSERTION",
        ),
        package(
            identifier="SPDXRef-Package-DebianInventory",
            name="debian-runtime-package-inventory",
            version="generated-at-image-build",
            download="NOASSERTION",
            license_name="NOASSERTION",
        ),
    ]
    packages.extend(python_packages())
    packages.extend(npm_packages())
    relationships = [
        {"spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES", "relatedSpdxElement": project_id},
        {"spdxElementId": project_id, "relationshipType": "DEPENDS_ON", "relatedSpdxElement": "SPDXRef-Package-NodeBase"},
        {"spdxElementId": project_id, "relationshipType": "DEPENDS_ON", "relatedSpdxElement": "SPDXRef-Package-PythonBase"},
        {"spdxElementId": project_id, "relationshipType": "CONTAINS", "relatedSpdxElement": "SPDXRef-Package-DebianBase"},
        {"spdxElementId": "SPDXRef-Package-DebianBase", "relationshipType": "GENERATES", "relatedSpdxElement": "SPDXRef-Package-DebianInventory"},
    ]
    relationships.extend(
        {"spdxElementId": project_id, "relationshipType": "DEPENDS_ON", "relatedSpdxElement": row["SPDXID"]}
        for row in packages
        if row["SPDXID"] not in {project_id, "SPDXRef-Package-NodeBase", "SPDXRef-Package-PythonBase", "SPDXRef-Package-DebianBase", "SPDXRef-Package-DebianInventory"}
    )
    document = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "ProjectB-demo-oci",
        "documentNamespace": "https://projectb.local/sbom/projectb-demo-oci",
        "creationInfo": {"created": "2026-08-10T00:00:00Z", "creators": ["Tool: scripts/generate_oci_sbom.py"]},
        "packages": packages,
        "relationships": relationships,
    }
    (OCI / "sbom.spdx.json").write_text(json.dumps(document, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
