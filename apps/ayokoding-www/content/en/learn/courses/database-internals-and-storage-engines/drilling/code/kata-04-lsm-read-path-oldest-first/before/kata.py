"""Kata 4 (before): the LSM read path checks SSTables OLDEST-to-newest, returning a stale value."""

from __future__ import annotations


def lsm_read(sstables_oldest_to_newest: list[dict[str, str]], key: str) -> str | None:
    for table in (
        sstables_oldest_to_newest
    ):  # BUG: scans oldest-first, so an OLDER value wins over a newer one
        if key in table:
            return table[key]
    return None


# sstables[0] is the OLDEST flush, sstables[-1] is the NEWEST -- "y" was updated in the newest table
sstables = [{"y": "original-value"}, {"y": "updated-value"}]
print(lsm_read(sstables, "y"))
print(
    lsm_read(sstables, "y") == "updated-value"
)  # expected True -- the NEWEST write must win
