"""Kata 6 (after): delete() sets xmax on the live version instead of physically removing it."""

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
        self.versions[
            -1
        ].xmax = (
            txn_id  # => co-21: tags the version deleted -- history is never destroyed
        )

    def snapshot_read(self, snapshot_at: int) -> str | None:
        for version in reversed(self.versions):
            if version.xmin < snapshot_at and (
                version.xmax is None or version.xmax >= snapshot_at
            ):
                return version.value
        return None


table = Table()
table.write("row-exists", txn_id=1)
old_snapshot = 2
table.delete(txn_id=2)
print(table.snapshot_read(old_snapshot))
