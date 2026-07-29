# pyright: strict
"""Kata 3 (before): cache-aside never POPULATES the cache on a miss."""

DB_QUERY_COUNT = [0]
DB = {1: "Task A"}
CACHE: dict[int, str] = {}


def read_task(task_id: int) -> tuple[str, str]:
    # THE BUG: on a MISS the DB is queried but the value is RETURNED without being
    # written to the cache -- so every subsequent read misses again and hits the DB.
    if task_id in CACHE:
        return CACHE[task_id], "cache"
    DB_QUERY_COUNT[0] += 1  # every read queries the DB
    value = DB[task_id]
    # BUG: missing CACHE[task_id] = value -- the cache is never populated.
    return value, "db"


first = read_task(1)
second = read_task(1)  # should be a cache hit, but the cache was never populated
print(f"first read:  source={first[1]}, db_queries={DB_QUERY_COUNT[0]}")  # db, 1
print(f"second read: source={second[1]}, db_queries={DB_QUERY_COUNT[0]}")  # BUG: db, 2 (missed again)
