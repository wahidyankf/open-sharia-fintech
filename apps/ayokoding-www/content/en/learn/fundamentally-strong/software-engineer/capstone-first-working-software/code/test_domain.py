"""Pass-1 capstone: unit tests for the OO domain model (topic 15 pytest, topic 08 OOP,
topic 07 hash-set). Pure, in-memory, no DB and no server -- the base of the testing pyramid.
"""

from datetime import date, timedelta

import pytest

from app.domain import Habit


class TestHabitInvariants:
    def test_blank_name_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="blank"):
            Habit(id=1, name="   ")  # => __post_init__ enforces the non-blank invariant

    def test_new_habit_has_no_checkins_and_zero_streak(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        assert habit.checkin_count() == 0
        assert habit.current_streak(date(2026, 7, 16)) == 0

    def test_new_habit_is_not_archived(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        assert habit.archived is False

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
        assert habit.checkin_count() == 1  # => still exactly one distinct day

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
        # => a GAP at day-3 -- the streak must stop counting there, not skip over it
        habit.record_checkin(today - timedelta(days=4))
        assert habit.current_streak(today) == 3

    def test_a_checkin_today_is_required_for_a_nonzero_streak(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        today = date(2026, 7, 16)
        habit.record_checkin(today - timedelta(days=1))  # => yesterday, but NOT today
        assert (
            habit.current_streak(today) == 0
        )  # => a streak with no check-in today is 0, not 1

    def test_full_month_of_consecutive_checkins(self) -> None:
        habit = Habit(id=1, name="Read 20 minutes")
        today = date(2026, 7, 16)
        for offset in range(
            30
        ):  # => 30 consecutive days, today back through 29 days ago
            habit.record_checkin(today - timedelta(days=offset))
        assert habit.current_streak(today) == 30
