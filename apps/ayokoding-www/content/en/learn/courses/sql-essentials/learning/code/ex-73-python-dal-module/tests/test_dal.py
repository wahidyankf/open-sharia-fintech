"""Example 73: pytest coverage for dal.py against a seeded, in-memory fixture DB."""

import sqlite3  # => stdlib DB-API module -- only needed here to type the fixture's connection
from collections.abc import Iterator  # => types the fixture's generator return

import pytest  # => the testing framework -- provides the @pytest.fixture decorator below

# tests/__init__.py makes THIS directory a package, so pytest inserts the PARENT dir (the
# example's root) into sys.path -- that is what makes `from dal import ...` resolve at all.
from dal import (  # => imports the module UNDER TEST
    create_schema,  # => builds the schema -- called once per test, via the fixture below
    delete_author,  # => the "D" in CRUD -- covered by test_delete_author
    get_author,  # => the "R" in CRUD -- covered by every test below
    insert_author,  # => the "C" in CRUD -- covered by every test below
    list_authors,  # => a bulk read -- covered by test_list_authors_returns_every_row
    update_author_name,  # => the "U" in CRUD -- covered by test_update_author_name
)  # => closes the import list -- all five dal.py functions under test in this file


@pytest.fixture  # => runs before EVERY test function below, fresh each time
def conn() -> Iterator[
    sqlite3.Connection
]:  # => Iterator, not Connection -- this is a generator
    # A FRESH in-memory DB per test -- no test can see another test's leftover rows.
    connection: sqlite3.Connection = sqlite3.connect(
        ":memory:"
    )  # => a throwaway, per-test DB
    create_schema(
        connection
    )  # => builds the ONE table every test below reads and writes
    yield connection  # => hands the ready connection to the test function below
    connection.close()  # => runs AFTER the test, whether it passed or failed


def test_insert_and_get_author(
    conn: sqlite3.Connection,
) -> None:  # => covers insert + get
    author_id: int = insert_author(
        conn, "Ada Lovelace"
    )  # => the function under test, first call
    assert get_author(conn, author_id) == (
        author_id,
        "Ada Lovelace",
    )  # => round-trips correctly


def test_list_authors_returns_every_row(
    conn: sqlite3.Connection,
) -> None:  # => covers the bulk read
    insert_author(conn, "Ada Lovelace")  # => row 1
    insert_author(conn, "Grace Hopper")  # => row 2
    assert list_authors(conn) == [
        (1, "Ada Lovelace"),
        (2, "Grace Hopper"),
    ]  # => both, in order


def test_update_author_name(
    conn: sqlite3.Connection,
) -> None:  # => covers the "U" in CRUD
    author_id: int = insert_author(conn, "Ada")  # => an initial, incomplete name
    update_author_name(conn, author_id, "Ada Lovelace")  # => the function under test
    assert get_author(conn, author_id) == (
        author_id,
        "Ada Lovelace",
    )  # => the UPDATE persisted


def test_delete_author(conn: sqlite3.Connection) -> None:  # => covers the "D" in CRUD
    author_id: int = insert_author(conn, "Ada Lovelace")  # => the row this test deletes
    delete_author(conn, author_id)  # => the function under test
    assert (
        get_author(conn, author_id) is None
    )  # => the row is genuinely gone, not just renamed
