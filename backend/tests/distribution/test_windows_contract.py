from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WINDOWS = ROOT / "packaging" / "windows"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _analysis_excludes(spec: str) -> set[str]:
    tree = ast.parse(spec)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "Analysis":
            continue
        for keyword in node.keywords:
            if keyword.arg == "excludes":
                value = ast.literal_eval(keyword.value)
                return {str(item) for item in value}
    raise AssertionError("analysis_excludes_missing")


def test_windows_distribution_files_and_resource_contract_exist() -> None:
    required = (
        WINDOWS / "build.ps1",
        WINDOWS / "ProjectB.spec",
        WINDOWS / "launcher.py",
        WINDOWS / "hooks" / "hook-keyring.py",
        WINDOWS / "hooks" / "hook-pypdfium2.py",
        WINDOWS / "smoke_test.ps1",
        ROOT / "docs" / "engineering" / "DIST-01_EVIDENCE.md",
    )
    assert all(path.is_file() for path in required)

    build = _text(WINDOWS / "build.ps1")
    spec = _text(WINDOWS / "ProjectB.spec")
    launcher = _text(WINDOWS / "launcher.py")
    assert "ProjectB.spec" in build
    assert "--clean" in build and "--noconfirm" in build
    assert "ProjectB.exe" in build
    assert "windows_x64_required" in build and "python_3_14_6_required" in build and "python_x64_required" in build
    assert "pyinstaller_6_21_0_required" in build and "Assert-NoReparse" in build
    assert "PKG-00.toc" in build and "package_resource_missing" in build
    assert "frontend_build_failed" in build and "$LASTEXITCODE -ne 0" in build
    assert "frontend_dist" in spec and "THIRD_PARTY_NOTICES.md" in spec
    assert "PIL" in _analysis_excludes(spec)
    assert "127.0.0.1" in launcher
    assert "LOCALAPPDATA" in launcher or "data-dir" in launcher


def test_windows_smoke_and_ci_are_fail_closed() -> None:
    smoke = _text(WINDOWS / "smoke_test.ps1")
    workflow = _text(ROOT / ".github" / "workflows" / "ci.yml")
    seed = _text(ROOT / "scripts" / "tests" / "ci_seed_contract.ps1")
    assert "127.0.0.1" in smoke
    assert "webui_resource_contract" in smoke and 'id="root"' in smoke
    assert "WinVault" in smoke or "credential" in smoke.lower()
    assert "finally" in smoke.lower() and "Stop-Process" in smoke and "Get-Process -Name" in smoke
    assert "Get-NetTCPConnection -OwningProcess" in smoke
    assert "data_root_must_be_disposable" in smoke and "artifact_already_running" in smoke and "Assert-NoReparse" in smoke
    assert "windows-package" in workflow
    assert "windows-2025" in workflow
    assert "packaging/windows/build.ps1" in workflow
    assert "scripts/scan_credentials.py --path dist/ProjectB.exe" in workflow
    assert "sha256" in workflow.lower()
    assert "windows-package" in seed
