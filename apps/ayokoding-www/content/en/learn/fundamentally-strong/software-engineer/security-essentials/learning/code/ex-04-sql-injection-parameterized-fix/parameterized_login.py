# learning/code/ex-04-sql-injection-parameterized-fix/parameterized_login.py
"""Example 4: SQL Injection -- Parameterized Fix."""  # => co-03: module docstring

from __future__ import (
    annotations,
)  # => co-03: DD-39 hygiene, unrelated to the fix itself

import sqlite3  # => co-03: same stdlib driver as Example 3 -- ONLY the query-building style changes


def seed_database(
    conn: sqlite3.Connection,
) -> None:  # => co-03: identical seed data to Example 3
    """Create a users table with exactly one legitimate account."""  # => co-03: doc
    conn.execute(
        "CREATE TABLE users (username TEXT, password TEXT)"
    )  # => co-03: same schema as Example 3
    conn.execute(
        "INSERT INTO users VALUES ('alice', 's3cret-pw')"
    )  # => co-03: the SAME only valid pair
    conn.commit()  # => co-03: persists the seed row before any login attempt runs


# ex-04: the FIX -- username and password are passed as a SEPARATE parameter
# tuple, never concatenated into the query text itself, closing the co-03 boundary
def parameterized_login(
    conn: sqlite3.Connection, username: str, password: str
) -> bool:  # => co-03: the fixed handler
    """Log in using a bound `?` placeholder query -- SQL text and data travel separately."""  # => doc
    query = "SELECT username FROM users WHERE username = ? AND password = ?"  # => co-03: NO f-string, ever
    print(
        f"QUERY: {query}  PARAMS: {(username, password)!r}"
    )  # => co-03: shows text and data are SEPARATE
    row = conn.execute(
        query, (username, password)
    ).fetchone()  # => co-03: driver binds params, never text-splices
    return (
        row is not None
    )  # => co-03: True means "logged in" -- a single matching row was found


if (
    __name__ == "__main__"
):  # => co-03: entry point -- re-runs BOTH Example 3 scenarios against the fix
    conn = sqlite3.connect(
        ":memory:"
    )  # => co-03: throwaway in-process DB, self-contained per-run
    seed_database(
        conn
    )  # => co-03: creates and seeds the one legitimate 'alice' account

    print(
        "=== Legitimate login (correct password) ==="
    )  # => co-03: the fix must NOT break real logins
    ok = parameterized_login(
        conn, "alice", "s3cret-pw"
    )  # => co-03: correct username AND correct password
    print(
        f"login success: {ok}"
    )  # => co-03: True -- the fix still authenticates real users

    print(
        "\n=== Same attacker payload as Example 3: ' OR '1'='1 ==="
    )  # => co-03: THE SAME payload, unchanged
    payload_username = (
        "alice' OR '1'='1"  # => co-03: identical string to Example 3's exploit
    )
    blocked = parameterized_login(
        conn, payload_username, "totally-wrong-password"
    )  # => co-01: attacker input, now inert
    print(
        f"login success: {blocked}"
    )  # => co-03: False -- the payload is now just a literal, non-matching string
