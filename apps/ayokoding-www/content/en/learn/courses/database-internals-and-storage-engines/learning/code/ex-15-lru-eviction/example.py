"""Example 15: LRU Eviction -- the least-recently-used frame is always the victim."""

from collections import (
    OrderedDict,
)  # => a dict that also remembers insertion/move-to-end order


class LRUCache:  # => insertion/access order IS the recency order, via OrderedDict
    def __init__(
        self, capacity: int
    ) -> None:  # => capacity is the max number of resident pages
        self.capacity = capacity  # => stored so touch() knows when it has overflowed
        self.pool: OrderedDict[int, bytes] = (
            OrderedDict()
        )  # => page_id -> bytes, oldest-first order
        self.evicted: list[
            int
        ] = []  # => records every page_id ever evicted, in eviction order

    def touch(
        self, page_id: int, data: bytes
    ) -> None:  # => access (or load) a page: marks it MOST recent
        if (
            page_id in self.pool
        ):  # => already resident: this is a re-access, not a fresh load
            self.pool.move_to_end(
                page_id
            )  # => re-access moves it to the "most recently used" end
        self.pool[page_id] = (
            data  # => insert (or refresh) this page at the most-recent end
        )
        if (
            len(self.pool) > self.capacity
        ):  # => over capacity: evict the LEAST recently used
            victim_id, _ = self.pool.popitem(
                last=False
            )  # => removes the OLDEST (front) entry
            self.evicted.append(
                victim_id
            )  # => record it for this example's own verification below


cache = LRUCache(capacity=3)  # => room for 3 resident pages
cache.touch(1, b"a")  # => page 1 loaded
cache.touch(2, b"b")  # => page 2 loaded
cache.touch(3, b"c")  # => pool is now full: order is [1, 2, 3], oldest-first
cache.touch(
    1, b"a"
)  # => RE-touching page 1 moves it to most-recent -- no eviction yet (still 3 entries)
cache.touch(4, b"d")  # => now over capacity: evicts the current LRU entry
print(cache.evicted)  # => Output: [2]
print(list(cache.pool.keys()))  # => Output: [3, 1, 4]

assert cache.evicted == [
    2
]  # => page 2 was evicted -- it was LRU once page 1 got re-touched before it
assert (
    1 in cache.pool and 2 not in cache.pool
)  # => the re-touched page survived; the untouched one did not
# => recency, not insertion order, is exactly what OrderedDict.move_to_end tracks here
print("ex-15 OK")  # => Output: ex-15 OK
