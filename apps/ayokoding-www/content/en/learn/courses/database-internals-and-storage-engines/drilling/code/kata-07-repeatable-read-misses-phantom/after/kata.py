"""Kata 7 (after): a real repeatable-read transaction takes an explicit COPY of the table at its start."""

from __future__ import annotations


class SnapshotRepeatableRead:
    def __init__(self, table: list[dict[str, str]]) -> None:
        self.snapshot = list(
            table
        )  # => co-24: an explicit copy taken NOW -- later inserts cannot affect it

    def count_rows(self, status: str) -> int:
        return sum(1 for row in self.snapshot if row["status"] == status)


table: list[dict[str, str]] = [{"status": "open"}]
txn = SnapshotRepeatableRead(table)
first_count = txn.count_rows("open")
table.append(
    {"status": "open"}
)  # the concurrent insert still happens -- but txn's snapshot never sees it
second_count = txn.count_rows("open")
print(first_count, second_count)
print(first_count == second_count)
