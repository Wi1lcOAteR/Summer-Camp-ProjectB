from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import uvicorn

from projectb.api.app import create_app
from projectb.security.credentials import CredentialService, WindowsCredentialBackend


LOCAL_BIND_HOST = "127.0.0.1"
LOCAL_DEFAULT_PORT = 4173


@dataclass(frozen=True, slots=True)
class LocalProfile:
    name: str = "local"
    bind_host: str = LOCAL_BIND_HOST
    default_port: int = LOCAL_DEFAULT_PORT


def create_local_app(data_dir: Path, static_dir: Path | None = None, *, credential_service=None):  # type: ignore[no-untyped-def]
    data = data_dir.resolve()
    data.mkdir(parents=True, exist_ok=True)
    if credential_service is None:
        credential_service = CredentialService(WindowsCredentialBackend(), target="provider-openai")
    return create_app(
        database_path=data / "projectb.sqlite3",
        content_dir=data / "content",
        static_dir=static_dir,
        credential_service=credential_service,
        profile_name="local",
    )


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
