from __future__ import annotations

from typing import Literal

from projectb.providers.mock import MockProvider
from projectb.providers.port import ProviderPort


class RegistryError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class ProviderRegistry:
    def __init__(self, environment: Literal["local", "test", "demo"] = "local") -> None:
        self.environment = environment
        self._providers: dict[str, ProviderPort] = {}

    def register(self, profile_id: str, provider: ProviderPort) -> None:
        if self.environment == "local" and isinstance(provider, MockProvider):
            raise RegistryError("mock_not_allowed")
        if self.environment == "local":
            raise RegistryError("dynamic_adapter_not_allowed")
        if not profile_id.strip():
            raise RegistryError("profile_id_required")
        self._providers[profile_id] = provider

    def resolve(self, profile_id: str) -> ProviderPort | None:
        return self._providers.get(profile_id)
