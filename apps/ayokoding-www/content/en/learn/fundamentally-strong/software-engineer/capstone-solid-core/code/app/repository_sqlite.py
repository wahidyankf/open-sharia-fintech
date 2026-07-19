"""capstone-solid-core: the ONE SQLite adapter (topic 10 SQL Essentials + topic 21 SOLID
Dependency Inversion) -- the imperative shell that actually talks to the database. Every
statement binds its inputs as `?` placeholders (co-20 parameterized-queries, carried forward
unchanged from Pass 1) -- never an f-string -- so user-controlled data is always treated as
DATA, never as SQL text. `init_db` applies the base schema, then two additive migrations
(schema-migration, topic 10 co-22), tracked by `PRAGMA user_version`, so calling it twice
against an already-migrated file is a safe no-op.

`SqliteHabitRepository` is the ONLY class in this codebase that satisfies `ports.HabitRepository`
that ships in production -- `HabitService` (services.py) never imports this module by name; it
only imports the `HabitRepository` Protocol from ports.py (Dependency Inversion Principle, topic
21). `test_services.py`'s `InMemoryHabitRepository` is a SECOND class satisfying the same
Protocol, added with zero edits here (Open/Closed Principle).
"""

from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path

from .domain import Habit
from .models import HabitCreate, UserPublic

SCHEMA_V1_PATH = Path(__file__).parent / "schema_v1.sql"
MIGRATION_V2_PATH = Path(__file__).parent / "migration_v2.sql"
MIGRATION_V3_PATH = Path(__file__).parent / "migration_v3.sql"


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = (
        sqlite3.Row
    )  # => rows addressable by column name, not just position
    conn.execute(
        "PRAGMA foreign_keys = ON"
    )  # => enforce FK constraints on this connection
    conn.execute(
        "PRAGMA journal_mode = WAL"
    )  # => co-XX (topic 24): Write-Ahead Logging lets one writer and MANY concurrent
    # => readers proceed without blocking each other -- Step 3's concurrent digest reads
    # => from several separate connections/processes WHILE the app keeps serving writes.
    return conn


def init_db(
    db_path: str,
) -> None:  # => topic 10 co-22 schema-migration: safe to call repeatedly
    conn = get_connection(db_path)
    current_version = int(conn.execute("PRAGMA user_version").fetchone()[0])
    if current_version < 1:  # => base schema not yet applied
        conn.executescript(SCHEMA_V1_PATH.read_text(encoding="utf-8"))
        conn.execute("PRAGMA user_version = 1")
        current_version = 1
    if current_version < 2:  # => additive migration (habits.archived) not yet applied
        conn.executescript(MIGRATION_V2_PATH.read_text(encoding="utf-8"))
        conn.execute("PRAGMA user_version = 2")
        current_version = 2
    if (
        current_version < 3
    ):  # => Step 3's composite index (co-XX, topic 26 EXPLAIN-guided)
        conn.executescript(MIGRATION_V3_PATH.read_text(encoding="utf-8"))
        conn.execute("PRAGMA user_version = 3")
    conn.commit()
    conn.close()


def ping(
    conn: sqlite3.Connection,
) -> bool:  # => the cheapest possible real query -- /ready
    conn.execute("SELECT 1")
    return True


# --- users -----------------------------------------------------------------------------------


