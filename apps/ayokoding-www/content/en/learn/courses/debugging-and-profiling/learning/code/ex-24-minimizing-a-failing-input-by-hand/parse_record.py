"""Example 24: Minimizing a Failing Input by Hand."""

from __future__ import annotations


def parse_record(raw: str) -> int:
    """Raises ValueError if the record contains the literal marker 'BADSEQ' anywhere."""
    if "BADSEQ" in raw:
        raise ValueError(
            f"malformed record near: ...{raw[max(0, raw.find('BADSEQ') - 5) : raw.find('BADSEQ') + 11]}..."
        )
    return len(raw)


def still_fails(raw: str) -> bool:
    try:
        parse_record(raw)
        return False
    except ValueError:
        return True
