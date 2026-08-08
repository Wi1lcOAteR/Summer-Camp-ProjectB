"""Fail-closed credential scanner for paths, tracked files, and Git index blobs."""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import re
import subprocess
import sys
import stat
from pathlib import Path


DIRECT_RULES = {
    "provider_api_key": re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,200}(?![A-Za-z0-9_-])"),
    "github_token": re.compile(r"(?<![A-Za-z0-9_-])(?:ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9]{20,255}(?![A-Za-z0-9_-])"),
    "aws_access_key": re.compile(r"(?<![A-Za-z0-9_-])(?:AKIA|ASIA)[A-Z0-9]{16}(?![A-Za-z0-9_-])"),
    "google_api_key": re.compile(r"(?<![A-Za-z0-9_-])AIza[A-Za-z0-9_-]{35}(?![A-Za-z0-9_-])"),
    "slack_token": re.compile(r"(?<![A-Za-z0-9_-])(?:xoxb-|xoxp-|xoxa-|xoxr-|xoxs-)[A-Za-z0-9-]{10,200}(?![A-Za-z0-9_-])"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
}

ASSIGNMENT = re.compile(
    r"(?im)(?<![A-Za-z0-9_-])(?:api_key|api-key|apikey|access_token|auth_token|client_secret|password|passwd|secret|token)[ \t]*[:=][ \t]*(?:(?:\"(?P<double>(?:[^\"\\\r\n]|\\[\"\\])*)\")|(?:'(?P<single>(?:[^'\\\r\n]|\\['\\])*)')|(?P<plain>[A-Za-z0-9_./+=:@-]{8,512})(?![A-Za-z0-9_./+=:@-]))"
)
ENCODED = (
    ("base64", re.compile(r"(?<![A-Za-z0-9+/=])(?P<value>[A-Za-z0-9+/]{16,4096}={0,2})(?![A-Za-z0-9+/=])")),
    ("base64url", re.compile(r"(?<![A-Za-z0-9_=-])(?P<value>[A-Za-z0-9_-]{16,4096}={0,2})(?![A-Za-z0-9_=-])")),
    ("hex", re.compile(r"(?<![0-9A-Fa-f])(?P<value>[0-9A-Fa-f]{32,8192})(?![0-9A-Fa-f])")),
)
TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".jsonl", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".conf", ".env",
    ".example", ".py", ".pyi", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".html", ".css", ".scss",
    ".sql", ".ps1", ".psm1", ".psd1", ".sh", ".bash", ".cmd", ".bat", ".lock", ".in",
}
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".ico", ".zip", ".gz", ".7z", ".exe", ".dll", ".pyd", ".so", ".woff", ".woff2", ".ttf", ".mp3", ".mp4", ".sqlite", ".db"}
EXTENSIONLESS = {".gitignore", ".gitattributes", ".dockerignore", ".python-version", ".npmrc", "Dockerfile", "Makefile", "LICENSE", "NOTICE", "uv-LICENSE-APACHE", "uv-LICENSE-MIT", "cpython-LICENSE", "node-LICENSE", "npm-LICENSE"}
SAFE_ASSIGNMENTS = {"example", "placeholder", "changeme", "not-set", "none", "null", "redacted"}


class ScanError(Exception):
    def __init__(self, code: str, source: str = "", path: str = "") -> None:
        self.code, self.source, self.path = code, source, path


def receipt(source: str, path: str = "", rule: str = "", code: str = "") -> str:
    record: dict[str, str] = {}
    if code:
        record["code"] = code
    if source:
        record["source"] = source
    if path:
        record["path"] = path
    if rule:
        record["rule"] = rule
    return json.dumps(record, separators=(",", ":"), ensure_ascii=True)


