from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = (ROOT / "README.md", ROOT / "docs" / "INDEX.md")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    checked = 0
    for document in FILES:
        text = document.read_text(encoding="utf-8")
        for raw_target in LINK.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (document.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError as error:
                raise SystemExit(f"LINK_OUTSIDE_REPOSITORY {document.relative_to(ROOT)} {target}") from error
            if not resolved.exists():
                raise SystemExit(f"LINK_MISSING {document.relative_to(ROOT)} {target}")
            checked += 1
    print(f"LINK_VERIFICATION_PASS files={len(FILES)} links={checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
