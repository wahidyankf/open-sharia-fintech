"""Example 66: After a Successful Flush, the New/Dirty/Deleted Sets Are Empty."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain object being flushed
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a domain object -- flushed once, then its tracking is cleared
class User:  # => the type this example's flush writes, then stops tracking
    id: int | None  # => None until flush() assigns it
    name: str  # => an ordinary column


class UnitOfWork:  # => co-16 + co-20: flush() must clear pending state so a SECOND flush is a no-op
    def __init__(self, conn: sqlite3.Connection) -> None:  # => needs a connection to flush against
        self._conn = conn  # => the ONE connection every flushed write goes through
        self._new: list[User] = []  # => co-16: objects registered as "new"

    def register_new(self, user: User) -> None:  # => tracked, not yet written
        self._new.append(user)  # => appended to the pending-insert set

    @property  # => read-only view of the CURRENTLY-pending new set, for observation in tests/examples
    def new_objects(self) -> list[User]:  # => empties out once flush() has run successfully
        return self._new  # => the SAME list every time -- no copy, no hidden mutation

    def flush(self) -> None:  # => co-20: writes every pending object, THEN clears the tracked-new set
        for user in self._new:  # => every tracked-new object gets its own INSERT
            cursor = self._conn.execute("INSERT INTO users(name) VALUES (?)", (user.name,))  # => real write
            user.id = cursor.lastrowid  # => the pk assigned by the database
        self._conn.commit()  # => makes every write durable together
        self._new = []  # => co-16: CLEARS the tracked-new set -- flushed objects are no longer "pending"


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.commit()  # => makes the schema visible
    uow = UnitOfWork(conn)  # => co-16 + co-20: one unit of work over this connection
    uow.register_new(User(id=None, name="Alice"))  # => one pending object before the first flush
    assert len(uow.new_objects) == 1  # => confirmed: exactly one object pending BEFORE flush
    uow.flush()  # => co-20: writes it, then clears the tracked-new set
    assert len(uow.new_objects) == 0  # => co-16: nothing pending AFTER a successful flush
    uow.flush()  # => a SECOND flush, with nothing pending -- must be a genuine no-op
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]  # => confirms no duplicate INSERT happened
    assert count == 1  # => still exactly one row -- the second flush wrote nothing
    print(count)  # => Output: 1
