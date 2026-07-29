# pyright: strict
"""Example 21: Unit of Work -- rollback discards tracked changes. (co-10, co-11)

Rolling back a Unit of Work throws away EVERY staged change: nothing the
transaction registered is written out. This is the atomic-commit boundary
(co-11) from the discard side -- either everything commits, or nothing does.
"""

from dataclasses import dataclass  # => a small typed domain object


@dataclass  # => the domain object staged in the transaction
class Task:
    id: int  # => the resource identifier
    title: str  # => the resource's own data


STORE: dict[int, Task] = {1: Task(1, "persistent")}  # => the durable store -- rollback must leave it untouched


class UnitOfWork:  # => co-10: a staging area for one business transaction
    def __init__(self, store: dict[int, Task]) -> None:
        self._store = store  # => the durable backing store
        self._pending: list[Task] = []  # => staged changes, NOT yet written

    def register_new(self, task: Task) -> None:  # => stage an insert
        self._pending.append(task)  # => queued, not yet visible in the store

    def commit(self) -> None:  # => co-10: write every staged change into the store
        for task in self._pending:  # => flush each staged object
            self._store[task.id] = task  # => durably written

    def rollback(self) -> None:  # => co-10/co-11: discard ALL staged changes
        self._pending.clear()  # => nothing staged is ever written -- the store is untouched


uow = UnitOfWork(STORE)  # => open a transaction over the durable store
uow.register_new(Task(2, "ephemeral"))  # => stage a change -- NOT yet in STORE
print(f"store before rollback: { {k: v.title for k, v in STORE.items()} }")  # => Output: only id 1

uow.rollback()  # => co-10/co-11: discard -- the staged task is gone
print(f"store after rollback:  { {k: v.title for k, v in STORE.items()} }")  # => Output: still only id 1

assert 2 not in STORE and STORE[1].title == "persistent"  # => co-11: no tracked change persisted after rollback
