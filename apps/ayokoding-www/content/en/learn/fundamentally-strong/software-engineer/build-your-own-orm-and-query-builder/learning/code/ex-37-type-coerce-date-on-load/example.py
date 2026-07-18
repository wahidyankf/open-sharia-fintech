"""Example 37: Coerce an ISO String to a date on Load."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import datetime  # => date.fromisoformat() is the coercion target
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


def coerce_date_on_load(raw: str) -> datetime.date:  # => co-12: SQLite has NO native date type
    return datetime.date.fromisoformat(raw)  # => the driver hands back a plain str, e.g. "2026-01-15"


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, placed_on TEXT)")  # => TEXT, not DATE
    conn.execute("INSERT INTO orders VALUES (1, '2026-01-15')")  # => stored as a plain ISO string
    conn.commit()  # => makes the seed row visible
    raw_date = conn.execute("SELECT placed_on FROM orders WHERE id = 1").fetchone()[0]  # => the RAW driver value
    assert isinstance(raw_date, str)  # => confirms it's still just text, not a date object
    coerced = coerce_date_on_load(raw_date)  # => THIS is the coercion step
    assert isinstance(coerced, datetime.date)  # => a REAL date object now
    assert coerced == datetime.date(2026, 1, 15)  # => the exact calendar date, correctly parsed
    print(coerced)  # => Output: 2026-01-15
