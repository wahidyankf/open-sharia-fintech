"""Example 12: pytest verification for Buffer Fetch on a Hit."""

from example import BufferPool


def test_second_fetch_of_same_page_is_a_hit() -> None:
    pool = BufferPool(disk={5: b"five"})
    pool.fetch(5)
    pool.fetch(5)
    assert pool.hits == 1 and pool.misses == 1


def test_disk_is_read_at_most_once_per_page() -> None:
    pool = BufferPool(disk={5: b"five"})
    for _ in range(5):
        pool.fetch(5)
    assert pool.disk_reads == [
        5
    ]  # => 5 fetches, but disk touched only on the very first one


# => Run: pytest -- Output: 2 passed
