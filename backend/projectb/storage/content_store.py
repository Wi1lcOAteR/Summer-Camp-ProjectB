from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path


class ContentStoreError(RuntimeError):
    pass


class ContentStore:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.objects_dir = self.root / "objects"
        self.staging_dir = self.root / ".staging"
        self.objects_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True)

    def path_for(self, content_hash: str) -> Path:
        if len(content_hash) != 64 or any(character not in "0123456789abcdef" for character in content_hash):
            raise ValueError("content_hash_invalid")
        return self.objects_dir / content_hash[:2] / content_hash

    def storage_ref(self, content_hash: str) -> str:
        return self.path_for(content_hash).relative_to(self.root).as_posix()

    def exists(self, content_hash: str) -> bool:
        return self.path_for(content_hash).is_file()

    def stage(self, source: Path, expected_hash: str) -> Path:
        handle, name = tempfile.mkstemp(prefix="material-", suffix=".tmp", dir=self.staging_dir)
        staged = Path(name)
        digest = hashlib.sha256()
        try:
            with source.open("rb") as reader, os.fdopen(handle, "wb") as writer:
                while chunk := reader.read(1024 * 1024):
                    digest.update(chunk)
                    writer.write(chunk)
            if digest.hexdigest() != expected_hash:
                raise ContentStoreError("content_hash_changed")
            return staged
        except BaseException:
            try:
                os.close(handle)
            except OSError:
                pass
            staged.unlink(missing_ok=True)
            raise

    def promote(self, staged: Path, content_hash: str) -> bool:
        destination = self.path_for(content_hash)
        if destination.is_file():
            staged.unlink(missing_ok=True)
            return False
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.replace(staged, destination)
        except FileExistsError:
            staged.unlink(missing_ok=True)
            return False
        return True

    def discard(self, staged: Path | None) -> None:
        if staged is not None:
            staged.unlink(missing_ok=True)

    def remove(self, content_hash: str) -> None:
        path = self.path_for(content_hash)
        path.unlink(missing_ok=True)
        try:
            path.parent.rmdir()
        except OSError:
            pass
