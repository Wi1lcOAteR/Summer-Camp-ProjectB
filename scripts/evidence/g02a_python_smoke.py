from __future__ import annotations

import os
import sys
from importlib.metadata import version
from io import BytesIO

site_packages = os.environ.get("PROJECTB_G02A_SITE_PACKAGES")
if site_packages:
    sys.path.insert(0, site_packages)

# These imports deliberately follow the optional, audited G-02A package path injection.
# ruff: noqa: E402
import httpx
import keyring.backends.Windows
import openai
import psutil
import pypdfium2
from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from PIL import Image
from pypdf import PdfReader, PdfWriter
from zoneinfo import ZoneInfo

EXPECTED = {
    "fastapi": "0.139.2",
    "pydantic": "2.13.4",
    "httpx": "0.28.1",
    "httpx2": "2.7.0",
    "openai": "2.46.0",
    "pypdf": "6.14.2",
    "pypdfium2": "5.12.1",
    "Pillow": "12.3.0",
    "keyring": "25.7.0",
    "tzdata": "2026.3",
    "python-multipart": "0.0.32",
    "psutil": "7.2.2",
    "pytest": "9.1.1",
    "ruff": "0.15.22",
    "mypy": "2.3.0",
    "pyinstaller": "6.21.0",
}


def main() -> None:
    assert sys.version_info[:3] == (3, 14, 6)
    for package, expected in EXPECTED.items():
        assert version(package) == expected, (package, version(package), expected)

    app = FastAPI()

    @app.get("/health")
    def health() -> dict[str, bool]:
        return {"ok": True}

    @app.post("/upload")
    async def upload(file: UploadFile = File(...)) -> dict[str, int]:
        return {"size": len(await file.read())}

    with TestClient(app) as client:
        assert client.get("/health").json() == {"ok": True}
        response = client.post("/upload", files={"file": ("x.txt", b"abc")})
        assert response.json() == {"size": 3}

    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"ok": request.method == "GET"})
    )
    with httpx.Client(transport=transport) as client:
        assert client.get("https://example.invalid").json() == {"ok": True}

    for image_format in ("PNG", "JPEG", "WEBP"):
        image_bytes = BytesIO()
        Image.new("RGB", (4, 4), "white").save(image_bytes, format=image_format)
        image_bytes.seek(0)
        with Image.open(image_bytes) as image:
            image.load()
            assert image.size == (4, 4)

    pdf = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(pdf)
    pdf_bytes = pdf.getvalue()
    assert len(PdfReader(BytesIO(pdf_bytes)).pages) == 1
    document = pypdfium2.PdfDocument(pdf_bytes)
    bitmap = document[0].render(scale=1)
    assert bitmap.to_pil().size == (72, 72)
    bitmap.close()
    document.close()

    assert ZoneInfo("Asia/Shanghai").key == "Asia/Shanghai"
    assert keyring.backends.Windows.WinVaultKeyring().priority == 5
    assert psutil.Process().memory_info().rss > 0
    assert openai.__version__ == "2.46.0"
    print(
        f"PYTHON_SMOKE_PASS packages={len(EXPECTED)} fastapi=health+multipart "
        "image=png+jpeg+webp pdf=read+render keyring=instantiate-only "
        "provider_network=0"
    )


if __name__ == "__main__":
    main()
