"""Example 36: Row Versions Tagged with xmin/xmax."""
# xmin/xmax (co-21) are the two columns MVCC tags every row version with.

from dataclasses import dataclass  # => a plain, typed record for one MVCC row version


@dataclass  # => a plain, typed record -- no custom __init__ needed
class RowVersion:  # => one version of one row -- MVCC never edits a version in place
    value: str  # => this version's actual data
    xmin: int  # => the transaction id that CREATED this version
    xmax: int | None = (
        None  # => the transaction id that DELETED (superseded) it, or None if still live
    )


def update(
    versions: list[RowVersion], new_value: str, txn_id: int
) -> RowVersion:  # => co-21: append, never edit
    current = versions[-1]  # => the most recent (currently live) version
    current.xmax = txn_id  # => the OLD version is now superseded, tagged with the updating txn's id
    new_version = RowVersion(
        value=new_value, xmin=txn_id
    )  # => a BRAND NEW version, not an edit in place
    versions.append(
        new_version
    )  # => the row's version chain grows -- nothing was overwritten
    return new_version  # => hand back the freshly created version


versions: list[RowVersion] = [
    RowVersion(value="original", xmin=1)
]  # => created by txn 1
update(versions, new_value="updated", txn_id=2)  # => txn 2 updates the row
print(versions[0])  # => Output: RowVersion(value='original', xmin=1, xmax=2)
print(versions[1])  # => Output: RowVersion(value='updated', xmin=2, xmax=None)

assert versions[0].xmax == 2  # => the OLD version is tagged as superseded by txn 2
assert versions[1].xmin == 2  # => the NEW version is tagged as created by txn 2
assert (
    versions[1].xmax is None
)  # => the new version is still live -- nothing has superseded IT yet
print("ex-36 OK")  # => Output: ex-36 OK
