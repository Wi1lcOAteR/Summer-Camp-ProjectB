from __future__ import annotations

import json
import tempfile
from dataclasses import asdict
from pathlib import Path

from fastapi import APIRouter, File, Request, UploadFile, status
from pydantic import BaseModel, ConfigDict

from projectb.api.app_support import ApiError
from projectb.repositories.courses import CourseRepository
from projectb.repositories.coverage import CoverageError
from projectb.services.materials.coverage import CoverageService
from projectb.services.materials.delete import MaterialDeletionService
from projectb.services.materials.importer import (
    MAX_BATCH_BYTES,
    MAX_BATCH_FILES,
    MAX_FILE_BYTES,
    ImportPolicyError,
    MaterialImporter,
)


router = APIRouter(tags=["materials"])


class ConceptCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str
    evaluator_id: str | None = None


class MappingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    locator_ids: list[str]
    decision: str


@router.get("/api/courses/{course_id}/materials")
def list_materials(course_id: str, request: Request) -> dict[str, object]:
    connection = request.app.state.database.connect()
    try:
        rows = connection.execute(
            "SELECT material_id, filename, media_type, content_hash, status, created_at FROM material "
            "WHERE course_id = ? ORDER BY created_at, material_id",
            (course_id,),
        ).fetchall()
    finally:
        connection.close()
    return {
        "materials": [
            {
                "material_id": str(row[0]),
                "filename": str(row[1]),
                "media_type": str(row[2]),
                "content_hash": str(row[3]),
                "status": str(row[4]),
                "created_at": str(row[5]),
            }
            for row in rows
        ]
    }


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


@router.get("/api/materials/{material_id}/sources")
def material_sources(material_id: str, request: Request) -> dict[str, object]:
    connection = request.app.state.database.connect()
    try:
        row = connection.execute(
            "SELECT mv.locator_index_json FROM material_version mv JOIN material m ON m.material_id = mv.material_id "
            "WHERE m.material_id = ? ORDER BY mv.rowid DESC LIMIT 1",
            (material_id,),
        ).fetchone()
    finally:
        connection.close()
    if row is None:
        raise ApiError("material_not_found", 404)
    try:
        sources = json.loads(row[0])
    except (TypeError, json.JSONDecodeError):
        raise ApiError("source_index_invalid", 500, retryable=True) from None
    return {"sources": sources}


@router.post("/api/courses/{course_id}/concepts", status_code=status.HTTP_201_CREATED)
def create_concept(course_id: str, payload: ConceptCreate, request: Request) -> dict[str, object]:
    if not CourseRepository(request.app.state.database).exists(course_id):
        raise ApiError("course_not_found", 404)
    try:
        concept = CoverageService(request.app.state.database).create_concept(
            course_id,
            payload.name,
            evaluator_id=payload.evaluator_id,
        )
    except CoverageError as error:
        raise ApiError(error.code, 400) from None
    return asdict(concept)


@router.post("/api/concepts/{concept_id}/mapping")
def map_concept(concept_id: str, payload: MappingCreate, request: Request) -> dict[str, object]:
    try:
        version = CoverageService(request.app.state.database).record_decision(
            concept_id,
            payload.locator_ids,
            payload.decision,
        )
    except CoverageError as error:
        status_code = 404 if error.code == "concept_not_found" else 400
        raise ApiError(error.code, status_code) from None
    return {"version": version, "decision": payload.decision}


@router.delete("/api/materials/{material_id}")
def delete_material(material_id: str, request: Request) -> dict[str, object]:
    connection = request.app.state.database.connect()
    try:
        exists = connection.execute("SELECT 1 FROM material WHERE material_id = ?", (material_id,)).fetchone()
    finally:
        connection.close()
    if exists is None:
        raise ApiError("material_not_found", 404)
    result = MaterialDeletionService(request.app.state.database, request.app.state.content_store).delete(material_id)
    return asdict(result)
