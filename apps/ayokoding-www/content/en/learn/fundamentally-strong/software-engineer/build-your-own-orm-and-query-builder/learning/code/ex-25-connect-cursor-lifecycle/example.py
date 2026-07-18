"""Example 25: The Full PEP 249 Lifecycle -- Connect, Cursor, Execute, Fetch, Close."""

import contextlib  # => guarantees Connection.close() even if this block raises partway through
import sqlite3  # => the stdlib DB-API v2.0 driver (PEP 249) this whole topic sits on

# => co-23: every one of the five stages below is a REQUIRED, explicit PEP 249 step --
# => no step is implicit, and skipping any of them either fails or leaks a resource.

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => STAGE 1: connect()
    # => conn is now a live Connection -- the context manager guarantees conn.close() runs
    conn.execute("CREATE TABLE events(id INTEGER PRIMARY KEY, name TEXT)")  # => schema setup
    conn.execute("INSERT INTO events(id, name) VALUES (1, 'startup'), (2, 'shutdown')")
    conn.commit()  # => makes both seed rows durable/visible to the cursor below

    cur = conn.cursor()  # => STAGE 2: cursor() -- the object every subsequent statement runs through
    assert isinstance(cur, sqlite3.Cursor)  # => a real Cursor object, not a bare function call

    cur.execute("SELECT id, name FROM events ORDER BY id")  # => STAGE 3: execute() -- runs the SQL
    # => execute() does NOT return rows itself -- it only prepares the cursor to be fetched from

    first_row = cur.fetchone()  # => STAGE 4a: fetchone() -- pulls exactly ONE row at a time
    remaining_rows = cur.fetchall()  # => STAGE 4b: fetchall() -- pulls every REMAINING row
    print(first_row, remaining_rows)  # => Output: (1, 'startup') [(2, 'shutdown')]
    # => fetchone() consumed row 1; fetchall() then only had row 2 left to return

    cur.close()  # => STAGE 5: cursor.close() -- releases the cursor BEFORE the connection closes
    assert cur.connection is conn  # => the cursor always remembers which connection it belongs to
# => STAGE 6 (implicit, via the context manager): conn.close() runs here, on exiting the `with`
# => without contextlib.closing, an unclosed Connection now emits a ResourceWarning on GC
