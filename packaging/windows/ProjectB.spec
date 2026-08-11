# PyInstaller one-file recipe for the local loopback application.
from pathlib import Path

from PyInstaller.building.build_main import Analysis, EXE, PYZ
from PyInstaller.utils.hooks import collect_submodules


ROOT = Path(SPECPATH).resolve().parents[1]
BACKEND = ROOT / "backend"
FRONTEND_DIST = ROOT / "frontend" / "dist"
MIGRATIONS = BACKEND / "projectb" / "storage" / "migrations"
NOTICES = ROOT / "licenses" / "THIRD_PARTY_NOTICES.md"
LAUNCHER = Path(SPECPATH).resolve() / "launcher.py"

datas = [
    (str(FRONTEND_DIST), "frontend_dist"),
    (str(MIGRATIONS), "projectb/storage/migrations"),
    (str(NOTICES), "licenses"),
]
hiddenimports = [
    "keyring.backends.Windows",
    "keyring.backends.chainer",
    "pypdfium2._helpers",
    *collect_submodules("projectb"),
]

a = Analysis(
    [str(LAUNCHER)],
    pathex=[str(BACKEND)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[str(Path(SPECPATH).resolve() / "hooks")],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "tests", "playwright", "PIL"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="ProjectB",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)
