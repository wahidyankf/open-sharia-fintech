"""Example 54: A Generic session.get[T](pk) -> T API."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the loaded domain object
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any, Protocol, Self  # => co-25: the generic bound and the classmethod's own return type


class FromRow(Protocol):  # => co-25: the bound every type T passed to session.get must satisfy
    @classmethod  # => a classmethod, not a plain method -- `cls` is what varies per concrete T
    def from_row(cls, row: tuple[Any, ...]) -> Self: ...  # => structural requirement, checked at call sites


@dataclasses.dataclass  # => a loaded domain object -- satisfies FromRow structurally, no inheritance needed
class User:  # => the concrete type this example passes as T
    id: int  # => primary key
    name: str  # => an ordinary column

    @classmethod  # => satisfies FromRow's classmethod requirement structurally
    def from_row(cls, row: tuple[Any, ...]) -> Self:  # => co-10, expressed as the FromRow contract
        return cls(id=row[0], name=row[1])  # => Self here resolves to User at the call site


class Session:  # => co-25: a fully-typed generic get, one method for every FromRow-satisfying type
    def __init__(self, conn: sqlite3.Connection) -> None:  # => handed one connection
        self._conn = conn  # => the ONE connection this session ever uses

    def get[T: FromRow](self, cls: type[T], table: str, pk: int) -> T:  # => T INFERRED from `cls`, PEP 695
        row = self._conn.execute(f"SELECT * FROM {table} WHERE id = ?", (pk,)).fetchone()  # => any row shape
        return cls.from_row(row)  # => pyright checks this returns EXACTLY T, not FromRow


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")  # => one seed row
    conn.commit()  # => makes the seed row visible
    session = Session(conn)  # => co-15 + co-25: a typed session over the one connection
    user: User = session.get(User, "users", 1)  # => pyright infers T=User from the `User` argument alone
    assert isinstance(user, User)  # => the runtime type matches what pyright inferred
    print(user)  # => Output: User(id=1, name='Alice')
