"""capstone-solid-core: tests for the application layer (topic 21 SOLID) -- AND the Open/Closed
Principle proof the syllabus spec requires: `InMemoryHabitRepository` below is a SECOND class
satisfying `ports.HabitRepository`, written ENTIRELY IN THIS TEST FILE. It required editing
NEITHER `app/services.py` NOR `app/ports.py` NOR `app/repository_sqlite.py` -- "closed for
modification" -- while `HabitService` accepts it exactly as it accepts the real SQLite adapter
-- "open for extension" (Python's `typing.Protocol`, PEP 544, matches by structural shape, not
by declared inheritance -- `InMemoryHabitRepository` never imports or subclasses
`HabitRepository`).

Every test below exercises `HabitService` with ZERO real database and ZERO HTTP server --
proof that the business rules in services.py are independently testable from the storage
mechanism (Dependency Inversion Principle).
"""

from __future__ import annotations

from datetime import date

import pytest

from app.domain import Habit
from app.models import HabitCreate
from app.services import HabitService


class InMemoryHabitRepository:
    """The NEW variation (topic 21 OCP): a dict-backed repository satisfying
    `ports.HabitRepository` by SHAPE alone. Never touches sqlite3. Never edits any shipped
    file. Exists ONLY in this test module."""

    def __init__(self) -> None:
        self._habits: dict[int, Habit] = {}
        self._owners: dict[int, int] = {}  # => habit_id -> user_id
        self._next_id = 1

    def create_habit(self, user_id: int, data: HabitCreate) -> Habit:
        habit = Habit(id=self._next_id, name=data.name)
        self._habits[habit.id] = habit
        self._owners[habit.id] = user_id
        self._next_id += 1
        return habit

    def get_habit(self, habit_id: int, user_id: int) -> Habit | None:
        if self._owners.get(habit_id) != user_id:
            return None
        return self._habits.get(habit_id)

    def list_habits(self, user_id: int, include_archived: bool = False) -> list[Habit]:
        return [
            h
            for hid, h in self._habits.items()
            if self._owners.get(hid) == user_id and (include_archived or not h.archived)
        ]

    def search_habits(self, user_id: int, q: str) -> list[Habit]:
        return [
            h
            for h in self.list_habits(user_id, include_archived=True)
            if q.lower() in h.name.lower()
        ]

    def archive_habit(self, habit_id: int, user_id: int) -> Habit | None:
        habit = self.get_habit(habit_id, user_id)
        if habit is None:
            return None
        habit.archive()
        return habit

    def delete_habit(self, habit_id: int, user_id: int) -> bool:
        if self._owners.get(habit_id) != user_id:
            return False
        del self._habits[habit_id]
        del self._owners[habit_id]
        return True

    def record_checkin(
        self, habit_id: int, user_id: int, checkin_date_iso: str
    ) -> None:
        habit = self._habits[habit_id]
        habit.record_checkin(date.fromisoformat(checkin_date_iso))

    def recent_activity(self, user_id: int, limit: int) -> list[tuple[int, str]]:
        entries: list[tuple[int, str]] = []
        for hid, habit in self._habits.items():
            if self._owners.get(hid) != user_id:
                continue
            for checkin_day in habit._checkin_dates:  # => test-only introspection
                entries.append((hid, checkin_day.isoformat()))
        entries.sort(key=lambda pair: pair[1], reverse=True)
        return entries[:limit]


@pytest.fixture()
def service() -> HabitService:
    return HabitService(
        InMemoryHabitRepository()
    )  # => the NEW variation, wired in directly


class TestHabitServiceWithInMemoryRepository:
    """Every assertion below is IDENTICAL in spirit to test_app.py's integration tests against
    the real SQLite-backed API -- proof the same business rules hold regardless of which
    HabitRepository implementation HabitService is handed (OCP + DIP working together)."""

    def test_create_then_get_round_trips(self, service: HabitService) -> None:
        created = service.create_habit(
            user_id=1, data=HabitCreate(name="Read 20 minutes")
        )
        fetched = service.get_habit(created.id, user_id=1)
        assert fetched is not None
        assert fetched.name == "Read 20 minutes"

    def test_checkin_updates_streak(self, service: HabitService) -> None:
        habit = service.create_habit(user_id=1, data=HabitCreate(name="Floss"))
        today = date(2026, 7, 16)
        updated = service.record_checkin(habit.id, user_id=1, checkin_day=today)
        assert updated is not None
        assert updated.current_streak(today) == 1

    def test_checkin_against_a_habit_the_caller_does_not_own_is_rejected(
        self, service: HabitService
    ) -> None:
        habit = service.create_habit(user_id=1, data=HabitCreate(name="Dave's habit"))
        result = service.record_checkin(
            habit.id, user_id=2, checkin_day=date(2026, 7, 16)
        )
        assert (
            result is None
        )  # => the SAME ownership rule test_app.py verifies over HTTP

    def test_search_filters_by_substring(self, service: HabitService) -> None:
        service.create_habit(user_id=1, data=HabitCreate(name="Read 20 minutes"))
        service.create_habit(user_id=1, data=HabitCreate(name="Drink water"))
        results = service.list_habits(user_id=1, q="Read")
        assert len(results) == 1
        assert results[0].name == "Read 20 minutes"

    def test_archiving_hides_from_the_default_list(self, service: HabitService) -> None:
        habit = service.create_habit(user_id=1, data=HabitCreate(name="Old habit"))
        service.archive_habit(habit.id, user_id=1)
        assert service.list_habits(user_id=1) == []
        assert len(service.list_habits(user_id=1, include_archived=True)) == 1

    def test_recent_activity_orders_newest_first(self, service: HabitService) -> None:
        habit = service.create_habit(
            user_id=1, data=HabitCreate(name="Read 20 minutes")
        )
        service.record_checkin(habit.id, user_id=1, checkin_day=date(2026, 7, 1))
        service.record_checkin(habit.id, user_id=1, checkin_day=date(2026, 7, 16))
        activity = service.recent_activity(user_id=1, limit=10)
        assert [checkin_date for _, checkin_date in activity] == [
            "2026-07-16",
            "2026-07-01",
        ]
