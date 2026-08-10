from __future__ import annotations

import tempfile
from dataclasses import asdict
from pathlib import Path

from fastapi import APIRouter, File, Request, UploadFile

from projectb.api.app_support import ApiError
from projectb.repositories.courses import CourseRepository
from projectb.services.materials.importer import (
    MAX_BATCH_BYTES,
    MAX_BATCH_FILES,
    MAX_FILE_BYTES,
    ImportPolicyError,
    MaterialImporter,
)


router = APIRouter(tags=["materials"])


@router.post("/api/courses/{course_id}/materials/import")
async def import_materials(
    course_id: str,
    request: Request,
    files: list[UploadFile] = File(...),
) -> dict[str, object]:
    if not CourseRepository(request.app.state.database).exists(course_id):
        raise ApiError("course_not_found", 404)
    if not files or len(files) > MAX_BATCH_FILES:
        raise ApiError("batch_file_limit", 400)
    total = 0
    paths: list[Path] = []
    try:
        with tempfile.TemporaryDirectory(prefix="projectb-import-") as temporary:
            root = Path(temporary)
            for index, upload in enumerate(files):
                filename = Path(upload.filename or "").name
                if not filename or filename != upload.filename:
                    raise ApiError("filename_invalid", 400)
                upload_root = root / str(index)
                upload_root.mkdir()
                target = upload_root / filename
                size = 0
                with target.open("wb") as output:
                    while chunk := await upload.read(1024 * 1024):
                        size += len(chunk)
                        total += len(chunk)
                        if size > MAX_FILE_BYTES:
                            raise ApiError("file_too_large", 413)
                        if total > MAX_BATCH_BYTES:
                            raise ApiError("batch_byte_limit", 413)
                        output.write(chunk)
                paths.append(target)
            try:
                outcomes = MaterialImporter(
                    request.app.state.database,
                    request.app.state.content_store,
                ).import_batch(course_id, paths)
            except ImportPolicyError as error:
                raise ApiError(error.code, 400, retryable=error.retryable) from None
            return {
                "results": [
                    {
                        key: value
                        for key, value in asdict(outcome).items()
                        if key != "path" and value is not None
                    }
                    for outcome in outcomes
                ]
            }
    finally:
        for upload in files:
            await upload.close()
