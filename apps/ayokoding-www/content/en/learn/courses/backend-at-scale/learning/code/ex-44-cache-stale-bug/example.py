# pyright: strict
"""Example 44: The stale-data bug -- a too-long TTL. (co-23)

A TTL longer than the data's real freshness window serves STALE data: the DB
changes but the cache keeps returning the old value until the (over-long) TTL
expires. This example shows the BUG, then applies the FIX (a correct TTL +
explicit invalidation).
"""

DB: dict[int, str] = {1: "v1"}  # => the source of truth
CACHE: dict[int, str] = {1: "v1"}  # => a pre-populated cache
CACHED_AT = [0]  # => when the cache entry was written (injected clock)
ttl_seconds = [9999]  # => co-23: the BUG -- a TTL far longer than the data's real freshness


def read_buggy(now: int) -> str:  # => the BUGGY read: trusts the over-long TTL
    entry_age = now - CACHED_AT[0]  # => how old the cached entry is
    if 1 in CACHE and entry_age < ttl_seconds[0]:  # => co-23: still "fresh" per the wrong TTL
        return CACHE[1]  # => BUG: returns STALE data after the DB changed
    return DB[1]  # => (unreachable while the buggy TTL holds)


DB[1] = "v2"  # => the DB changes -- but the cache is NOT invalidated
stale = read_buggy(now=10)  # => co-23: BUG -- age 10 < 9999, so "v1" is served from the stale cache
print(f"BUGGY (TTL=9999): DB is 'v2' but cache served {stale!r}")  # => Output: v1 (stale!)

# THE FIX: a correct TTL matching the freshness window, PLUS explicit invalidation on writes.
ttl_seconds[0] = 60  # => co-23: a TTL matching the real freshness window


def invalidate(key: int) -> None:  # => the FIX's other half -- evict on mutation
    CACHE.pop(key, None)  # => co-23: explicit invalidation


def read_fixed(now: int) -> str:  # => the FIXED read: correct TTL + invalidation
    entry_age = now - CACHED_AT[0]  # => age of the cached entry
    if 1 in CACHE and entry_age < ttl_seconds[0]:  # => within the CORRECT TTL -> fresh
        return CACHE[1]  # => fresh
    CACHE[1] = DB[1]  # => miss (evicted or expired) -> re-load the CURRENT DB value
    CACHED_AT[0] = now  # => record the reload time
    return CACHE[1]  # => the fresh value


invalidate(1)  # => co-23: the write path now invalidates the stale entry
fresh = read_fixed(now=10)  # => cache evicted -> re-loads the CURRENT DB value
print(f"FIXED (TTL=60 + invalidate): served {fresh!r}")  # => Output: v2 (fresh)

assert stale == "v1"  # => co-23: the bug served stale data
assert fresh == "v2"  # => co-23: the fix serves the fresh value
