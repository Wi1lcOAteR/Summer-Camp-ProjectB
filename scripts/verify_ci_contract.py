"""Verify the repository's GitHub Actions and GitLab CI contracts.

This checker intentionally uses a small, strict YAML subset parser.  CI files
are configuration inputs, so introducing a second unpinned parser dependency
would weaken the lock and distribution contracts.  Unsupported YAML constructs
fail closed instead of being silently interpreted.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683"
SETUP_PYTHON = "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065"
SETUP_NODE = "actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020"
POWERSHELL_IMAGE = (
    "mcr.microsoft.com/powershell:7.5-ubuntu-24.04@"
    "sha256:042240d57ec9e47e511033b92625a8d95875ee5860af3015992c248b58a8be81"
)
PYTHON_IMAGE = (
    "python:3.14.6-slim-bookworm@"
    "sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb"
)
NODE_IMAGE = (
    "node:24.18.0-bookworm-slim@"
    "sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6"
)

GITHUB_JOBS = {"scanner", "backend", "frontend", "windows-package", "oci-package"}
GITLAB_JOBS = {"unit-test", "backend", "frontend", "oci-package"}
GITHUB_TIMEOUTS = {"scanner": 10, "backend": 20, "frontend": 20, "windows-package": 30, "oci-package": 30}
GITLAB_TIMEOUTS = {"unit-test": "10m", "backend": "20m", "frontend": "20m", "oci-package": "30m"}
# Digest updates require a reviewed CI edit and a negative contract proving the intended drift.
GITHUB_JOB_DIGESTS = {
    "backend": "f46a09e56f21398661661df6066c08eec006666d9c29d681f031ed112a8f13e6",
    "frontend": "f0dd700abc2e07d0d72e9edba5871795d0ec68ad0069a60e36ad25d9bab06ac6",
    "oci-package": "fa4b85d1701cf7bbbd4657817bb98305bb49f49d0e5b4899cd5beea686bc1ccb",
    "scanner": "119139ca428119985d3c241fc856986b46de3df7e139d7ffb2f72bcb682d395b",
    "windows-package": "573d1ad290963e33b815a5ddb1db71544924358b6a38760030486a2220e5ed3b",
}
GITLAB_JOB_DIGESTS = {
    "backend": "c4224eae168e2de937b5269d0e6dfcac1770da1b5e409afbd0db79011bb569f9",
    "frontend": "267474b8939a71e1c190c8c1b1b503767c815e8b4664bded4fcf7a57ff36f148",
    "oci-package": "5733a4cb468e50e80c64daaecf90e4865941e9a766af616fd1381e08832b13cb",
    "unit-test": "d158e23fd9c8f178ade649edb56429d0ae5aa587b62ebe8f062a1c6eed209f42",
}


class ContractError(Exception):
    """A stable, value-free contract failure."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _structural_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            if value[0] == "'":
                return value[1:-1].replace("''", "'")
            raise ContractError("yaml_scalar_invalid") from None
        if not isinstance(parsed, str):
            raise ContractError("yaml_scalar_invalid")
        return parsed
    return value


def _split_inline(value: str) -> list[str]:
    pieces: list[str] = []
    start = 0
    quote = ""
    depth = 0
    for index, char in enumerate(value):
        if quote:
            if char == quote and (index == 0 or value[index - 1] != "\\"):
                quote = ""
        elif char in "'\"":
            quote = char
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
        elif char == "," and depth == 0:
            pieces.append(value[start:index].strip())
            start = index + 1
    pieces.append(value[start:].strip())
    return pieces


def _scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"{}", "{ }"}:
        return {}
    if value in {"[]", "[ ]"}:
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [_scalar(item) for item in _split_inline(inner)]
    value = _unquote(value)
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if re.fullmatch(r"-?[0-9]+", value):
        return int(value)
    return value


def _key_value(line: str) -> tuple[str, str]:
    quote = ""
    depth = 0
    for index, char in enumerate(line):
        if quote:
            if char == quote and (index == 0 or line[index - 1] != "\\"):
                quote = ""
        elif char in "'\"":
            quote = char
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
        elif char == ":" and depth == 0:
            key = _unquote(line[:index].strip())
            if not key:
                raise ContractError("yaml_key_invalid")
            return key, line[index + 1 :].strip()
    raise ContractError("yaml_mapping_invalid")


