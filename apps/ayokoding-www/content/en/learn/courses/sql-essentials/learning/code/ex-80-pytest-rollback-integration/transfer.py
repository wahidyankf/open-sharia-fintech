# pyright: strict
"""Example 80: transfer.py -- a transaction that rolls back when a CHECK constraint fails."""

import sqlite3  # => stdlib DB-API module (co-19)


def create_schema(
    conn: sqlite3.Connection,
) -> None:  # => called once per test, in the fixture
    # CHECK(balance >= 0) is the ENGINE-enforced invariant this example deliberately trips.
    conn.executescript(  # => raw DDL -- no placeholders needed for schema statements
        """
        -- a single-table ledger -- just enough to demonstrate a rolled-back transfer
        CREATE TABLE account(  -- => the ledger this whole test suite exercises
            id INTEGER PRIMARY KEY,           -- => aliases rowid (co-02)
            name TEXT NOT NULL,               -- => a human-readable label, not used for logic
            balance REAL NOT NULL CHECK (balance >= 0)
                                                -- => co-04 -- the engine itself rejects a negative balance
        );
        """
    )  # => one CHECK constraint is the ENTIRE mechanism this example's rollback relies on


def transfer(
    conn: sqlite3.Connection, from_id: int, to_id: int, amount: float
) -> None:  # co-18
    # `with conn:` opens an implicit transaction on the FIRST write below, commits on a clean
    # exit, and auto-ROLLBACKs the whole block if ANY statement inside raises (co-18).
    with conn:  # => the transaction boundary -- everything inside is all-or-nothing
        conn.execute(  # => the FIRST write -- opens the implicit transaction
            "UPDATE account SET balance = balance - ? WHERE id = ?",  # => the debit leg
            (amount, from_id),  # => if this drives balance negative, CHECK fails HERE
        )  # => the credit below never runs if this statement raises
        conn.execute(  # => the SECOND write -- only reached if the debit above succeeded
            "UPDATE account SET balance = balance + ? WHERE id = ?",  # => the credit leg
            (
                amount,
                to_id,
            ),  # => co-20 -- every value above is bound, never string-interpolated
        )  # => both legs commit TOGETHER when the with block exits cleanly
