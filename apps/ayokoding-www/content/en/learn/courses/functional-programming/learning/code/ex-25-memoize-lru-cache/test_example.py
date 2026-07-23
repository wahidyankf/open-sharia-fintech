"""Example 25: pytest verification for @lru_cache on a Recursive fib."""

from example import fib


def test_repeat_call_hits_the_cache() -> None:
    fib.cache_clear()  # => start from a known, empty cache
    fib(20)  # => first call: populates the cache
    before = fib.cache_info()
    fib(20)  # => identical call: should be served from cache
    after = fib.cache_info()
    assert after.hits > before.hits
    assert after.misses == before.misses


# => Run: pytest -- Output: 1 passed
