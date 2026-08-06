from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class ProviderProfileError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class ProviderProfile:
    profile_id: str
    adapter_id: str
    model_id: str
    budget_limit: int
    credential_ref: str
    config_fingerprint: str
    policy_fingerprint: str
    created_at: str


class ProviderProfileRepository:
    def __init__(self, database: Any) -> None:
        self.database = database

    def add(
        self,
        *,
        profile_id: str,
        adapter_id: str,
        model_id: str,
        budget_limit: int,
        credential_ref: str,
        config_fingerprint: str,
        policy_fingerprint: str,
    ) -> ProviderProfile:
        if adapter_id not in {"openai", "mock"}:
            raise ProviderProfileError("adapter_not_allowed")
        if not profile_id.strip() or not model_id.strip() or not credential_ref.strip():
            raise ProviderProfileError("profile_invalid")
        if type(budget_limit) is not int or budget_limit < 0:
            raise ProviderProfileError("budget_invalid")
        if HASH_PATTERN.fullmatch(config_fingerprint) is None or HASH_PATTERN.fullmatch(policy_fingerprint) is None:
            raise ProviderProfileError("profile_fingerprint_invalid")
        created_at = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
        connection = self.database.connect()
        try:
            connection.execute(
                "INSERT INTO provider_profile(profile_id, adapter_id, model_id, budget_limit, credential_ref, "
                "config_fingerprint, policy_fingerprint, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    profile_id,
                    adapter_id,
                    model_id,
                    budget_limit,
                    credential_ref,
                    config_fingerprint,
                    policy_fingerprint,
                    created_at,
                ),
            )
        finally:
            connection.close()
        return self.get(profile_id)

    def get(self, profile_id: str) -> ProviderProfile:
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT profile_id, adapter_id, model_id, budget_limit, credential_ref, config_fingerprint, "
                "policy_fingerprint, created_at FROM provider_profile WHERE profile_id = ?",
                (profile_id,),
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            raise ProviderProfileError("provider_unconfigured")
        return ProviderProfile(str(row[0]), str(row[1]), str(row[2]), int(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7]))
