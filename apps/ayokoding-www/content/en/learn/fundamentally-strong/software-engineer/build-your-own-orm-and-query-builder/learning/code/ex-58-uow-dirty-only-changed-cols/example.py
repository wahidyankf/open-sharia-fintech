"""Example 58: An UPDATE Statement Contains Only the Columns That Actually Changed."""  # => this concept

import dataclasses  # => the domain object and its snapshot representation
from typing import Any  # => a snapshot dict AND a changed-columns dict hold mixed-type values


@dataclasses.dataclass  # => a mutable, already-loaded domain object
class User:  # => the type this example diffs against its snapshot
    id: int  # => primary key -- excluded from the changed-columns diff below
    name: str  # => a mutable column, may or may not have changed
    email: str  # => a second mutable column, may or may not have changed


def changed_columns(user: User, snapshot: dict[str, Any]) -> dict[str, Any]:  # => co-17: the minimal diff
    live = dataclasses.asdict(user)  # => the object's CURRENT field values
    return {  # => co-17: only fields that actually diverged from the snapshot
        field: value  # => the NEW value, ready to bind into an UPDATE's SET clause
        for field, value in live.items()  # => walks every field the dataclass declares
        if field != "id" and value != snapshot[field]  # => excludes the pk, keeps only genuinely-changed fields
    }  # => an empty dict here would mean "nothing to update"


snapshot = {"id": 1, "name": "Alice", "email": "alice@example.com"}  # => load-time snapshot (co-17)
user = User(id=1, name="Alice", email="alice@example.com")  # => starts identical to its own snapshot
user.email = "alice@newmail.com"  # => mutates ONLY the email column, name stays untouched
diff = changed_columns(user, snapshot)  # => co-17: computes exactly what changed
assert diff == {"email": "alice@newmail.com"}  # => "name" is absent -- it never changed, so it's excluded
assert "name" not in diff  # => confirms the unchanged column was NOT included in the diff
print(diff)  # => Output: {'email': 'alice@newmail.com'}
