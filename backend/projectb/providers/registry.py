from __future__ import annotations

from typing import Literal

from projectb.providers.mock import MockProvider
from projectb.providers.openai_adapter import OpenAIAdapter
from projectb.providers.port import ProviderError, ProviderPort


class RegistryError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class ProviderRegistry:
    def __init__(self, environment: Literal["local", "test", "demo"] = "local") -> None:
        if environment not in {"local", "test", "demo"}:
            raise RegistryError("environment_invalid")
        self.environment = environment
        self._providers: dict[str, ProviderPort] = {}

    def register(self, profile_id: str, provider: ProviderPort) -> None:
        if not profile_id.strip():
            raise RegistryError("profile_id_required")
        if self.environment == "local" and profile_id in self._providers:
            raise RegistryError("profile_already_registered")
        if self.environment == "local" and isinstance(provider, MockProvider):
            raise RegistryError("mock_not_allowed")
        if self.environment == "local":
            if type(provider) is not OpenAIAdapter:
                raise RegistryError("dynamic_adapter_not_allowed")
            try:
                provider.validate_registration()
            except ProviderError as error:
                raise RegistryError(error.code) from None
        self._providers[profile_id] = provider

    def resolve(self, profile_id: str) -> ProviderPort | None:
        return self._providers.get(profile_id)

    def clear_local(self) -> None:
        if self.environment != "local":
            raise RegistryError("environment_invalid")
        self._providers.clear()
