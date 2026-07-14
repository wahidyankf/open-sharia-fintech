"""Example 47: pytest verification for A classmethod Alternative Constructor."""

from example import Date


def test_from_string_builds_instance_from_parsed_text() -> None:
    d: Date = Date.from_string("2026-07-14")
    assert (d.year, d.month, d.day) == (
        2026,
        7,
        14,
    )  # => parsed pieces landed in the right fields


# => Run: pytest -- Output: 1 passed
