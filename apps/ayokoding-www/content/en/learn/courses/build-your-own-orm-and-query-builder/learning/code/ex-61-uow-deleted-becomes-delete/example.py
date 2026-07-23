"""Example 61: Flushing the Deleted Set Issues Real DELETE Statements."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain object being tracked and, later, removed
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => an already-persisted domain object
class User:  # => the type this example tracks-then-deletes
    id: int  # => primary key -- a real row exists at this id, before flush
    name: str  # => an ordinary column


class UnitOfWork:  # => co-18 + co-20: tracks deleted objects, then flush() turns them into real DELETEs
    def __init__(self, conn: sqlite3.Connection) -> None:  # => needs a connection to flush against
        self._conn = conn  # => the ONE connection every flushed write goes through
        self._deleted: list[User] = []  # => co-18: objects registered as "deleted"

    def register_deleted(self, user: User) -> None:  # => tracked, not yet written
        self._deleted.append(user)  # => appended to the pending-delete set

    def flush(self) -> None:  # => co-20: turns EVERY tracked-deleted object into a real DELETE
        for user in self._deleted:  # => one DELETE per tracked-deleted object, in registration order
            self._conn.execute("DELETE FROM users WHERE id = ?", (user.id,))  # => real write, by pk
        self._deleted.clear()  # => flushed objects are no longer "deleted" -- clears the tracked set
        self._conn.commit()  # => makes every DELETE durable


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")  # => one seed row
    conn.commit()  # => makes the seed row visible
    uow = UnitOfWork(conn)  # => co-18 + co-20: one unit of work over this connection
    alice = User(id=1, name="Alice")  # => corresponds to the real seed row
    uow.register_deleted(alice)  # => tracked -- still no SQL has run for this object
    before = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]  # => confirms the row exists BEFORE flush
    assert before == 1  # => one real row present before flush
    uow.flush()  # => co-20: issues the real DELETE
    after = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]  # => confirms the row is GONE after flush
    assert after == 0  # => the row was genuinely removed, not just marked
    print(after)  # => Output: 0
