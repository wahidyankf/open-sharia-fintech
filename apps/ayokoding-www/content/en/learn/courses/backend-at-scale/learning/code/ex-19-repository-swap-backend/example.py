# pyright: strict
"""Example 19: Repository -- swap the backend, callers unchanged. (co-09)

A Repository is an ABSTRACTION over storage. Two implementations (an in-
memory dict and a "sql-like" list-backed one) both satisfy the SAME protocol,
so the domain code that uses them never changes when the backend is swapped.
"""

from dataclasses import dataclass  # => a small typed domain object
from typing import Protocol  # => Protocol: a structural interface both backends satisfy


@dataclass  # => the domain object
class Task:
    id: int  # => the resource identifier
    title: str  # => the resource's own data


class TaskRepository(Protocol):  # => co-09: the collection-like interface BOTH backends implement
    def add(self, title: str) -> Task: ...  # => add one member
    def all(self) -> list[Task]: ...  # => the whole collection


class InMemoryRepo:  # => co-09: backend 1 -- a dict
    def __init__(self) -> None:
        self._store: dict[int, Task] = {}  # => dict-backed storage
        self._next = 1  # => the next id

    def add(self, title: str) -> Task:
        task = Task(self._next, title)  # => builds the domain object
        self._store[task.id] = task  # => persists in a dict
        self._next += 1  # => advances the id
        return task  # => returns the added member

    def all(self) -> list[Task]:
        return list(self._store.values())  # => snapshot of the dict


class ListBackedRepo:  # => co-09: backend 2 -- a "sql-like" list of rows
    def __init__(self) -> None:
        self._rows: list[Task] = []  # => list-backed storage (stands in for a SQL table)

    def add(self, title: str) -> Task:
        next_id = (max((t.id for t in self._rows), default=0)) + 1  # => derives the next id from existing rows
        task = Task(next_id, title)  # => builds the domain object
        self._rows.append(task)  # => appends a row (stands in for an INSERT)
        return task  # => returns the added member

    def all(self) -> list[Task]:
        return list(self._rows)  # => snapshot of the list


def use(repo: TaskRepository) -> None:  # => co-09: domain code that depends on the PROTOCOL, not a backend
    repo.add("Shared task A")  # => add through the interface
    repo.add("Shared task B")  # => add through the interface
    print(f"  members: {[t.title for t in repo.all()]}")  # => Output: both tasks, regardless of backend


print("InMemoryRepo:")  # => Output: header for backend 1
use(InMemoryRepo())  # => co-09: callers unchanged
print("ListBackedRepo:")  # => Output: header for backend 2
use(ListBackedRepo())  # => co-09: SAME domain code, DIFFERENT backend

# The domain `use()` function references ONLY the protocol -- swapping the backend changed nothing in it.