def decode_text(raw: bytes) -> str:
    if raw.startswith((b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff")):
        raise ValueError("utf32")
    if raw.startswith(b"\xff\xfe"):
        text = raw[2:].decode("utf-16-le", errors="strict")
    elif raw.startswith(b"\xfe\xff"):
        text = raw[2:].decode("utf-16-be", errors="strict")
    else:
        text = raw.removeprefix(b"\xef\xbb\xbf").decode("utf-8", errors="strict")
    if "\ufffd" in text:
        raise ValueError("replacement")
    return text


def is_assignment_secret(text: str) -> bool:
    for match in ASSIGNMENT.finditer(text):
        value = match.group("double") or match.group("single") or match.group("plain") or ""
        value = re.sub(r"\\([\\\"'])", r"\1", value)
        if not 8 <= len(value) <= 512:
            continue
        clean = value.strip("\t\n\v\f\r ")
        if clean.casefold() in SAFE_ASSIGNMENTS:
            continue
        if re.fullmatch(r"<[^<>\r\n]+>|\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})|\[[^\]\r\n]*redacted[^\]\r\n]*\]", clean, re.I):
            continue
        return True
    return False


def is_encoded_secret(text: str) -> bool:
    for family, pattern in ENCODED:
        for match in pattern.finditer(text):
            value = match.group("value")
            try:
                if family == "hex":
                    decoded = bytes.fromhex(value)
                else:
                    canonical = value.replace("-", "+").replace("_", "/") if family == "base64url" else value
                    if len(canonical) % 4:
                        continue
                    decoded = base64.b64decode(canonical, validate=True)
                    if base64.b64encode(decoded).decode("ascii") != canonical:
                        continue
                decoded_text = decoded.decode("utf-8", errors="strict")
            except (UnicodeDecodeError, ValueError, binascii.Error):
                continue
            if any(rule.search(decoded_text) for rule in DIRECT_RULES.values()):
                return True
    return False


def find_rules(text: str) -> list[str]:
    found = [name for name, pattern in DIRECT_RULES.items() if pattern.search(text)]
    if is_assignment_secret(text):
        found.append("assignment_secret")
    if is_encoded_secret(text):
        found.append("encoded_secret")
    return sorted(set(found))


def git(repo: Path, *arguments: str) -> bytes:
    try:
        completed = subprocess.run(["git", *arguments], cwd=repo, capture_output=True, check=False, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ScanError("git_list_failed") from error
    if completed.returncode:
        raise ScanError("git_list_failed")
    return completed.stdout


def tracked_paths(repo: Path) -> list[str]:
    try:
        return [entry.decode("utf-8", errors="strict") for entry in git(repo, "ls-files", "-z").split(b"\0") if entry]
    except UnicodeDecodeError as error:
        raise ScanError("git_list_failed") from error


def index_entries(repo: Path) -> dict[str, str]:
    try:
        rows = git(repo, "ls-files", "--stage", "-z").split(b"\0")
        entries: dict[str, str] = {}
        for row in rows:
            if not row:
                continue
            metadata, raw_path = row.split(b"\t", 1)
            mode, oid, stage = metadata.decode("ascii").split()
            path = raw_path.decode("utf-8", errors="strict")
            if stage != "0":
                raise ScanError("index_entry_failed", "index", path)
            if mode not in {"100644", "100755"}:
                raise ScanError("index_mode_unsupported", "index", path)
            if path in entries:
                raise ScanError("index_entry_failed", "index", path)
            entries[path] = oid
        return entries
    except (UnicodeDecodeError, ValueError) as error:
        raise ScanError("git_list_failed") from error


def assert_repo_path(path: str, source: str) -> None:
    candidate = Path(path)
    if not path or "\\" in path or path.startswith("/") or candidate.is_absolute() or path.endswith("/") or "//" in path or any(part in {"", ".", ".."} for part in path.split("/")):
        raise ScanError("path_escape", source, path)


def read_worktree(repo: Path, path: str) -> bytes | None:
    assert_repo_path(path, "worktree")
    candidate = repo.joinpath(*path.split("/"))
    try:
        candidate.relative_to(repo)
        cursor = repo
        for part in path.split("/"):
            cursor /= part
            attributes = getattr(cursor.lstat(), "st_file_attributes", 0)
            if cursor.is_symlink() or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
                raise ScanError("reparse_point", "worktree", path)
        if not candidate.is_file():
            raise ScanError("read_failed", "worktree", path)
        return candidate.read_bytes()
    except FileNotFoundError:
        return None
    except OSError as error:
        raise ScanError("read_failed", "worktree", path) from error


def supports_text(path: str, source: str = "") -> bool:
    name = Path(path).name
    suffix = Path(path).suffix.lower()
    if suffix in BINARY_SUFFIXES:
        return False
    if suffix not in TEXT_SUFFIXES and name not in EXTENSIONLESS:
        raise ScanError("unsupported_file_type", source, path)
    return True


def scan_bytes(source: str, path: str, raw: bytes) -> list[dict[str, str]]:
    if not supports_text(path, source):
        return []
    marked = raw.startswith((b"\xff\xfe", b"\xfe\xff", b"\xef\xbb\xbf"))
    if not marked and b"\0" in raw:
        raise ScanError("nul_unmarked", source, path)
    try:
        text = decode_text(raw)
    except UnicodeError as error:
        raise ScanError("decode_failed", source, path) from error
    except ValueError as error:
        raise ScanError("decode_failed", source, path) from error
    return [{"source": source, "path": path, "rule": rule} for rule in find_rules(text)]


def scan_git_snapshot(
    repo: Path, *, include_tracked: bool, include_staged: bool
) -> tuple[list[dict[str, str]], int]:
    if not (repo / ".git").exists():
        raise ScanError("git_root_failed")
    findings: list[dict[str, str]] = []
    count = 0
    if include_tracked:
        paths = tracked_paths(repo)
        for path in paths:
            raw = read_worktree(repo, path)
            if raw is None:
                continue
            if supports_text(path, "worktree"):
                count += 1
                findings.extend(scan_bytes("worktree", path, raw))
    if include_staged:
        entries = index_entries(repo)
        for path, oid in entries.items():
            assert_repo_path(path, "index")
            try:
                raw = git(repo, "cat-file", "blob", oid)
            except ScanError as error:
                raise ScanError("read_failed", "index", path) from error
            if supports_text(path, "index"):
                count += 1
                findings.extend(scan_bytes("index", path, raw))
    return sorted(findings, key=lambda row: (row["source"], row["path"], row["rule"])), count


def scan_git_sources(repo: Path, *, include_tracked: bool, include_staged: bool) -> list[dict[str, str]]:
    findings, _ = scan_git_snapshot(repo, include_tracked=include_tracked, include_staged=include_staged)
    return findings


def main(arguments: list[str]) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--path")
    parser.add_argument("--root")
    parser.add_argument("--tracked", action="store_true")
    parser.add_argument("--staged", action="store_true")
    try:
        namespace, extras = parser.parse_known_args(arguments)
    except SystemExit:
        extras = ["invalid"]
        namespace = argparse.Namespace(path=None, root=None, tracked=False, staged=False)
    if extras or (not namespace.path and not namespace.tracked and not namespace.staged) or (namespace.path and (namespace.tracked or namespace.staged)):
        print(receipt("path", code="usage_missing_scope"))
        return 3
    try:
        if namespace.path:
            supplied = namespace.path.replace("\\", "/")
            if supplied.startswith("./"):
                supplied = supplied[2:]
            if namespace.root:
                repo = Path(namespace.root).resolve()
                raw = read_worktree(repo, supplied)
                if raw is None:
                    raise ScanError("read_failed", "path", supplied)
            else:
                target = Path(namespace.path)
                if not target.is_file() or target.is_symlink():
                    raise ScanError("read_failed", "path", supplied)
                raw = target.read_bytes()
            findings = scan_bytes("path", supplied, raw)
            count = 1 if supports_text(supplied, "path") else 0
        else:
            repo = Path.cwd()
            findings, count = scan_git_snapshot(repo, include_tracked=namespace.tracked, include_staged=namespace.staged)
    except ScanError as error:
        print(receipt(error.source, error.path, code=error.code))
        return 3
    if findings:
        for finding in findings:
            print(receipt(finding["source"], finding["path"], finding["rule"]))
        return 2
    print(f"CREDENTIAL_SCAN_PASS files={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
