"""Example 39: Readers Don't Block Writers."""
# Snapshot isolation (co-22) means readers need no lock at all.

from dataclasses import dataclass  # => a plain, typed record for one MVCC row version


@dataclass  # => a plain, typed record -- no custom __init__ needed
class RowVersion:  # => one version of one row
    value: str  # => this version's actual data
    xmin: int  # => transaction id that created this version
    xmax: int | None = None  # => transaction id that deleted it, or None if still live


commit_order: dict[int, int] = {
    1: 0
}  # => txn 1 already committed the row's original version
versions: list[RowVersion] = [
    RowVersion(value="original", xmin=1)
]  # => one live version so far


def snapshot_read(
    snapshot_at: int,
) -> str | None:  # => acquires NO lock -- pure read of existing data
    for version in reversed(versions):  # => newest-to-oldest, first visible match wins
        creator_pos = commit_order.get(
            version.xmin
        )  # => when (if ever) this version's creator committed
        if (
            creator_pos is not None and creator_pos < snapshot_at
        ):  # => created before this snapshot
            return version.value  # => the first (newest) visible version found
    return None  # => no version of this row was visible to the snapshot at all


def writer_update(
    new_value: str, txn_id: int
) -> None:  # => a concurrent writer, appends a new version
    versions[-1].xmax = txn_id  # => tag the current version as superseded
    versions.append(
        RowVersion(value=new_value, xmin=txn_id)
    )  # => append the new version -- no lock taken
    commit_order[txn_id] = len(
        commit_order
    )  # => commits immediately for this example's purposes


reader_snapshot_at = len(
    commit_order
)  # => the reader's snapshot position, taken BEFORE the writer runs
reader_result = snapshot_read(
    reader_snapshot_at
)  # => the reader's read -- acquired NO lock to do this
writer_update(
    "written-concurrently", txn_id=2
)  # => the writer proceeds WITHOUT waiting on the reader
print(reader_result)  # => Output: original
print(len(versions))  # => Output: 2

assert (
    reader_result == "original"
)  # => the reader's result reflects its OWN snapshot, unaffected
assert (
    len(versions) == 2
)  # => the writer's append succeeded -- it was never blocked by the reader
print("ex-39 OK")  # => Output: ex-39 OK
