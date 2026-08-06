"""Run ProjectB quality gates with no mode that can silently skip a suite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_mode(arguments: list[str]) -> str | None:
    if not arguments or arguments == ["--all"]:
        return "all"
    if len(arguments) == 1 and arguments[0] in {"--backend", "--frontend"}:
        return arguments[0][2:]
    return None


def run_child(command: list[str], *, cwd: Path) -> int:
    try:
        return subprocess.run(command, cwd=cwd, check=False, timeout=300).returncode
    except (OSError, subprocess.TimeoutExpired):
        return 70


def npm_command(root: Path) -> str:
    if sys.platform == "win32":
        runtimes = root / "tmp/toolchains/f01a/runtimes"
        candidates = sorted(runtimes.glob("node-v24.18.0-win-x64/npm.cmd"))
        if len(candidates) == 1 and candidates[0].is_file():
            return str(candidates[0])
    return "npm"


def build_commands(root: Path, mode: str, python: str, npm: str) -> list[list[str]]:
    commands: list[list[str]] = []
    if mode in {"all", "backend"}:
        discovered = sorted((root / "backend/tests").rglob("test_*.py")) if (root / "backend/tests").is_dir() else []
        commands.append([python, "-m", "pytest", "scripts/tests", *(path.as_posix() for path in discovered), "-q"])
    if mode in {"all", "frontend"}:
        commands.extend([
            [npm, "exec", "--", "vitest", "run"],
            [npm, "exec", "--", "tsc", "--noEmit"],
            [npm, "exec", "--", "vite", "build"],
        ])
    commands.extend([
        [python, "scripts/scan_credentials.py", "--tracked", "--staged"],
        [python, "scripts/verify_licenses.py"],
    ])
    return commands


def main(arguments: list[str]) -> int:
    mode = parse_mode(arguments)
    if mode is None:
        print("TEST_ALL_ERROR usage")
        return 3
    python = sys.executable
    npm = npm_command(ROOT)
    for command in build_commands(ROOT, mode, python, npm):
        if command[0] == npm:
            code = run_child(command, cwd=ROOT / "frontend")
        else:
            code = run_child(command, cwd=ROOT)
        if code:
            print(f"TEST_ALL_ERROR child_exit={code}")
            return code
    print(f"TEST_ALL_PASS mode={mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
