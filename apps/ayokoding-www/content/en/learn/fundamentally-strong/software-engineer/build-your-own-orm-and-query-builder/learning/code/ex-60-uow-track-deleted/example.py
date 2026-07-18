"""Example 60: UnitOfWork.register_deleted -- Marking an Object for Removal."""  # => this concept

import dataclasses  # => the domain object being marked for deletion


@dataclasses.dataclass  # => an already-persisted domain object
class User:  # => the type this unit of work marks for removal
    id: int  # => primary key -- must be real, since deletion needs a row to target
    name: str  # => an ordinary column


class UnitOfWork:  # => co-18: collects objects marked for deletion, writes nothing yet
    def __init__(self) -> None:  # => starts with nothing tracked
        self._deleted: list[User] = []  # => co-18: objects registered as "deleted" -- become DELETEs later

    def register_deleted(self, user: User) -> None:  # => co-18: the ONLY way an object enters the "deleted" set
        self._deleted.append(user)  # => appended, not written -- no SQL runs here at all

    @property  # => read-only view of the tracked-deleted set, for observation in tests/examples
    def deleted_objects(self) -> list[User]:  # => exposes what would become DELETEs on a later flush
        return self._deleted  # => the SAME list every time -- no copy, no hidden mutation


uow = UnitOfWork()  # => co-18: one unit of work, tracking pending deletions for a "session"
alice = User(id=1, name="Alice")  # => a real, already-persisted object -- has a real pk
uow.register_deleted(alice)  # => co-18: tracked as "deleted" -- STILL no SQL has run
assert uow.deleted_objects == [alice]  # => exactly one object tracked, and it is `alice` itself
assert len(uow.deleted_objects) == 1  # => the tracked-deleted set has exactly one entry
print(len(uow.deleted_objects))  # => Output: 1
