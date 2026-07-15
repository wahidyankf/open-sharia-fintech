"""Pass-1 capstone: Habit Tracker -- the OO domain model (topic 08) + apt data structure (topic 07).

`Habit` bundles its check-in state with the ONE operation allowed to mutate it
(`record_checkin`) and the operations that read it (`has_checkin_on`, `current_streak`) --
topic 08's big idea: "bundle state with the operations that guard it, and expose behavior,
not fields." Nothing outside this class ever touches `_checkin_dates` directly.

The check-in dates are stored in a `set[date]` (co-09 hash-set, topic 07) rather than a
`list[date]`: `current_streak()` below asks "is this ONE specific day present?" once per day
of the streak, and a hash-set answers that in average O(1) -- a `list` would need an O(n)
linear scan (co-13) per day checked, turning an O(streak) walk into an O(streak * n) one.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass(
    slots=True
)  # => slots=True (Python 3.10+): no per-instance __dict__ (topic 08 co-06)
class Habit:
    """A single habit, its archived flag, and the check-in history that decides its streak."""

    id: int  # => the DB row id; 0 for a not-yet-persisted (in-memory only) instance
    name: str  # => e.g. "Read 20 minutes" -- validated non-blank in __post_init__ below
    archived: bool = (
        False  # => guarded ONLY by archive() below -- never flipped from outside
    )
    _checkin_dates: set[date] = field(
        default_factory=set[date]
    )  # => co-09: hash-set, O(1) average membership

    def __post_init__(self) -> None:
        if (
            not self.name.strip()
        ):  # => co-04 constraint enforced in the domain layer, not just the DB
            raise ValueError(
                "habit name must not be blank"
            )  # => an invalid Habit can never exist

    def archive(self) -> None:
        """The ONE way to archive a habit -- bundles the state change with its own guard
        (topic 08's big idea): archiving twice is a safe no-op, never an error."""
        self.archived = True

    def record_checkin(self, day: date) -> None:
        """Record a check-in for `day`. Idempotent: checking in twice on the same day is a no-op,
        because `set.add` on an already-present element changes nothing (co-09)."""
        self._checkin_dates.add(day)  # => O(1) average insert into the hash-set

    def has_checkin_on(self, day: date) -> bool:
        """O(1) average membership test -- the exact operation a hash-set is apt for (co-09),
        versus an O(n) scan a `list` would force (co-13)."""
        return day in self._checkin_dates

    def checkin_count(self) -> int:
        """Total distinct days checked in, ever -- used only for reporting, never for the streak."""
        return len(self._checkin_dates)

    def current_streak(self, today: date) -> int:
        """The number of CONSECUTIVE days, walking backward from `today`, that have a check-in.

        Big-O: this walks at most `streak + 1` days, each a single hash-set lookup -- O(streak)
        total (co-01 big-o-notation), not O(streak * total_checkins) the way a `list`-backed
        linear scan per day would cost.
        """
        streak = 0
        day = today
        while self.has_checkin_on(
            day
        ):  # => stops at the first missing day, walking backward
            streak += 1
            day -= timedelta(days=1)  # => one calendar day earlier
        return streak
