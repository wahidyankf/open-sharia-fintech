"""Example 76: Wiring the Full Write Stack -- Session, UnitOfWork, and a Real Flush."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain object the whole write stack tracks and flushes
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a domain object -- mutable so flush() can assign the pk after insert
class User:  # => the type this write stack tracks-then-persists
    id: int | None  # => None until flush() assigns it
    name: str  # => an ordinary, mutable column


class UnitOfWork:  # => co-16 + co-20: the tracking-then-writing layer, owned by the session below
    def __init__(self, conn: sqlite3.Connection) -> None:  # => shares the session's OWN connection
        self._conn = conn  # => co-15: the SAME connection the owning Session uses
        self._new: list[User] = []  # => co-16: objects registered as "new"

    def register_new(self, user: User) -> None:  # => tracked, not yet written
        self._new.append(user)  # => appended to the pending-insert set

    def flush(self) -> None:  # => co-20: turns EVERY tracked-new object into a real INSERT, atomically
        for user in self._new:  # => one INSERT per tracked-new object
            cursor = self._conn.execute("INSERT INTO users(name) VALUES (?)", (user.name,))  # => real write
            user.id = cursor.lastrowid  # => the pk assigned by the database, written back onto the object
        self._new.clear()  # => flushed objects are no longer "new"


class Session:  # => co-15: owns the connection AND the unit of work built around it -- the public API
    def __init__(self, conn: sqlite3.Connection) -> None:  # => handed one connection, kept for its lifetime
        self._conn = conn  # => co-15: the ONE connection this session ever uses
        self.uow = UnitOfWork(conn)  # => co-16 + co-20: composed INTO the session, sharing self._conn

    def add(self, user: User) -> None:  # => co-16: the session's public "track this new object" entry point
        self.uow.register_new(user)  # => delegates to the unit of work -- the session never writes SQL itself

    def commit(self) -> None:  # => co-15 + co-20: the session's public "make it durable" entry point
        self.uow.flush()  # => co-20: turns pending writes into real INSERTs
        self._conn.commit()  # => co-15: makes the WHOLE batch durable, as one transaction boundary

    def query_all(self) -> list[tuple[int, str]]:  # => a minimal read, to verify the write actually landed
        return self._conn.execute("SELECT id, name FROM users").fetchall()  # => co-23: reads over the SAME connection


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.commit()  # => makes the schema visible
    session = Session(conn)  # => co-15 + co-16 + co-20: the ENTIRE write stack, wired around one connection
    alice = User(id=None, name="Alice")  # => a brand-new object, no pk yet
    session.add(alice)  # => co-16: tracked via the session's public API -- still no SQL has run
    assert alice.id is None  # => confirmed: nothing written yet, before commit
    session.commit()  # => co-15 + co-20: flush() then conn.commit() -- the FULL write path, in one call
    assert alice.id is not None  # => co-20: the SAME object now carries a real, database-assigned pk
    rows = session.query_all()  # => reads back to prove the write is genuinely durable
    assert rows == [(alice.id, "Alice")]  # => the wired stack produced exactly the expected row
    print(rows)  # => Output: [(1, 'Alice')]
