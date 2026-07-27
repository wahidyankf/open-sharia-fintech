"""Example 11: pytest verification for Buffer Fetch on a Miss."""

from example import BufferPool


def test_first_fetch_of_a_page_is_a_miss() -> None:
    pool = BufferPool(disk={10: b"ten"})
    pool.fetch(10)
    assert pool.misses == 1 and pool.hits == 0


def test_miss_loads_the_page_into_frames() -> None:
    pool = BufferPool(disk={10: b"ten"})
    pool.fetch(10)
    assert 10 in pool.frames  # => now resident for future fetches


# => Run: pytest -- Output: 2 passed
