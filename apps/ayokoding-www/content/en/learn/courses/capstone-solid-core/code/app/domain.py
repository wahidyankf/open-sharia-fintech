"""capstone-solid-core: the functional core (topic 22 Programming Paradigms, topic 23
Functional Programming) plus the thin imperative-shell object it backs (topic 08 OOP, topic 21
SOLID). Every computation below is a PURE function -- no I/O, no mutation of anything outside
its own arguments, same output for the same input every time -- so each one is independently
unit-testable and benchmarkable with zero database and zero HTTP server (functional core /
imperative shell, DD-33 taming-state). `Habit` is the imperative shell: it owns identity and
mutable state (its own check-in set), and delegates every actual computation to the pure
functions below instead of inlining the logic as methods, the same "bundle state with the
operations that guard it" idea Pass 1 topic 08 taught, now split so the REASONING part carries
no state at all.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


def current_streak(checkin_dates: set[date], today: date) -> int:
    """PURE (topic 23): the count of CONSECUTIVE days, walking backward from `today`, present
    in `checkin_dates`. Unchanged from Pass 1's algorithm (topic 07 co-09 hash-set: O(1)
    average membership per day) -- now extracted as a free function so it can be called,
    tested, and benchmarked without ever constructing a `Habit`."""
    streak = 0
    day = today
    while day in checkin_dates:  # => O(1) average hash-set membership test (topic 07)
        streak += 1
        day -= timedelta(days=1)
    return streak  # => O(streak) total, same bound Pass 1 established


def longest_streak_ever_naive(checkin_dates: set[date]) -> int:
    """BEFORE (topic 25 Advanced Algorithms baseline, kept here for the benchmark's own
    comparison -- never called by the shipped app): sort every date, then scan once for the
    longest run of consecutive days. `sorted()` costs O(n log n) (Timsort) and DOMINATES the
    total cost for a large check-in history -- the O(n) scan that follows it is comparatively
    free."""
    if not checkin_dates:
        return 0
    ordered = sorted(
        checkin_dates
    )  # => O(n log n): the cost this function exists to remove
    longest = 1
    current = 1
    for previous_day, this_day in zip(ordered, ordered[1:]):
        if this_day - previous_day == timedelta(days=1):  # => consecutive calendar days
            current += 1
            longest = max(longest, current)
        else:
            current = 1  # => the run broke; restart counting from this_day
    return longest


def longest_streak_ever(checkin_dates: set[date]) -> int:
    """AFTER (topic 25 Advanced Algorithms): O(n) total, no sort. The classic "longest
    consecutive sequence over a hash-set" technique applied to calendar dates instead of
    integers: a date only STARTS counting a run if the day before it is absent from the set --
    every other date is skipped in O(1) by that one membership test. Because only run-STARTS
    trigger the inner walk, and every date is visited by at most one run's walk across the
    WHOLE function, the total work across all iterations is O(n), not O(n^2) and not
    O(n log n) -- this is an amortized argument (topic 19 CS Foundations complexity
    reasoning), not a per-call bound on the inner while loop alone.

    IMPLEMENTATION NOTE (measured, not assumed -- see bench/benchmark_algorithm.py): a FIRST
    version of this function worked directly with `date`/`timedelta` objects (`day -
    timedelta(days=1) in checkin_dates`, `probe += timedelta(days=1)`) and was actually SLOWER
    in wall-clock terms than the O(n log n) `_naive` baseline above at every size tested, up to
    n=500,000 -- Python's built-in `sorted()` is implemented in C with very low per-comparison
    overhead, while constructing a new `timedelta` object on every iteration of a pure-Python
    loop is comparatively expensive. Converting each `date` to its integer ordinal
    (`date.toordinal()`, Python stdlib -- docs.python.org/3/library/datetime.html:
    "Return the proleptic Gregorian ordinal of the date") once up front, then doing the SAME
    algorithm over a `set[int]` with plain integer +/-1 instead of `timedelta` construction,
    measured 2.59x-2.86x FASTER than the naive baseline across the same size range -- the
    asymptotic O(n) advantage only became a real wall-clock advantage once the Python-level
    constant-factor overhead (repeated object construction) was removed. Big-O describes what
    happens as n grows; it does not by itself guarantee a win at any one concrete n in a
    language with per-object overhead -- that has to be measured."""
    if not checkin_dates:
        return 0
    ordinals = {
        day.toordinal() for day in checkin_dates
    }  # => O(n): once, not per-comparison
    longest = 0
    for ordinal in ordinals:  # => O(n) over the set, one membership test per element
        if (ordinal - 1) in ordinals:
            continue  # => NOT a run-start -- some other day's walk already counts this one
        run_length = 1
        probe = ordinal + 1
        while probe in ordinals:  # => walks forward ONLY from a genuine run-start
            run_length += 1
            probe += 1
        longest = max(longest, run_length)
    return longest


@dataclass(slots=True)  # => slots=True (topic 08 co-06): no per-instance __dict__
class Habit:
    """The imperative shell (DD-33 taming-state): owns identity (`id`, `name`, `archived`) and
    the ONE piece of mutable state (`_checkin_dates`), and is the ONLY thing anything outside
    this module ever touches directly. Every computation is DELEGATED to the pure functions
    above, not inlined -- so `current_streak`/`longest_streak_ever` never need a `Habit`
    instance to be tested or benchmarked, and this class never needs to know HOW they work."""

    id: int  # => the DB row id; 0 for a not-yet-persisted (in-memory only) instance
    name: str  # => validated non-blank in __post_init__ below
    archived: bool = (
        False  # => guarded ONLY by archive() below -- never flipped from outside
    )
    _checkin_dates: set[date] = field(
        default_factory=set[date]
    )  # => co-09: hash-set, O(1) average membership

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("habit name must not be blank")

    def archive(self) -> None:
        """The ONE way to archive a habit -- archiving twice is a safe no-op, never an error."""
        self.archived = True

    def record_checkin(self, day: date) -> None:
        """Record a check-in for `day`. Idempotent: `set.add` on an already-present element
        changes nothing."""
        self._checkin_dates.add(day)  # => O(1) average insert into the hash-set

    def has_checkin_on(self, day: date) -> bool:
        return day in self._checkin_dates  # => O(1) average

    def checkin_count(self) -> int:
        return len(self._checkin_dates)

    def current_streak(self, today: date) -> int:
        """Delegates to the pure `current_streak` function above -- this method adds no logic
        of its own, only the state to compute over."""
        return current_streak(self._checkin_dates, today)

    def longest_streak_ever(self) -> int:
        """Delegates to the pure, O(n) `longest_streak_ever` function above."""
        return longest_streak_ever(self._checkin_dates)
