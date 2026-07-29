# pyright: strict
"""Example 18: Repository -- a collection-like interface over a store. (co-09)

A Repository mediates between the domain and the data store, exposing a
COLLECTION-LIKE interface (add/get/all/remove) so the domain never touches
the storage mechanism directly. Source: Martin Fowler, PoEAA -- "a
collection-like interface for accessing domain objects."
"""

from dataclasses import dataclass  # => a small typed domain object


@dataclass  # => the domain object this repository holds
class Task:
    id: int  # => the resource identifier
    title: str  # => the resource's own data


class TaskRepository:  # => co-09: a collection-like interface over an in-memory store
    def __init__(self) -> None:
        self._store: dict[int, Task] = {}  # => the private storage; callers never touch this
        self._next_id = 1  # => the id minted by the NEXT add()

    def add(self, title: str) -> Task:  # => add one member to the collection
        task = Task(id=self._next_id, title=title)  # => a new domain object
        self._store[task.id] = task  # => persists it
        self._next_id += 1  # => advances the id counter
        return task  # => returns the added member

    def get(self, task_id: int) -> Task | None:  # => fetch one member by id
        return self._store.get(task_id)  # => None when absent -- a collection's "not found"

    def all(self) -> list[Task]:  # => the whole collection
        return list(self._store.values())  # => a snapshot list, decoupled from internal storage

    def remove(self, task_id: int) -> bool:  # => remove one member
        if task_id in self._store:  # => present -> delete and report success
            del self._store[task_id]  # => removes the member
            return True  # => removed
        return False  # => nothing to remove


repo = TaskRepository()  # => co-09: the domain talks to THIS, not to a dict directly
created = repo.add("Write docs")  # => CREATE through the collection interface
repo.add("Ship release")  # => a second member
print(f"get(1): {repo.get(1)}")  # => Output: Task(id=1, title='Write docs')
print(f"all():  {repo.all()}")  # => Output: both tasks
print(f"remove(1): {repo.remove(1)}")  # => Output: True
print(f"get(1) after remove: {repo.get(1)}")  # => Output: None -- gone from the collection

assert repo.get(1) is None and len(repo.all()) == 1  # => co-09: full CRUD round-trip through the repository
