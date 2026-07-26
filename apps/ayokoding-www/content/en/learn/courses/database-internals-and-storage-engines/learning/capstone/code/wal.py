"""Capstone Step 3: write-ahead logging with a simulated crash and restart.

Time/space complexity (n = log records since the last checkpoint-equivalent):

- ``append``: O(1) -- appends one record to the log.
- ``commit``: O(n) -- scans the WHOLE log to find this transaction's
  records, not just the records it appended; this capstone never
  truncates/checkpoints the log, so the scan is a genuine O(n), not O(1).
  A production WAL indexes open transactions instead of rescanning; this
  capstone keeps the simpler scan on purpose, to avoid touching tests and
  documented output for no learner benefit.
- ``crash_and_recover``: O(n) -- a single forward pass replays every logged
  write into a fresh ``BufferPool`` + ``BTreeIndex``, exactly like Example 67's
  end-to-end recovery, generalized to write through pages.py's real page
  format instead of a bare dict.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from index import BTreeIndex
from pages import BufferPool, insert_record, read_record


@dataclass
class WalRecord:  # => co-16/co-17: one durable, append-only log entry
    lsn: int  # => co-17: strictly increasing -- this record's position in the log
    txn_id: int  # => which transaction produced this write
    key: int  # => the logical key this write affects
    value: bytes  # => the row bytes this write sets
    committed: bool = False  # => flips True once this record's transaction commits


@dataclass
class WriteAheadLog:  # => co-16: the log is the source of truth a crash can always recover from
    pool: BufferPool = field(
        default_factory=lambda: BufferPool(capacity=8)
    )  # => co-04: pages live here
    index: BTreeIndex = field(
        default_factory=BTreeIndex
    )  # => co-07: key -> page_id routing
    log: list[WalRecord] = field(
        default_factory=list[WalRecord]
    )  # => co-16: the durable, append-only log
    next_page_id: int = 0  # => a simple monotonic page allocator

    def append(
        self, txn_id: int, key: int, value: bytes
    ) -> None:  # => co-16: durable BEFORE materializing
        lsn = len(
            self.log
        )  # => co-17: LSNs are just this record's position -- strictly increasing
        self.log.append(
            WalRecord(lsn=lsn, txn_id=txn_id, key=key, value=value)
        )  # => durable, uncommitted

    def commit(
        self, txn_id: int
    ) -> None:  # => marks every of this txn's records committed + materializes
        for record in self.log:  # => co-19: O(n) -- scans the WHOLE log for this txn's records (never truncated here); a real WAL indexes open txns instead of rescanning
            if (
                record.txn_id == txn_id and not record.committed
            ):  # => an un-committed record of this txn
                record.committed = (
                    True  # => now durable AND eligible for redo on any future recovery
                )
                self._materialize(
                    record
                )  # => write it into a real page right now, not just the log

    def _materialize(
        self, record: WalRecord
    ) -> None:  # => co-01/co-07: turn a committed write into a page
        page = self.pool.get_page(
            self.next_page_id
        )  # => a fresh page for this row (kept simple: 1 row/page)
        insert_record(
            page, record.value
        )  # => co-02/co-03: the row's bytes, slotted onto the page
        self.pool.unpin(
            self.next_page_id, mark_dirty=True
        )  # => release it, marking it dirty
        self.index.insert(
            record.key, self.next_page_id
        )  # => co-07: the index now routes to this page
        self.next_page_id += 1  # => the next materialized write gets the next page id

    def crash_and_recover(
        self,
    ) -> None:  # => co-18: a fresh pool+index, rebuilt PURELY from the durable log
        self.pool = BufferPool(
            capacity=8
        )  # => volatile state is lost -- only self.log survives a crash
        self.index = (
            BTreeIndex()
        )  # => same for the index -- rebuilt entirely from scratch
        self.next_page_id = (
            0  # => page ids are reassigned during replay, in commit order
        )
        for record in self.log:  # => co-18: analysis+redo folded into one pass -- this course's simplified WAL
            if (
                record.committed
            ):  # => co-19: only committed records are redone -- uncommitted ones vanish
                self._materialize(
                    record
                )  # => rebuilds the page and index entry exactly as commit() first did

    def read(
        self, key: int
    ) -> bytes | None:  # => a read through the SAME index -> page path as pages.py
        page_id = self.index.lookup(
            key
        )  # => co-07: the index answers WHERE this key's row lives
        if (
            page_id is None
        ):  # => never committed (or not yet re-materialized after a crash)
            return None
        page = self.pool.get_page(
            page_id
        )  # => co-06: served from the pool if resident, else loaded
        self.pool.unpin(page_id)  # => this read does not need the page held any longer
        return read_record(
            page, slot=0
        )  # => co-03: slot 0, since this WAL keeps exactly one row per page


def demo() -> (
    None
):  # => a genuine, runnable walkthrough of commit-survives / abort-vanishes across a crash
    wal = WriteAheadLog()  # => a fresh WAL, nothing written yet
    wal.append(
        txn_id=1, key=100, value=b"committed-row"
    )  # => durable in the log immediately
    wal.commit(txn_id=1)  # => txn 1 commits -- materialized into a page and indexed
    wal.append(
        txn_id=2, key=200, value=b"uncommitted-row"
    )  # => durable in the log, but NEVER committed

    before_crash = wal.read(100)  # => a read while everything is still live in memory
    wal.crash_and_recover()  # => simulate a crash: wipe volatile state, rebuild purely from the log
    after_crash_committed = wal.read(
        100
    )  # => the committed write, re-read after recovery
    after_crash_uncommitted = wal.read(
        200
    )  # => the never-committed write, re-read after recovery
    print(before_crash)  # => the committed row, readable before any crash
    print(after_crash_committed)  # => co-16: the committed row SURVIVED the crash
    print(
        after_crash_uncommitted
    )  # => co-19: the uncommitted row is GONE -- never redone


if (
    __name__ == "__main__"
):  # => only runs the demo when this file is executed directly, not on import
    demo()
