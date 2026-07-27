"""Example 11: Buffer Fetch on a Miss -- loads from the fake disk and counts the miss."""

from dataclasses import dataclass, field  # => a typed, mutable buffer-pool model


@dataclass  # => auto-generates __init__ from the fields below
class BufferPool:  # => models the whole read path: disk, resident frames, hit/miss counters
    disk: dict[int, bytes]  # => stand-in for a real file on disk, keyed by page id
    frames: dict[int, bytes] = field(
        default_factory=dict[int, bytes]
    )  # => resident pages
    hits: int = 0  # => counts fetches that found the page already resident
    misses: int = 0  # => counts fetches that had to load from disk

    def fetch(
        self, page_id: int
    ) -> bytes:  # => the ONLY read path -- callers never touch disk directly
        if page_id in self.frames:  # => already resident: no disk access needed
            self.hits += 1  # => counted as a hit -- disk untouched
            return self.frames[page_id]  # => serve straight from memory
        self.misses += 1  # => not resident: this IS a miss
        data = self.disk[page_id]  # => load from the fake disk
        self.frames[page_id] = (
            data  # => cache it so the NEXT fetch of this page is a hit
        )
        return data  # => the newly-loaded bytes


pool = BufferPool(
    disk={1: b"page-one", 2: b"page-two"}
)  # => a fake disk with two pages, empty pool
print(pool.fetch(1))  # => Output: b'page-one'
print((pool.hits, pool.misses))  # => Output: (0, 1)
# => one miss, zero hits -- this was the very first fetch of page 1

assert pool.misses == 1  # => the first fetch of an unloaded page is always a miss
assert (
    1 in pool.frames
)  # => after the miss, the page IS now resident for future fetches
print("ex-11 OK")  # => Output: ex-11 OK
