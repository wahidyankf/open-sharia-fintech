# learning/code/ex-05-sql-injection-union-data-exfil/union_search.py
"""Example 5: SQL Injection -- UNION Data Exfiltration."""  # => co-03: module docstring

from __future__ import (
    annotations,
)  # => co-03: DD-39 hygiene, unrelated to the exploit itself

import sqlite3  # => co-03: stdlib DB driver -- both the vulnerable AND fixed search reuse this schema


def seed_database(
    conn: sqlite3.Connection,
) -> None:  # => co-03: TWO tables -- one public, one secret
    """Create a public products table and a separate, sensitive users table."""  # => co-03: doc
    conn.execute(
        "CREATE TABLE products (name TEXT, price TEXT)"
    )  # => co-03: the table the search UI exposes
    conn.execute(
        "INSERT INTO products VALUES ('Widget', '9.99')"
    )  # => co-03: public row #1
    conn.execute(
        "INSERT INTO products VALUES ('Gadget', '19.99')"
    )  # => co-03: public row #2
    conn.execute(
        "CREATE TABLE users (username TEXT, password TEXT)"
    )  # => co-01: the table NEVER meant to be exposed
    conn.execute(
        "INSERT INTO users VALUES ('alice', 's3cret-pw')"
    )  # => co-01: secret row #1 -- the exfil target
    conn.execute(
        "INSERT INTO users VALUES ('bob', 'hunter2')"
    )  # => co-01: secret row #2 -- the exfil target
    conn.commit()  # => co-03: persists all four rows before any search runs


# ex-05: a search box concatenates the search term straight into a LIKE clause --
# same column COUNT (2) in both tables is what makes a UNION SELECT syntactically legal
def naive_search(
    conn: sqlite3.Connection, term: str
) -> list[tuple[str, str]]:  # => co-03: the vulnerable handler
    """Search products by name -- VULNERABLE, builds the query with an f-string."""  # => co-03: doc
    query = f"SELECT name, price FROM products WHERE name LIKE '%{term}%'"  # => co-01: term is tainted input
    print(
        f"QUERY: {query}"
    )  # => co-03: prints the ACTUAL query -- shows the UNION splice landing inside LIKE
    return conn.execute(
        query
    ).fetchall()  # => co-03: executes the attacker-controlled query as-is


def parameterized_search(
    conn: sqlite3.Connection, term: str
) -> list[tuple[str, str]]:  # => co-03: the FIXED handler
    """Search products by name -- FIXED, the LIKE pattern is a bound parameter."""  # => co-03: doc
    like_pattern = f"%{term}%"  # => co-03: the wildcard wrapping happens in PYTHON, not in SQL text
    query = "SELECT name, price FROM products WHERE name LIKE ?"  # => co-03: NO f-string in the query text
    print(
        f"QUERY: {query}  PARAM: {like_pattern!r}"
    )  # => co-03: shows the whole payload travels as ONE opaque value
    return conn.execute(
        query, (like_pattern,)
    ).fetchall()  # => co-03: driver binds it -- can never become SQL syntax


UNION_PAYLOAD = "zzz' UNION SELECT username, password FROM users -- "  # => co-01: closes LIKE, unions in the secret table


if (
    __name__ == "__main__"
):  # => co-03: entry point -- normal search, then the exploit, then the fix
    conn = sqlite3.connect(
        ":memory:"
    )  # => co-03: throwaway in-process DB, self-contained per-run
    seed_database(conn)  # => co-03: creates products + the secret users table

    print(
        "=== VULNERABLE: normal search ==="
    )  # => co-03: sanity check -- the naive search works normally
    print(
        naive_search(conn, "Widget")
    )  # => co-03: [('Widget', '9.99')] -- correct, unremarkable result

    print("\n=== VULNERABLE: UNION SELECT exfiltration ===")  # => co-03: the attack
    leaked = naive_search(
        conn, UNION_PAYLOAD
    )  # => co-01: attacker-supplied search term carries the UNION
    print(
        f"LEAKED ROWS: {leaked}"
    )  # => co-03: the users table's usernames AND passwords, printed verbatim

    print(
        "\n=== FIXED: same payload against the parameterized search ==="
    )  # => co-03: re-run against the fix
    safe_result = parameterized_search(
        conn, UNION_PAYLOAD
    )  # => co-01: the SAME string, now inert
    print(
        f"RESULT: {safe_result}"
    )  # => co-03: [] -- no product NAME literally contains the whole payload text
