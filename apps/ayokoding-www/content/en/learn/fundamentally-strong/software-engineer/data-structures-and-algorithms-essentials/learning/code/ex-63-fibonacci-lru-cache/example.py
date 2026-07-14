"""Example 63: Memoized Fibonacci with functools.lru_cache."""

# lru_cache is memoization built into the standard library -- one decorator
# replaces Example 62's hand-written dict cache entirely (co-19).
from functools import lru_cache  # => imports the stdlib memoizing decorator


@lru_cache(
    maxsize=None
)  # => maxsize=None means "cache every distinct call, no eviction"
def fib(
    n: int,
) -> int:  # => identical recurrence to Example 61; the decorator caches it
    if n <= 1:  # => BASE CASE
        return n  # => n itself is the answer for 0 and 1
    return fib(n - 1) + fib(
        n - 2
    )  # => RECURSIVE CASE; lru_cache intercepts repeat calls


result = fib(10)  # => computed once per distinct n, then served from cache
print(result)  # => Output: 55
info = fib.cache_info()  # => introspects the decorator's own hit/miss bookkeeping
print(info)  # => Output: CacheInfo(hits=8, misses=11, maxsize=None, currsize=11)

assert result == 55  # => confirms the cached recursion still returns the correct value
assert info.hits > 0  # => confirms the cache actually served at least one repeated call
print("ex-63 OK")  # => Output: ex-63 OK
