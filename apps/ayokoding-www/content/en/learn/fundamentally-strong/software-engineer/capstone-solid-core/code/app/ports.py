"""capstone-solid-core: the repository PORT (topic 21 SOLID -- Dependency Inversion Principle).

`HabitService` (services.py) depends ONLY on this `Protocol` (structural typing, PEP 544 --
stable in the Python standard library `typing` module since Python 3.8, no third-party
dependency) -- never on `sqlite3`, never on a concrete database driver. A new storage backend
is added later by writing a new class shaped like this Protocol, with ZERO edits to
`HabitService` or to this file (Open/Closed Principle -- "open for extension, closed for
modification"). `test_services.py`'s `InMemoryHabitRepository` is exactly that new variation,
and it proves the point: it satisfies this same Protocol, `HabitService` never imports it, and
every existing test keeps passing unmodified.
"""

from __future__ import annotations

from typing import Protocol

from .domain import Habit
from .models import HabitCreate


class HabitRepository(Protocol):
    """The shape any storage backend must satisfy. Pure interface: no implementation, no
    state -- `Protocol` classes are never instantiated directly."""

    def create_habit(self, user_id: int, data: HabitCreate) -> Habit: ...

    def get_habit(self, habit_id: int, user_id: int) -> Habit | None: ...

    def list_habits(
        self, user_id: int, include_archived: bool = False
    ) -> list[Habit]: ...

    def search_habits(self, user_id: int, q: str) -> list[Habit]: ...

    def archive_habit(self, habit_id: int, user_id: int) -> Habit | None: ...

    def delete_habit(self, habit_id: int, user_id: int) -> bool: ...

    def record_checkin(
        self, habit_id: int, user_id: int, checkin_date_iso: str
    ) -> None: ...

    def recent_activity(self, user_id: int, limit: int) -> list[tuple[int, str]]: ...
