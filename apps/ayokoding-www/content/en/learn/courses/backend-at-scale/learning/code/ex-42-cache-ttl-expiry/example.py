# pyright: strict
"""Example 42: Cache TTL expiry -- entries expire and re-load. (co-23)

A TTL (time-to-live) bounds how long a cached entry is considered fresh.
After the TTL elapses, the entry EXPIRES and the next read re-loads from the
DB. The clock is INJECTED so the expiry is deterministic.
"""

from dataclasses import dataclass  # => a small typed record for a cache entry


@dataclass  # => co-23: a cached value plus the time it was cached
class Entry:
    value: str  # => the cached value
    cached_at: int  # => the (injected) clock time the entry was written


DB: dict[int, str] = {1: "fresh-from-db"}  # => the source of truth
CACHE: dict[int, Entry] = {}  # => co-23: the TTL-governed cache
TTL_SECONDS = 60  # => co-23: an entry is fresh for 60s after cached_at


def populate(key: int, now: int) -> None:  # => load a value into the cache
    CACHE[key] = Entry(value=DB[key], cached_at=now)  # => record the value AND when it was cached


def read(key: int, now: int) -> tuple[str, str]:  # => returns (value, source) honoring the TTL
    entry = CACHE.get(key)  # => look up the cached entry
    if entry is not None and now < entry.cached_at + TTL_SECONDS:  # => co-23: present AND within TTL -> fresh
        return entry.value, "cache"  # => served from cache
    CACHE.pop(key, None)  # => co-23: EXPIRED -> evict the stale entry
    populate(key, now)  # => re-load from the DB
    return DB[key], "db"  # => re-loaded


populate(1, now=0)  # => cache the value at t=0
within_ttl = read(1, now=30)  # => 30 < 0+60 -> still fresh
print(f"within TTL (t=30): value={within_ttl[0]!r}, source={within_ttl[1]}")  # => Output: fresh-from-db, cache

expired = read(1, now=70)  # => 70 >= 0+60 -> EXPIRED -> re-load
print(f"after TTL (t=70):  value={expired[0]!r}, source={expired[1]}")  # => Output: fresh-from-db, db

assert within_ttl[1] == "cache" and expired[1] == "db"  # => co-23: entry expired and re-loaded past the TTL
