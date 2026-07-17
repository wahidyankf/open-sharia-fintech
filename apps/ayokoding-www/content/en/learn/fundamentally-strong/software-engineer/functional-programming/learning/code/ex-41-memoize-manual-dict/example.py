"""Example 41: A Hand-Rolled Memoization Dict."""

from typing import Callable  # => Callable types the function memoize wraps

call_count = 0  # => tracks how many times the EXPENSIVE function body actually ran


def expensive(n: int) -> int:  # => stands in for a slow, pure computation
    global call_count  # => declares intent to mutate the MODULE-level counter
    call_count += 1  # => only increments when the body actually executes
    return n * n  # => the actual (slow, pure) computation being cached


def memoize(
    fn: Callable[[int], int],
) -> Callable[[int], int]:  # => a hand-rolled cache, no lru_cache
    cache: dict[int, int] = {}  # => the memo table, one entry per unique argument

    def wrapper(n: int) -> int:  # => the returned, cache-checking function
        if n not in cache:  # => cache MISS: compute once and store
            cache[n] = fn(n)  # => computes ONCE and stores under key n
        return cache[
            n
        ]  # => cache HIT or freshly-stored value, either way no recomputation

    return wrapper  # => memoize itself returns the wrapping function


memoized_expensive = memoize(expensive)  # => wraps expensive with the hand-rolled cache

first = memoized_expensive(5)  # => cache miss -- call_count becomes 1
second = memoized_expensive(5)  # => cache HIT -- call_count stays 1
third = memoized_expensive(6)  # => a NEW argument -- cache miss, call_count becomes 2

# => memoization trades memory for time, valid ONLY because expensive is pure
print(first, second, third)  # => Output: 25 25 36
print(
    call_count
)  # => Output: 2 -- expensive body ran exactly twice, for the two unique arguments