def create_user(
    conn: sqlite3.Connection, username: str, password_hash: str
) -> UserPublic:
    cursor = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",  # => parameterized
        (username, password_hash),
    )
    conn.commit()
    row = conn.execute(
        "SELECT id, username, created_at FROM users WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    assert row is not None  # => guaranteed by the INSERT above
    return UserPublic(
        id=int(row["id"]),
        username=str(row["username"]),
        created_at=str(row["created_at"]),
    )


def get_user_by_username(conn: sqlite3.Connection, username: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()


# --- habits + check-ins: the class satisfying ports.HabitRepository ---------------------------


def _load_habit(conn: sqlite3.Connection, habit_row: sqlite3.Row) -> Habit:
    """Build a `Habit` domain object from a `habits` row plus its `checkins` rows, replaying
    every stored check-in through `record_checkin` -- the DB is the source of truth; the domain
    object is a transient in-memory VIEW of it, rebuilt on every load (DD-33 taming-state)."""
    habit = Habit(
        id=int(habit_row["id"]),
        name=str(habit_row["name"]),
        archived=bool(habit_row["archived"]),
    )
    for checkin_row in conn.execute(
        "SELECT checkin_date FROM checkins WHERE habit_id = ?", (habit_row["id"],)
    ):
        habit.record_checkin(date.fromisoformat(str(checkin_row["checkin_date"])))
    return habit


class SqliteHabitRepository:
    """Implements `ports.HabitRepository` against a `sqlite3.Connection`. Structural typing
    (PEP 544) means this class need not, and does not, inherit from `HabitRepository` --
    Python's `Protocol` matches by SHAPE, not by declared ancestry."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def create_habit(self, user_id: int, data: HabitCreate) -> Habit:
        cursor = self._conn.execute(
            "INSERT INTO habits (user_id, name) VALUES (?, ?)", (user_id, data.name)
        )
        self._conn.commit()
        row = self._conn.execute(
            "SELECT * FROM habits WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        assert row is not None
        return _load_habit(self._conn, row)

    def get_habit(self, habit_id: int, user_id: int) -> Habit | None:
        row = self._conn.execute(
            "SELECT * FROM habits WHERE id = ? AND user_id = ?", (habit_id, user_id)
        ).fetchone()
        return _load_habit(self._conn, row) if row is not None else None

    def list_habits(self, user_id: int, include_archived: bool = False) -> list[Habit]:
        if include_archived:
            rows = self._conn.execute(
                "SELECT * FROM habits WHERE user_id = ? ORDER BY id", (user_id,)
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM habits WHERE user_id = ? AND archived = 0 ORDER BY id",
                (user_id,),
            ).fetchall()
        return [_load_habit(self._conn, row) for row in rows]

    def search_habits(self, user_id: int, q: str) -> list[Habit]:
        rows = self._conn.execute(
            "SELECT * FROM habits WHERE user_id = ? AND name LIKE '%' || ? || '%' ORDER BY id",
            (user_id, q),  # => `?`: q is DATA, never spliced into the SQL text
        ).fetchall()
        return [_load_habit(self._conn, row) for row in rows]

    def archive_habit(self, habit_id: int, user_id: int) -> Habit | None:
        row = self._conn.execute(
            "SELECT * FROM habits WHERE id = ? AND user_id = ?", (habit_id, user_id)
        ).fetchone()
        if row is None:
            return None
        habit = _load_habit(self._conn, row)
        habit.archive()  # => the ONE guarded mutator (topic 08), not a hand-written flag flip
        self._conn.execute(
            "UPDATE habits SET archived = ? WHERE id = ? AND user_id = ?",
            (int(habit.archived), habit_id, user_id),
        )
        self._conn.commit()
        return habit

    def delete_habit(self, habit_id: int, user_id: int) -> bool:
        cursor = self._conn.execute(
            "DELETE FROM habits WHERE id = ? AND user_id = ?", (habit_id, user_id)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def record_checkin(
        self, habit_id: int, user_id: int, checkin_date_iso: str
    ) -> None:
        self._conn.execute(
            "INSERT INTO checkins (habit_id, user_id, checkin_date) VALUES (?, ?, ?) "
            "ON CONFLICT (habit_id, checkin_date) DO NOTHING",  # => a repeat check-in is a no-op
            (habit_id, user_id, checkin_date_iso),
            # => `user_id` is written HERE too (Step 3's denormalization, migration_v3.sql) --
            # => the ONE place this app ever creates a checkins row, so the copy can never drift
        )
        self._conn.commit()

    def recent_activity(self, user_id: int, limit: int) -> list[tuple[int, str]]:
        """Step 3's EXPLAIN-guided-index query (topic 26 co-XX denormalization-tradeoffs): this
        user's most recent check-ins across EVERY habit, newest first -- no join, thanks to
        migration_v3.sql's denormalized `checkins.user_id` + composite index."""
        rows = self._conn.execute(
            "SELECT habit_id, checkin_date FROM checkins "
            "WHERE user_id = ? ORDER BY checkin_date DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return [(int(row["habit_id"]), str(row["checkin_date"])) for row in rows]
