from __future__ import annotations

from projectb.profiles.local import LocalProfile


PROFILES = {"local": LocalProfile()}


def get_profile(name: str):  # type: ignore[no-untyped-def]
    try:
        return PROFILES[name]
    except KeyError:
        raise ValueError("profile_not_found") from None
