"""Contract tests for the F-01E repository quality gates."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

import pytest


REPO = Path(__file__).resolve().parents[2]
PYTHON = sys.executable


def run_script(relative: str, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(REPO / relative), *args],
        cwd=cwd or REPO,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def load_module(relative: str):
    spec = importlib.util.spec_from_file_location("quality_gate_module", REPO / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_shape(prefix: str, size: int) -> str:
    return prefix + ("q" * size)


def test_quality_gate_scripts_exist() -> None:
    for relative in (
        "scripts/test_all.py",
        "scripts/scan_credentials.py",
        "scripts/verify_licenses.py",
        "licenses/THIRD_PARTY_NOTICES.md",
    ):
        assert (REPO / relative).is_file(), relative


def test_scanner_rejects_unknown_scope() -> None:
    result = run_script("scripts/scan_credentials.py", "--unknown")
    assert result.returncode == 3
    assert "usage_missing_scope" in result.stdout


def test_scanner_redacts_detected_value() -> None:
    candidate = make_shape("sk-", 20)
    temp_root = REPO / "tmp"
    temp_root.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="quality-gate-", dir=temp_root))
    try:
        target = work / "candidate.txt"
        target.write_text(candidate, encoding="utf-8")
        result = run_script("scripts/scan_credentials.py", "--path", str(target))

        assert result.returncode == 2
        assert candidate not in result.stdout
        assert json.loads(result.stdout)["rule"] == "provider_api_key"
    finally:
        shutil.rmtree(work)


def test_scanner_pass_receipt_counts_scanned_path() -> None:
    result = run_script("scripts/scan_credentials.py", "--path", "scripts/tests/fixtures/scanner/clean.txt")
    assert result.returncode == 0
    assert result.stdout.strip() == "CREDENTIAL_SCAN_PASS files=1"


def test_scanner_skips_real_binary_fixture() -> None:
    fixture = REPO / "scripts/tests/fixtures/scanner/binary.png"
    assert fixture.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    result = run_script("scripts/scan_credentials.py", "--path", str(fixture))
    assert result.returncode == 0
    assert result.stdout.strip() == "CREDENTIAL_SCAN_PASS files=0"


def test_scanner_reports_unsupported_path_context(tmp_path: Path) -> None:
    target = tmp_path / "candidate.weird"
    target.write_text("plain", encoding="utf-8")
    result = run_script("scripts/scan_credentials.py", "--path", str(target))
    assert result.returncode == 3
    assert json.loads(result.stdout) == {
        "code": "unsupported_file_type",
        "source": "path",
        "path": str(target).replace("\\", "/"),
    }


def test_python_scanner_reports_index_and_worktree_separately(monkeypatch: pytest.MonkeyPatch) -> None:
    scanner = load_module("scripts/scan_credentials.py")
    observed: set[str] = set()

    def observe(source: str, path: str, raw: bytes) -> list[dict[str, str]]:
        assert path and raw
        observed.add(source)
        return []

    monkeypatch.setattr(scanner, "scan_bytes", observe)

    findings = scanner.scan_git_sources(REPO, include_tracked=True, include_staged=True)

    assert findings == []
    assert observed == {"index", "worktree"}


def test_python_scanner_reads_exact_index_blob_and_worktree_bytes(tmp_path: Path) -> None:
    scanner = load_module("scripts/scan_credentials.py")
    repo = tmp_path / "repo"
    repo.mkdir()

    def git_run(*arguments: str) -> None:
        result = subprocess.run(
            ["git", *arguments],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        assert result.returncode == 0, result.stderr

    git_run("init", "-q")
    target = repo / "dual.txt"
    target.write_text("clean\n", encoding="utf-8")
    git_run("add", "dual.txt")
    candidate = make_shape("sk-", 20)
    target.write_text(candidate, encoding="utf-8")

    findings = scanner.scan_git_sources(repo, include_tracked=True, include_staged=True)
    assert findings == [{"source": "worktree", "path": "dual.txt", "rule": "provider_api_key"}]

    git_run("add", "dual.txt")
    target.write_text("clean\n", encoding="utf-8")
    findings = scanner.scan_git_sources(repo, include_tracked=True, include_staged=True)
    assert findings == [{"source": "index", "path": "dual.txt", "rule": "provider_api_key"}]


def test_git_scan_snapshot_returns_findings_and_count_from_one_enumeration(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    scanner = load_module("scripts/scan_credentials.py")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    calls = {"tracked": 0, "index": 0}

    def tracked(_: Path) -> list[str]:
        calls["tracked"] += 1
        assert calls["tracked"] == 1
        return ["worktree.txt"]

    def index(_: Path) -> dict[str, str]:
        calls["index"] += 1
        assert calls["index"] == 1
        return {"index.txt": "oid"}

    monkeypatch.setattr(scanner, "tracked_paths", tracked)
    monkeypatch.setattr(scanner, "index_entries", index)
    monkeypatch.setattr(scanner, "read_worktree", lambda *_: b"clean\n")
    monkeypatch.setattr(scanner, "git", lambda *_: b"clean\n")
    findings, count = scanner.scan_git_snapshot(repo, include_tracked=True, include_staged=True)
    assert findings == []
    assert count == 2
    assert calls == {"tracked": 1, "index": 1}


def test_git_scan_skips_a_tracked_file_deleted_from_the_worktree(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    scanner = load_module("scripts/scan_credentials.py")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    monkeypatch.setattr(scanner, "tracked_paths", lambda _: ["deleted.md"])
    monkeypatch.setattr(scanner, "index_entries", lambda _: {})

    assert scanner.scan_git_snapshot(repo, include_tracked=True, include_staged=True) == ([], 0)


def test_index_mode_error_matches_bootstrap_contract(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    scanner = load_module("scripts/scan_credentials.py")

    def fake_git(_: Path, *arguments: str) -> bytes:
        assert arguments == ("ls-files", "--stage", "-z")
        return b"120000 abcdef0123456789abcdef0123456789abcdef 0\tlink.txt\0"

    monkeypatch.setattr(scanner, "git", fake_git)
    with pytest.raises(scanner.ScanError) as error:
        scanner.index_entries(tmp_path)
    assert error.value.code == "index_mode_unsupported"


def test_git_failures_map_to_redacted_stable_receipts(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    scanner = load_module("scripts/scan_credentials.py")

    def timeout(*_: object, **__: object) -> subprocess.CompletedProcess[bytes]:
        raise subprocess.TimeoutExpired(["git"], 30)

    monkeypatch.setattr(scanner.subprocess, "run", timeout)
    with pytest.raises(scanner.ScanError) as timeout_error:
        scanner.git(tmp_path, "status")
    assert timeout_error.value.code == "git_list_failed"

    def unavailable(*_: object, **__: object) -> subprocess.CompletedProcess[bytes]:
        raise OSError("private command detail")

    monkeypatch.setattr(scanner.subprocess, "run", unavailable)
    with pytest.raises(scanner.ScanError) as os_error:
        scanner.git(tmp_path, "status")
    assert os_error.value.code == "git_list_failed"


def test_scanner_is_superset_of_bootstrap_direct_rules() -> None:
    scanner = load_module("scripts/scan_credentials.py")
    bootstrap = (REPO / "scripts/bootstrap_scan_credentials.ps1").read_text(encoding="utf-8")
    expected = {
        "provider_api_key": make_shape("sk-", 20),
        "github_token": make_shape("ghp_", 20),
        "aws_access_key": "AKIA" + ("A" * 16),
        "google_api_key": "AIza" + ("A" * 35),
        "slack_token": "xoxb-" + ("A" * 10),
        "private_key": "-----BEGIN " + "PRIVATE KEY-----",
    }
    assert set(expected).issubset(scanner.DIRECT_RULES)
    for rule, shape in expected.items():
        assert rule in bootstrap
        assert rule in scanner.find_rules(shape)


def test_scanner_does_not_treat_source_expressions_as_assignments() -> None:
    scanner = load_module("scripts/scan_credentials.py")
    source_expression = "secret=[byte[]]$utf8.GetBytes($positive)"
    assert "assignment_secret" not in scanner.find_rules(source_expression)


def test_license_verifier_requires_full_notice_inventory() -> None:
    result = run_script("scripts/verify_licenses.py")
    assert result.returncode == 0, result.stderr
    assert "LICENSE_VERIFICATION_PASS" in result.stdout
    notice = (REPO / "licenses/THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    assert "FastAPI 0.139.2" in notice
    assert "React 19.2.7" in notice
    assert "licenses/bootstrap" in notice


def test_license_verifier_rejects_incompatible_terms_and_binds_closures() -> None:
    verifier = load_module("scripts/verify_licenses.py")
    assert verifier.is_allowed_license("MIT")
    assert verifier.is_allowed_license("GPL-2.0-or-later WITH Bootloader-exception")
    assert not verifier.is_allowed_license("AGPL-3.0-only")
    assert not verifier.is_allowed_license("GPL-3.0-only")
    assert len(verifier.python_lock_pairs()) == 54
    assert verifier.npm_package_count() == 166


def test_license_verifier_binds_all_platform_closures() -> None:
    verifier = load_module("scripts/verify_licenses.py")
    windows = verifier.python_lock_pairs()
    baseline = verifier.baseline_python_licenses()
    assert len(verifier.linux_ci_python_pairs()) == 41
    assert len(verifier.linux_demo_python_pairs()) == 14
    assert verifier.linux_ci_python_pairs() <= windows
    assert verifier.linux_demo_python_pairs() <= windows
    assert set(baseline) == windows

    npm = verifier.npm_license_pairs()
    assert len(npm) == 166
    assert all(version and verifier.is_allowed_license(license_name) for version, license_name in npm.values())
    assert verifier.npm_closure_sha256() == "f8c74a494fc945ddb724607b85166408cfbbe6dee1a79ac16f1a579da0fc4c47"
    assert verifier.baseline_license_sha256() == "7013e4d8dee96ab1c461bf7b093c35770cd371b5ea7462a77f050f8912f51beb"


def test_runner_rejects_bad_mode_and_propagates_child_failure() -> None:
    runner = load_module("scripts/test_all.py")
    assert runner.parse_mode(["--bad"]) is None
    command = [PYTHON, "-c", "raise SystemExit(17)"]
    assert runner.run_child(command, cwd=REPO) == 17


def test_runner_backend_always_includes_script_suite() -> None:
    runner = load_module("scripts/test_all.py")
    temp_root = REPO / "tmp"
    temp_root.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="quality-runner-", dir=temp_root))
    try:
        backend_test = work / "backend/tests/test_discovered.py"
        backend_test.parent.mkdir(parents=True)
        backend_test.write_text("def test_discovered(): pass\n", encoding="utf-8")
        commands = runner.build_commands(work, "backend", PYTHON, "npm")
        flattened = "\n".join(" ".join(command) for command in commands)
        assert "scripts/tests" in flattened
        assert "backend/tests/test_discovered.py" in flattened
        assert "scan_credentials.py" in flattened
        assert "verify_licenses.py" in flattened
    finally:
        shutil.rmtree(work)


def test_runner_frontend_includes_build() -> None:
    runner = load_module("scripts/test_all.py")
    commands = runner.build_commands(REPO, "frontend", PYTHON, "npm")
    assert ["npm", "exec", "--", "vite", "build"] in commands


def test_runner_quality_commands_use_exact_mode_and_working_directory() -> None:
    runner = load_module("scripts/test_all.py")
    backend = runner.build_quality_commands(REPO, "backend", PYTHON, "npm")
    frontend = runner.build_quality_commands(REPO, "frontend", PYTHON, "npm")

    assert backend == [
        ([PYTHON, "-m", "ruff", "check", "backend", "scripts", "--select", "F401,F841"], REPO),
        ([PYTHON, "-m", "ruff", "check", "backend", "scripts"], REPO),
        ([PYTHON, "-m", "mypy", "--explicit-package-bases", "projectb"], REPO / "backend"),
    ]
    assert frontend == [
        (["npm", "exec", "--", "tsc", "-p", "tsconfig.json", "--noEmit", "--noUnusedLocals", "--noUnusedParameters"], REPO / "frontend"),
    ]
    assert runner.build_quality_commands(REPO, "all", PYTHON, "npm") == backend + frontend


def test_evidence_smoke_documents_only_the_deliberate_e402_suppression() -> None:
    source = (REPO / "scripts/evidence/g02a_python_smoke.py").read_text(encoding="utf-8")
    assert "# ruff: noqa: E402" in source
    assert "PROJECTB_G02A_SITE_PACKAGES" in source.split("# ruff: noqa: E402", 1)[0]


def test_frontend_exposes_plan_build_command() -> None:
    package = json.loads((REPO / "frontend/package.json").read_text(encoding="utf-8"))
    assert package.get("scripts", {}).get("build") == "vite build"


def test_planned_e2e_command_loads_all_viewport_projects() -> None:
    runner = load_module("scripts/test_all.py")
    result = subprocess.run(
        [
            runner.npm_command(REPO),
            "--prefix",
            "frontend",
            "exec",
            "--",
            "playwright",
            "test",
            "e2e/mapping.spec.ts",
            "--list",
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "[mobile-360]" in result.stdout
    assert "[tablet-768]" in result.stdout
    assert "[desktop-1440]" in result.stdout


def test_runner_prefers_project_local_npm() -> None:
    runner = load_module("scripts/test_all.py")
    command = Path(runner.npm_command(REPO))
    if os.name == "nt":
        assert command.name.casefold() == "npm.cmd"
        assert "tmp" in command.parts
        assert "toolchains" in command.parts
    else:
        assert str(command) == "npm"


def test_seeded_ci_uses_the_current_runner() -> None:
    gitlab = (REPO / ".gitlab-ci.yml").read_text(encoding="utf-8")
    github = (REPO / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "python scripts/test_all.py --backend" in gitlab
    assert "python scripts/test_all.py --backend" in github


def test_completed_process_archive_preserves_exact_historical_bytes() -> None:
    archive = REPO / "docs/archive/completed-process-2026-08-07"
    expected = {
        "SKILLS_SETUP.md": ("SKILLS_SETUP.md", 8235, "0e42daec5853cb156368681e29d0b3b4f376e5a19564dc32f5cc12ad06e67409"),
        "PROJECT_AUDIT.md": ("docs/PROJECT_AUDIT.md", 19217, "71f38c9a2672eedc616c70692e718f669b575a921e740193b7924a6594012205"),
        "plans/2026-07-30-g03-progress-logging.md": ("docs/plans/2026-07-30-g03-progress-logging.md", 4588, "ae6b95bb69014b9fefc64d155d56db7d06f6f178f7f32826b005b1508147dc86"),
        "plans/2026-07-31-g03-structured-output-env.md": ("docs/plans/2026-07-31-g03-structured-output-env.md", 15290, "08ea1306074b581569e8df7257737e42942158306b422ae619efc9590b371534"),
        "specs/2026-07-31-g03-structured-output-env-design.md": ("docs/specs/2026-07-31-g03-structured-output-env-design.md", 6673, "0741e660e0254cdf0890c33d7cc700b8edd3ab0145860aa60a4605a489734914"),
        "specs/2026-08-01-g03-atomic-execution-design.md": ("docs/specs/2026-08-01-g03-atomic-execution-design.md", 4264, "e8d41420870bee0c52990e7bf7a0fc99b83a9c98c21eb7f3461e5ec5944a9b63"),
        "engineering/SESSION_HANDOFF.md": ("docs/engineering/SESSION_HANDOFF.md", 3288, "f8f842f05510f1b5e341e5aec9ea61c4d24d5ca3e0e7c82de0dfd5c40576c83e"),
        "engineering/WRITING_PLANS_VALIDATION.md": ("docs/engineering/WRITING_PLANS_VALIDATION.md", 38244, "b30f72cd18da68cfc6fb75e2d02c528817438ffd04e0152a902abe2c70d3411e"),
    }
    manifest = (archive / "MANIFEST.md").read_text(encoding="utf-8")

    for destination, (source, size, digest) in expected.items():
        target = archive / destination
        assert not (REPO / source).exists(), source
        assert target.stat().st_size == size
        assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
        assert f"`{source}`" in manifest
        assert f"`docs/archive/completed-process-2026-08-07/{destination}`" in manifest
        assert f"`{digest}`" in manifest


def test_completed_process_archive_disables_line_ending_normalization() -> None:
    archive_file = "docs/archive/completed-process-2026-08-07/SKILLS_SETUP.md"
    result = subprocess.run(
        ["git", "check-attr", "text", "diff", "--", archive_file],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert f"{archive_file}: text: unset" in result.stdout
    assert f"{archive_file}: diff: unset" in result.stdout


def test_active_markdown_local_links_resolve() -> None:
    link_pattern = re.compile(r"(?<!!)\[[^]]+\]\(([^)\s]+)")
    broken: list[str] = []
    for document in REPO.rglob("*.md"):
        relative = document.relative_to(REPO).as_posix()
        if relative.startswith(("docs/archive/", "tmp/", "node_modules/", "frontend/node_modules/")):
            continue
        for target in link_pattern.findall(document.read_text(encoding="utf-8")):
            path_part = unquote(target.split("#", 1)[0])
            if not path_part or "://" in path_part or path_part.startswith(("#", "mailto:")):
                continue
            resolved = (document.parent / path_part).resolve()
            if not resolved.exists():
                broken.append(f"{relative} -> {target}")
    assert broken == []


def test_generated_test_result_directories_are_ignored() -> None:
    for relative in ("test-results/results.json", "frontend/test-results/results.json"):
        result = subprocess.run(
            ["git", "check-ignore", "-q", "--", relative],
            cwd=REPO,
            check=False,
            timeout=30,
        )
        assert result.returncode == 0, relative


def test_e2e_screenshots_stay_in_ignored_test_results() -> None:
    shell_spec = (REPO / "frontend/e2e/shell.spec.ts").read_text(encoding="utf-8")
    assert "'docs', 'engineering', 'open-design'" not in shell_spec
    assert "test-results" in shell_spec
