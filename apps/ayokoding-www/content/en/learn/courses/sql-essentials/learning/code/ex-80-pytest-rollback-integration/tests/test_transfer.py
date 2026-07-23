"""Example 80: pytest integration test -- a failing transfer leaves the DB unchanged."""

import sqlite3  # => stdlib DB-API module -- only needed here to type the fixture's connection
from collections.abc import Iterator  # => types the fixture's generator return

import pytest  # => the testing framework -- provides @pytest.fixture and pytest.raises below

# tests/__init__.py makes THIS directory a package, so pytest inserts the PARENT dir (the
# example's root) into sys.path -- that is what makes `from transfer import ...` resolve at all.
from transfer import create_schema, transfer  # => imports the module UNDER TEST


@pytest.fixture  # => runs before EVERY test function below, fresh each time
def conn() -> Iterator[
    sqlite3.Connection
]:  # => Iterator, not Connection -- this is a generator
    connection: sqlite3.Connection = sqlite3.connect(
        ":memory:"
    )  # => a throwaway, per-test DB
    create_schema(connection)  # => builds the ONE table both tests below read and write
    connection.execute(  # => a direct execute, not the transfer() function -- just seeding
        "INSERT INTO account(id, name, balance) VALUES (1, 'checking', 100.0), (2, 'savings', 50.0)"  # seed
        # => two seeded accounts -- checking starts with exactly 100.0, savings with 50.0
    )
    connection.commit()  # => persists the seed before either test's transfer() call runs
    yield connection  # => hands the ready connection to the test function below
    connection.close()  # => runs AFTER the test, whether it passed or failed


def test_transfer_commits_on_success(
    conn: sqlite3.Connection,
) -> None:  # => co-18's happy path
    transfer(
        conn, 1, 2, 30.0
    )  # => the function under test -- a valid, affordable transfer
    rows: list[tuple[int, float]] = (
        conn.execute(  # => re-reads BOTH accounts, post-transfer
            "SELECT id, balance FROM account ORDER BY id"  # => ordered so the assertion is deterministic
        ).fetchall()
    )  # => reads BOTH accounts back, in id order
    assert rows == [
        (1, 70.0),
        (2, 80.0),
    ]  # => both legs landed together -- co-18's happy path


def test_failed_transfer_leaves_db_unchanged(
    conn: sqlite3.Connection,
) -> None:  # => the ROLLBACK path
    before: list[tuple[int, float]] = (
        conn.execute(  # => the pre-failure snapshot, read FIRST
            "SELECT id, balance FROM account ORDER BY id"
        ).fetchall()
    )  # => captured BEFORE the failing call -- the baseline this test proves is preserved

    # 1000.0 exceeds checking's 100.0 balance -- the debit alone would violate CHECK(balance >= 0).
    with pytest.raises(
        sqlite3.IntegrityError
    ):  # => asserts the CHECK violation actually fires
        transfer(
            conn, 1, 2, 1000.0
        )  # => `with conn:` inside transfer() auto-rolls-back on failure

    after: list[tuple[int, float]] = (
        conn.execute(  # => the post-failure snapshot, read SECOND
            "SELECT id, balance FROM account ORDER BY id"
        ).fetchall()
    )  # => re-reads BOTH accounts, AFTER the failed call
    assert (
        before == after
    )  # => the failed debit never persisted -- balances are BIT-for-bit identical
    count: int = conn.execute("SELECT count(*) FROM account").fetchone()[
        0
    ]  # co-19 scalar read
    # => a SEPARATE, independent check -- row count, not just balance values
    assert (
        count == 2
    )  # => row COUNT is unchanged too -- no half-applied transfer left a trace
