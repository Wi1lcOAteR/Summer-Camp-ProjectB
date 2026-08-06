"""Verify the committed notice inventory against pinned project manifests."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTICE = ROOT / "licenses/THIRD_PARTY_NOTICES.md"
PYPROJECT = ROOT / "pyproject.toml"
PACKAGE_LOCK = ROOT / "frontend/package-lock.json"
PYTHON_LOCK = ROOT / "backend/requirements-windows-x64.lock"
LINUX_CI_LOCK = ROOT / "requirements.linux-ci.lock"
LINUX_DEMO_LOCK = ROOT / "packaging/oci/requirements.linux-demo.lock"
BASELINE = ROOT / "docs/engineering/DEPENDENCY_BASELINE.md"
PYTHON_LOCK_SHA256 = "246083f8b210c3e33904f3057dfd48e7d8db548804d11fa5b087ecb291ad0fc6"
NPM_LOCK_SHA256 = "8b793ee9ca823ca1079efe12c4962a8786059b4aaf08bcb715264ad7b4718354"
LINUX_CI_LOCK_SHA256 = "d24ddf3789ea9f276ee6ba4062634fef3c85c4572a7eb62096cbd570bfb0fc35"
LINUX_DEMO_LOCK_SHA256 = "09ce57726c02a090f134d4f2c25f2681dce58ebf2d8425502129d42ac2be34f7"
NPM_CLOSURE_SHA256 = "f8c74a494fc945ddb724607b85166408cfbbe6dee1a79ac16f1a579da0fc4c47"
BASELINE_LICENSE_SHA256 = "7013e4d8dee96ab1c461bf7b093c35770cd371b5ea7462a77f050f8912f51beb"
REQUIRED_BOOTSTRAP = {
    "uv-LICENSE-APACHE", "uv-LICENSE-MIT", "cpython-LICENSE", "node-LICENSE", "npm-LICENSE",
}


def pinned_python_names() -> set[str]:
    text = PYPROJECT.read_text(encoding="utf-8")
    return {match.group(1).casefold() for match in re.finditer(r'^\s*"([A-Za-z0-9_.-]+)==', text, re.M)}


def pinned_python_pairs() -> set[tuple[str, str]]:
    text = PYPROJECT.read_text(encoding="utf-8")
    return {
        (match.group(1).casefold().replace("_", "-").replace(".", "-"), match.group(2))
        for match in re.finditer(r'^\s*"([A-Za-z0-9_.-]+)==([^\"]+)', text, re.M)
    }


def pinned_npm_names() -> set[str]:
    lock = json.loads(PACKAGE_LOCK.read_text(encoding="utf-8"))
    root = lock["packages"][""]
    return set(root.get("dependencies", {})) | set(root.get("devDependencies", {}))


def canonical_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def python_lock_pairs() -> set[tuple[str, str]]:
    return lock_pairs(PYTHON_LOCK)


def lock_pairs(path: Path) -> set[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    return {
        (match.group(1).casefold().replace("_", "-").replace(".", "-"), match.group(2))
        for match in re.finditer(r"^([A-Za-z0-9_.-]+)==([^\s\\]+)", text, re.M)
    }


def linux_ci_python_pairs() -> set[tuple[str, str]]:
    return lock_pairs(LINUX_CI_LOCK)


def linux_demo_python_pairs() -> set[tuple[str, str]]:
    return lock_pairs(LINUX_DEMO_LOCK)


def npm_license_pairs() -> dict[str, tuple[str, str]]:
    lock = json.loads(PACKAGE_LOCK.read_text(encoding="utf-8"))
    pairs: dict[str, tuple[str, str]] = {}
    for path, metadata in lock.get("packages", {}).items():
        if not path:
            continue
        if not path.startswith("node_modules/") or not isinstance(metadata, dict):
            raise ValueError("npm_package_path")
        pairs[path] = (str(metadata.get("version", "")), str(metadata.get("license", "")))
    return pairs


def npm_closure_sha256() -> str:
    rows = [f"{path}\t{version}\t{license_name}" for path, (version, license_name) in npm_license_pairs().items()]
    payload = ("\n".join(sorted(rows)) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def notice_closure_rows(text: str) -> set[tuple[str, str, str, str]]:
    return {
        (match.group(1), match.group(2).strip(), match.group(3).strip(), match.group(4).strip())
        for match in re.finditer(r"^\| (python|npm) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", text, re.M)
    }


def baseline_python_licenses() -> dict[tuple[str, str], str]:
    text = BASELINE.read_text(encoding="utf-8")
    rows: dict[tuple[str, str], str] = {}
    for match in re.finditer(r"^\| python \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", text, re.M):
        rows[(match.group(1).strip().casefold().replace("_", "-").replace(".", "-"), match.group(2).strip())] = match.group(3).strip()
    return rows


def baseline_license_sha256() -> str:
    rows = [f"{name}\t{version}\t{license_name}" for (name, version), license_name in baseline_python_licenses().items()]
    payload = ("\n".join(sorted(rows)) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def npm_package_count() -> int:
    lock = json.loads(PACKAGE_LOCK.read_text(encoding="utf-8"))
    return len(lock["packages"]) - 1


def is_allowed_license(term: str) -> bool:
    upper = term.upper()
    if term == "GPL-2.0-or-later standard hooks; Apache-2.0 runtime hooks":
        return True
    if not term or "UNKNOWN" in upper or "AGPL" in upper or "SSPL" in upper:
        return False
    if "GPL" in upper and "BOOTLOADER-EXCEPTION" not in upper:
        return False
    return any(marker in upper for marker in ("MIT", "APACHE", "BSD", "MPL", "PSF", "ISC", "ARTISTIC", "CC-BY", "BLUEOAK", "CC0", "BOOTLOADER-EXCEPTION"))


def main() -> int:
    if not NOTICE.is_file():
        print("LICENSE_VERIFICATION_ERROR notice_missing")
        return 3
    if any(not (ROOT / "licenses/bootstrap" / name).is_file() for name in REQUIRED_BOOTSTRAP):
        print("LICENSE_VERIFICATION_ERROR bootstrap_notice_missing")
        return 3
    if (
        canonical_sha256(PYTHON_LOCK) != PYTHON_LOCK_SHA256
        or canonical_sha256(LINUX_CI_LOCK) != LINUX_CI_LOCK_SHA256
        or canonical_sha256(LINUX_DEMO_LOCK) != LINUX_DEMO_LOCK_SHA256
        or canonical_sha256(PACKAGE_LOCK) != NPM_LOCK_SHA256
    ):
        print("LICENSE_VERIFICATION_ERROR lock_hash_mismatch")
        return 3
    licenses = baseline_python_licenses()
    if (
        baseline_license_sha256() != BASELINE_LICENSE_SHA256
        or
        set(licenses) != python_lock_pairs()
        or not linux_ci_python_pairs() <= python_lock_pairs()
        or not linux_demo_python_pairs() <= python_lock_pairs()
        or not pinned_python_pairs().issubset(python_lock_pairs())
        or len(licenses) != 54
        or not all(is_allowed_license(term) for term in licenses.values())
    ):
        print("LICENSE_VERIFICATION_ERROR python_closure_invalid")
        return 3
    npm = npm_license_pairs()
    if (
        len(npm) != 166
        or any(not version or not is_allowed_license(license_name) for version, license_name in npm.values())
        or npm_closure_sha256() != NPM_CLOSURE_SHA256
    ):
        print("LICENSE_VERIFICATION_ERROR npm_closure_invalid")
        return 3
    text = NOTICE.read_text(encoding="utf-8")
    expected_notice = {
        ("python", name, version, license_name)
        for (name, version), license_name in licenses.items()
    }
    expected_notice.update(
        ("npm", path.removeprefix("node_modules/"), version, license_name)
        for path, (version, license_name) in npm.items()
    )
    if not expected_notice <= notice_closure_rows(text):
        print("LICENSE_VERIFICATION_ERROR inventory_missing")
        return 3
    missing_python = sorted(name for name in pinned_python_names() if name not in text.casefold())
    missing_npm = sorted(name for name in pinned_npm_names() if name.casefold() not in text.casefold())
    if missing_python or missing_npm:
        print("LICENSE_VERIFICATION_ERROR inventory_missing")
        return 3
    print(f"LICENSE_VERIFICATION_PASS python=54 npm=166 direct_python={len(pinned_python_names())} direct_npm={len(pinned_npm_names())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
