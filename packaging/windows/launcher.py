from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import uvicorn

from projectb.profiles.local import LOCAL_BIND_HOST, LOCAL_DEFAULT_PORT, create_local_app
from projectb.services.materials.extract_text import run_material_worker


def _resource_root() -> Path:
    frozen_root = getattr(sys, "_MEIPASS", None)
    if frozen_root:
        return Path(frozen_root)
    return Path(__file__).resolve().parents[2]


def _default_data_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "ProjectB"
    return Path.home() / "AppData" / "Local" / "ProjectB"


def main() -> None:
    parser = argparse.ArgumentParser(description="ProjectB local study workbench")
    parser.add_argument("--data-dir", type=Path, default=_default_data_dir())
    parser.add_argument("--port", type=int, default=LOCAL_DEFAULT_PORT)
    parser.add_argument("--material-worker", nargs=2, type=Path, help=argparse.SUPPRESS)
    arguments = parser.parse_args()
    if arguments.material_worker:
        source_path, output_path = arguments.material_worker
        raise SystemExit(run_material_worker(source_path, output_path))
    if LOCAL_BIND_HOST != "127.0.0.1":
        raise SystemExit("local_bind_contract")
    static_dir = _resource_root() / "frontend_dist"
    if not (static_dir / "index.html").is_file():
        raise SystemExit("frontend_resources_missing")
    app = create_local_app(arguments.data_dir, static_dir)
    uvicorn.run(app, host=LOCAL_BIND_HOST, port=arguments.port, proxy_headers=False)


if __name__ == "__main__":
    main()
