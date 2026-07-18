"""Example 59: Flushing a Clean Object Issues Zero UPDATE Statements."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain object and its snapshot representation
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => a snapshot dict holds mixed-type field values


@dataclasses.dataclass  # => a mutable, already-loaded domain object
class User:  # => the type this unit of work tracks for dirty-then-flush
    id: int  # => primary key
    name: str  # => a mutable column


class UnitOfWork:  # => co-17 + co-20: tracks clean objects, flush() writes ONLY the dirty ones
    def __init__(self, conn: sqlite3.Connection) -> None:  # => needs a connection to flush against
        self._conn = conn  # => the ONE connection every flushed write goes through
        self._snapshots: dict[int, dict[str, Any]] = {}  # => keyed by id(obj)
        self._identity: dict[int, User] = {}  # => keyed by id(obj), keeps tracked objects reachable
        self.update_count = 0  # => co-17: instrumented so this example can PROVE zero writes happen

    def track_clean(self, user: User) -> None:  # => registers an already-persisted object as "clean"
        self._identity[id(user)] = user  # => reachable for the flush loop below
        self._snapshots[id(user)] = dataclasses.asdict(user)  # => the baseline to diff against

    def flush(self) -> None:  # => co-20: writes ONLY objects whose live state diverged from their snapshot
        for key, user in self._identity.items():  # => walks every tracked object
            live = dataclasses.asdict(user)  # => the object's CURRENT state
            if live != self._snapshots[key]:  # => co-17: only issues SQL when something actually changed
                self._conn.execute("UPDATE users SET name = ? WHERE id = ?", (user.name, user.id))  # => real write
                self.update_count += 1  # => counts ONLY the writes that actually ran
                self._snapshots[key] = live  # => re-baselines -- this object is clean again after flush
        self._conn.commit()  # => makes any real writes durable


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")  # => one seed row
    conn.commit()  # => makes the seed row visible
    uow = UnitOfWork(conn)  # => co-17 + co-20: one unit of work over this connection
    alice = User(id=1, name="Alice")  # => matches the seed row's CURRENT state exactly
    uow.track_clean(alice)  # => snapshot taken -- identical to alice's own current fields
    uow.flush()  # => co-17: alice is CLEAN -- this flush issues zero UPDATE statements
    assert uow.update_count == 0  # => no write happened -- the object was never dirty
    print(uow.update_count)  # => Output: 0
