"""Example 25: @lru_cache on a Recursive fib."""

from functools import (
    lru_cache,
)  # => decorator-based memoization, keyed by call arguments


@lru_cache(
    maxsize=None
)  # => unbounded cache -- every unique n is computed at most once
def fib(
    n: int,
) -> int:  # => the classic exponential-without-caching recursive definition
    if n < 2:  # => base case: fib(0) = 0, fib(1) = 1
        return n  # => no further recursion needed below n=2
    return fib(n - 1) + fib(n - 2)  # => WITHOUT caching this branches exponentially


result = fib(
    30
)  # => triggers a burst of recursive calls, each cached the FIRST time it runs
info_after_first = fib.cache_info()  # => snapshot: hits so far, misses so far

fib(
    30
)  # => calling AGAIN with the same n=30 -- served entirely from cache, no recursion
info_after_second = fib.cache_info()  # => hits increased, misses did NOT

print(result)  # => Output: 832040
print(
    info_after_second.hits > info_after_first.hits
)  # => Output: True -- repeat call hit the cache
print(
    info_after_second.misses == info_after_first.misses
)  # => Output: True -- no NEW work happened
