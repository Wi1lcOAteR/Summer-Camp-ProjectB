from __future__ import annotations

import asyncio
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

import uvicorn


ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from projectb.profiles.demo import create_demo_app  # noqa: E402


def main() -> None:
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("demo_e2e_node_missing")
    vite = ROOT / "frontend" / "node_modules" / "vite" / "bin" / "vite.js"
    subprocess.run([node, str(vite), "build"], cwd=ROOT / "frontend", check=True)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 7860))
    listener.listen(2048)
    listener.setblocking(False)
    session_root = Path(tempfile.mkdtemp(prefix="demo-e2e-", dir=ROOT / "tmp"))
    app = create_demo_app(
        session_root=session_root,
        static_dir=ROOT / "frontend" / "dist",
        environment={"PROJECTB_DEMO_LOCAL_SMOKE": "1"},
    )
    server = uvicorn.Server(
        uvicorn.Config(
            app,
            host="127.0.0.1",
            port=7860,
            proxy_headers=False,
            access_log=False,
            log_level="warning",
        )
    )
    try:
        loop.run_until_complete(server.serve(sockets=[listener]))
    finally:
        app.state.demo_sessions.close()
        listener.close()
        loop.close()
        shutil.rmtree(session_root, ignore_errors=True)


if __name__ == "__main__":
    main()
