"""Pass-1 capstone: a Hypothesis property test for `Habit.current_streak()` (topic 15
co-18 property-based-testing, co-20 strategies). Instead of a handful of hand-picked
example dates, this generates HUNDREDS of random streak lengths and re-checks the same
invariant every time -- a much stronger guarantee than any fixed set of examples in
test_domain.py could offer alone.
"""

from datetime import date, timedelta

from hypothesis import (
    given,
)  # => same property-test decorator style as software-testing/ex-44 (co-18)
from hypothesis import strategies as st  # => st.integers() generates the streak length to test  # fmt: skip

from app.domain import Habit

TODAY = date(
    2026, 7, 16
)  # => a FIXED reference date -- keeps every generated example reproducible


@given(st.integers(min_value=0, max_value=90))  # => co-20 strategies: any streak from 0 to 90 days  # fmt: skip
def test_n_consecutive_checkins_ending_today_produce_a_streak_of_exactly_n(
    streak_length: int,
) -> None:
    # => INVARIANT: recording exactly `streak_length` CONSECUTIVE days ending at TODAY must
    # => always produce current_streak(TODAY) == streak_length -- true for streak_length == 0
    # => (no check-ins at all) all the way up to any arbitrarily long run Hypothesis picks (co-18)
    habit = Habit(id=1, name="Read 20 minutes")
    for offset in range(
        streak_length
    ):  # => offset 0 = today, offset 1 = yesterday, ...
        habit.record_checkin(TODAY - timedelta(days=offset))
    assert habit.current_streak(TODAY) == streak_length


@given(st.integers(min_value=1, max_value=90))  # => fmt: skip
def test_a_single_gap_the_day_before_the_streak_never_extends_it(
    streak_length: int,
) -> None:
    # => INVARIANT: check-ins are recorded for `streak_length` consecutive days ending today,
    # => but the day IMMEDIATELY BEFORE that run is deliberately left un-checked-in -- the
    # => streak must stop exactly at `streak_length`, never accidentally "leak" past the gap
    habit = Habit(id=1, name="Read 20 minutes")
    for offset in range(streak_length):
        habit.record_checkin(TODAY - timedelta(days=offset))
    gap_day = TODAY - timedelta(
        days=streak_length
    )  # => the one day this test NEVER checks in
    assert habit.has_checkin_on(gap_day) is False  # => sanity: the gap really is a gap
    assert (
        habit.current_streak(TODAY) == streak_length
    )  # => the gap bounds the streak exactly
