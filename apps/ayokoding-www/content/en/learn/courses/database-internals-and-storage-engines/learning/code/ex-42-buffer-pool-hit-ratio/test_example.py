"""Example 42: pytest verification for Buffer Pool Hit Ratio."""

from example import BufferPool, access, hit_ratio


def test_hit_ratio_equals_hits_over_total() -> None:
    pool = BufferPool()
    for page_id in [1, 1, 2]:
        access(pool, page_id)
    assert hit_ratio(pool) == pool.hits / (pool.hits + pool.misses)


def test_all_misses_gives_zero_hit_ratio() -> None:
    pool = BufferPool()
    for page_id in [1, 2, 3]:
        access(pool, page_id)
    assert hit_ratio(pool) == 0.0


# => Run: pytest -- Output: 2 passed
