# learning/code/ex-13-plaintext-password-store-is-broken/plaintext_store.py
"""Example 13: Plaintext Password Store Is Broken."""  # => co-09: module docstring

from __future__ import (
    annotations,
)  # => co-09: DD-39 hygiene, unrelated to the exploit itself

import sqlite3  # => co-09: stdlib DB driver -- the schema below stores passwords AS-ENTERED


def seed_database(
    conn: sqlite3.Connection,
) -> None:  # => co-09: three accounts, each with a REAL plaintext password
    """Create a users table that stores passwords in plaintext -- VULNERABLE, do not copy."""  # => co-09: doc
    conn.execute(
        "CREATE TABLE users (username TEXT, password TEXT)"
    )  # => co-09: 'password' column holds RAW text
    conn.execute(
        "INSERT INTO users VALUES ('alice', 'Summer2026!')"
    )  # => co-09: user #1's REAL password, verbatim
    conn.execute(
        "INSERT INTO users VALUES ('bob', 'hunter2')"
    )  # => co-09: user #2's REAL password, verbatim
    conn.execute(
        "INSERT INTO users VALUES ('carol', 'correct-horse-battery')"
    )  # => co-09: user #3's REAL password
    conn.commit()  # => co-09: persists all three rows before the dump below reads them back


def dump_all_passwords(
    conn: sqlite3.Connection,
) -> list[tuple[str, str]]:  # => co-09: the read this example proves is unsafe
    """Read every username/password pair straight out of the table -- no transformation at all."""  # => co-09: doc
    return conn.execute(
        "SELECT username, password FROM users"
    ).fetchall()  # => co-09: whatever was stored comes back AS-IS


if (
    __name__ == "__main__"
):  # => co-09: entry point -- seed, then dump, then show every password in the clear
    conn = sqlite3.connect(
        ":memory:"
    )  # => co-09: throwaway in-process DB, self-contained per-run
    seed_database(conn)  # => co-09: creates and seeds three plaintext-password accounts

    print(
        "=== Dumping the users table (a leaked backup, a compromised DB, a careless SELECT *) ==="
    )  # => co-09: scenario
    rows = dump_all_passwords(
        conn
    )  # => co-09: a single read is ALL that is needed to see every password
    for (
        username,
        password,
    ) in rows:  # => co-09: one line per account -- nothing to crack, nothing to decode
        print(
            f"{username:<8} password={password}"
        )  # => co-09: printed VERBATIM, exactly as the user typed it

    all_visible = (
        all(  # => co-09: mechanically confirms EVERY row is exposed, not just a sample
            password
            in {
                "Summer2026!",
                "hunter2",
                "correct-horse-battery",
            }  # => co-09: the real passwords, unchanged
            for _, password in rows  # => co-09: checked against every dumped row
        )
    )  # => co-09: end of the all() check
    print(
        f"\nevery password recovered with zero effort: {all_visible}"
    )  # => co-09: True -- no attack needed at all
