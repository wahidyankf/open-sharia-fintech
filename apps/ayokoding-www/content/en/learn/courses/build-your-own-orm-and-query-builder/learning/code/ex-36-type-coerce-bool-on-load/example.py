"""Example 36: Coerce a Driver 0/1 Integer to a Python bool on Load."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


def coerce_bool_on_load(raw: int) -> bool:  # => co-12: SQLite has NO native boolean type
    return raw != 0  # => the driver hands back a plain int -- 0 or 1 -- never a real bool


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, is_active INTEGER)")  # => INTEGER, not BOOLEAN
    conn.execute("INSERT INTO users VALUES (1, 1), (2, 0)")  # => stored as raw 1 and 0
    conn.commit()  # => makes both seed rows visible
    raw_active = conn.execute("SELECT is_active FROM users WHERE id = 1").fetchone()[0]  # => the RAW driver value
    raw_inactive = conn.execute("SELECT is_active FROM users WHERE id = 2").fetchone()[0]  # => also raw
    assert isinstance(raw_active, int) and not isinstance(raw_active, bool)  # => confirms it's a plain int
    coerced_active = coerce_bool_on_load(raw_active)  # => THIS is the coercion step
    coerced_inactive = coerce_bool_on_load(raw_inactive)  # => coerces the second row too
    assert coerced_active is True  # => a REAL Python bool now, not an int that happens to equal 1
    assert coerced_inactive is False  # => and a real False for the 0 row
    print(coerced_active, coerced_inactive)  # => Output: True False
