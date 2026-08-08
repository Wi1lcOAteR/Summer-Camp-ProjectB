"""Contract tests for the Phase A read-only repository inventory."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def load_audit():
    spec = importlib.util.spec_from_file_location("repository_audit", REPO / "scripts/audit_repository.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(repo: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=repo, capture_output=True, text=True, check=False, timeout=30
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def init_checkout(root: Path) -> Path:
    checkout = root / "checkout"
    checkout.mkdir()
    git(checkout, "init", "-q")
    (checkout / ".gitignore").write_text("ignored/\ntmp/\nfrontend/dist/\n", encoding="utf-8")
    (checkout / "README.md").write_text("# fixture\n", encoding="utf-8")
    git(checkout, "add", ".gitignore", "README.md")
    return checkout


def records(inventory: dict[str, object]) -> list[dict[str, object]]:
    return inventory["records"]  # type: ignore[return-value]


def record_for(inventory: dict[str, object], path: str) -> dict[str, object]:
    return next(row for row in records(inventory) if row["path"] == path)


def test_scope_and_paths_inventories_only_checkout_content_and_excluded_trees(tmp_path: Path) -> None:
    audit = load_audit()
    checkout = init_checkout(tmp_path)
    (checkout / "backend").mkdir()
    (checkout / "backend" / "tracked.py").write_text("answer = 42\n", encoding="utf-8")
    (checkout / "notes.txt").write_text("untracked\n", encoding="utf-8")
    (checkout / "ignored").mkdir()
    (checkout / "ignored" / "secret.txt").write_text("do not inventory\n", encoding="utf-8")
    (checkout / "node_modules").mkdir()
    (checkout / "node_modules" / "package.js").write_text("ignored tree\n", encoding="utf-8")
    (checkout / "tmp" / "finished-run").mkdir(parents=True)
    (checkout / "tmp" / "finished-run" / "private.txt").write_text(
        "metadata only\n", encoding="utf-8"
    )
    (checkout / "tmp" / "receipt.json").write_text("{}\n", encoding="utf-8")
    (checkout / "frontend" / "dist").mkdir(parents=True)
    (checkout / "frontend" / "dist" / "bundle.js").write_text("generated\n", encoding="utf-8")
    git(checkout, "add", "backend/tracked.py")

    inventory = audit.build_inventory(checkout, tmp_path)

    assert inventory["schema_version"] == 1
    assert record_for(inventory, "checkout/backend/tracked.py")["owner_status"] == "tracked"
    assert record_for(inventory, "checkout/notes.txt")["owner_status"] == "untracked"
    assert not any(row["path"].endswith("ignored/secret.txt") for row in records(inventory))
    excluded = record_for(inventory, "checkout/node_modules")
    assert excluded["kind"] == "excluded_tree"
    assert excluded["action"] == "retain"
    assert set(excluded["checks"]) == {
        "containment", "process_use", "reference_scan", "credential_scan", "ownership"
    }
    assert set(excluded["checks"].values()) <= {"pass", "fail", "unknown", "not_applicable"}
    finished_run = record_for(inventory, "checkout/tmp/finished-run")
    assert finished_run["kind"] == "directory_candidate"
    assert finished_run["action"] == "retain"
    assert not any(row["path"].endswith("finished-run/private.txt") for row in records(inventory))
    assert record_for(inventory, "checkout/tmp/receipt.json")["kind"] == "runtime_file"
    generated = record_for(inventory, "checkout/frontend/dist")
    assert generated["kind"] == "generated_tree"
    assert not any(row["path"].endswith("frontend/dist/bundle.js") for row in records(inventory))


def test_scope_and_paths_derives_the_checkout_root_from_a_nested_path(tmp_path: Path) -> None:
    audit = load_audit()
    checkout = init_checkout(tmp_path)
    nested = checkout / "backend" / "nested"
    nested.mkdir(parents=True)

    derived_checkout, coordination_root = audit.discover_roots(nested)

    assert derived_checkout == checkout.resolve()
    assert coordination_root == checkout.resolve()


def test_syntax_inventory_records_pass_contexts_and_quality_check_receipts(tmp_path: Path) -> None:
    audit = load_audit()
    checkout = init_checkout(tmp_path)
    source = checkout / "backend" / "sample.py"
    source.parent.mkdir()
    source.write_text(
        "import unused_module\n\n"
        "def parse(value: str) -> int:\n"
        "    try:\n"
        "        return int(value)\n"
        "    except ValueError:\n"
        "        pass\n"
        "    ignored = 1  # type: ignore[assignment]\n"
        "    return ignored\n",
        encoding="utf-8",
    )
    (checkout / "frontend").mkdir()
    (checkout / "frontend" / "route.ts").write_text(
        "const unusedRoute = '/review';\nexport const route = '/';\n", encoding="utf-8"
    )
    git(checkout, "add", "backend/sample.py", "frontend/route.ts")

    inventory = audit.build_inventory(checkout, tmp_path)

    python_record = record_for(inventory, "checkout/backend/sample.py")
    assert python_record["analysis"]["python"]["pass_contexts"] == ["except"]
    assert python_record["analysis"]["python"]["type_ignores"] == 1
    assert python_record["analysis"]["quality"]["ruff_f401_f841"] in {"not_run", "pass", "fail"}
    typescript_record = record_for(inventory, "checkout/frontend/route.ts")
    assert typescript_record["analysis"]["typescript"]["unused_symbol_check"] in {"not_run", "pass", "fail"}
    assert typescript_record["analysis"]["routes"]["metadata_reads"] >= 0


def test_docs_and_duplicates_classify_links_and_retain_unproven_duplicates(tmp_path: Path) -> None:
    audit = load_audit()
    checkout = init_checkout(tmp_path)
    docs = checkout / "docs"
    docs.mkdir()
    (docs / "guide.md").write_text("[readme](../README.md)\n", encoding="utf-8")
    (docs / "copy.md").write_text("[readme](../README.md)\n", encoding="utf-8")
    git(checkout, "add", "docs/guide.md", "docs/copy.md")

    inventory = audit.build_inventory(checkout, tmp_path)

    guide = record_for(inventory, "checkout/docs/guide.md")
    copy = record_for(inventory, "checkout/docs/copy.md")
    assert guide["analysis"]["markdown"]["classification"] == "active_document"
    assert guide["analysis"]["markdown"]["links"] == {"checked": 1, "broken": 0}
    assert guide["sha256"] == copy["sha256"]
    assert guide["duplicate_proof"] == {
        "owner": "unknown", "reference_scan": "unknown", "basis": "unproven"
    }
    assert guide["action"] == "retain"
    encoded = json.dumps(inventory, sort_keys=True)
    assert "[readme]" not in encoded


def test_ownership_and_worktrees_record_metadata_without_deleting_or_following_links(tmp_path: Path) -> None:
    audit = load_audit()
    checkout = init_checkout(tmp_path)
    sibling = tmp_path / ".worktrees" / "peer"
    sibling.mkdir(parents=True)
    (sibling / "private.txt").write_text("sibling content must not be parsed\n", encoding="utf-8")
    link = checkout / "linked"
    toolchains = checkout / "tmp" / "toolchains"
    toolchains.parent.mkdir()
    for target in (link, toolchains):
        try:
            os.symlink(sibling, target, target_is_directory=True)
        except OSError:
            result = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(target), str(sibling)],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
            assert result.returncode == 0, result.stderr

    inventory = audit.build_inventory(checkout, tmp_path)

    worktree = record_for(inventory, ".worktrees/peer")
    assert worktree["kind"] == "worktree"
    assert worktree["action"] == "retain"
    assert worktree["checks"]["ownership"] in {"pass", "unknown"}
    link_record = record_for(inventory, "checkout/linked")
    assert link_record["kind"] == "symlink"
    assert link_record["action"] == "retain"
    assert link_record["symlink_target"].endswith(".worktrees/peer")
    toolchain_record = record_for(inventory, "checkout/tmp/toolchains")
    assert toolchain_record["kind"] == "symlink"
    assert toolchain_record["reason"] == "symlink_or_reparse_point"
    assert toolchain_record["checks"]["containment"] == "fail"
    assert (sibling / "private.txt").read_text(encoding="utf-8") == "sibling content must not be parsed\n"


def test_ownership_and_worktrees_retain_a_tracked_path_below_a_junction(tmp_path: Path) -> None:
    audit = load_audit()
    checkout = init_checkout(tmp_path)
    tracked = checkout / "nested" / "record.py"
    tracked.parent.mkdir()
    tracked.write_text("value = 1\n", encoding="utf-8")
    git(checkout, "add", "nested/record.py")
    external = tmp_path / "external"
    external.mkdir()
    (external / "record.py").write_text("external = 2\n", encoding="utf-8")
    tracked.parent.rename(checkout / "nested-original")
    result = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(checkout / "nested"), str(external)],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr

    inventory = audit.build_inventory(checkout, tmp_path)

    boundary = record_for(inventory, "checkout/nested/record.py")
    assert boundary["kind"] == "symlink"
    assert boundary["reason"] == "symlink_or_reparse_point"
    assert "sha256" not in boundary


def test_ownership_and_worktrees_marks_registered_and_orphaned_checkouts(tmp_path: Path, monkeypatch: object) -> None:
    audit = load_audit()
    checkout = init_checkout(tmp_path)
    peer = tmp_path / ".worktrees" / "peer"
    peer.mkdir(parents=True)

    monkeypatch.setattr(audit, "registered_worktrees", lambda _: {peer.resolve()})
    registered = record_for(audit.build_inventory(checkout, tmp_path), ".worktrees/peer")
    assert registered["registration"] == "registered"

    monkeypatch.setattr(audit, "registered_worktrees", lambda _: set())
    orphaned = record_for(audit.build_inventory(checkout, tmp_path), ".worktrees/peer")
    assert orphaned["registration"] == "orphan_or_unknown"
