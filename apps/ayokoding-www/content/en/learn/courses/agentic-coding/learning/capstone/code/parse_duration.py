"""Capstone final: parse_duration -- convert an "1h30m"-style duration string to total seconds."""

from __future__ import annotations

import re

_TOKEN = re.compile(r"(\d+)([hms])")
_UNIT_SECONDS: dict[str, int] = {"h": 3600, "m": 60, "s": 1}


def parse_duration(s: str) -> int:
    """Parse a duration string like "1h30m" or "45s" into total whole seconds.

    Raises ValueError if `s` is empty, has no valid tokens, or has any
    unmatched/malformed trailing content.
    """
    if not s:
        raise ValueError("duration string must not be empty")
    total = 0
    consumed = 0
    for match in _TOKEN.finditer(s):
        total += _seconds_for_token(match.group(1), match.group(2))
        consumed += len(match.group(0))
    if consumed != len(s):
        raise ValueError(f"invalid duration string: {s!r}")
    return total


def _seconds_for_token(digits: str, unit: str) -> int:
    """Convert one (digits, unit) token into whole seconds."""
    return int(digits) * _UNIT_SECONDS[unit]
