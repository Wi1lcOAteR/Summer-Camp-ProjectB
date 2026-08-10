from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from threading import RLock
from typing import Any

import httpx
import uvicorn

from projectb.api.app import create_app
from projectb.providers.openai_adapter import OpenAIAdapter
from projectb.providers.port import ProviderBinding, ProviderError
from projectb.providers.registry import ProviderRegistry
from projectb.repositories.provider_profiles import ProviderProfileError, ProviderProfileRepository
from projectb.security.credentials import CredentialError, CredentialService, WindowsCredentialBackend


LOCAL_BIND_HOST = "127.0.0.1"
LOCAL_DEFAULT_PORT = 4173


@dataclass(frozen=True, slots=True)
class LocalProfile:
    name: str = "local"
    bind_host: str = LOCAL_BIND_HOST
    default_port: int = LOCAL_DEFAULT_PORT


class LocalProviderError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class LocalProviderController:
    def __init__(
        self,
        *,
        data_dir: Path,
        database: Any,
        registry: ProviderRegistry,
        credential_service: CredentialService,
        provider_transport: httpx.BaseTransport | None = None,
        utc_now=None,  # type: ignore[no-untyped-def]
    ) -> None:
        self.config_path = data_dir / "provider.json"
        self.profiles = ProviderProfileRepository(database)
        self.registry = registry
        self.credential_service = credential_service
        self.provider_transport = provider_transport
        self.utc_now = utc_now or (lambda: datetime.now(UTC))
        self.active_profile_id: str | None = None
        self._lock = RLock()

    def restore(self) -> None:
        with self._lock:
            config = self._read_config()
            if config == {"enabled": False, "schema_version": 1}:
                return
            try:
                adapter = self._adapter(str(config["model_id"]))
                binding = adapter.binding
                profile_id = str(config["profile_id"])
                if config != self._enabled_config(profile_id, binding):
                    raise LocalProviderError("provider_config_invalid")
                self._require_profile(profile_id, binding)
                if not self.credential_service.status().configured:
                    raise LocalProviderError("credential_unconfigured")
                self.credential_service.read_for_provider()
                self.registry.register(profile_id, adapter)
                self.active_profile_id = profile_id
            except (
                CredentialError,
                ProviderError,
                ProviderProfileError,
                KeyError,
                TypeError,
                ValueError,
                LocalProviderError,
            ):
                self._clear_runtime()

    def enable(self, model_id: str) -> dict[str, object]:
        with self._lock:
            try:
                adapter = self._adapter(model_id)
                binding = adapter.binding
                if not self.credential_service.status().configured:
                    raise LocalProviderError("credential_unconfigured")
                self.credential_service.read_for_provider()
                profile_id = "openai-" + binding.config_fingerprint[:20]
                self._ensure_profile(profile_id, binding)
                self._write_config({"enabled": False, "schema_version": 1})
                self._clear_runtime()
                self.registry.register(profile_id, adapter)
                self.active_profile_id = profile_id
                try:
                    self._write_config(self._enabled_config(profile_id, binding))
                except OSError:
                    self._clear_runtime()
                    raise LocalProviderError("provider_config_unavailable") from None
            except CredentialError as error:
                raise LocalProviderError(error.code) from None
            except ProviderError as error:
                raise LocalProviderError(error.code) from None
            except OSError:
                raise LocalProviderError("provider_config_unavailable") from None
            return self._snapshot_unlocked()

    def disable(self) -> dict[str, object]:
        with self._lock:
            try:
                self._write_config({"enabled": False, "schema_version": 1})
            except OSError:
                try:
                    configured = self.credential_service.status().configured
                except CredentialError:
                    configured = False
                if not configured:
                    self._clear_runtime()
                raise LocalProviderError("provider_config_unavailable") from None
            self._clear_runtime()
            return self._snapshot_unlocked()

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            return self._snapshot_unlocked()

    def _snapshot_unlocked(self) -> dict[str, object]:
        try:
            configured = self.credential_service.status().configured
        except CredentialError:
            configured = False
        if not configured:
            self._clear_runtime()
        provider = self.registry.resolve(self.active_profile_id or "")
        try:
            binding = getattr(provider, "binding", None)
        except ProviderError:
            self._clear_runtime()
            binding = None
        active = configured and isinstance(binding, ProviderBinding)
        return {
            "profile": "local",
            "bind_host": LOCAL_BIND_HOST,
            "provider_mode": "L+P" if active else "L",
            "provider_configured": configured,
            "provider_profile": self._profile_payload(self.active_profile_id, binding) if active else None,
        }

    def _clear_runtime(self) -> None:
        self.registry.clear_local()
        self.active_profile_id = None

    def _adapter(self, model_id: str) -> OpenAIAdapter:
        return OpenAIAdapter(
            model_id=model_id,
            input_token_cap=20_000,
            output_token_cap=3_000,
            credential_ref="provider-openai",
            credential_configured=True,
            credential_supplier=self.credential_service.read_for_provider,
            transport=self.provider_transport,
            utc_now=self.utc_now,
        )

    def _ensure_profile(self, profile_id: str, binding: ProviderBinding) -> None:
        try:
            self._require_profile(profile_id, binding)
            return
        except ProviderProfileError as error:
            if error.code != "provider_unconfigured":
                raise
        self.profiles.add(
            profile_id=profile_id,
            adapter_id=binding.adapter_id,
            model_id=binding.model_id,
            budget_limit=binding.max_cost_microusd,
            credential_ref=binding.credential_ref,
            config_fingerprint=binding.config_fingerprint,
            policy_fingerprint=binding.policy_fingerprint,
        )

    def _require_profile(self, profile_id: str, binding: ProviderBinding) -> None:
        profile = self.profiles.get(profile_id)
        if (
            profile.adapter_id != binding.adapter_id
            or profile.model_id != binding.model_id
            or profile.budget_limit != binding.max_cost_microusd
            or profile.credential_ref != binding.credential_ref
            or profile.config_fingerprint != binding.config_fingerprint
            or profile.policy_fingerprint != binding.policy_fingerprint
        ):
            raise LocalProviderError("provider_config_mismatch")

    def _read_config(self) -> dict[str, object]:
        if not self.config_path.exists():
            return {"enabled": False, "schema_version": 1}
        try:
            value = json.loads(self.config_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return {"enabled": False, "schema_version": 1}
        return value if isinstance(value, dict) else {"enabled": False, "schema_version": 1}

    def _write_config(self, value: dict[str, object]) -> None:
        temporary = self.config_path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.config_path)

    @staticmethod
    def _enabled_config(profile_id: str, binding: ProviderBinding) -> dict[str, object]:
        return {
            "adapter_id": binding.adapter_id,
            "config_fingerprint": binding.config_fingerprint,
            "credential_ref": binding.credential_ref,
            "enabled": True,
            "input_token_cap": binding.input_token_cap,
            "max_cost_microusd": binding.max_cost_microusd,
            "model_id": binding.model_id,
            "output_token_cap": binding.output_token_cap,
            "policy_fingerprint": binding.policy_fingerprint,
            "profile_id": profile_id,
            "schema_version": 1,
        }

    @staticmethod
    def _profile_payload(profile_id: str | None, binding: object) -> dict[str, object]:
        assert profile_id is not None and isinstance(binding, ProviderBinding)
        return {
            "profile_id": profile_id,
            "adapter_id": binding.adapter_id,
            "model_id": binding.model_id,
            "input_token_cap": binding.input_token_cap,
            "output_token_cap": binding.output_token_cap,
            "max_cost_microusd": binding.max_cost_microusd,
            "config_fingerprint": binding.config_fingerprint,
            "policy_fingerprint": binding.policy_fingerprint,
        }


