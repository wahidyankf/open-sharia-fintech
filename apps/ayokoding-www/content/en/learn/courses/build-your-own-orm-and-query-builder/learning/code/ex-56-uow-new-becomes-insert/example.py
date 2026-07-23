"""Example 56: Flushing the New Set Issues Real INSERTs and Assigns Primary Keys."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain object being tracked and, later, persisted
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a domain object -- mutable so flush() can assign the pk after insert
class User:  # => the type this example tracks-then-inserts
    id: int | None  # => None until flush() assigns it from the database's rowid
    name: str  # => an ordinary column


class UnitOfWork:  # => co-16 + co-20: tracks new objects, then flush() turns them into real writes
    def __init__(self, conn: sqlite3.Connection) -> None:  # => needs a connection to flush against
        self._conn = conn  # => the ONE connection every flushed write goes through
        self._new: list[User] = []  # => co-16: objects registered as "new"

    def register_new(self, user: User) -> None:  # => tracked, not yet written
        self._new.append(user)  # => appended to the pending-insert set

    def flush(self) -> None:  # => co-20: turns EVERY tracked-new object into a real INSERT
        for user in self._new:  # => one INSERT per tracked-new object, in registration order
            cursor = self._conn.execute("INSERT INTO users(name) VALUES (?)", (user.name,))  # => real write
            user.id = cursor.lastrowid  # => co-16: the pk assigned BY the database, written back onto the object
        self._new.clear()  # => flushed objects are no longer "new" -- clears the tracked set


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.commit()  # => makes the schema visible
    uow = UnitOfWork(conn)  # => co-16 + co-20: one unit of work over this connection
    alice = User(id=None, name="Alice")  # => a brand-new object, no pk yet
    uow.register_new(alice)  # => tracked -- still no SQL has run for this object
    assert alice.id is None  # => confirmed: no pk assigned before flush
    uow.flush()  # => co-20: issues the real INSERT, assigns the pk
    assert alice.id is not None  # => the SAME object now carries a real, database-assigned pk
    row = conn.execute("SELECT name FROM users WHERE id = ?", (alice.id,)).fetchone()  # => proves it's durable
    assert row is not None and row[0] == "Alice"  # => a real row exists at that pk
    print(alice.id)  # => Output: 1
