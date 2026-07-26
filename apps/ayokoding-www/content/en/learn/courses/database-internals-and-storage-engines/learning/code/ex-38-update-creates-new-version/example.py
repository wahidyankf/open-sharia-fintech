"""Example 38: An Update Creates a New Version."""
# MVCC never mutates a row version in place (co-21) -- every update appends a new one.

from dataclasses import dataclass  # => a plain, typed record for one MVCC row version


@dataclass  # => a plain, typed record -- no custom __init__ needed
class RowVersion:  # => one version of one row
    value: str  # => this version's actual data
    xmin: int  # => the transaction id that created this version
    xmax: int | None = (
        None  # => the transaction id that deleted it, or None if still live
    )


def update(
    versions: list[RowVersion], new_value: str, txn_id: int
) -> RowVersion:  # => append, never mutate
    current = versions[-1]  # => the current, live version -- about to be superseded
    current.xmax = txn_id  # => tag the OLD version as superseded, but do NOT change its value field
    new_version = RowVersion(value=new_value, xmin=txn_id)  # => a genuinely NEW object
    versions.append(new_version)  # => appended, not swapped in place
    return new_version  # => hand back the freshly created version


versions: list[RowVersion] = [RowVersion(value="v1", xmin=1)]  # => the original version
original = versions[0]  # => keep a reference to compare against later
update(versions, new_value="v2", txn_id=2)  # => first update
update(versions, new_value="v3", txn_id=3)  # => second update
print(len(versions))  # => Output: 3
print([v.value for v in versions])  # => Output: ['v1', 'v2', 'v3']

assert (
    len(versions) == 3
)  # => two updates produced TWO new versions, plus the original -- three total
assert (
    original.value == "v1"
)  # => the ORIGINAL object's value was never mutated in place
assert (
    versions[0] is original
)  # => it is literally the same object, still sitting in the chain
assert (
    len({id(v) for v in versions}) == 3
)  # => three genuinely distinct objects, not aliases of each other
print("ex-38 OK")  # => Output: ex-38 OK
