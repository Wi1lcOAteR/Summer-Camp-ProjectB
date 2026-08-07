from __future__ import annotations

import statistics
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.api.app import create_app  # noqa: E402


def test_cached_settings_api_p95_is_below_500ms(tmp_path: Path) -> None:
    app = create_app(database_path=tmp_path / "db.sqlite3", content_dir=tmp_path / "content")
    value = TestClient(app, base_url="http://127.0.0.1")
    value.get("/api/settings")
    durations = []
    for _ in range(25):
        started = time.perf_counter()
        assert value.get("/api/settings").status_code == 200
        durations.append((time.perf_counter() - started) * 1000)

    p95 = statistics.quantiles(durations, n=20)[18]
    assert p95 < 500
