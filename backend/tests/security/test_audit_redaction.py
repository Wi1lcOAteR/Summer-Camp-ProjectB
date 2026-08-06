"""F-04 contract for value-free audit records."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]


def load_audit_module():
    path = ROOT / "backend/projectb/observability/audit.py"
    spec = importlib.util.spec_from_file_location("projectb_audit", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_audit_record_has_an_exact_value_free_field_allowlist() -> None:
    audit = load_audit_module()
    record = audit.build_audit_record(
        actor="local",
        action="attempt.evaluate",
        result="ok",
        opaque_refs=("course-1", "attempt-2"),
        fingerprint="a" * 64,
        request_id="request-1",
        error_code=None,
    )

    assert set(record) == {"actor", "action", "result", "opaque_refs", "fingerprint", "request_id", "error_code"}
    assert json.loads(audit.serialize_audit_record(record)) == record

    numeric_request = audit.build_audit_record(
        actor="local",
        action="attempt.evaluate",
        result="ok",
        opaque_refs=(),
        fingerprint="d" * 64,
        request_id="0" * 32,
        error_code=None,
    )
    assert numeric_request["request_id"] == "0" * 32


@pytest.mark.parametrize("field", ["body", "path", "answer", "fragment", "secret", "credential", "exception"])
def test_audit_record_rejects_forbidden_or_unknown_fields(field: str) -> None:
    audit = load_audit_module()
    values = {
        "actor": "local",
        "action": "attempt.evaluate",
        "result": "rejected",
        "opaque_refs": ("attempt-2",),
        "fingerprint": "b" * 64,
        "request_id": "request-2",
        "error_code": "invalid_attempt",
        field: "private material or answer",
    }

    with pytest.raises(audit.AuditValidationError):
        audit.build_audit_record(**values)


@pytest.mark.parametrize("reference", ["C:/private/file.pdf", "answer text with spaces", "sk-" + "x" * 24])
def test_audit_record_rejects_non_opaque_references(reference: str) -> None:
    audit = load_audit_module()
    with pytest.raises(audit.AuditValidationError):
        audit.build_audit_record(
            actor="local",
            action="material.read",
            result="rejected",
            opaque_refs=(reference,),
            fingerprint="c" * 64,
            request_id="request-3",
            error_code="source_stale",
        )
