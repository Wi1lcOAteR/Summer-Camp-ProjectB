from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def test_local_l_mode_does_not_import_optional_runtime_dependencies() -> None:
    code = textwrap.dedent(
        f"""
        import json
        import sys
        import tempfile
        from pathlib import Path
        from types import SimpleNamespace

        sys.path.insert(0, {str(ROOT / "backend")!r})

        from projectb.profiles.local import create_local_app

        with tempfile.TemporaryDirectory() as temporary:
            if sys.platform == "win32":
                create_local_app(Path(temporary))
            else:
                credentials = type(
                    "Credentials",
                    (),
                    {{"status": lambda self: SimpleNamespace(configured=False)}},
                )()
                create_local_app(Path(temporary), credential_service=credentials)

        heavy_dependencies = {{
            "httpx",
            "keyring",
            "openai",
            "psutil",
            "pypdf",
            "pypdfium2",
            "win32ctypes",
        }}
        print(json.dumps(sorted(heavy_dependencies.intersection(sys.modules))))
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == []
