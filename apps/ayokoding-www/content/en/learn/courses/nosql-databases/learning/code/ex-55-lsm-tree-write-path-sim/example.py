"""Example 55: LSM-Tree Write Path, Simulated."""  # => co-25: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-25: typed memtable/SSTable stand-ins for the real write path


@dataclass  # => intentionally MUTABLE -- a memtable genuinely accumulates writes before it flushes
class Memtable:  # => co-25: an in-memory, sorted write buffer -- every write lands HERE first, never on disk directly
    entries: dict[str, str] = field(default_factory=dict)  # => co-25: key -> value, held in memory only

    def write(self, key: str, value: str) -> None:  # => co-25: the ENTIRE cost of a write, from the caller's perspective
        self.entries[key] = value  # => co-25: an in-memory dict write -- no disk I/O on the write's own critical path


@dataclass(frozen=True)  # => frozen -- an SSTable, once flushed, is IMMUTABLE -- this is the whole point of the design
class SSTable:  # => co-25: Sorted String Table -- an immutable, on-disk, sorted snapshot of a memtable
    entries: dict[str, str]  # => a frozen COPY of whatever the memtable held at flush time


class LsmStore:  # => co-25: models the real memtable -> flush -> SSTable -> compaction write path
    def __init__(self) -> None:  # => builds an empty store with no SSTables yet
        self.memtable = Memtable()  # => co-25: the ONE active, mutable, in-memory buffer
        self.sstables: list[SSTable] = []  # => co-25: immutable, on-disk snapshots, oldest first

    def write(self, key: str, value: str) -> None:  # => co-25: every write goes through the memtable, never directly to an SSTable
        self.memtable.write(key, value)  # => co-25: fast, in-memory -- this is WHY LSM trees favor write throughput

    def flush(self) -> None:  # => co-25: converts the CURRENT memtable into a new, immutable SSTable
        self.sstables.append(SSTable(dict(self.memtable.entries)))  # => co-25: a frozen snapshot -- the memtable's writes are now durable, on disk, immutable
        self.memtable = Memtable()  # => co-25: a FRESH, empty memtable replaces the flushed one -- ready for more writes


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    store = LsmStore()  # => co-25: a fresh LSM-tree-style store, no SSTables yet

    store.write("k1", "v1")  # => co-25: lands in the memtable ONLY -- not yet on disk as an SSTable
    store.write("k2", "v2")  # => co-25: also memtable-only so far
    assert len(store.sstables) == 0  # => co-25: NO SSTable exists yet -- both writes are still purely in-memory
    print(f"After 2 writes, before flush: {len(store.sstables)} SSTables, memtable has {len(store.memtable.entries)} entries")  # => Output: After 2 writes, before flush: 0 SSTables, memtable has 2 entries

    store.flush()  # => co-25: the memtable's contents become an IMMUTABLE SSTable -- writes are now durable on disk
    assert len(store.sstables) == 1  # => co-25: exactly ONE SSTable now exists, holding the 2 flushed writes
    assert len(store.memtable.entries) == 0  # => co-25: the ACTIVE memtable is fresh and empty again, ready for new writes
    print(f"After flush: {len(store.sstables)} SSTable(s), memtable has {len(store.memtable.entries)} entries")  # => Output: After flush: 1 SSTable(s), memtable has 0 entries
    print(f"SSTable 0 contents (immutable, on disk): {store.sstables[0].entries}")  # => Output: SSTable 0 contents (immutable, on disk): {'k1': 'v1', 'k2': 'v2'}
    # => co-25: writes land in an IMMUTABLE SSTable ONLY after a flush -- exactly the verification the spec requires


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
