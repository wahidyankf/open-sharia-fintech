"""Kata 4 (after): the LSM read path checks SSTables NEWEST-to-oldest, so the newest write wins."""

from __future__ import annotations


def lsm_read(sstables_oldest_to_newest: list[dict[str, str]], key: str) -> str | None:
    for table in reversed(
        sstables_oldest_to_newest
    ):  # => co-12: newest-to-oldest -- the first match wins
        if key in table:
            return table[key]
    return None


sstables = [{"y": "original-value"}, {"y": "updated-value"}]
print(lsm_read(sstables, "y"))
print(lsm_read(sstables, "y") == "updated-value")
