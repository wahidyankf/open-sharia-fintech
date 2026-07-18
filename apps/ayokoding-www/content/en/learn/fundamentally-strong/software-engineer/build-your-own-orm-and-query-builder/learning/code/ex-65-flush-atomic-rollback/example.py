"""Example 65: A Flush Failure Rolls Back EVERY Write in the Batch, Not Just the Failing One."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain objects being flushed together
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a domain object -- multiple of these flush in ONE transaction
class User:  # => the type this example's flush writes, several at once
    id: int | None  # => None until flush() assigns it
    name: str  # => must be UNIQUE -- a duplicate triggers the failure this example exercises


class UnitOfWork:  # => co-20: a failing write rolls back the WHOLE batch, not just itself
    def __init__(self, conn: sqlite3.Connection) -> None:  # => needs a connection to flush against
        self._conn = conn  # => the ONE connection every flushed write goes through
        self._new: list[User] = []  # => co-16: objects registered as "new"

    def register_new(self, user: User) -> None:  # => tracked, not yet written
        self._new.append(user)  # => appended to the pending-insert set

    def flush(self) -> None:  # => co-20: ALL writes attempted, but ANY failure rolls back the ENTIRE batch
        try:  # => wraps the whole batch -- one failure anywhere aborts everything
            for user in self._new:  # => every tracked-new object gets its own INSERT attempt
                cursor = self._conn.execute("INSERT INTO users(name) VALUES (?)", (user.name,))  # => real write
                user.id = cursor.lastrowid  # => the pk assigned by the database, IF this INSERT succeeded
            self._conn.commit()  # => co-20: reached ONLY if every INSERT in the loop succeeded
        except sqlite3.IntegrityError:  # => co-20: the UNIQUE constraint failed on some write in the batch
            self._conn.rollback()  # => undoes EVERY write attempted since the last commit, not just the bad one
            raise  # => the caller still sees the failure -- rollback does not hide it


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT UNIQUE)")  # => UNIQUE forces a failure
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")  # => pre-existing row -- 'Alice' is already taken
    conn.commit()  # => makes the seed row visible
    uow = UnitOfWork(conn)  # => co-20: one unit of work over this connection
    uow.register_new(User(id=None, name="Bob"))  # => this one WOULD succeed on its own
    uow.register_new(User(id=None, name="Alice"))  # => this one collides with the seed row -- forces a failure
    try:  # => catches the IntegrityError the second INSERT raises
        uow.flush()  # => co-20: attempts BOTH inserts, the second one fails, BOTH roll back
    except sqlite3.IntegrityError:  # => expected -- proves the batch-level failure propagates
        pass  # => the exception is expected here, so silently continue past it
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]  # => checks what survived the rollback
    assert count == 1  # => co-20: still just the ORIGINAL seed row -- Bob's write was rolled back TOO
    print(count)  # => Output: 1
