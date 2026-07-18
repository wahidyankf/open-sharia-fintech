"""Example 64: A Flush's Multiple Writes Commit Together, as One Atomic Unit."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain objects being flushed together
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a domain object -- multiple of these flush in ONE transaction
class User:  # => the type this example's flush writes, several at once
    id: int | None  # => None until flush() assigns it
    name: str  # => an ordinary column


class UnitOfWork:  # => co-20: one flush, one commit, covering EVERY pending write
    def __init__(self, conn: sqlite3.Connection) -> None:  # => needs a connection to flush against
        self._conn = conn  # => the ONE connection every flushed write goes through
        self._new: list[User] = []  # => co-16: objects registered as "new"

    def register_new(self, user: User) -> None:  # => tracked, not yet written
        self._new.append(user)  # => appended to the pending-insert set

    def flush(self) -> None:  # => co-20: ALL pending writes, then ONE commit -- atomic as a group
        for user in self._new:  # => every tracked-new object gets its own INSERT
            cursor = self._conn.execute("INSERT INTO users(name) VALUES (?)", (user.name,))  # => real write
            user.id = cursor.lastrowid  # => the pk assigned by the database
        self._conn.commit()  # => co-20: a SINGLE commit makes EVERY write above durable together
        self._new.clear()  # => flushed objects are no longer "new"


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.commit()  # => makes the schema visible
    uow = UnitOfWork(conn)  # => co-20: one unit of work over this connection
    uow.register_new(User(id=None, name="Alice"))  # => three pending objects, none written yet
    uow.register_new(User(id=None, name="Bob"))  # => co-20: all three flush in ONE transaction
    uow.register_new(User(id=None, name="Carol"))  # => and become durable via ONE commit call
    uow.flush()  # => co-20: three INSERTs, then a SINGLE commit
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]  # => proves ALL three are durable
    assert count == 3  # => not one, not two -- every write from this flush landed together
    print(count)  # => Output: 3
