"""capstone-solid-core: unit tests for the functional core (topic 15 pytest, topic 23 pure
functions, topic 25 Advanced Algorithms). Pure, in-memory, no DB and no server -- the base of
the testing pyramid, and behavior-preservation evidence for Step 2's refactor: every one of
these assertions ALSO passed against Pass-1's `Habit` before this capstone touched it.
"""

import random
from datetime import date, timedelta

import pytest

from app.domain import Habit, longest_streak_ever, longest_streak_ever_naive


class TestHabitInvariants:
    def test_blank_name_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="blank"):
            Habit(id=1, name="   ")

    def test_new_habit_has_no_checkins_and_zero_streak(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        assert habit.checkin_count() == 0
        assert habit.current_streak(date(2026, 7, 16)) == 0

    def test_new_habit_is_not_archived(self) -> None:
        assert Habit(id=1, name="Read 20 minutes").archived is False

    def test_archive_is_idempotent(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        habit.archive()
        habit.archive()  # => a second call is a safe no-op, never an error
        assert habit.archived is True


class TestCheckins:
    def test_record_checkin_is_idempotent(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        today = date(2026, 7, 16)
        habit.record_checkin(today)
        habit.record_checkin(today)  # => recording the SAME day twice changes nothing
        assert habit.checkin_count() == 1

    def test_has_checkin_on_reflects_exactly_what_was_recorded(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        recorded_day = date(2026, 7, 16)
        other_day = date(2026, 7, 15)
        habit.record_checkin(recorded_day)
        assert habit.has_checkin_on(recorded_day) is True
        assert habit.has_checkin_on(other_day) is False


class TestCurrentStreak:
    def test_streak_breaks_on_the_first_missing_day(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        today = date(2026, 7, 16)
        habit.record_checkin(today)
        habit.record_checkin(today - timedelta(days=1))
        habit.record_checkin(today - timedelta(days=2))
        habit.record_checkin(today - timedelta(days=4))  # => a GAP at day-3
        assert habit.current_streak(today) == 3

    def test_a_checkin_today_is_required_for_a_nonzero_streak(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        today = date(2026, 7, 16)
        habit.record_checkin(today - timedelta(days=1))  # => yesterday, but NOT today
        assert habit.current_streak(today) == 0

    def test_full_month_of_consecutive_checkins(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        today = date(2026, 7, 16)
        for offset in range(30):
            habit.record_checkin(today - timedelta(days=offset))
        assert habit.current_streak(today) == 30


class TestLongestStreakEver:
    """Step 2/Step 3: the O(n) `longest_streak_ever` (topic 25) must agree with the O(n log n)
    `longest_streak_ever_naive` baseline on every input -- correctness-preserving, not just
    faster. `test_algorithms_agree_on_random_histories` below is the cross-check the
    benchmark's own honesty depends on: if the two ever disagreed, the "before/after" timing
    comparison in bench/benchmark_algorithm.py would be comparing two DIFFERENT computations,
    not one computation done two ways."""

    def test_empty_history_has_longest_streak_zero(self) -> None:
        assert longest_streak_ever(set()) == 0
        assert longest_streak_ever_naive(set()) == 0

    def test_single_checkin_is_a_streak_of_one(self) -> None:
        dates = {date(2026, 7, 16)}
        assert longest_streak_ever(dates) == 1
        assert longest_streak_ever_naive(dates) == 1

    def test_two_separate_single_day_checkins_do_not_combine(self) -> None:
        dates = {date(2026, 7, 1), date(2026, 7, 16)}  # => 15 days apart, no run
        assert longest_streak_ever(dates) == 1
        assert longest_streak_ever_naive(dates) == 1

    def test_a_past_streak_can_be_longer_than_the_current_one(self) -> None:
        today = date(2026, 7, 16)
        dates = {
            today - timedelta(days=100),
            today - timedelta(days=99),
            today - timedelta(days=98),
            today - timedelta(days=97),
            today - timedelta(days=96),  # => a 5-day run, long ago
            today,  # => today alone -- current_streak() is 1, but longest_streak_ever is 5
        }
        habit = Habit(id=1, name="Read 20 minutes")
        for day in dates:
            habit.record_checkin(day)
        assert habit.current_streak(today) == 1
        assert habit.longest_streak_ever() == 5

    def test_overlapping_runs_pick_the_longest_one(self) -> None:
        today = date(2026, 7, 16)
        dates: set[date] = set()
        for offset in range(10):  # => a 10-day run
            dates.add(today - timedelta(days=offset))
        for offset in range(50, 55):  # => a separate, shorter 5-day run
            dates.add(today - timedelta(days=offset))
        assert longest_streak_ever(dates) == 10
        assert longest_streak_ever_naive(dates) == 10

    @pytest.mark.parametrize("seed", range(20))
    def test_algorithms_agree_on_random_histories(self, seed: int) -> None:
        """The O(n) and O(n log n) implementations must return the SAME answer for the SAME
        input, across 20 independently randomized histories -- correctness before speed."""
        rng = random.Random(seed)
        base = date(2020, 1, 1)
        dates = {
            base + timedelta(days=offset) for offset in rng.sample(range(2000), 300)
        }
        assert longest_streak_ever(dates) == longest_streak_ever_naive(dates)
