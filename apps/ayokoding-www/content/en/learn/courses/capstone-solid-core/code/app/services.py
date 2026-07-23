"""capstone-solid-core: the application/use-case layer (topic 21 SOLID -- Single
Responsibility Principle). `HabitService` knows the HABIT-TRACKING RULES (e.g. "a check-in
needs an existing, owned habit") and orchestrates the repository port + the functional core --
it never touches `sqlite3`, never touches FastAPI's `Request`/`Response`. `main.py`'s route
handlers (the imperative shell's HTTP edge) are thin: parse the request, call one
`HabitService` method, shape the response -- no business rule lives in a route handler.

This is exactly the layer `test_services.py` exercises directly, with a fake in-memory
repository and zero real database -- proof that the business rules are independently testable
from the storage mechanism (Dependency Inversion, topic 21).
"""

from __future__ import annotations

from datetime import date

from .domain import Habit
from .models import HabitCreate
from .ports import HabitRepository


class HabitService:
    def __init__(self, repo: HabitRepository) -> None:
        self._repo = (
            repo  # => depends on the ABSTRACTION (DIP), never a concrete DB class
        )

    def create_habit(self, user_id: int, data: HabitCreate) -> Habit:
        return self._repo.create_habit(user_id, data)

    def get_habit(self, habit_id: int, user_id: int) -> Habit | None:
        return self._repo.get_habit(habit_id, user_id)

    def list_habits(
        self, user_id: int, include_archived: bool = False, q: str | None = None
    ) -> list[Habit]:
        if q:  # => the ONE business rule this method owns: q present means SEARCH, not LIST
            return self._repo.search_habits(user_id, q)
        return self._repo.list_habits(user_id, include_archived)

    def archive_habit(self, habit_id: int, user_id: int) -> Habit | None:
        return self._repo.archive_habit(habit_id, user_id)

    def delete_habit(self, habit_id: int, user_id: int) -> bool:
        return self._repo.delete_habit(habit_id, user_id)

    def record_checkin(
        self, habit_id: int, user_id: int, checkin_day: date
    ) -> Habit | None:
        """The business rule this method owns: a check-in is only valid against a habit this
        user actually owns -- the ownership check happens HERE, once, rather than being
        re-implemented by every caller."""
        habit = self._repo.get_habit(habit_id, user_id)
        if habit is None:
            return None
        self._repo.record_checkin(habit_id, user_id, checkin_day.isoformat())
        habit.record_checkin(
            checkin_day
        )  # => mirror the write into the in-memory object too --
        return (
            habit  # => the caller's response reflects it without a second DB round trip
        )

    def recent_activity(self, user_id: int, limit: int) -> list[tuple[int, str]]:
        return self._repo.recent_activity(user_id, limit)
