# pyright: strict
"""Example 39: Cache-aside -- miss -> DB -> populate, then hit. (co-21)

Cache-aside (lazy loading): on a cache MISS, read the DB, populate the cache,
return the value; on a HIT, return straight from the cache. The DB query
counter proves the second read never touches the DB. Source: AWS Redis
caching strategies whitepaper (cache-aside / lazy load).
"""

from dataclasses import dataclass  # => a small typed record for the read result


DB_QUERY_COUNT = [0]  # => a mutable counter -- how many times the DB was actually queried
DB: dict[int, str] = {1: "Task A", 2: "Task B"}  # => the source of truth
CACHE: dict[int, str] = {}  # => co-21: the cache, populated lazily on a miss


@dataclass  # => co-21: distinguishes a cache hit from a miss
class ReadResult:
    value: str  # => the value returned
    source: str  # => "cache" or "db" -- proves which path served the read


def read_task(task_id: int) -> ReadResult:  # => GET /tasks/{id} -- cache-aside
    if task_id in CACHE:  # => co-21: HIT -> return straight from the cache
        return ReadResult(value=CACHE[task_id], source="cache")  # => no DB query
    DB_QUERY_COUNT[0] += 1  # => co-21: MISS -> query the DB (counted)
    value = DB[task_id]  # => the DB read
    CACHE[task_id] = value  # => co-21: populate the cache so the next read hits
    return ReadResult(value=value, source="db")  # => served from the DB this time


first = read_task(1)  # => MISS -> DB -> populate
print(f"first read:  value={first.value!r}, source={first.source}, db_queries={DB_QUERY_COUNT[0]}")  # => Output: db, 1

second = read_task(1)  # => HIT -> cache, no DB query
print(f"second read: value={second.value!r}, source={second.source}, db_queries={DB_QUERY_COUNT[0]}")  # => Output: cache, 1

assert first.source == "db" and second.source == "cache"  # => co-21: miss-then-hit
assert DB_QUERY_COUNT[0] == 1  # => the cached read issued ZERO additional DB queries
