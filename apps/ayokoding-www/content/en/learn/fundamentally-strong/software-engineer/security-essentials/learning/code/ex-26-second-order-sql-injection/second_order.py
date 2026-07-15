# learning/code/ex-26-second-order-sql-injection/second_order.py
"""Example 26: Second-Order SQL Injection."""  # => co-03: module docstring

from __future__ import (
    annotations,
)  # => co-03: DD-39 hygiene, unrelated to the exploit itself

import sqlite3  # => co-03: stdlib DB driver -- the FIRST write is safe, the SECOND read-then-query is not


def seed_database(
    conn: sqlite3.Connection,
) -> None:  # => co-03: two tables -- one public, one an admin-only secret
    """Create a users table and a separate admin_secrets table."""  # => co-03: doc
    conn.execute(
        "CREATE TABLE users (id INTEGER, display_name TEXT)"
    )  # => co-03: display_name is USER-CHOSEN text
    conn.execute(
        "CREATE TABLE admin_secrets (secret TEXT)"
    )  # => co-01: never meant to be reachable from a users query
    conn.execute(
        "INSERT INTO admin_secrets VALUES ('TOP-SECRET-VALUE')"
    )  # => co-01: the exfil target
    conn.commit()  # => co-03: persists both tables before any registration/report runs


def register_user(
    conn: sqlite3.Connection, user_id: int, display_name: str
) -> None:  # => co-03: the FIRST, SAFE write
    """Store a new user's display name -- SAFE, uses a parameterized INSERT."""  # => co-03: doc
    conn.execute(  # => co-03: bound parameters -- display_name can NEVER become SQL syntax at THIS step
        "INSERT INTO users (id, display_name) VALUES (?, ?)",
        (user_id, display_name),  # => co-01: tainted at input, SAFE here
    )  # => co-03: end of the parameterized INSERT
    conn.commit()  # => co-03: the payload is now PERSISTED, exactly as typed, byte for byte


def build_activity_report_naive(
    conn: sqlite3.Connection, user_id: int
) -> list[tuple[str]]:  # => co-03: the SECOND, UNSAFE use
    """Build a report query with an f-string using a STORED value -- VULNERABLE, do not copy."""  # => co-03: doc
    row = conn.execute(
        "SELECT display_name FROM users WHERE id = ?", (user_id,)
    ).fetchone()  # => co-03: SAFE read, id is bound
    stored_name = row[
        0
    ]  # => co-01: the value LOOKS like "our own data" -- it is still attacker-chosen text
    query = f"SELECT display_name FROM users WHERE display_name = '{stored_name}'"  # => co-03: f-string on a STORED value
    print(
        f"QUERY: {query}"
    )  # => co-03: prints the ACTUAL second-stage query -- shows the payload firing HERE, not at insert
    return conn.execute(
        query
    ).fetchall()  # => co-03: executes the now-attacker-controlled second query


def build_activity_report_fixed(
    conn: sqlite3.Connection, user_id: int
) -> list[tuple[str]]:  # => co-03: the FIXED second use
    """Build a report query with a bound parameter for the STORED value -- FIXED."""  # => co-03: doc
    row = conn.execute(
        "SELECT display_name FROM users WHERE id = ?", (user_id,)
    ).fetchone()  # => co-03: SAFE read, id is bound
    stored_name = row[
        0
    ]  # => co-03: the SAME stored value as the naive version -- only the SECOND query changes
    query = "SELECT display_name FROM users WHERE display_name = ?"  # => co-03: bound parameter, NO f-string, second time too
    print(
        f"QUERY: {query}  PARAM: {stored_name!r}"
    )  # => co-03: shows the whole stored value travels as ONE opaque value
    return conn.execute(
        query, (stored_name,)
    ).fetchall()  # => co-03: driver binds it -- can never become SQL syntax


if (
    __name__ == "__main__"
):  # => co-03: entry point -- safe write, unsafe second use, then the fix on BOTH paths
    conn = sqlite3.connect(
        ":memory:"
    )  # => co-03: throwaway in-process DB, self-contained per-run
    seed_database(conn)  # => co-03: creates users + the secret admin_secrets table

    payload = "x' UNION SELECT secret FROM admin_secrets -- "  # => co-01: designed to fire on the SECOND query, not the first
    print(
        "=== Step 1: registration, via a parameterized INSERT (SAFE) ==="
    )  # => co-03: the first, safe write
    register_user(
        conn, 1, payload
    )  # => co-03: stored EXACTLY as typed -- no injection happens at THIS step
    print(
        "registration completed with no error -- the payload is stored, inert, in the users table"
    )  # => co-03: no crash yet

    print(
        "\n=== Step 2: VULNERABLE report -- fires on the SECOND, later use ==="
    )  # => co-03: the second-order fire
    leaked = build_activity_report_naive(
        conn, 1
    )  # => co-01: the STORED payload now reaches an f-string query
    print(
        f"LEAKED ROWS: {leaked}"
    )  # => co-03: admin_secrets' contents, leaked through a users-table query

    print(
        "\n=== Step 3: FIXED report -- parameterizing the SECOND query too ==="
    )  # => co-03: re-run against the fix
    safe_result = build_activity_report_fixed(
        conn, 1
    )  # => co-01: the SAME stored payload, now inert at the SECOND step
    print(
        f"RESULT: {safe_result}"
    )  # => co-03: the payload string itself, treated as a literal, non-matching value
