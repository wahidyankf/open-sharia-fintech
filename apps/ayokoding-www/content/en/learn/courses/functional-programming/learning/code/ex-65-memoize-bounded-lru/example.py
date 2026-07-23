"""Example 65: A Memoization Decorator With a Bounded maxsize."""

from collections import (
    OrderedDict,
)  # => insertion-ordered dict -- the basis of this LRU cache
from typing import Callable  # => Callable types every layer of this decorator factory


def bounded_memoize(
    maxsize: int,
) -> Callable[[Callable[[int], int]], Callable[[int], int]]:  # => a decorator FACTORY
    def decorator(
        fn: Callable[[int], int],
    ) -> Callable[[int], int]:  # => the actual decorator
        cache: OrderedDict[int, int] = (
            OrderedDict()
        )  # => insertion order tracks recency

        def wrapper(n: int) -> int:  # => the cache-checking, eviction-aware wrapper
            if n in cache:  # => cache HIT: refresh its recency, return the stored value
                cache.move_to_end(n)  # => marks n as the MOST recently used entry
                return cache[n]  # => the stored value, no recomputation
            result = fn(n)  # => cache MISS: run the real computation
            cache[n] = result  # => stores the fresh result as the newest entry
            if (
                len(cache) > maxsize
            ):  # => over budget -- evict the LEAST recently used entry
                cache.popitem(
                    last=False
                )  # => last=False pops the OLDEST inserted/touched key
            return result  # => the freshly computed value

        return wrapper  # => decorator itself returns the cache-checking wrapper

    return decorator  # => bounded_memoize itself returns the decorator


calls: list[
    int
] = []  # => records every argument that actually triggered a real computation


@bounded_memoize(
    maxsize=2
)  # => keeps at most 2 cached results -- the THIRD distinct key evicts one
def track(n: int) -> int:  # => the function being memoized
    calls.append(n)  # => only runs on a cache MISS
    return n * n  # => the actual (slow, pure) computation being cached


track(1)  # => miss: cache holds {1}
track(2)  # => miss: cache holds {1, 2}
track(1)  # => HIT: 1 becomes the most recently used entry, no new call recorded
track(3)  # => miss, over budget: evicts 2 (least recently used); cache holds {1, 3}
track(2)  # => 2 was evicted -- this is a MISS again, not a hit
track(1)  # => 1 was ALSO evicted by the previous miss -- another MISS

# => bounding a cache trades perfect memoization for a fixed memory budget
print(calls)  # => Output: [1, 2, 3, 2, 1] -- five real computations out of six calls