def _meaningful_lines(text: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if "\t" in raw[:indent]:
            raise ContractError("yaml_tabs_unsupported")
        rows.append((indent, raw[indent:]))
    return rows


def _parse_block(rows: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(rows) or rows[index][0] < indent:
        return {}, index
    if rows[index][0] != indent:
        raise ContractError("yaml_indent_invalid")
    sequence = rows[index][1].startswith("-")
    value: Any = [] if sequence else {}
    seen: set[str] = set()
    while index < len(rows) and rows[index][0] == indent:
        content = rows[index][1]
        if sequence:
            if not content.startswith("-"):
                raise ContractError("yaml_sequence_invalid")
            item = content[1:].strip()
            index += 1
            if not item:
                if index < len(rows) and rows[index][0] > indent:
                    parsed, index = _parse_block(rows, index, rows[index][0])
                else:
                    parsed = None
            elif item in {"|", ">"}:
                parsed, index = _parse_literal(rows, index, indent, item == ">")
            elif re.search(r":(?:\s|$)", item) and not item.startswith(("http://", "https://")):
                key, scalar = _key_value(item)
                parsed = {key: _scalar(scalar)} if scalar else {key: {}}
                if index < len(rows) and rows[index][0] > indent:
                    child, index = _parse_block(rows, index, rows[index][0])
                    if scalar:
                        if not isinstance(child, dict):
                            raise ContractError("yaml_sequence_mapping_invalid")
                        parsed.update(child)
                    elif isinstance(parsed[key], dict):
                        parsed[key] = child
            else:
                parsed = _scalar(item)
            value.append(parsed)
            continue
        key, scalar = _key_value(content)
        if key in seen:
            raise ContractError("yaml_duplicate_key")
        seen.add(key)
        index += 1
        if scalar in {"|", ">"}:
            parsed, index = _parse_literal(rows, index, indent, scalar == ">")
        elif scalar:
            parsed = _scalar(scalar)
        elif index < len(rows) and rows[index][0] > indent:
            parsed, index = _parse_block(rows, index, rows[index][0])
        else:
            parsed = {}
        value[key] = parsed
    return value, index


def _parse_literal(rows: list[tuple[int, str]], index: int, parent_indent: int, folded: bool) -> tuple[str, int]:
    if index >= len(rows) or rows[index][0] <= parent_indent:
        return "", index
    child_indent = rows[index][0]
    chunks: list[str] = []
    while index < len(rows) and rows[index][0] > parent_indent:
        current_indent, content = rows[index]
        chunks.append(" " * max(0, current_indent - child_indent) + content)
        index += 1
    return (" ".join(chunks) if folded else "\n".join(chunks)) + "\n", index


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        raise ContractError("ci_read_failed") from None
    rows = _meaningful_lines(text)
    if not rows:
        raise ContractError("yaml_empty")
    parsed, index = _parse_block(rows, 0, rows[0][0])
    if index != len(rows) or not isinstance(parsed, dict):
        raise ContractError("yaml_root_invalid")
    return parsed


def _as_mapping(value: Any, code: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(code)
    return value


def _as_list(value: Any, code: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError(code)
    return value


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return ""


def _github_job_text(job: dict[str, Any]) -> str:
    steps = _as_list(job.get("steps"), "github_steps_invalid")
    chunks: list[str] = []
    for step in steps:
        if isinstance(step, dict):
            chunks.append(_text(step.get("run")))
            chunks.append(json.dumps(step, ensure_ascii=True, sort_keys=True))
    return "\n".join(chunks)


def _direct_run_lines(steps: list[Any]) -> set[str]:
    """Return commands outside shell/PowerShell conditional blocks."""
    direct: set[str] = set()
    for step in steps:
        if not isinstance(step, dict) or not isinstance(step.get("run"), str):
            continue
        shell = _text(step.get("shell")).lower()
        powershell = shell in {"pwsh", "powershell"}
        depth = 0
        for raw_line in step["run"].splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if powershell:
                closes = line.startswith("}")
                if closes:
                    depth = max(0, depth - 1)
                control = line.startswith(("if ", "if(", "elseif ", "else ", "foreach ", "for ", "while "))
                if depth == 0 and not closes and not control:
                    direct.add(line)
                depth += line.count("{") - line.count("}")
                depth = max(0, depth)
                continue
            closes = bool(re.match(r"^(?:fi|done|esac)(?:\s*;?\s*(?:#.*)?)?$", line)) or line in {"}", ")"}
            if closes:
                depth = max(0, depth - 1)
            function_start = bool(
                re.match(
                    r"^(?:(?:function\s+)[A-Za-z_][A-Za-z0-9_]*(?:\s*\(\s*\))?|[A-Za-z_][A-Za-z0-9_]*\s*\(\s*\))\s*\{\s*$",
                    line,
                )
            )
            group_start = line in {"{", "("}
            control = line.startswith(("if ", "for ", "while ", "until ", "case ")) or function_start or group_start
            if depth == 0 and not closes and not control:
                direct.add(line)
            if control and (
                " then" in line
                or line.endswith("then")
                or line.startswith(("for ", "while ", "until ", "case "))
                or function_start
                or group_start
            ):
                depth += 1
    return direct


def _gitlab_job_text(job: dict[str, Any]) -> str:
    scripts = _as_list(job.get("script"), "gitlab_script_invalid")
    if not all(isinstance(item, str) for item in scripts):
        raise ContractError("gitlab_script_invalid")
    return "\n".join(scripts)


def _walk(value: Any, path: str = "") -> list[tuple[str, Any]]:
    found: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            found.append((child_path, child))
            found.extend(_walk(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_walk(child, f"{path}[{index}]"))
    return found


def _check_no_bypass(data: dict[str, Any], platform: str, jobs: dict[str, Any]) -> None:
    bad_keys = {"allow_failure", "continue-on-error", "only", "except", "changes", "paths", "paths-ignore", "branches", "branches-ignore", "rules"}
    for path, value in _walk(data):
        if path == "workflow.rules" or path.startswith("workflow.rules["):
            continue
        if path.rsplit(".", 1)[-1] in bad_keys:
            name = path.rsplit(".", 1)[-1]
            job = next((candidate for candidate in jobs if f"{candidate}." in path), "root")
            raise ContractError(f"bypass:{platform}:{job}:{name}")
        if path.endswith(".when") and value in {"manual", "delayed"}:
            job = next((candidate for candidate in jobs if f"{candidate}." in path), "root")
            raise ContractError(f"bypass:{platform}:{job}:when")
    joined = "\n".join(
        _github_job_text(job) if platform == "github" else _gitlab_job_text(job)
        for job in jobs.values()
        if isinstance(job, dict)
    )
    if re.search(r"\|\|\s*true|passWithNoTests|runner_absent_pre_feature|if\s*:\s*false", joined, re.IGNORECASE):
        raise ContractError(f"bypass:{platform}:script")
    if platform == "github":
        if re.search(r"permissions\s*:\s*\{?[^}]*write", joined, re.IGNORECASE):
            raise ContractError("bypass:github:permissions:write")
        if re.search(r"docker\s+(?:push|login)", joined, re.IGNORECASE):
            raise ContractError("bypass:github:publication")
    if platform == "gitlab" and re.search(r"docker\s+(?:push|login)", joined, re.IGNORECASE):
        raise ContractError("bypass:gitlab:publication")


def _check_github(path: Path) -> dict[str, Any]:
    data = load_yaml(path)
    allowed_root = {"name", "on", "permissions", "jobs"}
    if set(data) != allowed_root:
        raise ContractError("github_root_keys")
    triggers = _as_mapping(data["on"], "github_triggers_invalid")
    if triggers != {"push": {}, "pull_request": {}}:
        raise ContractError("github_push_trigger_missing")
    if data["permissions"] != {"contents": "read"}:
        raise ContractError("github_permissions_invalid")
    jobs = _as_mapping(data["jobs"], "github_jobs_invalid")
    unknown = sorted(set(jobs) - GITHUB_JOBS)
    if unknown:
        raise ContractError(f"unknown_job:github:{unknown[0]}")
    if set(jobs) != GITHUB_JOBS:
        raise ContractError("github_jobs_incomplete")
    _check_no_bypass(data, "github", jobs)
    action_refs: list[str] = []
    for name, raw in jobs.items():
        job = _as_mapping(raw, f"github_job_invalid:{name}")
        if job.get("timeout-minutes") != GITHUB_TIMEOUTS[name]:
            raise ContractError(f"timeout:github:{name}")
        if "if" in job:
            raise ContractError(f"bypass:github:{name}:if")
        runner = job.get("runs-on")
        expected_runner = "windows-2025" if name == "windows-package" else "ubuntu-24.04"
        if runner != expected_runner:
            raise ContractError(f"runner:github:{name}")
        if "permissions" in job:
            raise ContractError(f"permissions:github:{name}")
        if name in {"scanner", "backend"}:
            expected_git_env = {
                "GIT_CONFIG_COUNT": 1,
                "GIT_CONFIG_KEY_0": "safe.directory",
                "GIT_CONFIG_VALUE_0": "${{ github.workspace }}",
            }
            if job.get("env") != expected_git_env:
                raise ContractError(f"git_safe_directory:github:{name}")
        steps = _as_list(job.get("steps"), f"github_steps_invalid:{name}")
        if name in {"scanner", "backend"}:
            git_bootstrap = "apt-get update && apt-get install -y --no-install-recommends git"
            if (
                len(steps) < 2
                or not isinstance(steps[0], dict)
                or steps[0].get("run") != git_bootstrap
                or not isinstance(steps[1], dict)
                or steps[1].get("uses") != CHECKOUT
            ):
                raise ContractError(f"git_before_checkout:github:{name}")
        for step in steps:
            if not isinstance(step, dict):
                raise ContractError(f"github_step_invalid:{name}")
            if "if" in step:
                raise ContractError(f"bypass:github:{name}:step_if")
            if "uses" in step:
                ref = _text(step["uses"])
                action_refs.append(ref)
                if "@" not in ref or not re.fullmatch(r"[0-9a-f]{40}", ref.rsplit("@", 1)[1]):
                    raise ContractError(f"github_action_unpinned:{name}")
        if any(ref not in {CHECKOUT, SETUP_PYTHON, SETUP_NODE} for ref in action_refs):
            raise ContractError("github_action_allowlist")
        text = _github_job_text(job)
        direct_lines = _direct_run_lines(steps)
        if name in {"scanner", "backend", "frontend"}:
            container = _as_mapping(job.get("container"), f"github_container_missing:{name}")
            expected = {"scanner": POWERSHELL_IMAGE, "backend": PYTHON_IMAGE, "frontend": NODE_IMAGE}[name]
            if container.get("image") != expected:
                raise ContractError(f"github_image_pin:{name}")
        if name == "scanner":
            for literal in ("scripts/tests/bootstrap_scanner_contract.ps1", "scripts/tests/ci_seed_contract.ps1", "scripts/bootstrap_scan_credentials.ps1 -Tracked"):
                if literal not in text:
                    raise ContractError(f"scanner_command:github:{literal}")
            for command in (
                "run: pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1",
                "run: pwsh -NoProfile -File scripts/tests/ci_seed_contract.ps1",
                "run: pwsh -NoProfile -File scripts/bootstrap_scan_credentials.ps1 -Tracked",
            ):
                if command.removeprefix("run: ") not in direct_lines:
                    raise ContractError(f"scanner_command:github:direct:{command.removeprefix('run: ')}")
        if name == "backend":
            for literal in ("python -m pip install --require-hashes -r requirements.linux-ci.lock", "python scripts/test_all.py --backend"):
                if literal not in text:
                    raise ContractError(f"backend_command:github:{literal}")
            if "python scripts/test_all.py --backend" not in direct_lines:
                raise ContractError("backend_command:github:direct")
        if name == "frontend":
            if job.get("defaults") != {"run": {"working-directory": "frontend"}}:
                raise ContractError("frontend_directory:github")
            for literal in ("npm ci --ignore-scripts", "npm exec -- vitest run", "npm exec -- tsc --noEmit", "npm exec -- vite build"):
                if literal not in text:
                    raise ContractError(f"frontend_command:github:{literal}")
            for command in ("npm exec -- vitest run", "npm exec -- tsc --noEmit", "npm exec -- vite build"):
                if command not in direct_lines:
                    raise ContractError(f"frontend_command:github:direct:{command}")
        if name == "windows-package":
            uses_text = "\n".join(_text(step.get("uses")) for step in steps if isinstance(step, dict))
            with_values = {
                str(key): str(value)
                for step in steps
                if isinstance(step, dict) and isinstance(step.get("with"), dict)
                for key, value in step["with"].items()
            }
            required = ("actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065", "actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020", "backend/requirements-windows-x64.lock", "packaging/windows/build.ps1", "backend/tests/distribution/test_windows_contract.py", "Get-FileHash -Algorithm SHA256", "scripts/scan_credentials.py --path dist/ProjectB.exe")
            for literal in required:
                if literal not in text and literal not in uses_text:
                    raise ContractError(f"windows_command:github:{literal}")
            direct_windows = {
                "install": "python -m pip install --require-hashes -r backend/requirements-windows-x64.lock",
                "npm_ci": "npm.cmd --prefix frontend ci --ignore-scripts",
                "npm_build": "npm.cmd --prefix frontend run build",
                "contract": "python -m pytest backend/tests/distribution/test_windows_contract.py -q",
                "build": "powershell -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1 -Python python -Output dist/ProjectB.exe",
                "scan": "python scripts/scan_credentials.py --path dist/ProjectB.exe",
                "hash": "Get-FileHash -Algorithm SHA256 -LiteralPath dist/ProjectB.exe",
            }
            for command_name, command in direct_windows.items():
                if command not in direct_lines:
                    raise ContractError(f"windows_command:github:direct:{command_name}")
            if with_values.get("python-version") != "3.14.6" or with_values.get("node-version") != "24.18.0":
                raise ContractError("windows_tool_pin:github")
        if name == "oci-package":
            for literal in ("docker build --platform linux/amd64 --file packaging/oci/Dockerfile", "docker image inspect", "docker run -d --rm --read-only", "packaging/oci/smoke_test.ps1", "sbom.spdx.json", "THIRD_PARTY_NOTICES.md"):
                if literal not in text:
                    raise ContractError(f"oci_command:github:{literal}")
            direct_oci = {
                "build": "docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:ci .",
                "inspect_arch": "test \"$(docker image inspect --format '{{.Architecture}}' projectb-demo:ci)\" = \"amd64\"",
                "inspect_user": "test \"$(docker image inspect --format '{{.Config.User}}' projectb-demo:ci)\" = \"10001:10001\"",
                "resources": "docker run --rm --entrypoint /bin/sh projectb-demo:ci -c 'test -s /opt/projectb/licenses/sbom.spdx.json && test -s /opt/projectb/licenses/THIRD_PARTY_NOTICES.md && test -s /opt/projectb/licenses/OCI_THIRD_PARTY_NOTICES.md && test -s /opt/projectb/licenses/debian-packages.tsv'",
                "run": "docker run -d --rm --read-only --tmpfs /tmp/projectb-demo:rw,size=64m \\",
                "smoke": "pwsh -NoProfile -File packaging/oci/smoke_test.ps1 -Container projectb-demo-ci -Image projectb-demo:ci -BaseUrl http://127.0.0.1:7860",
            }
            for command_name, command in direct_oci.items():
                if command not in direct_lines:
                    raise ContractError(f"oci_command:github:direct:{command_name}")
        if _structural_digest(job) != GITHUB_JOB_DIGESTS[name]:
            raise ContractError(f"github_steps_drift:{name}")
    if action_refs.count(CHECKOUT) != 5 or action_refs.count(SETUP_PYTHON) != 1 or action_refs.count(SETUP_NODE) != 1 or len(action_refs) != 7:
        raise ContractError("github_action_refs")
    if any(ref not in {CHECKOUT, SETUP_PYTHON, SETUP_NODE} for ref in action_refs):
        raise ContractError("github_action_allowlist")
    return jobs


def _check_gitlab(path: Path) -> dict[str, Any]:
    data = load_yaml(path)
    allowed_root = {"stages", "workflow", *GITLAB_JOBS}
    unknown_root = sorted(set(data) - allowed_root)
    if unknown_root:
        raise ContractError(f"unknown_job:gitlab:{unknown_root[0]}")
    if data.get("stages") != ["test"]:
        raise ContractError("gitlab_stages")
    workflow = _as_mapping(data.get("workflow"), "gitlab_workflow_missing")
    rules = _as_list(workflow.get("rules"), "gitlab_workflow_rules")
    if len(rules) != 2 or rules[0] != {"if": '$CI_PIPELINE_SOURCE == "push"'} or rules[1] != {"when": "never"}:
        raise ContractError("gitlab_push_trigger_missing")
    jobs = {name: data[name] for name in GITLAB_JOBS if name in data}
    if set(jobs) != GITLAB_JOBS:
        raise ContractError("gitlab_jobs_incomplete")
    _check_no_bypass(data, "gitlab", jobs)
    for name, raw in jobs.items():
        job = _as_mapping(raw, f"gitlab_job_invalid:{name}")
        if job.get("timeout") != GITLAB_TIMEOUTS[name]:
            raise ContractError(f"timeout:gitlab:{name}")
        text = _gitlab_job_text(job)
        if name == "unit-test":
            image = job.get("image")
            if not isinstance(image, dict) or image.get("name") != POWERSHELL_IMAGE:
                raise ContractError("gitlab_image_pin:unit-test")
            if "unit-test" not in data:
                raise ContractError("gitlab_unit_test_missing")
            for literal in ("scripts/tests/bootstrap_scanner_contract.ps1", "scripts/tests/ci_seed_contract.ps1", "scripts/bootstrap_scan_credentials.ps1 -Tracked"):
                if literal not in text:
                    raise ContractError(f"scanner_command:gitlab:{literal}")
            unit_direct = _direct_run_lines(
                [{"run": item} for item in _as_list(job.get("script"), "gitlab_script_invalid")]
            )
            for command in (
                "pwsh -NoProfile -File scripts/tests/bootstrap_scanner_contract.ps1",
                "pwsh -NoProfile -File scripts/tests/ci_seed_contract.ps1",
                "pwsh -NoProfile -File scripts/bootstrap_scan_credentials.ps1 -Tracked",
            ):
                if command not in unit_direct:
                    raise ContractError(f"scanner_command:gitlab:direct:{command}")
        if name == "backend":
            if job.get("image") != PYTHON_IMAGE:
                raise ContractError("gitlab_image_pin:backend")
            for literal in ("python -m pip install --require-hashes -r requirements.linux-ci.lock", "python scripts/test_all.py --backend"):
                if literal not in text:
                    raise ContractError(f"backend_command:gitlab:{literal}")
            if "python scripts/test_all.py --backend" not in _direct_run_lines([{"run": item} for item in _as_list(job.get("script"), "gitlab_script_invalid")]):
                raise ContractError("backend_command:gitlab:direct")
        if name == "frontend":
            if job.get("image") != NODE_IMAGE:
                raise ContractError("gitlab_image_pin:frontend")
            for literal in ("npm ci --ignore-scripts", "npm exec -- vitest run", "npm exec -- tsc --noEmit", "npm exec -- vite build"):
                if literal not in text:
                    raise ContractError(f"frontend_command:gitlab:{literal}")
            for command in ("npm exec -- vitest run", "npm exec -- tsc --noEmit", "npm exec -- vite build"):
                if command not in _direct_run_lines([{"run": item} for item in _as_list(job.get("script"), "gitlab_script_invalid")]):
                    raise ContractError(f"frontend_command:gitlab:direct:{command}")
            gitlab_direct = _direct_run_lines([{"run": item} for item in _as_list(job.get("script"), "gitlab_script_invalid")])
            if "cd frontend" not in gitlab_direct:
                raise ContractError("frontend_directory:gitlab")
        if name == "oci-package":
            if job.get("tags") != ["projectb-docker-linux-amd64"]:
                raise ContractError("gitlab_runner_tag")
            for literal in ("29.1.2", "DOCKER_BUILDKIT", "PROJECTB_RUNNER_PRIVILEGED", "PROJECTB_RUNNER_HOST_MOUNTS", "docker buildx version", "name=seccomp", "docker build --platform linux/amd64 --file packaging/oci/Dockerfile", "docker image inspect", "docker run -d --rm --read-only", "packaging/oci/smoke_test.ps1", "sbom.spdx.json", "THIRD_PARTY_NOTICES.md"):
                if literal not in text:
                    raise ContractError(f"oci_command:gitlab:{literal}")
            direct_oci = {
                "build": 'docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag "$IMAGE_TAG" .',
                "inspect_arch": 'test "$(docker image inspect --format \'{{.Architecture}}\' "$IMAGE_TAG")" = "amd64"',
                "inspect_user": 'test "$(docker image inspect --format \'{{.Config.User}}\' "$IMAGE_TAG")" = "10001:10001"',
                "resources": "docker run --rm --entrypoint /bin/sh \"$IMAGE_TAG\" -c 'test -s /opt/projectb/licenses/sbom.spdx.json && test -s /opt/projectb/licenses/THIRD_PARTY_NOTICES.md && test -s /opt/projectb/licenses/OCI_THIRD_PARTY_NOTICES.md && test -s /opt/projectb/licenses/debian-packages.tsv'",
                "run": 'docker run -d --rm --read-only --tmpfs /tmp/projectb-demo:rw,size=64m -e PROJECTB_DEMO_LOCAL_SMOKE=1 -p 127.0.0.1:${HOST_PORT}:7860 --name "$CONTAINER_NAME" "$IMAGE_TAG"',
                "smoke": 'pwsh -NoProfile -File packaging/oci/smoke_test.ps1 -Container "$CONTAINER_NAME" -Image "$IMAGE_TAG" -BaseUrl "http://127.0.0.1:${HOST_PORT}"',
            }
            for command_name, command in direct_oci.items():
                if command not in _direct_run_lines([{"run": item} for item in _as_list(job.get("script"), "gitlab_script_invalid")]):
                    raise ContractError(f"oci_command:gitlab:direct:{command_name}")
        if _structural_digest(job) != GITLAB_JOB_DIGESTS[name]:
            if set(job) - {"stage", "timeout", "image", "script", "variables", "tags", "after_script"}:
                raise ContractError(f"gitlab_job_keys:{name}")
            raise ContractError(f"gitlab_script_drift:{name}")
    return jobs


def build_mapping(github_path: Path, gitlab_path: Path) -> dict[str, Any]:
    github = _check_github(github_path)
    gitlab = _check_gitlab(gitlab_path)
    return {
        "schema": "ci-contract-v1",
        "status": "pass",
        "platforms": {"github": "pass", "gitlab": "pass"},
        "jobs": {
            "github": sorted(github),
            "gitlab": sorted(gitlab),
        },
        "commands": {
            "backend": {
                "github": "python scripts/test_all.py --backend",
                "gitlab": "python scripts/test_all.py --backend",
            },
            "frontend": {
                "github": "npm exec -- vitest run; npm exec -- tsc --noEmit; npm exec -- vite build",
                "gitlab": "npm exec -- vitest run; npm exec -- tsc --noEmit; npm exec -- vite build",
            },
            "scanner": {
                "github": "pwsh bootstrap contract; seed contract; tracked credential scan",
                "gitlab": "pwsh bootstrap contract; seed contract; tracked credential scan",
            },
            "windows": {
                "github": "distribution contract; build.ps1; credential scan; SHA256",
            },
            "oci": {
                "github": "linux/amd64 build; inspect; resource check; smoke",
                "gitlab": "linux/amd64 build; inspect; resource check; smoke",
            },
        },
        "requirements": {
            "push_triggers": ["github:on.push", "gitlab:workflow.push"],
            "gitlab_unit_test": ["gitlab:unit-test"],
            "windows_package": ["github:windows-package"],
            "oci_package": ["github:oci-package", "gitlab:oci-package"],
            "pins": ["github:actions@sha", "github:container@digest", "gitlab:image@digest"],
            "lock_installs": ["github:backend", "github:frontend", "github:windows-package", "gitlab:backend", "gitlab:frontend"],
            "failure_propagation": ["github:strict-defaults", "gitlab:strict-defaults"],
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--github", type=Path)
    parser.add_argument("--gitlab", type=Path)
    parser.add_argument("--requirement")
    try:
        args, unknown = parser.parse_known_args(argv)
    except SystemExit:
        print("CI_CONTRACT_RED usage_invalid")
        return 3
    if unknown:
        print("CI_CONTRACT_RED usage_unknown_argument")
        return 3
    if args.requirement is not None and args.requirement not in {"all", "pins", "commands"}:
        print("CI_CONTRACT_RED usage_unknown_requirement")
        return 3
    github = (args.github or ROOT / ".github" / "workflows" / "ci.yml").resolve()
    gitlab = (args.gitlab or ROOT / ".gitlab-ci.yml").resolve()
    try:
        mapping = build_mapping(github, gitlab)
    except ContractError as error:
        print(f"CI_CONTRACT_RED {error.code}")
        return 2
    except (OSError, UnicodeError):
        print("CI_CONTRACT_RED ci_io_failed")
        return 2
    print(json.dumps(mapping, ensure_ascii=True, indent=2, sort_keys=True))
    print("CI_CONTRACT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
