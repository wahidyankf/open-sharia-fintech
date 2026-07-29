# pyright: strict
"""Example 20: Unit of Work -- track changes, commit once. (co-10)

A Unit of Work maintains a list of objects affected by a business transaction
and coordinates writing them out -- all changes commit together on commit().
Source: Martin Fowler, PoEAA -- Unit of Work pattern.
"""

from dataclasses import dataclass  # => a small typed domain object


@dataclass  # => the domain object; mutated in memory, flushed by the UoW
class Task:
    id: int  # => the resource identifier
    title: str  # => mutated during the transaction


@dataclass  # => co-10: a fully-typed snapshot of everything commit() writes out, together
class Flush:
    inserted: list[dict[str, object]]  # => the new objects, serialized
    updated: list[dict[str, object]]  # => the modified objects, serialized
    deleted_ids: list[int]  # => the removed ids


class UnitOfWork:  # => co-10: tracks the objects changed in one business transaction
    def __init__(self) -> None:
        self._new: list[Task] = []  # => objects to INSERT on commit
        self._dirty: list[Task] = []  # => objects to UPDATE on commit
        self._deleted_ids: list[int] = []  # => object ids to DELETE on commit
        self.committed = False  # => whether commit() has run

    def register_new(self, task: Task) -> None:  # => track a brand-new object
        self._new.append(task)  # => queued for INSERT

    def register_dirty(self, task: Task) -> None:  # => track a modified existing object
        self._dirty.append(task)  # => queued for UPDATE

    def register_deleted(self, task_id: int) -> None:  # => track a removal
        self._deleted_ids.append(task_id)  # => queued for DELETE

    def commit(self) -> Flush:  # => co-10: write ALL tracked changes out, together
        flush = Flush(  # => one coordinated write-out of every change
            inserted=[t.__dict__ for t in self._new],  # => the new objects, serialized
            updated=[t.__dict__ for t in self._dirty],  # => the modified objects, serialized
            deleted_ids=list(self._deleted_ids),  # => the removed ids
        )
        self.committed = True  # => the transaction is now durably written
        return flush  # => the single, coordinated result


uow = UnitOfWork()  # => co-10: open a business transaction
uow.register_new(Task(id=1, title="New task"))  # => stage an INSERT (not written yet)
existing = Task(id=2, title="old")  # => an existing object loaded into the transaction
existing.title = "updated"  # => mutate it in memory
uow.register_dirty(existing)  # => stage an UPDATE (not written yet)
uow.register_deleted(7)  # => stage a DELETE (not written yet)
print(f"committed before commit(): {uow.committed}")  # => Output: False -- nothing written yet

flush = uow.commit()  # => co-10: ALL three changes land TOGETHER in one write-out
print(f"flush: {flush}")  # => Output: inserted + updated + deleted, all at once

assert uow.committed is True  # => co-10: the transaction committed
assert len(flush.inserted) == 1 and len(flush.updated) == 1 and flush.deleted_ids == [7]  # => all three changes landed
