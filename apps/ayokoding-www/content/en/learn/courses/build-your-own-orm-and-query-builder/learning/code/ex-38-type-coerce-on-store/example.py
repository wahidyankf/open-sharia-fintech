"""Example 38: Coerce bool and date Back to Driver-Native Types on Store."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import datetime  # => date.isoformat() is the coercion target for storing
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


def coerce_bool_on_store(value: bool) -> int:  # => co-12: reverse of Example 36
    return 1 if value else 0  # => SQLite has no bool storage class -- store its INTEGER equivalent


def coerce_date_on_store(value: datetime.date) -> str:  # => co-12: reverse of Example 37
    return value.isoformat()  # => SQLite has no date storage class -- store its ISO TEXT equivalent


is_active = True  # => a Python bool the domain object carries
placed_on = datetime.date(2026, 3, 1)  # => a Python date the domain object carries
stored_active = coerce_bool_on_store(is_active)  # => coerced BEFORE it ever reaches the driver
stored_date = coerce_date_on_store(placed_on)  # => same coercion pattern, different type pair
assert stored_active == 1 and isinstance(stored_active, int)  # => a plain int, driver-native
assert stored_date == "2026-03-01" and isinstance(stored_date, str)  # => a plain str, driver-native

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, is_active INTEGER, placed_on TEXT)")  # => real table
    conn.execute("INSERT INTO orders VALUES (?, ?, ?)", (1, stored_active, stored_date))  # => co-02: parameterized
    conn.commit()  # => makes the coerced-and-stored row visible
    row = conn.execute("SELECT is_active, placed_on FROM orders WHERE id = 1").fetchone()  # => reads it back raw
    print(row)  # => Output: (1, '2026-03-01')
