"""Produce a fail-closed, redacted inventory for the repository cleanup plan."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


CHECK_NAMES = ("containment", "process_use", "reference_scan", "credential_scan", "ownership")
CHECK_VALUES = {"pass", "fail", "unknown", "not_applicable"}
EXCLUDED_TREES = (
    ".git",
    ".worktrees",
    "node_modules",
    "frontend/node_modules",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "tmp/toolchains",
)
GENERATED_TREES = ("frontend/dist", "frontend/test-results", "test-results")
TEXT_SUFFIXES = {".md", ".py", ".pyi", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".json", ".toml", ".yml", ".yaml", ".ps1"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def normalized(path: Path) -> str:
    return path.as_posix().replace("\\", "/")


def is_reparse_or_link(path: Path) -> bool:
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except OSError:
        return False
    return path.is_symlink() or bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def git(root: Path, *args: str) -> bytes | None:
    try:
        result = subprocess.run(["git", *args], cwd=root, capture_output=True, check=False, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def git_paths(root: Path, *args: str) -> list[str]:
    raw = git(root, *args, "-z")
    if raw is None:
        return []
    try:
        return sorted(item.decode("utf-8") for item in raw.split(b"\0") if item)
    except UnicodeDecodeError:
        return []


def safe_relative(path: str) -> bool:
    pure = Path(path)
    return bool(path) and not pure.is_absolute() and "\\" not in path and all(part not in {"", ".", ".."} for part in path.split("/"))


def is_excluded_path(path: str) -> bool:
    return any(path == excluded or path.startswith(f"{excluded}/") for excluded in EXCLUDED_TREES)


def tracked_and_untracked(root: Path) -> dict[str, str]:
    candidates: dict[str, str] = {}
    for path in git_paths(root, "ls-files"):
        if safe_relative(path) and not is_excluded_path(path):
            candidates[path] = "tracked"
    for path in git_paths(root, "ls-files", "--others", "--exclude-standard"):
        if safe_relative(path) and not is_excluded_path(path):
            candidates.setdefault(path, "untracked")
    return candidates


def staged_submodules(root: Path) -> set[str]:
    raw = git(root, "ls-files", "--stage", "-z")
    if raw is None:
        return set()
    result: set[str] = set()
    for row in raw.split(b"\0"):
        if not row:
            continue
        try:
            metadata, raw_path = row.split(b"\t", 1)
            mode = metadata.decode("ascii").split(maxsplit=1)[0]
            path = raw_path.decode("utf-8")
        except (UnicodeDecodeError, ValueError):
            continue
        if mode == "160000":
            result.add(path)
    return result


def status_for(root: Path) -> str:
    if not (root / ".git").exists():
        return "unknown"
    output = git(root, "status", "--short", "--untracked-files=all")
    if output is None:
        return "unknown"
    return "clean" if not output else "dirty"


def registered_worktrees(root: Path) -> set[Path]:
    raw = git(root, "worktree", "list", "--porcelain")
    if raw is None:
        return set()
    result: set[Path] = set()
    for row in raw.splitlines():
        if not row.startswith(b"worktree "):
            continue
        try:
            result.add(Path(row[9:].decode("utf-8")).resolve())
        except UnicodeDecodeError:
            continue
    return result


def first_reparse_component(root: Path, relative_path: str) -> Path | None:
    cursor = root
    for part in relative_path.split("/"):
        cursor /= part
        if is_reparse_or_link(cursor):
            return cursor
    return None


def check_set(*, containment: str = "pass", ownership: str = "unknown") -> dict[str, str]:
    result = {
        "containment": containment,
        "process_use": "unknown",
        "reference_scan": "unknown",
        "credential_scan": "unknown",
        "ownership": ownership,
    }
    assert set(result) == set(CHECK_NAMES)
    assert set(result.values()) <= CHECK_VALUES
    return result


def record(path: str, kind: str, owner_status: str, reason: str, evidence_id: str, *, checks: dict[str, str] | None = None) -> dict[str, Any]:
    resolved_checks = checks or check_set(ownership="pass" if owner_status in {"tracked", "untracked", "current_checkout"} else "unknown")
    return {
        "path": path,
        "kind": kind,
        "owner_status": owner_status,
        "action": "retain",
        "reason": reason,
        "evidence_id": evidence_id,
        "checks": resolved_checks,
    }


class PassContextVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.context: list[str] = []
        self.contexts: list[str] = []

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.context.append("except")
        self.generic_visit(node)
        self.context.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.context.append("function")
        self.generic_visit(node)
        self.context.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.context.append("function")
        self.generic_visit(node)
        self.context.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.context.append("class")
        self.generic_visit(node)
        self.context.pop()

    def visit_Pass(self, node: ast.Pass) -> None:
        self.contexts.append(self.context[-1] if self.context else "module")


def text_for(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
        if b"\0" in raw:
            return None
        return raw.decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError):
        return None


def file_sha256(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def python_analysis(text: str) -> dict[str, Any]:
    try:
        tree = ast.parse(text, type_comments=True)
    except SyntaxError:
        return {"parse": "fail", "pass_contexts": [], "type_ignores": 0}
    visitor = PassContextVisitor()
    visitor.visit(tree)
    return {
        "parse": "pass",
        "pass_contexts": sorted(set(visitor.contexts)),
        "type_ignores": len(tree.type_ignores),
    }


def markdown_analysis(path: Path, text: str) -> dict[str, Any]:
    checked = broken = 0
    for match in MARKDOWN_LINK.finditer(text):
        raw_target = match.group(1).split("#", 1)[0]
        if not raw_target or "://" in raw_target or raw_target.startswith(("mailto:", "#", "/")):
            continue
        checked += 1
        target = path.parent / raw_target
        if any(is_reparse_or_link(parent) for parent in (path.parent, *target.parents) if parent.exists()):
            broken += 1
        elif not target.exists():
            broken += 1
    path_text = normalized(path)
    classification = "archive_document" if "/docs/archive/" in f"/{path_text}" else "active_document"
    if classification == "active_document" and path.name in {"AGENT_LOG.md", "SPEC_PROCESS.md", "PROJECT_AUDIT.md"}:
        classification = "historical_process_document"
    return {"classification": classification, "links": {"checked": checked, "broken": broken}}


def analysis_for(path: Path, text: str | None) -> dict[str, Any]:
    suffix = path.suffix.lower()
    analysis: dict[str, Any] = {"quality": {"ruff_f401_f841": "not_run"}}
    if text is None:
        return analysis
    if suffix == ".py":
        analysis["python"] = python_analysis(text)
    if suffix in {".ts", ".tsx", ".js", ".jsx", ".mjs"}:
        analysis["typescript"] = {"unused_symbol_check": "not_run"}
        analysis["routes"] = {"metadata_reads": len(re.findall(r"\b(?:icon|id|path|label)\b", text))}
    if suffix == ".md":
        analysis["markdown"] = markdown_analysis(path, text)
    return analysis


def coordination_relative(coordination_root: Path, path: Path) -> str:
    try:
        return normalized(path.relative_to(coordination_root)) or "."
    except ValueError:
        return normalized(path)


def discover_roots(checkout_root: Path | None) -> tuple[Path, Path]:
    probe_root = (checkout_root or Path.cwd()).resolve()
    output = git(probe_root, "rev-parse", "--show-toplevel")
    if output is None:
        raise ValueError("checkout_root_unavailable")
    checkout_root = Path(output.decode("utf-8").strip()).resolve()
    common_dir = git(checkout_root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if common_dir is None:
        raise ValueError("git_common_dir_unavailable")
    coordination_root = Path(common_dir.decode("utf-8").strip()).parent.resolve()
    return checkout_root, coordination_root


def add_metadata_record(records: list[dict[str, Any]], coordination_root: Path, target: Path, *, kind: str, owner_status: str, reason: str, registration: str | None = None) -> None:
    relative = coordination_relative(coordination_root, target)
    entry = record(relative, kind, owner_status, reason, "metadata")
    entry["git_status"] = status_for(target) if target.is_dir() and not is_reparse_or_link(target) else "unknown"
    if registration is not None:
        entry["registration"] = registration
    if is_reparse_or_link(target):
        entry["kind"] = "symlink"
        try:
            entry["symlink_target"] = normalized(Path(os.readlink(target)))
        except OSError:
            entry["symlink_target"] = "unreadable"
        entry["checks"] = check_set(containment="fail", ownership="unknown")
        entry["reason"] = "symlink_or_reparse_point"
    records.append(entry)


def build_inventory(checkout_root: Path, coordination_root: Path | None = None) -> dict[str, Any]:
    checkout_root = checkout_root.resolve()
    if coordination_root is None:
        _, coordination_root = discover_roots(checkout_root)
    coordination_root = coordination_root.resolve()
    records: list[dict[str, Any]] = []
    add_metadata_record(records, coordination_root, coordination_root, kind="coordination_root", owner_status="coordination_root", reason="hard_retain")
    add_metadata_record(records, coordination_root, checkout_root, kind="checkout", owner_status="current_checkout", reason="hard_retain")

    # Inspect only coordination-root entries; never descend into sibling checkouts.
    try:
        top_level = sorted(coordination_root.iterdir(), key=lambda item: item.name.casefold())
    except OSError:
        top_level = []
    for entry_path in top_level:
        if entry_path == checkout_root or entry_path.name in {".git", ".worktrees"}:
            continue
        add_metadata_record(records, coordination_root, entry_path, kind="coordination_entry", owner_status="metadata_only", reason="sibling_not_content_scanned")

    worktree_root = coordination_root / ".worktrees"
    registered = registered_worktrees(checkout_root)
    if worktree_root.is_dir() and not is_reparse_or_link(worktree_root):
        for entry_path in sorted(worktree_root.iterdir(), key=lambda entry: entry.name.casefold()):
            is_registered = entry_path.resolve() in registered
            add_metadata_record(
                records,
                coordination_root,
                entry_path,
                kind="worktree",
                owner_status="registered" if is_registered else "orphan_or_unknown",
                reason="hard_retain_worktree",
                registration="registered" if is_registered else "orphan_or_unknown",
            )

    candidates = tracked_and_untracked(checkout_root)
    submodules = staged_submodules(checkout_root)
    directory_candidates: set[str] = set()
    hashes: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    recorded_paths: set[str] = set()
    for source_path, owner_status in candidates.items():
        candidate = checkout_root.joinpath(*source_path.split("/"))
        path = coordination_relative(coordination_root, candidate)
        recorded_paths.add(path)
        for parent in Path(source_path).parents:
            if str(parent) != ".":
                directory_candidates.add(parent.as_posix())
        boundary = first_reparse_component(checkout_root, source_path)
        if boundary is not None:
            entry_record = record(path, "symlink", owner_status, "symlink_or_reparse_point", "content_boundary", checks=check_set(containment="fail", ownership="unknown"))
            try:
                entry_record["symlink_target"] = normalized(Path(os.readlink(boundary)))
            except OSError:
                entry_record["symlink_target"] = "unreadable"
            records.append(entry_record)
            continue
        if source_path in submodules:
            records.append(record(path, "submodule", owner_status, "submodule_retained", "git_index", checks=check_set(ownership="unknown")))
            continue
        if not candidate.is_file():
            records.append(record(path, "unreadable_candidate", owner_status, "not_regular_file", "content_boundary", checks=check_set(containment="fail", ownership="unknown")))
            continue
        entry_record = record(path, "file", owner_status, "inventory_only", "git_candidate")
        entry_record["analysis"] = analysis_for(candidate, text_for(candidate) if candidate.suffix.lower() in TEXT_SUFFIXES else None)
        digest = file_sha256(candidate)
        if digest:
            entry_record["sha256"] = digest
            hashes[digest].append(entry_record)
        records.append(entry_record)

    # Git does not consistently enumerate untracked Windows junctions. Record
    # their metadata at the checkout boundary without traversing through them.
    try:
        checkout_entries = list(checkout_root.iterdir())
    except OSError:
        checkout_entries = []
    for candidate in checkout_entries:
        path = coordination_relative(coordination_root, candidate)
        if path in recorded_paths or not is_reparse_or_link(candidate):
            continue
        entry_record = record(path, "symlink", "metadata_only", "symlink_or_reparse_point", "content_boundary", checks=check_set(containment="fail", ownership="unknown"))
        try:
            entry_record["symlink_target"] = normalized(Path(os.readlink(candidate)))
        except OSError:
            entry_record["symlink_target"] = "unreadable"
        records.append(entry_record)

    for directory in sorted(directory_candidates):
        candidate = checkout_root.joinpath(*directory.split("/"))
        if candidate.is_dir() and not is_reparse_or_link(candidate):
            records.append(record(coordination_relative(coordination_root, candidate), "directory", "derived_from_candidate", "directory_candidate", "git_candidate", checks=check_set(ownership="unknown")))

    # Runtime output is Git-ignored by design. Enumerate only its direct
    # children as metadata candidates, without reading any child content.
    runtime_root = checkout_root / "tmp"
    if runtime_root.is_dir() and not is_reparse_or_link(runtime_root):
        try:
            runtime_entries = sorted(runtime_root.iterdir(), key=lambda entry: entry.name.casefold())
        except OSError:
            runtime_entries = []
        for entry_path in runtime_entries:
            source_path = normalized(entry_path.relative_to(checkout_root))
            if source_path in EXCLUDED_TREES:
                continue
            add_metadata_record(
                records,
                coordination_root,
                entry_path,
                kind="directory_candidate" if entry_path.is_dir() else "runtime_file",
                owner_status="ignored_runtime_metadata",
                reason="runtime_candidate",
            )

    for generated in GENERATED_TREES:
        candidate = checkout_root.joinpath(*generated.split("/"))
        if candidate.exists() or is_reparse_or_link(candidate):
            add_metadata_record(
                records,
                coordination_root,
                candidate,
                kind="generated_tree",
                owner_status="generated_metadata",
                reason="generated_output_candidate",
            )

    for excluded in EXCLUDED_TREES:
        candidate = checkout_root.joinpath(*excluded.split("/"))
        if is_reparse_or_link(candidate):
            add_metadata_record(
                records,
                coordination_root,
                candidate,
                kind="symlink",
                owner_status="excluded",
                reason="symlink_or_reparse_point",
            )
        else:
            records.append(record(coordination_relative(coordination_root, candidate), "excluded_tree", "excluded", "content_scan_exclusion", "scope_boundary", checks=check_set(containment="not_applicable", ownership="unknown")))

    for digest, members in hashes.items():
        if len(members) < 2:
            continue
        for entry_record in members:
            entry_record["duplicate_group"] = f"sha256:{digest[:16]}"
            entry_record["duplicate_proof"] = {"owner": "unknown", "reference_scan": "unknown", "basis": "unproven"}

    records.sort(key=lambda item: (str(item["path"]), str(item["kind"])))
    counts = Counter(str(item["kind"]) for item in records)
    return {
        "schema_version": 1,
        "mode": "read_only",
        "checkout_root": coordination_relative(coordination_root, checkout_root),
        "coordination_root": ".",
        "records": records,
        "summary": {"record_count": len(records), "by_kind": dict(sorted(counts.items()))},
    }


def render_summary(inventory: dict[str, Any]) -> str:
    summary = inventory["summary"]
    kinds = summary["by_kind"]
    rows = "\n".join(f"| `{kind}` | {count} |" for kind, count in kinds.items())
    return (
        "# Repository Cleanup Inventory\n\n"
        "Generated by `scripts/audit_repository.py`. This is a read-only inventory; every listed candidate is retained. "
        "It contains paths and classification metadata only, never source contents or credential values.\n\n"
        f"- Schema version: `{inventory['schema_version']}`\n"
        f"- Records: `{summary['record_count']}`\n"
        "- Disposition: `retain` for all records; no deletion was attempted.\n\n"
        "| Kind | Count |\n| --- | ---: |\n"
        f"{rows}\n\n"
        "The machine-readable inventory records containment, process-use, reference, credential, and ownership checks. "
        "Any `unknown`, `fail`, or `not_applicable` check is fail-closed and requires retention.\n"
    )


def main(arguments: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
    namespace = parser.parse_args(arguments)
    try:
        checkout_root, coordination_root = discover_roots(namespace.checkout_root)
        inventory = build_inventory(checkout_root, coordination_root)
    except ValueError as error:
        print(json.dumps({"code": str(error)}, separators=(",", ":")))
        return 3
    output = namespace.output
    if not output.is_absolute():
        output = checkout_root / output
    summary = namespace.summary or checkout_root / "docs" / "engineering" / "REPOSITORY_CLEANUP_INVENTORY.md"
    if not summary.is_absolute():
        summary = checkout_root / summary
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(inventory, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    summary.write_text(render_summary(inventory), encoding="utf-8")
    print(f"REPOSITORY_AUDIT_PASS records={inventory['summary']['record_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
