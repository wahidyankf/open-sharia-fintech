"""Example 57: LSM Read Amplification."""  # => co-25: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-25: typed memtable/SSTable stand-ins, reused from Example 55's model


@dataclass  # => intentionally MUTABLE -- the memtable accumulates writes before it flushes
class Memtable:  # => co-25: the same in-memory write buffer Example 55 modeled
    entries: dict[str, str] = field(default_factory=dict[str, str])  # => key -> value, held in memory only


@dataclass(frozen=True)  # => frozen -- an SSTable is immutable once flushed
class SSTable:  # => co-25: an immutable, on-disk, sorted snapshot
    entries: dict[str, str]  # => a frozen copy of whatever was flushed


class LsmStore:  # => co-25: extends Example 55's model with a READ path that must check MULTIPLE files
    def __init__(self) -> None:  # => builds an empty store with no SSTables yet
        self.memtable = Memtable()  # => the one active, mutable, in-memory buffer
        self.sstables: list[SSTable] = []  # => immutable, on-disk snapshots, NEWEST last (checked first on read)

    def write(self, key: str, value: str) -> None:  # => every write goes through the memtable first
        self.memtable.entries[key] = value  # => co-25: fast, in-memory

    def flush(self) -> None:  # => converts the current memtable into a new, immutable SSTable
        self.sstables.append(SSTable(dict(self.memtable.entries)))  # => a frozen snapshot
        self.memtable = Memtable()  # => a fresh, empty memtable replaces the flushed one

    def read(self, key: str) -> tuple[str | None, int]:  # => co-25: returns (value, files_checked) -- read cost is EXPLICIT here
        """Read a key, checking the memtable then EVERY SSTable newest-first, counting files examined."""  # => documents the contract
        files_checked = 1  # => co-25: the memtable itself always counts as one "file" checked first
        if key in self.memtable.entries:  # => co-25: the memtable is always checked FIRST -- it holds the most recent writes
            return self.memtable.entries[key], files_checked  # => found in the memtable -- cheapest possible read
        for sstable in reversed(self.sstables):  # => co-25: NEWEST SSTable first -- a later write shadows an earlier one
            files_checked += 1  # => co-25: each SSTable consulted adds ONE to the read's own file-check cost
            if key in sstable.entries:  # => co-25: this key was found in THIS SSTable
                return sstable.entries[key], files_checked  # => co-25: stop as soon as found -- no need to check OLDER SSTables
        return None, files_checked  # => co-25: not found anywhere -- the read still paid for checking every file

    def compact(self) -> None:  # => co-25: merges ALL current SSTables into ONE, reducing future read cost
        """Merge every SSTable into a single one, newer values winning over older ones for the same key."""  # => documents contract
        merged: dict[str, str] = {}  # => co-25: the merged result, built oldest-to-newest so later writes win
        for sstable in self.sstables:  # => co-25: iterates OLDEST first so a later SSTable's value overwrites an earlier one
            merged.update(sstable.entries)  # => co-25: a later SSTable's entries LEGITIMATELY overwrite an earlier SSTable's same key
        self.sstables = [SSTable(merged)]  # => co-25: replaces N SSTables with exactly 1 -- this is what compaction buys a future read


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    store = LsmStore()  # => co-25: a fresh store, no SSTables yet

    store.write("k1", "v1")  # => a write that will be flushed into its own SSTable, below
    store.flush()  # => co-25: k1 now lives in SSTable 0
    store.write("k2", "v2")  # => a second write, flushed separately
    store.flush()  # => co-25: k2 now lives in SSTable 1 -- SEPARATE from SSTable 0
    store.write("k3", "v3")  # => a third write, flushed separately
    store.flush()  # => co-25: k3 now lives in SSTable 2 -- k1's read must now check THROUGH 3 files to find k1

    _value, files_before = store.read("k1")  # => co-25: k1 lives in the OLDEST SSTable -- the read must check memtable + all 3 SSTables
    print(f"Read k1 BEFORE compaction: checked {files_before} files (memtable + {len(store.sstables)} SSTables)")  # => Output: Read k1 BEFORE compaction: checked 4 files (memtable + 3 SSTables)
    assert files_before == 4  # => co-25: memtable (empty, still checked) + 3 separate SSTables, k1 found only in the LAST one checked

    store.compact()  # => co-25: merges all 3 SSTables into exactly 1
    assert len(store.sstables) == 1  # => co-25: compaction reduced the SSTable COUNT from 3 to 1
    _value2, files_after = store.read("k1")  # => the SAME key, re-read after compaction
    print(f"Read k1 AFTER compaction:  checked {files_after} files (memtable + {len(store.sstables)} SSTable)")  # => Output: Read k1 AFTER compaction:  checked 2 files (memtable + 1 SSTable)
    assert files_after == 2  # => co-25: memtable + exactly 1 merged SSTable -- read cost dropped once compaction reduced the SSTable count
    assert files_after < files_before  # => co-25: verifies the improvement directly -- read amplification genuinely dropped


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
