"""Example 47: A classmethod Alternative Constructor."""

from __future__ import (
    annotations,
)  # => lets "Date" be used as a forward-referenced return type


class Date:  # => begins the Date class body
    def __init__(
        self, year: int, month: int, day: int
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.year = year  # => stores year on this instance
        self.month = month  # => stores month on this instance
        self.day = day  # => stores day on this instance

    @classmethod  # => marks the next method as receiving cls, not self
    def from_string(
        cls, s: str
    ) -> Date:  # => cls is the Date class itself, passed automatically
        year_s, month_s, day_s = s.split(
            "-"
        )  # => parses "YYYY-MM-DD" into three string pieces
        return cls(
            int(year_s), int(month_s), int(day_s)
        )  # => builds an instance via cls(...)


d: Date = Date.from_string(
    "2026-07-14"
)  # => an alternative entry point beside Date(...)
print(
    d.year, d.month, d.day
)  # => confirms the parsed pieces landed in the right fields
# => Output: 2026 7 14
# => `@classmethod` alternative constructors give a class more than one named entry point
