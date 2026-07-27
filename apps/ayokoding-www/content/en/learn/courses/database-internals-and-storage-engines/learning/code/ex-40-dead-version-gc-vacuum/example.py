"""Example 40: Vacuum Reclaims Dead Versions."""

from dataclasses import dataclass  # => a plain, typed record for one MVCC row version


@dataclass  # => a plain, typed record -- no custom __init__ needed
class RowVersion:  # => one version of one row
    value: str  # => this version's actual data
    xmin: int  # => the transaction id that created this version
    xmax: int | None = (
        None  # => the transaction id that deleted it, or None if still live
    )


commit_order: dict[int, int] = {
    1: 0,
    2: 1,
    3: 2,
}  # => three transactions, each already committed
versions: list[RowVersion] = [  # => three versions of the same logical row
    RowVersion(
        value="v1", xmin=1, xmax=2
    ),  # => superseded by txn 2 -- may be dead, depending on readers
    RowVersion(
        value="v2", xmin=2, xmax=3
    ),  # => superseded by txn 3 -- may be dead, depending on readers
    RowVersion(
        value="v3", xmin=3
    ),  # => the current, live version -- xmax is None, never dead
]  # => end of the version-chain fixture


def vacuum(
    versions: list[RowVersion], oldest_active_snapshot: int
) -> list[RowVersion]:  # => co-23: reclaim
    live: list[RowVersion] = []  # => survivors after vacuuming
    for version in versions:  # => decide each version's fate independently
        if version.xmax is None:  # => never superseded -- always kept
            live.append(version)  # => keep it -- still the current row
            continue  # => move on to the next version, nothing more to check
        deleter_pos = commit_order.get(
            version.xmax
        )  # => when (if ever) the deleter committed
        if (
            deleter_pos is None or deleter_pos >= oldest_active_snapshot
        ):  # => some active reader might need it
            live.append(version)  # => not yet safe to reclaim
        # => else: deleter_pos < oldest_active_snapshot -- NO active reader can possibly still see it
    return live  # => the pruned, still-valid version set


before_count = len(versions)  # => 3 versions before vacuuming
after = vacuum(
    versions, oldest_active_snapshot=2
)  # => the oldest active snapshot is at position 2
print(len(after))  # => Output: 2

assert before_count == 3  # => confirms the starting point before reclaiming anything
assert (
    len(after) == 2
)  # => v1 was reclaimed -- its delete (position 1) predates the oldest active snapshot
assert [v.value for v in after] == [
    "v2",
    "v3",
]  # => the two still-relevant versions survive
print("ex-40 OK")  # => Output: ex-40 OK
