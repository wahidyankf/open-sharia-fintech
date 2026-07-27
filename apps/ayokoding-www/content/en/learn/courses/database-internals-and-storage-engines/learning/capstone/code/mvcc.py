"""Capstone Step 4: an MVCC snapshot read, layered on wal.py -- the full pipeline, end to end.

Time/space complexity (n = versions of one key, m = total WAL log records):

- ``write``: O(1) -- appends one version to this key's chain (plus wal.py's
  O(1) ``append``).
- ``commit``: O(m) -- delegates to ``wal.py``'s ``commit``, which scans the
  ENTIRE WAL log, not just this key's n versions; see wal.py's own docstring
  for why that scan is O(m), not O(1).
- ``snapshot_read``: O(n) worst case -- walks one key's version chain newest to
  oldest, exactly like Example 37's visibility rule, generalized here to sit
  on top of ``wal.py``'s durable, crash-recoverable storage instead of a bare
  module-level dict.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from wal import WriteAheadLog


@dataclass
class RowVersion:  # => co-21: one version of one row -- MVCC never edits a version in place
    value: bytes  # => this version's actual data
    xmin: int  # => co-21: the transaction id that CREATED this version
    xmax: int | None = (
        None  # => co-21: the transaction id that deleted it, or None if still live
    )


@dataclass
class MVCCEngine:  # => co-01, co-07, co-16, co-21 wired together into one small, complete engine
    wal: WriteAheadLog = field(
        default_factory=WriteAheadLog
    )  # => co-16: durability underneath everything
    versions: dict[int, list[RowVersion]] = field(
        default_factory=dict[int, list[RowVersion]]
    )  # => co-21
    commit_order: dict[int, int] = field(
        default_factory=dict[int, int]
    )  # => co-22: txn_id -> commit position

    def write(
        self, key: int, value: bytes, txn_id: int
    ) -> None:  # => co-16 + co-21: durable, then versioned
        self.wal.append(
            txn_id, key, value
        )  # => co-16: durable in the log before anything else happens
        chain = self.versions.setdefault(
            key, []
        )  # => this key's version chain so far, possibly empty
        chain.append(
            RowVersion(value=value, xmin=txn_id)
        )  # => co-21: append a NEW version, never overwrite

    def commit(
        self, txn_id: int
    ) -> None:  # => co-16 + co-19: durability AND visibility, together
        self.wal.commit(
            txn_id
        )  # => co-19: materializes this txn's writes into real pages via the WAL -- O(m) since wal.py's commit scans the whole log (see wal.py's docstring)
        self.commit_order[txn_id] = len(
            self.commit_order
        )  # => co-22: this txn's position in commit order

    def snapshot_read(
        self, key: int, snapshot_at: int
    ) -> bytes | None:  # => co-22: Example 37's rule, reused
        chain = self.versions.get(
            key, []
        )  # => every version of this key ever written, in creation order
        for version in reversed(
            chain
        ):  # => newest-to-oldest -- the first VISIBLE match wins
            creator_pos = self.commit_order.get(
                version.xmin
            )  # => when (if ever) this version's writer committed
            if (
                creator_pos is not None and creator_pos < snapshot_at
            ):  # => created before this snapshot
                return (
                    version.value
                )  # => co-22: visible -- return it without ever taking a lock
        return None  # => no version of this key was visible to the snapshot at all

    def crash_and_recover(
        self,
    ) -> None:  # => co-16/co-18: durability survives; in-memory versions do not
        self.wal.crash_and_recover()  # => rebuilds pages+index purely from the durable log, like Example 67
        # => versions/commit_order are volatile MVCC bookkeeping -- a real engine rebuilds them from the
        # WAL too; this course's simplified model instead reads committed state straight from wal.read()
        # after a crash, which is exactly what read_after_recovery() below does.

    def read_after_recovery(
        self, key: int
    ) -> bytes | None:  # => co-16: the durable, post-crash source of truth
        return self.wal.read(
            key
        )  # => co-07: routed through the index, exactly like wal.py's own reads


def demo() -> (
    None
):  # => a genuine, runnable walkthrough: a snapshot stays stable across a concurrent write
    engine = MVCCEngine()  # => a fresh engine, nothing written yet
    engine.write(
        key=1, value=b"original", txn_id=1
    )  # => co-21: the first version of key 1
    engine.commit(
        txn_id=1
    )  # => co-16/co-22: durable AND visible to any snapshot taken after this point

    reader_snapshot_at = len(
        engine.commit_order
    )  # => co-22: the reader's snapshot, taken BEFORE the writer
    reader_result = engine.snapshot_read(
        key=1, snapshot_at=reader_snapshot_at
    )  # => acquires NO lock at all

    engine.write(
        key=1, value=b"concurrently-updated", txn_id=2
    )  # => co-21: a NEW version, not an overwrite
    engine.commit(
        txn_id=2
    )  # => the concurrent writer proceeds and commits WITHOUT waiting on the reader

    print(
        reader_result
    )  # => the reader's snapshot value -- unaffected by the concurrent commit
    print(
        engine.snapshot_read(key=1, snapshot_at=len(engine.commit_order))
    )  # => a NEW snapshot sees the update

    engine.crash_and_recover()  # => co-18: simulate a crash right after the concurrent commit
    print(
        engine.read_after_recovery(1)
    )  # => co-16/co-19: the LAST committed write survived the crash


if (
    __name__ == "__main__"
):  # => only runs the demo when this file is executed directly, not on import
    demo()
