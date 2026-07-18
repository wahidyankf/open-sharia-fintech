"""Example 51: The Mapper Checks the Identity Map Before Constructing a New Object."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the loaded domain object
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a loaded domain object, mapped from a row (co-10)
class User:  # => the type the identity map holds one instance of, per pk
    id: int  # => primary key
    name: str  # => an ordinary column


class Mapper:  # => co-10, instrumented to COUNT how many times it actually constructs a User
    def __init__(self) -> None:  # => starts with zero constructions
        self.construct_count = 0  # => co-13: proves a cache hit skips construction, not just the query

    def row_to_user(self, row: tuple[int, str]) -> User:  # => co-10: the mapping step, now counted
        self.construct_count += 1  # => counts EVERY time a new User actually gets built
        return User(id=row[0], name=row[1])  # => the real construction


class IdentityMap:  # => co-13: consults the map BEFORE ever calling the mapper
    def __init__(self, mapper: Mapper) -> None:  # => holds a reference to the shared, counted mapper
        self._mapper = mapper  # => the SAME mapper instance every load routes through
        self._cache: dict[tuple[str, int], User] = {}  # => keyed by (table, pk)

    def load(self, conn: sqlite3.Connection, pk: int) -> User:  # => co-13 + co-10, composed
        key = ("users", pk)  # => this pk's identity key
        if key in self._cache:  # => a HIT -- the mapper is NEVER called on this path
            return self._cache[key]  # => reused object, mapper.construct_count untouched
        row = conn.execute("SELECT id, name FROM users WHERE id = ?", (pk,)).fetchone()  # => real query
        user = self._mapper.row_to_user(row)  # => a MISS -- the mapper constructs a fresh object
        self._cache[key] = user  # => caches it so the NEXT load of this pk is a hit
        return user  # => a fresh, newly-constructed, now-cached object


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")  # => one seed row
    conn.commit()  # => makes the seed row visible
    mapper = Mapper()  # => the shared, instrumented mapper
    identity_map = IdentityMap(mapper)  # => co-13 + co-10 wired together
    first = identity_map.load(conn, 1)  # => MISS -- constructs a User, count becomes 1
    second = identity_map.load(conn, 1)  # => HIT -- reuses `first`, count STAYS at 1
    assert first is second  # => the identity guarantee still holds
    assert mapper.construct_count == 1  # => co-13: the cached path skipped the mapper entirely
    print(mapper.construct_count)  # => Output: 1
