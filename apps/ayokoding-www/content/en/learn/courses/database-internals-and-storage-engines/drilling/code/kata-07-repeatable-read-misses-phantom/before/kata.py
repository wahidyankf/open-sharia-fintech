"""Kata 7 (before): a "repeatable read" that re-queries live state on every call is NOT actually snapshot-stable."""

from __future__ import annotations


class NaiveRepeatableRead:
    def __init__(self, table: list[dict[str, str]]) -> None:
        self.table = table  # BUG: holds a reference to the LIVE table, never actually takes a snapshot

    def count_rows(self, status: str) -> int:
        return sum(
            1 for row in self.table if row["status"] == status
        )  # re-reads live state every call


table: list[dict[str, str]] = [{"status": "open"}]
txn = NaiveRepeatableRead(table)
first_count = txn.count_rows("open")
table.append(
    {"status": "open"}
)  # a concurrent transaction inserts a new matching row (a phantom)
second_count = txn.count_rows("open")
print(first_count, second_count)
print(
    first_count == second_count
)  # expected True under repeatable read -- the SAME transaction's two reads must agree
