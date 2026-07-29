# pyright: strict
"""Example 46: Cache-Control: max-age. (co-24)

The Cache-Control: max-age=N directive tells a cache the representation is
fresh for N seconds. Within max-age the cache serves without revalidating;
past max-age the cache must revalidate. Source: RFC 9111.
"""

from dataclasses import dataclass  # => a small typed record for a cached representation


@dataclass  # => co-24: a representation plus when it was cached
class Cached:
    value: str  # => the representation
    cached_at: int  # => the (injected) clock time it was cached


CACHE: dict[int, Cached] = {}  # => a cache honoring Cache-Control


def serve(item_id: int, now: int) -> tuple[str, str]:  # => returns (value, source) honoring max-age
    max_age = 60  # => co-24: Cache-Control: max-age=60
    entry = CACHE.get(item_id)  # => look up the cached representation
    if entry is not None and now < entry.cached_at + max_age:  # => co-24: within max-age -> fresh, no revalidation
        return entry.value, "cache (within max-age)"  # => served fresh
    value = f"resource-{item_id}-at-{now}"  # => a fresh origin fetch (simulated)
    CACHE[item_id] = Cached(value, now)  # => cache it with the current time
    return value, "origin (past max-age or cold)"  # => had to revalidate


first = serve(1, now=0)  # => cold -> origin, cached at t=0
print(f"t=0:  {first}")  # => Output: origin

within = serve(1, now=30)  # => 30 < 0+60 -> fresh within max-age
print(f"t=30: {within}")  # => Output: cache (within max-age)

past = serve(1, now=70)  # => 70 >= 0+60 -> past max-age -> revalidate
print(f"t=70: {past}")  # => Output: origin (past max-age)

assert first[1].startswith("origin") and within[1].startswith("cache")  # => co-24: max-age honored within the window
assert past[1].startswith("origin")  # => co-24: past max-age, revalidation required
