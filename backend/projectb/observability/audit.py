"""Value-free audit record construction and deterministic serialization."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence


AUDIT_FIELDS = frozenset({"actor", "action", "result", "opaque_refs", "fingerprint", "request_id", "error_code"})
REQUIRED_FIELDS = AUDIT_FIELDS - {"error_code"}
OPAQUE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_.-]{0,63}$")
FINGERPRINT_PATTERN = re.compile(r"^[0-9a-f]{64}$")
SECRET_SHAPE = re.compile(r"^sk-[A-Za-z0-9_-]{20,200}$")


class AuditValidationError(ValueError):
    pass


def _require_code(value: object, field: str) -> str:
    if not isinstance(value, str) or CODE_PATTERN.fullmatch(value) is None:
        raise AuditValidationError(f"invalid_{field}")
    return value


def _require_opaque(value: object, field: str) -> str:
    if not isinstance(value, str) or OPAQUE_PATTERN.fullmatch(value) is None:
        raise AuditValidationError(f"invalid_{field}")
    return value


def build_audit_record(**values: object) -> dict[str, object]:
    """Accept only fields and opaque identifiers explicitly safe for logs."""
    keys = set(values)
    if keys - AUDIT_FIELDS or not REQUIRED_FIELDS <= keys:
        raise AuditValidationError("audit_field_not_allowed")

    references = values["opaque_refs"]
    if isinstance(references, (str, bytes)) or not isinstance(references, Sequence):
        raise AuditValidationError("invalid_opaque_refs")
    normalized_refs: list[str] = []
    for reference in references:
        if (
            not isinstance(reference, str)
            or OPAQUE_PATTERN.fullmatch(reference) is None
            or SECRET_SHAPE.fullmatch(reference) is not None
        ):
            raise AuditValidationError("invalid_opaque_ref")
        normalized_refs.append(reference)

    fingerprint = values["fingerprint"]
    if not isinstance(fingerprint, str) or FINGERPRINT_PATTERN.fullmatch(fingerprint) is None:
        raise AuditValidationError("invalid_fingerprint")

    error_code = values.get("error_code")
    if error_code is not None:
        error_code = _require_code(error_code, "error_code")

    return {
        "actor": _require_code(values["actor"], "actor"),
        "action": _require_code(values["action"], "action"),
        "result": _require_code(values["result"], "result"),
        "opaque_refs": normalized_refs,
        "fingerprint": fingerprint,
        "request_id": _require_opaque(values["request_id"], "request_id"),
        "error_code": error_code,
    }


def serialize_audit_record(record: Mapping[str, object]) -> str:
    normalized = build_audit_record(**dict(record))
    return json.dumps(normalized, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
