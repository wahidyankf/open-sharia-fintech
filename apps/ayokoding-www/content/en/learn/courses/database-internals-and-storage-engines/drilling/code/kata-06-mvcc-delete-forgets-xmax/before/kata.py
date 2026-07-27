"""Kata 6 (before): delete() removes the version from the LIST instead of setting xmax, breaking history."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RowVersion:
    value: str
    xmin: int
    xmax: int | None = None


@dataclass
class Table:
    versions: list[RowVersion] = field(default_factory=list[RowVersion])

    def write(self, value: str, txn_id: int) -> None:
        self.versions.append(RowVersion(value=value, xmin=txn_id))

    def delete(self, txn_id: int) -> None:
        self.versions.pop()  # BUG: physically removes the version instead of tagging it with xmax

    def snapshot_read(self, snapshot_at: int) -> str | None:
        for version in reversed(self.versions):
            if version.xmin < snapshot_at and (
                version.xmax is None or version.xmax >= snapshot_at
            ):
                return version.value
        return None


table = Table()
table.write("row-exists", txn_id=1)
old_snapshot = 2  # a snapshot taken BEFORE the delete below
table.delete(txn_id=2)
print(
    table.snapshot_read(old_snapshot)
)  # expected "row-exists" -- a snapshot BEFORE the delete must still see it
