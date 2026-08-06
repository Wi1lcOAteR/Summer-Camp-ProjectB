from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles


class StaticBoundaryError(RuntimeError):
    pass


def mount_static(app: FastAPI, build_directory: Path, *, private_roots: tuple[Path, ...]) -> None:
    build = build_directory.resolve(strict=True)
    if not build.is_dir():
        raise StaticBoundaryError("static_directory_invalid")
    for private_root in private_roots:
        private = private_root.resolve(strict=False)
        if build == private or build.is_relative_to(private) or private.is_relative_to(build):
            raise StaticBoundaryError("static_private_overlap")
    app.mount("/", StaticFiles(directory=build, html=True, check_dir=True), name="webui")