def create_local_app(
    data_dir: Path,
    static_dir: Path | None = None,
    *,
    credential_service=None,  # type: ignore[no-untyped-def]
    provider_transport: httpx.BaseTransport | None = None,
    utc_now=None,  # type: ignore[no-untyped-def]
):  # type: ignore[no-untyped-def]
    data = data_dir.resolve()
    data.mkdir(parents=True, exist_ok=True)
    if credential_service is None:
        credential_service = CredentialService(WindowsCredentialBackend(), target="provider-openai")
    registry = ProviderRegistry("local")
    app = create_app(
        database_path=data / "projectb.sqlite3",
        content_dir=data / "content",
        static_dir=static_dir,
        credential_service=credential_service,
        provider_registry=registry,
        profile_name="local",
    )
    controller = LocalProviderController(
        data_dir=data,
        database=app.state.database,
        registry=registry,
        credential_service=credential_service,
        provider_transport=provider_transport,
        utc_now=utc_now,
    )
    controller.restore()
    app.state.provider_controller = controller
    return app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--static-dir", type=Path)
    parser.add_argument("--port", type=int, default=LOCAL_DEFAULT_PORT)
    arguments = parser.parse_args()
    app = create_local_app(arguments.data_dir, arguments.static_dir)
    uvicorn.run(app, host=LOCAL_BIND_HOST, port=arguments.port, proxy_headers=False)


if __name__ == "__main__":
    main()
