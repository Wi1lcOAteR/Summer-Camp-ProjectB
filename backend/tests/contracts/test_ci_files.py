"""CI-01 contract tests for the structural dual-pipeline verifier."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PYTHON = sys.executable


def run_verifier(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(ROOT / "scripts" / "verify_ci_contract.py"), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=30,
    )


def test_ci_verifier_emits_stable_structural_mapping_and_receipt() -> None:
    result = run_verifier()
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip().splitlines()
    assert lines[-1] == "CI_CONTRACT_PASS"
    mapping = json.loads("\n".join(lines[:-1]))
    assert mapping["schema"] == "ci-contract-v1"
    assert mapping["status"] == "pass"
    assert mapping["platforms"] == {"github": "pass", "gitlab": "pass"}
    assert mapping["requirements"]["push_triggers"] == ["github:on.push", "gitlab:workflow.push"]
    assert mapping["requirements"]["gitlab_unit_test"] == ["gitlab:unit-test"]
    assert mapping["requirements"]["windows_package"] == ["github:windows-package"]
    assert mapping["requirements"]["oci_package"] == [
        "github:oci-package",
        "gitlab:oci-package",
    ]
    assert mapping["jobs"] == {
        "github": ["backend", "frontend", "oci-package", "scanner", "windows-package"],
        "gitlab": ["backend", "frontend", "oci-package", "unit-test"],
    }
    assert mapping["commands"]["backend"] == {
        "github": "python scripts/test_all.py --backend",
        "gitlab": "python scripts/test_all.py --backend",
    }


def test_ci_verifier_rejects_unknown_job_without_mutating_repository(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    candidate = tmp_path / "ci.yml"
    candidate.write_bytes(github.read_bytes() + b"\n  mystery:\n    runs-on: ubuntu-24.04\n")
    result = run_verifier("--github", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED unknown_job:github:mystery"


def test_ci_verifier_rejects_bypass_and_reports_stable_code(tmp_path: Path) -> None:
    gitlab = ROOT / ".gitlab-ci.yml"
    candidate = tmp_path / ".gitlab-ci.yml"
    text = gitlab.read_text(encoding="utf-8")
    text = text.replace("backend:\n  stage: test", "backend:\n  allow_failure: true\n  stage: test", 1)
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--gitlab", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED bypass:gitlab:backend:allow_failure"


def test_ci_verifier_requires_backend_suite_as_a_direct_command(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    candidate = tmp_path / "ci.yml"
    text = github.read_text(encoding="utf-8").replace(
        "run: python scripts/test_all.py --backend",
        "run: if false; then python scripts/test_all.py --backend; fi",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--github", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED backend_command:github:direct"


def test_ci_verifier_rejects_unknown_requirement_argument() -> None:
    result = run_verifier("--requirement", "unknown")
    assert result.returncode == 3
    assert result.stdout.strip() == "CI_CONTRACT_RED usage_unknown_requirement"


def test_ci_verifier_rejects_unapproved_github_action(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    candidate = tmp_path / "ci.yml"
    text = github.read_text(encoding="utf-8")
    text = text.replace(
        "actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020",
        "evil/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--github", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED github_action_allowlist"


def test_ci_verifier_rejects_github_publication(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    candidate = tmp_path / "ci.yml"
    text = github.read_text(encoding="utf-8").replace(
        "run: docker build --platform linux/amd64",
        "run: docker login example.test && docker build --platform linux/amd64",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--github", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED bypass:github:publication"


def test_ci_verifier_rejects_github_job_condition(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    candidate = tmp_path / "ci.yml"
    text = github.read_text(encoding="utf-8").replace(
        "  backend:\n    runs-on:",
        "  backend:\n    if: ${{ false }}\n    runs-on:",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--github", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED bypass:github:backend:if"


def test_ci_verifier_rejects_github_step_condition(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    candidate = tmp_path / "ci.yml"
    text = github.read_text(encoding="utf-8").replace(
        "      - name: Run current backend suite\n",
        "      - name: Run current backend suite\n        if: ${{ false }}\n",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--github", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED bypass:github:backend:step_if"


def test_ci_verifier_requires_windows_build_as_direct_command(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    candidate = tmp_path / "ci.yml"
    text = github.read_text(encoding="utf-8").replace(
        "run: powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1",
        "run: echo powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--github", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED windows_command:github:direct:build"


def test_ci_verifier_requires_github_oci_build_as_direct_command(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    candidate = tmp_path / "ci.yml"
    text = github.read_text(encoding="utf-8").replace(
        "run: docker build --platform linux/amd64",
        "run: echo docker build --platform linux/amd64",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--github", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED oci_command:github:direct:build"


def test_ci_verifier_requires_gitlab_oci_build_as_direct_command(tmp_path: Path) -> None:
    gitlab = ROOT / ".gitlab-ci.yml"
    candidate = tmp_path / ".gitlab-ci.yml"
    text = gitlab.read_text(encoding="utf-8").replace(
        "    - docker build --platform linux/amd64",
        "    - if false; then docker build --platform linux/amd64",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--gitlab", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED oci_command:gitlab:direct:build"


def test_ci_verifier_rejects_multiline_bypass_wrappers(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    github_candidate = tmp_path / "ci.yml"
    github_text = github.read_text(encoding="utf-8").replace(
        "        run: python scripts/test_all.py --backend",
        "        run: |\n          if false; then\n            python scripts/test_all.py --backend\n          fi",
        1,
    )
    github_candidate.write_text(github_text, encoding="utf-8")
    github_result = run_verifier("--github", str(github_candidate))
    assert github_result.returncode == 2
    assert github_result.stdout.strip() == "CI_CONTRACT_RED backend_command:github:direct"

    gitlab = ROOT / ".gitlab-ci.yml"
    gitlab_candidate = tmp_path / ".gitlab-ci.yml"
    gitlab_text = gitlab.read_text(encoding="utf-8").replace(
        "    - pwsh -NoProfile -File scripts/bootstrap_scan_credentials.ps1 -Tracked",
        "    - |\n      if false; then\n        pwsh -NoProfile -File scripts/bootstrap_scan_credentials.ps1 -Tracked\n      fi",
        1,
    )
    gitlab_candidate.write_text(gitlab_text, encoding="utf-8")
    gitlab_result = run_verifier("--gitlab", str(gitlab_candidate))
    assert gitlab_result.returncode == 2
    assert gitlab_result.stdout.strip() == "CI_CONTRACT_RED scanner_command:gitlab:direct:pwsh -NoProfile -File scripts/bootstrap_scan_credentials.ps1 -Tracked"


def test_ci_verifier_rejects_case_wrapped_oci_command(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    candidate = tmp_path / "ci.yml"
    text = github.read_text(encoding="utf-8").replace(
        "        run: docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:ci .",
        "        run: |\n          case 0 in\n            1)\n              docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:ci .\n              ;;\n          esac",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--github", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED oci_command:github:direct:build"


def test_ci_verifier_locks_frontend_working_directories(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    github_candidate = tmp_path / "ci.yml"
    github_candidate.write_text(
        github.read_text(encoding="utf-8").replace("working-directory: frontend", "working-directory: .", 1),
        encoding="utf-8",
    )
    github_result = run_verifier("--github", str(github_candidate))
    assert github_result.returncode == 2
    assert github_result.stdout.strip() == "CI_CONTRACT_RED frontend_directory:github"

    gitlab = ROOT / ".gitlab-ci.yml"
    gitlab_candidate = tmp_path / ".gitlab-ci.yml"
    gitlab_candidate.write_text(
        gitlab.read_text(encoding="utf-8").replace("    - cd frontend\n", "", 1),
        encoding="utf-8",
    )
    gitlab_result = run_verifier("--gitlab", str(gitlab_candidate))
    assert gitlab_result.returncode == 2
    assert gitlab_result.stdout.strip() == "CI_CONTRACT_RED frontend_directory:gitlab"
