"""Example 57: Detecting a Dirty Object by Comparing Live State to Its Load-Time Snapshot."""  # => this concept

import dataclasses  # => the domain object and its snapshot representation
from typing import Any  # => a snapshot dict holds mixed-type field values


@dataclasses.dataclass  # => a mutable, ALREADY-loaded domain object -- dirty checks compare against this
class User:  # => the type this unit of work tracks for changes
    id: int  # => primary key -- already assigned, this object has a real row
    name: str  # => an ordinary, mutable column


class UnitOfWork:  # => co-17: snapshots at load time, compares later to detect dirt
    def __init__(self) -> None:  # => starts with nothing tracked
        self._snapshots: dict[int, dict[str, Any]] = {}  # => keyed by id(obj), one snapshot PER tracked object
        self._identity: dict[int, User] = {}  # => keyed by id(obj) too -- keeps the tracked objects reachable

    def track_clean(self, user: User) -> None:  # => co-17: registers an ALREADY-persisted object as "clean"
        self._identity[id(user)] = user  # => keeps a reference so dirty_objects() can iterate it later
        self._snapshots[id(user)] = dataclasses.asdict(user)  # => the state to compare future mutations against

    def dirty_objects(self) -> list[User]:  # => co-17: compares EVERY tracked object's live state to its snapshot
        dirty: list[User] = []  # => co-17: accumulates objects whose state has diverged
        for key, user in self._identity.items():  # => walks every tracked (clean-registered) object
            if dataclasses.asdict(user) != self._snapshots[key]:  # => live state vs load-time snapshot
                dirty.append(user)  # => diverged -- this object needs an UPDATE on the next flush
        return dirty  # => every object whose fields changed since track_clean() was called


uow = UnitOfWork()  # => co-17: one unit of work, tracking clean objects for dirty detection
alice = User(id=1, name="Alice")  # => simulates an already-loaded, persisted object
uow.track_clean(alice)  # => co-17: snapshot taken NOW -- {"id": 1, "name": "Alice"}
assert uow.dirty_objects() == []  # => nothing has changed yet -- the dirty set is empty

alice.name = "Alicia"  # => mutates the LIVE object -- the snapshot stays untouched
dirty = uow.dirty_objects()  # => co-17: compares live state to the frozen snapshot
assert dirty == [alice]  # => exactly one object diverged, and it's `alice`
print(len(dirty))  # => Output: 1
