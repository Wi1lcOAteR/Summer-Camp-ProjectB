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
    assert set(mapping["commands"]) == {"backend", "frontend", "oci", "scanner", "windows"}


def test_github_git_consumers_install_git_before_checkout() -> None:
    github = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    bootstrap = "run: apt-get update && apt-get install -y --no-install-recommends git"
    checkout = "uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683"

    for job_name, next_job in (("scanner", "backend"), ("backend", "frontend")):
        section = github.split(f"  {job_name}:\n", 1)[1].split(f"\n  {next_job}:\n", 1)[0]
        assert section.index(bootstrap) < section.index(checkout)


def test_github_git_consumers_trust_only_the_current_workspace() -> None:
    github = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    trust = (
        "    env:\n"
        "      GIT_CONFIG_COUNT: 1\n"
        "      GIT_CONFIG_KEY_0: safe.directory\n"
        "      GIT_CONFIG_VALUE_0: ${{ github.workspace }}\n"
    )

    for job_name, next_job in (("scanner", "backend"), ("backend", "frontend")):
        section = github.split(f"  {job_name}:\n", 1)[1].split(f"\n  {next_job}:\n", 1)[0]
        assert trust in section


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


def test_ci_verifier_rejects_gitlab_job_rules(tmp_path: Path) -> None:
    gitlab = ROOT / ".gitlab-ci.yml"
    candidate = tmp_path / ".gitlab-ci.yml"
    text = gitlab.read_text(encoding="utf-8").replace(
        "backend:\n  stage: test",
        "backend:\n  rules:\n    - when: never\n  stage: test",
        1,
    )
    candidate.write_text(text, encoding="utf-8")
    result = run_verifier("--gitlab", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED bypass:gitlab:backend:rules"


def test_ci_verifier_rejects_gitlab_stage_drift(tmp_path: Path) -> None:
    gitlab = ROOT / ".gitlab-ci.yml"
    candidate = tmp_path / ".gitlab-ci.yml"
    candidate.write_text(
        gitlab.read_text(encoding="utf-8").replace("stages:\n  - test", "stages:\n  - test\n  - deploy", 1),
        encoding="utf-8",
    )
    result = run_verifier("--gitlab", str(candidate))
    assert result.returncode == 2
    assert result.stdout.strip() == "CI_CONTRACT_RED gitlab_stages"


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


def test_ci_verifier_rejects_function_and_until_wrappers(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    github_candidate = tmp_path / "ci.yml"
    github_text = github.read_text(encoding="utf-8").replace(
        "        run: python scripts/test_all.py --backend",
        "        run: |\n          run_backend() {\n            python scripts/test_all.py --backend\n          }",
        1,
    )
    github_candidate.write_text(github_text, encoding="utf-8")
    github_result = run_verifier("--github", str(github_candidate))
    assert github_result.returncode == 2
    assert github_result.stdout.strip() == "CI_CONTRACT_RED backend_command:github:direct"

    no_parens_candidate = tmp_path / "function-no-parens.yml"
    no_parens_text = github.read_text(encoding="utf-8").replace(
        "        run: python scripts/test_all.py --backend",
        "        run: |\n          function run_backend {\n            python scripts/test_all.py --backend\n          }",
        1,
    )
    no_parens_candidate.write_text(no_parens_text, encoding="utf-8")
    no_parens_result = run_verifier("--github", str(no_parens_candidate))
    assert no_parens_result.returncode == 2
    assert no_parens_result.stdout.strip() == "CI_CONTRACT_RED backend_command:github:direct"

    close_prefix_candidate = tmp_path / "function-close-prefix.yml"
    close_prefix_text = github.read_text(encoding="utf-8").replace(
        "        run: python scripts/test_all.py --backend",
        "        run: |\n          function run_backend {\n            find . -maxdepth 0\n            python scripts/test_all.py --backend\n          }",
        1,
    )
    close_prefix_candidate.write_text(close_prefix_text, encoding="utf-8")
    close_prefix_result = run_verifier("--github", str(close_prefix_candidate))
    assert close_prefix_result.returncode == 2
    assert close_prefix_result.stdout.strip() == "CI_CONTRACT_RED backend_command:github:direct"

    for name, opener, closer in (("subshell", "(", ")"), ("brace", "{", "}")):
        grouped_candidate = tmp_path / f"{name}.yml"
        grouped_text = github.read_text(encoding="utf-8").replace(
            "        run: python scripts/test_all.py --backend",
            f"        run: |\n          {opener}\n            python scripts/test_all.py --backend\n          {closer}",
            1,
        )
        grouped_candidate.write_text(grouped_text, encoding="utf-8")
        grouped_result = run_verifier("--github", str(grouped_candidate))
        assert grouped_result.returncode == 2
        assert grouped_result.stdout.strip() == "CI_CONTRACT_RED backend_command:github:direct"

    gitlab = ROOT / ".gitlab-ci.yml"
    gitlab_candidate = tmp_path / ".gitlab-ci.yml"
    gitlab_text = gitlab.read_text(encoding="utf-8").replace(
        "    - pwsh -NoProfile -File scripts/bootstrap_scan_credentials.ps1 -Tracked",
        "    - |\n      until true; do\n        pwsh -NoProfile -File scripts/bootstrap_scan_credentials.ps1 -Tracked\n      done",
        1,
    )
    gitlab_candidate.write_text(gitlab_text, encoding="utf-8")
    gitlab_result = run_verifier("--gitlab", str(gitlab_candidate))
    assert gitlab_result.returncode == 2
    assert gitlab_result.stdout.strip() == "CI_CONTRACT_RED scanner_command:gitlab:direct:pwsh -NoProfile -File scripts/bootstrap_scan_credentials.ps1 -Tracked"


def test_ci_verifier_rejects_heredoc_and_command_substitution(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    for name, replacement in (
        (
            "heredoc",
            "        run: |\n          cat <<'COMMAND'\n          python scripts/test_all.py --backend\n          COMMAND",
        ),
        (
            "substitution",
            "        run: |\n          ignored=$(\n            python scripts/test_all.py --backend\n          )",
        ),
    ):
        candidate = tmp_path / f"{name}.yml"
        candidate.write_text(
            github.read_text(encoding="utf-8").replace(
                "        run: python scripts/test_all.py --backend",
                replacement,
                1,
            ),
            encoding="utf-8",
        )
        result = run_verifier("--github", str(candidate))
        assert result.returncode == 2
        assert result.stdout.strip() == "CI_CONTRACT_RED github_steps_drift:backend"


def test_ci_verifier_rejects_gitlab_shell_shadow_and_before_script(tmp_path: Path) -> None:
    gitlab = ROOT / ".gitlab-ci.yml"
    shadow_candidate = tmp_path / "shadow.yml"
    shadow_candidate.write_text(
        gitlab.read_text(encoding="utf-8").replace(
            "  script:\n    - python --version",
            "  script:\n    - 'python() { return 0; }'\n    - python --version",
            1,
        ),
        encoding="utf-8",
    )
    shadow_result = run_verifier("--gitlab", str(shadow_candidate))
    assert shadow_result.returncode == 2
    assert shadow_result.stdout.strip() == "CI_CONTRACT_RED gitlab_script_drift:backend"

    before_candidate = tmp_path / "before.yml"
    before_candidate.write_text(
        gitlab.read_text(encoding="utf-8").replace(
            "backend:\n  stage: test",
            "backend:\n  before_script:\n    - 'python() { return 0; }'\n  stage: test",
            1,
        ),
        encoding="utf-8",
    )
    before_result = run_verifier("--gitlab", str(before_candidate))
    assert before_result.returncode == 2
    assert before_result.stdout.strip() == "CI_CONTRACT_RED gitlab_job_keys:backend"


def test_ci_verifier_rejects_wrapped_lock_and_preflight_commands(tmp_path: Path) -> None:
    github = ROOT / ".github" / "workflows" / "ci.yml"
    gitlab = ROOT / ".gitlab-ci.yml"
    lock_candidate = tmp_path / "github-lock.yml"
    lock_candidate.write_text(
        github.read_text(encoding="utf-8").replace(
            "        run: python -m pip install --require-hashes -r requirements.linux-ci.lock",
            "        run: |\n          if false; then\n            python -m pip install --require-hashes -r requirements.linux-ci.lock\n          fi",
            1,
        ),
        encoding="utf-8",
    )
    lock_result = run_verifier("--github", str(lock_candidate))
    assert lock_result.returncode == 2
    assert lock_result.stdout.strip() == "CI_CONTRACT_RED github_steps_drift:backend"

    preflight_candidate = tmp_path / "github-preflight.yml"
    preflight_candidate.write_text(
        github.read_text(encoding="utf-8").replace(
            "          test \"$(docker info --format '{{.OSType}}')\" = \"linux\"",
            "          if false; then test \"$(docker info --format '{{.OSType}}')\" = \"linux\"; fi",
            1,
        ),
        encoding="utf-8",
    )
    preflight_result = run_verifier("--github", str(preflight_candidate))
    assert preflight_result.returncode == 2
    assert preflight_result.stdout.strip() == "CI_CONTRACT_RED github_steps_drift:oci-package"

    gitlab_candidate = tmp_path / "gitlab-lock.yml"
    gitlab_candidate.write_text(
        gitlab.read_text(encoding="utf-8").replace(
            "    - python -m pip install --require-hashes -r requirements.linux-ci.lock",
            "    - if false; then python -m pip install --require-hashes -r requirements.linux-ci.lock; fi",
            1,
        ),
        encoding="utf-8",
    )
    gitlab_result = run_verifier("--gitlab", str(gitlab_candidate))
    assert gitlab_result.returncode == 2
    assert gitlab_result.stdout.strip() == "CI_CONTRACT_RED gitlab_script_drift:backend"


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
