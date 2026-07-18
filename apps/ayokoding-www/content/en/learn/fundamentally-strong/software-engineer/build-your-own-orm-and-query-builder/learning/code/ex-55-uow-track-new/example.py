"""Example 55: UnitOfWork.register_new -- Tracking a Brand-New, Not-Yet-Saved Object."""  # => this concept

import dataclasses  # => the domain object being tracked


@dataclasses.dataclass  # => a domain object -- not yet persisted anywhere
class User:  # => the type this example's unit of work tracks
    id: int | None  # => None because it has NO row yet -- the pk is assigned by the database on insert
    name: str  # => an ordinary column


class UnitOfWork:  # => co-16: collects pending changes, does not write anything itself yet
    def __init__(self) -> None:  # => starts with nothing tracked
        self._new: list[User] = []  # => co-16: objects registered as "new" -- will become INSERTs later

    def register_new(self, user: User) -> None:  # => co-16: the ONLY way an object enters the "new" set
        self._new.append(user)  # => appended, not written -- no SQL runs here at all

    @property  # => read-only view of the tracked-new set, for observation in tests/examples
    def new_objects(self) -> list[User]:  # => exposes what would become INSERTs on a later flush
        return self._new  # => the SAME list every time -- no copy, no hidden mutation


uow = UnitOfWork()  # => co-16: one unit of work, tracking pending changes for a "session"
alice = User(id=None, name="Alice")  # => a brand-new object -- no pk yet, no row in the database
uow.register_new(alice)  # => co-16: tracked as "new" -- STILL no SQL has run
assert alice not in []  # => sanity: alice exists as a Python object regardless of tracking
assert uow.new_objects == [alice]  # => co-16: exactly one object tracked, and it is `alice` itself
assert len(uow.new_objects) == 1  # => the tracked-new set has exactly one entry
print(len(uow.new_objects))  # => Output: 1
