"""Example 37: Snapshot Visibility Rule."""
# Snapshot visibility (co-22) is decided entirely from xmin/xmax and commit order.

from dataclasses import dataclass  # => a plain, typed record for one MVCC row version


@dataclass  # => a plain, typed record -- no custom __init__ needed
class RowVersion:  # => one version of one row, tagged with its creating/deleting transactions
    value: str  # => this version's actual data
    xmin: int  # => transaction id that created this version
    xmax: int | None = None  # => transaction id that deleted it, or None if still live


commit_order: dict[
    int, int
] = {}  # => txn_id -> the position it committed at (lower = earlier)


def commit(
    txn_id: int,
) -> None:  # => records WHEN (in commit order) a transaction committed
    commit_order[txn_id] = len(commit_order)  # => the Nth commit gets position N


def is_visible(
    version: RowVersion, snapshot_at: int
) -> bool:  # => snapshot_at is a commit-order position
    creator_pos = commit_order.get(
        version.xmin
    )  # => None if the creator hasn't committed at all yet
    if (
        creator_pos is None or creator_pos >= snapshot_at
    ):  # => created too late (or not committed) -- hide it
        return False  # => this snapshot cannot possibly see a version created after (or not before) it
    if (
        version.xmax is not None
    ):  # => this version WAS superseded by some later transaction
        deleter_pos = commit_order.get(
            version.xmax
        )  # => None means the deleter hasn't committed yet either
        if (
            deleter_pos is not None and deleter_pos < snapshot_at
        ):  # => the delete was ALREADY visible too
            return False  # => superseded before this snapshot was taken -- hidden
    return True  # => created before the snapshot, and not (visibly) deleted before it either


commit(txn_id=1)  # => commit position 0
version = RowVersion(value="v1", xmin=1)  # => a version created by txn 1
snapshot_before = 0  # => taken BEFORE txn 1's commit is visible (at position 0, nothing has committed yet)
snapshot_after = 1  # => taken AFTER txn 1's commit
print(is_visible(version, snapshot_before))  # => Output: False
print(is_visible(version, snapshot_after))  # => Output: True

assert (
    is_visible(version, snapshot_before) is False
)  # => a snapshot before the commit cannot see it
assert (
    is_visible(version, snapshot_after) is True
)  # => a snapshot after the commit CAN see it
print("ex-37 OK")  # => Output: ex-37 OK
