# pyright: strict
"""Example 73: A Typed Data-Access-Layer Module -- Parameterized CRUD."""

import sqlite3  # => stdlib DB-API module (co-19) -- no third-party driver anywhere in this file


def create_schema(
    conn: sqlite3.Connection,
) -> None:  # => called once per test, in the fixture
    # Every function in this module takes an ALREADY-OPEN connection -- callers (including
    # tests) control the connection's lifetime, this module never opens or closes one itself.
    conn.executescript(  # => executescript, not execute -- runs raw DDL, no placeholders needed
        "CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);"  # => single DDL statement
    )  # => the ONLY table this module manages -- a minimal fixture for CRUD demonstration


def insert_author(conn: sqlite3.Connection, name: str) -> int:  # => the "C" in CRUD
    # `?` (qmark) parameterization -- name is BOUND, never string-interpolated (co-20).
    cur: sqlite3.Cursor = conn.execute(  # => returns a Cursor -- lastrowid is read off it below
        "INSERT INTO author(name) VALUES (?)",  # => one placeholder, one bound value
        (
            name,
        ),  # => a 1-tuple -- the trailing comma is REQUIRED for a single-element tuple
    )
    conn.commit()  # => persists the insert before returning the new row's id to the caller
    new_id: int | None = cur.lastrowid  # => the rowid SQLite just assigned (co-02)
    assert (
        new_id is not None
    )  # => narrows int | None to int -- always set right after an INSERT
    return (
        new_id  # => the caller uses this id for every follow-up get/update/delete call
    )


def get_author(
    conn: sqlite3.Connection, author_id: int
) -> tuple[int, str] | None:  # "R" in CRUD
    cur: sqlite3.Cursor = (
        conn.execute(  # => a read -- no conn.commit() needed for a SELECT
            "SELECT id, name FROM author WHERE id = ?",  # => a single bound parameter
            (author_id,),  # => co-20 again, this time for a lookup, not an insert
        )
    )
    row: tuple[int, str] | None = (
        cur.fetchone()
    )  # => None if no row matched the given id
    return row  # => the caller must handle the None case -- pyright enforces this via the type


def list_authors(
    conn: sqlite3.Connection,
) -> list[tuple[int, str]]:  # => reads EVERY row
    cur: sqlite3.Cursor = conn.execute(
        "SELECT id, name FROM author ORDER BY id"
    )  # => the bulk read
    # => no WHERE clause -- every row, oldest id first
    return (
        cur.fetchall()
    )  # => every row by this ONE call -- no filter needed for a full listing


def update_author_name(
    conn: sqlite3.Connection, author_id: int, new_name: str
) -> None:  # "U"
    conn.execute(  # => a write -- conn.commit() below persists it
        "UPDATE author SET name = ? WHERE id = ?",  # => TWO placeholders -- order matters below
        (new_name, author_id),  # => the SAME order as the ?s in the SQL text (co-20)
    )
    conn.commit()  # => this module commits eagerly -- no long-lived open transaction to forget


def delete_author(
    conn: sqlite3.Connection, author_id: int
) -> None:  # => the "D" in CRUD
    conn.execute("DELETE FROM author WHERE id = ?", (author_id,))
    # => DELETE ... WHERE with a bound id -- co-20 once more, no string interpolation anywhere
    conn.commit()  # => a no-op commit if author_id didn't exist -- DELETE ... WHERE is safe to repeat
