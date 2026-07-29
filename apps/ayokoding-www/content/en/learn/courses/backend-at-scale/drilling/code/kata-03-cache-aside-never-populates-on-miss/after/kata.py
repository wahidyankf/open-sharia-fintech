# pyright: strict
"""Kata 3 (after): cache-aside POPULATES the cache on a miss."""

DB_QUERY_COUNT = [0]
DB = {1: "Task A"}
CACHE: dict[int, str] = {}


def read_task(task_id: int) -> tuple[str, str]:
    if task_id in CACHE:
        return CACHE[task_id], "cache"
    DB_QUERY_COUNT[0] += 1
    value = DB[task_id]
    CACHE[task_id] = value  # THE FIX: populate the cache so the next read hits.
    return value, "db"


first = read_task(1)
second = read_task(1)  # now a cache hit
print(f"first read:  source={first[1]}, db_queries={DB_QUERY_COUNT[0]}")  # db, 1
print(f"second read: source={second[1]}, db_queries={DB_QUERY_COUNT[0]}")  # cache, 1
assert second[1] == "cache" and DB_QUERY_COUNT[0] == 1
