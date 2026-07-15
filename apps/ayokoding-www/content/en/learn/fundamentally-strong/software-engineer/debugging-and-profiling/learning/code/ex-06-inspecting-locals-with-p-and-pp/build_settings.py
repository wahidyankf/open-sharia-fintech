"""Example 6: Inspecting Locals with p and pp."""

from __future__ import annotations


def build_settings(pairs: list[tuple[str, str]]) -> dict[str, str]:
    settings: dict[str, str] = {}
    for key, value in pairs:
        breakpoint()
        settings[key] = (
            value  # seeded bug source: a reused key silently overwrites its old value
        )
    return settings


if __name__ == "__main__":
    pairs = [("theme", "dark"), ("region", "us-west"), ("theme", "light")]
    print(build_settings(pairs))
