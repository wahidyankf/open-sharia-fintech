"""Example 64: A Test Against the App with a Real Temporary Database (SQLite File)."""
# Every test below opens a GENUINE SQLite file under pytest's own tmp_path -- never ":memory:"
# and never a mocked connection -- so the write-then-read round trip proves something real.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

import sqlite3  # => co-23: a REAL, file-backed database engine -- part of the stdlib  # fmt: skip
from collections.abc import Iterator  # => types the fixture's generator return below  # fmt: skip
from pathlib import Path  # => types the real filesystem path the fixture hands out  # fmt: skip

import pytest  # => co-05: provides the tmp_path fixture this example builds on  # fmt: skip


class NoteRepository:  # => co-23/co-25: talks to a REAL SQLite file, not an in-memory fake  # fmt: skip
    """A tiny repository backed by a genuine SQLite database file on disk."""  # => co-23

    def __init__(self, db_path: Path) -> None:  # => opens the connection at construction time  # fmt: skip
        self.conn = sqlite3.connect(db_path)  # => a REAL file-backed connection, not ":memory:"  # fmt: skip
        self.conn.execute(  # => creates the REAL table this repository reads/writes  # fmt: skip
            "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT NOT NULL)"
        )
        self.conn.commit()  # => the schema is now genuinely persisted to the temp file  # fmt: skip

    def add(self, text: str) -> int:  # => co-23: a REAL INSERT, returns the new row's id  # fmt: skip
        cursor = self.conn.execute("INSERT INTO notes (text) VALUES (?)", (text,))  # => real write  # fmt: skip
        self.conn.commit()  # => flushes the write to the REAL file on disk  # fmt: skip
        assert cursor.lastrowid is not None  # => narrows int | None for the type checker  # fmt: skip
        return cursor.lastrowid  # => co-23: the REAL id SQLite assigned to this row  # fmt: skip

    def get(
        self, note_id: int
    ) -> str | None:  # => co-23: a REAL SELECT, reading back what add() wrote
        row = self.conn.execute(
            "SELECT text FROM notes WHERE id = ?", (note_id,)
        ).fetchone()  # => real read
        return row[0] if row else None  # => None only if genuinely absent, not a mocked default  # fmt: skip

    def close(self) -> None:  # => releases the real file handle  # fmt: skip
        self.conn.close()  # => co-23: a REAL close(), not a no-op on a mock  # fmt: skip


@pytest.fixture
def db_path(tmp_path: Path) -> Iterator[Path]:  # => co-05/co-25: pytest's OWN real-temp-dir fixture  # fmt: skip
    path = tmp_path / "notes.db"  # => a genuine file path on the real filesystem, not a mock path  # fmt: skip
    yield path  # => hands the path to the test -- pytest deletes tmp_path's whole tree afterward  # fmt: skip


def test_integration_write_then_read_round_trips(
    db_path: Path,
) -> None:  # => co-23: app + REAL db
    repo = NoteRepository(db_path)  # => opens a REAL SQLite file at a REAL temp path  # fmt: skip
    try:  # => wrapped so close() below always runs, even if an assertion fails  # fmt: skip
        new_id = repo.add("buy milk")  # => a genuine INSERT against a genuine file  # fmt: skip
        fetched = repo.get(new_id)  # => a genuine SELECT reading that SAME file back  # fmt: skip
        assert fetched == "buy milk"  # => the write-then-read round trip -- co-23's defining check  # fmt: skip
    finally:  # => runs whether the assertion above passed or raised  # fmt: skip
        repo.close()  # => always releases the real file handle, pass or fail  # fmt: skip


def test_integration_write_persists_across_new_connection(
    db_path: Path,
) -> None:  # => file, not memory
    first_repo = NoteRepository(db_path)  # => connection #1, writes and closes  # fmt: skip
    note_id = first_repo.add("call the vet")  # => a genuine write through connection #1  # fmt: skip
    first_repo.close()  # => the FIRST connection is fully gone now  # fmt: skip

    second_repo = NoteRepository(db_path)  # => connection #2, a BRAND NEW connection object  # fmt: skip
    try:  # => wrapped so close() below always runs  # fmt: skip
        # co-25: this only works because the data lives in a REAL FILE, not in-process memory --
        # a mocked/in-memory-dict repository would have LOST this data when the first repo closed.
        assert second_repo.get(note_id) == "call the vet"  # => the file, not the object, held the data  # fmt: skip
    finally:  # => runs whether the assertion above passed or raised  # fmt: skip
        second_repo.close()  # => releases connection #2's real file handle  # fmt: skip


def test_integration_missing_note_returns_none(
    db_path: Path,
) -> None:  # => a REAL empty-result path
    repo = NoteRepository(db_path)  # => a fresh, real SQLite file, with no rows yet  # fmt: skip
    try:  # => wrapped so close() below always runs  # fmt: skip
        assert repo.get(999) is None  # => a genuine "no such row" result from the real database  # fmt: skip
    finally:  # => runs whether the assertion above passed or raised  # fmt: skip
        repo.close()  # => releases the real file handle  # fmt: skip
