"""Example 42: Buffer Pool Hit Ratio."""
# Hit ratio (co-06) is the standard buffer-pool health metric.

from dataclasses import dataclass, field  # => typed pool + counters


@dataclass  # => a plain, typed record -- no custom __init__ needed
class BufferPool:  # => a minimal pool that just tracks resident pages and hit/miss counts
    frames: set[int] = field(default_factory=set[int])  # => currently resident page ids
    hits: int = 0  # => count of accesses that found the page already resident
    misses: int = 0  # => count of accesses that had to load the page


def access(
    pool: BufferPool, page_id: int
) -> None:  # => one workload access against the pool
    if page_id in pool.frames:  # => already resident -- a hit
        pool.hits += 1  # => tally the hit -- no load needed
    else:  # => not resident -- a miss, must be loaded
        pool.misses += 1  # => tally the miss before loading
        pool.frames.add(page_id)  # => now resident for any future access


def hit_ratio(
    pool: BufferPool,
) -> float:  # => co-06: the standard buffer-pool efficiency metric
    total = pool.hits + pool.misses  # => total accesses attempted
    return (
        pool.hits / total if total else 0.0
    )  # => guard against dividing by zero on an empty workload


pool = BufferPool()  # => a fresh, empty pool
workload = [
    1,
    2,
    1,
    3,
    1,
    2,
]  # => a mix of repeated (hits) and new (misses) page accesses
for page_id in workload:  # => replay the whole workload through the pool
    access(pool, page_id)  # => feed each workload access through the pool
print(pool.hits)  # => Output: 3
print(pool.misses)  # => Output: 3
ratio = hit_ratio(pool)  # => compute the final hit ratio for this workload
print(ratio)  # => Output: 0.5

assert (
    pool.hits == 3
)  # => pages 1 (two repeat hits) and 2 (one repeat hit) -- three hits total
assert pool.misses == 3  # => pages 1, 2, 3 each loaded once -- three misses total
assert ratio == pool.hits / (
    pool.hits + pool.misses
)  # => the exact formula the spec requires
print("ex-42 OK")  # => Output: ex-42 OK
