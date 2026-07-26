"""Example 12: Buffer Fetch on a Hit -- no disk read when the page is already resident."""

from dataclasses import dataclass, field  # => a typed, mutable buffer-pool model


@dataclass  # => auto-generates __init__ from the fields below
class BufferPool:  # => same shape as ex-11, plus a disk_reads audit trail
    disk: dict[int, bytes]  # => stand-in for a real file on disk, keyed by page id
    frames: dict[int, bytes] = field(
        default_factory=dict[int, bytes]
    )  # => resident pages
    hits: int = 0  # => counts fetches that found the page already resident
    misses: int = 0  # => counts fetches that had to load from disk
    disk_reads: list[int] = field(
        default_factory=list[int]
    )  # => records EVERY page_id read from disk

    def fetch(
        self, page_id: int
    ) -> bytes:  # => same read path as ex-11, now tracking disk_reads too
        if page_id in self.frames:  # => already resident: no disk access needed
            self.hits += 1  # => resident: counted as a hit, disk untouched
            return self.frames[page_id]  # => serve straight from memory
        self.misses += 1  # => not resident: this IS a miss
        self.disk_reads.append(page_id)  # => only a miss ever appends here
        data = self.disk[
            page_id
        ]  # => the ONLY line in this file that reads the fake disk
        self.frames[page_id] = (
            data  # => now resident -- the NEXT fetch of this page is a hit
        )
        return data  # => the newly-loaded bytes


pool = BufferPool(disk={5: b"page-five"})  # => a fake disk with one page, empty pool
pool.fetch(5)  # => first fetch: a miss, loads page 5 into frames
second = pool.fetch(5)  # => second fetch: page 5 is now resident
print(second)  # => Output: b'page-five'
print((pool.hits, pool.misses, pool.disk_reads))  # => Output: (1, 1, [5])
# => two fetches total, but disk_reads has only ONE entry -- the second fetch never touched it

assert pool.hits == 1  # => exactly one hit occurred (the second fetch)
assert pool.disk_reads == [
    5
]  # => disk was read exactly once, never again for the same page
print("ex-12 OK")  # => Output: ex-12 OK
