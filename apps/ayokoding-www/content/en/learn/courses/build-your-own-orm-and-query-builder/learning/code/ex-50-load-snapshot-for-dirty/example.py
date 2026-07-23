"""Example 50: Snapshot an Object's Attributes at Load Time, for Later Dirty Checks."""  # => this concept

import dataclasses  # => the loaded domain object AND its snapshot representation
from typing import Any  # => a snapshot dict holds mixed-type field values


@dataclasses.dataclass  # => a loaded, mutable domain object -- dirty checks compare against THIS
class User:  # => the type this example snapshots
    id: int  # => primary key
    name: str  # => an ordinary, mutable column


class Session:  # => co-17: takes a snapshot the MOMENT an object is loaded
    def __init__(self) -> None:  # => starts with no snapshots recorded
        self._snapshots: dict[int, dict[str, Any]] = {}  # => keyed by id(obj) -- one snapshot PER object

    def load(self, user: User) -> User:  # => simulates "just finished mapping this row into `user`"
        self._snapshots[id(user)] = dataclasses.asdict(user)  # => co-17: snapshot taken AT LOAD TIME
        return user  # => the caller gets the same object back, now tracked

    def snapshot_of(self, user: User) -> dict[str, Any]:  # => reads a previously-taken snapshot back
        return self._snapshots[id(user)]  # => keyed by THIS object's identity, not its pk value


session = Session()  # => one session, tracking snapshots for every object it loads
user = User(id=1, name="Alice")  # => simulates a freshly-mapped row (co-10 already ran)
session.load(user)  # => co-17: records {"id": 1, "name": "Alice"} as the snapshot for THIS object
snapshot = session.snapshot_of(user)  # => reads the snapshot back out
assert snapshot == {"id": 1, "name": "Alice"}  # => matches the object's state AT LOAD TIME, exactly

user.name = "Alicia"  # => mutates the object AFTER the snapshot was taken
assert user.name == "Alicia"  # => the LIVE object reflects the mutation
assert session.snapshot_of(user)["name"] == "Alice"  # => the SNAPSHOT does not -- it's frozen at load time
print(session.snapshot_of(user))  # => Output: {'id': 1, 'name': 'Alice'}
