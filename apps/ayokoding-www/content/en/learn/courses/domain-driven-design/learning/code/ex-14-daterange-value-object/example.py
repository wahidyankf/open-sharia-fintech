# => Keeps this domain step explicit and reviewable.
"""Example 14: a date range owns its ordering invariant."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass

# => Keeps the artifact runnable with explicit dependencies.
from datetime import date


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class DateRange:
    # => Keeps this domain step explicit and reviewable.
    start: date
    # => Keeps this domain step explicit and reviewable.
    end: date

    # => Names policy so callers do not recreate the rule.
    def __post_init__(self) -> None:
        # => Checks policy before a state change is allowed.
        if self.start >= self.end:
            raise ValueError("start must precede end")  # => prevent inversion


# => Proves the stated business rule is observable.
assert DateRange(date(2026, 1, 1), date(2026, 1, 2)).start.year == 2026
