# pyright: strict
"""Example 43: Explicit cache invalidation on a mutation. (co-23)

A TTL alone cannot guarantee freshness if the DB changes before the TTL
expires. A write therefore EXPLICITLY invalidates (evicts) the cached key so
the next read re-loads the fresh value. "Cache invalidation is a correctness
problem" -- the wrong TTL serves stale data.
"""

DB: dict[int, str] = {1: "v1"}  # => the source of truth
CACHE: dict[int, str] = {1: "v1"}  # => co-23: a pre-populated cache


def read(key: int) -> tuple[str, str]:  # => returns (value, source)
    if key in CACHE:  # => hit
        return CACHE[key], "cache"  # => served from cache
    value = DB[key]  # => miss -> load from DB
    CACHE[key] = value  # => repopulate
    return value, "db"  # => re-loaded


def update(key: int, value: str) -> None:  # => a mutation that MUST invalidate the cache
    DB[key] = value  # => the durable write
    CACHE.pop(key, None)  # => co-23: EXPLICIT invalidation -- evict the now-stale entry


before = read(1)  # => served from the pre-populated cache
print(f"before update: value={before[0]!r}, source={before[1]}")  # => Output: v1, cache

update(1, "v2")  # => co-23: writes the DB AND invalidates the cached key
after = read(1)  # => cache was evicted -> re-loads the FRESH value from the DB
print(f"after update:  value={after[0]!r}, source={after[1]}")  # => Output: v2, db

assert DB[1] == "v2" and after[0] == "v2" and after[1] == "db"  # => co-23: invalidation forced a fresh re-load
assert 1 not in CACHE or CACHE[1] == "v2"  # => the cache no longer holds the stale "v1"
