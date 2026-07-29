# pyright: strict
"""Example 40: Cache-aside -- a cached read issues no DB query. (co-21)

Same cache-aside pattern as Example 39, but the focus is the instrumented
DB: a COLD read costs exactly one query, while every subsequent WARM read
costs ZERO -- proving the cache absorbs the load the DB would otherwise see.
"""


class Database:  # => co-21: an instrumented DB that counts every query against it
    def __init__(self, rows: dict[int, str]) -> None:
        self._rows = rows  # => the source of truth
        self.queries = 0  # => the query counter

    def fetch(self, key: int) -> str | None:  # => each call is one real query
        self.queries += 1  # => count it
        return self._rows.get(key)  # => the value (or None)


class CacheAside:  # => co-21: the lazy-loading cache layer over the DB
    def __init__(self, db: Database) -> None:
        self._db = db  # => the backing store
        self._cache: dict[int, str] = {}  # => the cache, populated on a miss

    def read(self, key: int) -> str | None:  # => miss -> DB -> populate; hit -> cache
        if key in self._cache:  # => HIT
            return self._cache[key]  # => no DB query
        value = self._db.fetch(key)  # => MISS -> one DB query
        if value is not None:  # => only cache real values (not missing keys)
            self._cache[key] = value  # => populate
        return value  # => the value


db = Database({1: "Task A"})  # => co-21: an instrumented DB with one row
store = CacheAside(db)  # => the cache layer over it

cold = store.read(1)  # => MISS -> one DB query
warm = store.read(1)  # => HIT -> zero DB queries
warm2 = store.read(1)  # => HIT -> zero DB queries
print(f"cold read:  value={cold!r}, db.queries={db.queries}")  # => Output: 'Task A', 1
print(f"warm reads: value={warm!r}, db.queries={db.queries}")  # => Output: 'Task A', still 1

assert db.queries == 1  # => co-21: a cached read issues ZERO db queries; only the cold read cost one
assert cold == warm == warm2 == "Task A"  # => all three reads returned the same value
