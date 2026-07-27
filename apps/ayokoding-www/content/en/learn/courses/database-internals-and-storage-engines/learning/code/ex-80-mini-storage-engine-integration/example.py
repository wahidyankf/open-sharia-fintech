"""Example 80: A Mini Storage Engine -- Pages + B-Tree Index + WAL + Snapshot Read."""
# The four load-bearing pieces (co-01, co-07, co-16, co-21) wired together into one tiny engine.

from dataclasses import dataclass, field  # => plain, typed records for each moving part


@dataclass  # => a plain, typed record -- no custom __init__ needed
class WalRecord:  # => co-16: an append-only, durable-before-the-page log entry
    key: str  # => which key this record wrote
    value: str  # => the value written
    committed: bool = False  # => flips True once the writing transaction commits


@dataclass  # => fields carry their own default_factory
class MiniEngine:  # => co-01/co-07/co-16/co-21, wired into one small engine
    wal: list[WalRecord] = field(
        default_factory=list[WalRecord]
    )  # => the durable, append-only log
    index: dict[str, int] = field(
        default_factory=dict[str, int]
    )  # => co-07: key -> page id (the "B-tree")
    pages: dict[int, str] = field(
        default_factory=dict[int, str]
    )  # => co-01: page id -> the row's bytes
    next_page_id: int = 0  # => a simple monotonic page allocator

    def write(
        self, key: str, value: str
    ) -> None:  # => co-16: log FIRST, then materialize on commit
        self.wal.append(
            WalRecord(key=key, value=value, committed=False)
        )  # => durable before the page exists

    def commit(
        self, key: str
    ) -> None:  # => marks the record committed AND materializes it into a page
        for record in reversed(
            self.wal
        ):  # => find this key's most recent (still-uncommitted) write
            if (
                record.key == key and not record.committed
            ):  # => the record this commit() call applies to
                record.committed = True  # => now durable AND visible
                page_id = self.next_page_id  # => allocate a fresh page for this row
                self.next_page_id += 1  # => the next write gets the next page id
                self.pages[page_id] = (
                    record.value
                )  # => co-01: the row's actual bytes live in the page
                self.index[key] = (
                    page_id  # => co-07: the index now routes lookups to this page
                )
                return  # => only the single most recent matching record is committed

    def crash_and_recover(
        self,
    ) -> None:  # => co-16: rebuild index+pages from the WAL, exactly like ex-67
        self.index.clear()  # => volatile structures are lost -- only the WAL survives a crash
        self.pages.clear()  # => same for the page store -- rebuilt entirely from the durable log
        self.next_page_id = (
            0  # => page ids are reassigned during the replay, in commit order
        )
        for record in self.wal:  # => redo, but ONLY for committed records (this engine skips undo for brevity)
            if (
                record.committed
            ):  # => co-19-style filter -- an uncommitted record has nothing to redo
                page_id = (
                    self.next_page_id
                )  # => allocate a page for this recovered record
                self.next_page_id += (
                    1  # => advance the allocator for the next recovered record
                )
                self.pages[page_id] = (
                    record.value
                )  # => rebuild the page exactly as commit() first created it
                self.index[record.key] = (
                    page_id  # => and rebuild the index entry pointing at it
                )

    def snapshot_read(
        self, key: str
    ) -> str | None:  # => co-21: reads through the index -> page path
        page_id = self.index.get(
            key
        )  # => co-07: the index answers WHERE this key's row lives
        if (
            page_id is None
        ):  # => never committed (or not yet recovered) -- nothing to read
            return None  # => nothing to read -- this key was never committed
        return self.pages[page_id]  # => co-01: the page holds the actual row bytes


engine = MiniEngine()  # => a fresh mini engine, nothing written yet
engine.write(
    "user:1", "alice"
)  # => co-16: durable in the WAL immediately, but not yet committed
engine.commit("user:1")  # => now committed -- materialized into a page and indexed

before_crash = engine.snapshot_read(
    "user:1"
)  # => a read while everything is still in memory
engine.crash_and_recover()  # => simulate a crash: wipe volatile state, rebuild purely from the WAL
after_crash = engine.snapshot_read(
    "user:1"
)  # => the SAME read, now served from recovered state
print(before_crash)  # => Output: alice
print(after_crash)  # => Output: alice

assert (
    before_crash == "alice"
)  # => the write was correctly readable before any crash happened
assert (
    after_crash == "alice"
)  # => co-16: the committed write survived the crash, via WAL replay
assert (
    before_crash == after_crash
)  # => co-21: a snapshot read stays consistent across the whole scenario
print("ex-80 OK")  # => Output: ex-80 OK
