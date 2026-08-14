"""Example 14: a date range owns its ordering invariant."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError("start must precede end")  # => prevent inversion


assert DateRange(date(2026, 1, 1), date(2026, 1, 2)).start.year == 2026
