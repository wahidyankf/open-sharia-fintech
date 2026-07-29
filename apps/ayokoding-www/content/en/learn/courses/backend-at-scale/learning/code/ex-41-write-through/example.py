# pyright: strict
"""Example 41: Write-through cache -- update cache and DB together. (co-22)

Write-through updates the cache SYNCHRONOUSLY on every write, so reads stay
fresh without waiting for a TTL or a lazy reload. Source: AWS Redis caching
strategies whitepaper (write-through).
"""

from dataclasses import dataclass  # => a small typed record for the read result


@dataclass  # => co-22: distinguishes a cache hit from a DB read
class ReadResult:
    value: str  # => the value returned
    source: str  # => "cache" or "db"


DB: dict[int, str] = {}  # => the durable store
CACHE: dict[int, str] = {}  # => co-22: kept IN SYNC with the DB on every write


def write_through(key: int, value: str) -> None:  # => co-22: update DB THEN cache, synchronously
    DB[key] = value  # => the durable write
    CACHE[key] = value  # => co-22: the cache is updated in the SAME operation -> reads stay fresh


def read(key: int) -> ReadResult:  # => a read always hits the fresh cache after a write-through
    if key in CACHE:  # => write-through keeps the cache populated
        return ReadResult(CACHE[key], "cache")  # => fresh, no DB read needed
    return ReadResult(DB.get(key, "<missing>"), "db")  # => cold cache fallback


write_through(1, "v1")  # => co-22: write updates BOTH DB and cache
read1 = read(1)  # => reads the FRESH value straight from the cache
print(f"after write-through: value={read1.value!r}, source={read1.source}")  # => Output: v1, cache

write_through(1, "v2")  # => co-22: a SECOND write rewrites BOTH -> cache is never stale
read2 = read(1)  # => reads the NEW value from the (synchronously updated) cache
print(f"after second write:  value={read2.value!r}, source={read2.source}")  # => Output: v2, cache

assert DB[1] == "v2" and CACHE[1] == "v2"  # => co-22: both reflect the latest write
assert read2.value == "v2" and read2.source == "cache"  # => reads are fresh, never stale
