"""Example 74: Read a Failing pytest Traceback -- Locate the Assertion and the Offending Values."""

from __future__ import annotations


def parse_price(text: str) -> float:  # => co-27: the function whose bug the traceback below exposes  # fmt: skip
    cleaned = text.strip("$")  # => strips a leading "$" -- but NOT thousands-separating commas  # fmt: skip
    return float(cleaned)  # => co-03: this line is where the REAL exception below actually raises  # fmt: skip


def test_parse_price_handles_thousands_separator() -> None:  # => co-27: deliberately exposes the bug  # fmt: skip
    # "$1,234.56" is a realistic price string -- but parse_price() above never strips the comma,
    # so float() receives "1,234.56" and raises ValueError, two frames below THIS assertion.
    assert parse_price("$1,234.56") == 1234.56  # => co-03/co-27: this line is frame #1 in the traceback  # fmt: skip
