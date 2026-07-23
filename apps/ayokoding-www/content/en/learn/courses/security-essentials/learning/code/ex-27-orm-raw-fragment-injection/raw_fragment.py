# learning/code/ex-27-orm-raw-fragment-injection/raw_fragment.py
"""Example 27: ORM Raw-Fragment Injection -- sqlite3 stands in for an ORM's text() escape hatch."""  # => co-03/co-21: docstring

from __future__ import (
    annotations,
)  # => co-03: DD-39 hygiene, unrelated to the exploit itself

import sqlite3  # => co-03: stands in for an ORM's raw-execute escape hatch -- see the markdown prose for the honest substitution note


def seed_database(
    conn: sqlite3.Connection,
) -> None:  # => co-03: a public catalog table + a separate admin secret
    """Create a products table and a separate admin_secrets table."""  # => co-03: doc
    conn.execute(
        "CREATE TABLE products (name TEXT, category TEXT)"
    )  # => co-03: the table a category filter searches
    conn.execute(
        "INSERT INTO products VALUES ('Widget', 'tools')"
    )  # => co-03: public row #1
    conn.execute(
        "INSERT INTO products VALUES ('Gadget', 'electronics')"
    )  # => co-03: public row #2
    conn.execute(
        "CREATE TABLE admin_secrets (secret TEXT)"
    )  # => co-01: never meant to be reachable from a category filter
    conn.execute(
        "INSERT INTO admin_secrets VALUES ('TOP-SECRET-VALUE')"
    )  # => co-01: the exfil target
    conn.commit()  # => co-03: persists all rows before any filter runs


def naive_category_filter(
    conn: sqlite3.Connection, category: str
) -> list[tuple[str]]:  # => co-03: the vulnerable "ORM" call
    """Filter products by category, building a raw SQL fragment via string concatenation -- VULNERABLE."""  # => co-03: doc
    raw_fragment = f"category = '{category}'"  # => co-01: the exact anti-pattern -- a WHERE fragment built by hand
    query = f"SELECT name FROM products WHERE {raw_fragment}"  # => co-03: the fragment is spliced into the full query
    print(
        f"QUERY: {query}"
    )  # => co-03: prints the ACTUAL query -- stands in for text()'s compiled SQL string
    return conn.execute(
        query
    ).fetchall()  # => co-03: executes the attacker-controlled fragment as-is


def fixed_category_filter(
    conn: sqlite3.Connection, category: str
) -> list[tuple[str]]:  # => co-03: the FIXED "ORM" call
    """Filter products by category using a named bound parameter -- FIXED, mirrors ORM text() bindparams."""  # => co-03: doc
    query = "SELECT name FROM products WHERE category = :category"  # => co-03: named placeholder, NO string interpolation
    print(
        f"QUERY: {query}  PARAMS: {{'category': {category!r}}}"
    )  # => co-03: shows the value travels SEPARATELY from SQL text
    return conn.execute(
        query, {"category": category}
    ).fetchall()  # => co-03: driver binds it -- can never become SQL syntax


if (
    __name__ == "__main__"
):  # => co-03: entry point -- normal filter, then the exploit, then the fix
    conn = sqlite3.connect(
        ":memory:"
    )  # => co-03: throwaway in-process DB, self-contained per-run
    seed_database(conn)  # => co-03: creates products + the secret admin_secrets table

    print(
        "=== VULNERABLE: normal category filter ==="
    )  # => co-03: sanity check -- the naive filter works normally
    print(
        naive_category_filter(conn, "tools")
    )  # => co-03: [('Widget',)] -- correct, unremarkable result

    print(
        "\n=== VULNERABLE: UNION SELECT through the raw fragment ==="
    )  # => co-03: the attack
    payload = "nope' UNION SELECT secret FROM admin_secrets -- "  # => co-01: closes the fragment's quote, unions in the secret
    leaked = naive_category_filter(
        conn, payload
    )  # => co-01: attacker-supplied category carries the UNION
    print(
        f"LEAKED ROWS: {leaked}"
    )  # => co-03: admin_secrets' contents, leaked through a products-table filter

    print(
        "\n=== FIXED: same payload against the named-bound-parameter filter ==="
    )  # => co-03: re-run against the fix
    safe_result = fixed_category_filter(
        conn, payload
    )  # => co-01: the SAME string, now inert
    print(
        f"RESULT: {safe_result}"
    )  # => co-03: [] -- no product category literally equals the whole payload text
