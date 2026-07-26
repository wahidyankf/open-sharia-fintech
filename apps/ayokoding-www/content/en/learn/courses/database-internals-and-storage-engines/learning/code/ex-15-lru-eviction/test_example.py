"""Example 15: pytest verification for LRU Eviction."""

from example import LRUCache


def test_re_touched_page_survives_eviction() -> None:
    cache = LRUCache(capacity=2)
    cache.touch(1, b"a")
    cache.touch(2, b"b")
    cache.touch(1, b"a")  # => re-touch page 1 -- it is now the most recent
    cache.touch(3, b"c")  # => forces an eviction
    assert cache.evicted == [2]  # => page 2, not page 1, was the true LRU victim


def test_capacity_is_never_exceeded() -> None:
    cache = LRUCache(capacity=2)
    for page_id in range(5):
        cache.touch(page_id, b"x")
    assert len(cache.pool) == 2  # => the pool never grows past its declared capacity


# => Run: pytest -- Output: 2 passed
