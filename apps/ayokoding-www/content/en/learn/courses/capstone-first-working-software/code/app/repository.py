"""Pass-1 capstone: Habit Tracker -- the ONLY module that talks to the database (topic 10).

Every statement below binds its inputs as `?` placeholders (co-20 parameterized-queries) --
never an f-string -- so user-controlled data is always treated as DATA, never as SQL text.
`init_db` applies the base schema then an additive migration, tracked by `PRAGMA user_version`
(co-22 schema-migration), so calling it twice against an already-migrated file is a safe no-op.
"""

from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path

from .domain import Habit
from .models import HabitCreate, UserPublic

SCHEMA_V1_PATH = Path(__file__).parent / "schema_v1.sql"
MIGRATION_V2_PATH = Path(__file__).parent / "migration_v2.sql"


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = (
        sqlite3.Row
    )  # => rows are addressable by column name, not just position
    conn.execute(
        "PRAGMA foreign_keys = ON"
    )  # => co-03: enforce FK constraints on this connection
    return conn


def init_db(db_path: str) -> None:  # => co-22 schema-migration: safe to call repeatedly
    conn = get_connection(db_path)
    current_version = int(conn.execute("PRAGMA user_version").fetchone()[0])
    if current_version < 1:  # => base schema not yet applied
        conn.executescript(SCHEMA_V1_PATH.read_text(encoding="utf-8"))
        conn.execute("PRAGMA user_version = 1")
        current_version = 1
    if current_version < 2:  # => additive migration (habits.archived) not yet applied
        conn.executescript(MIGRATION_V2_PATH.read_text(encoding="utf-8"))
        conn.execute("PRAGMA user_version = 2")
    conn.commit()
    conn.close()


def ping(
    conn: sqlite3.Connection,
) -> bool:  # => the cheapest possible real query -- used by /ready
    conn.execute("SELECT 1")
    return True


# --- users -----------------------------------------------------------------------------------


def create_user(
    conn: sqlite3.Connection, username: str, password_hash: str
) -> UserPublic:
    cursor = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",  # => parameterized; hash only, never raw
        (username, password_hash),
    )
    conn.commit()
    row = conn.execute(
        "SELECT id, username, created_at FROM users WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    assert (
        row is not None
    )  # => guaranteed by the INSERT above -- narrows Row | None for strict-mode pyright
    return UserPublic(
        id=int(row["id"]),
        username=str(row["username"]),
        created_at=str(row["created_at"]),
    )


def get_user_by_username(conn: sqlite3.Connection, username: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()  # => co-20


# --- habits + check-ins -----------------------------------------------------------------------


def _load_habit(conn: sqlite3.Connection, habit_row: sqlite3.Row) -> Habit:
    """Build a `Habit` domain object (topic 08) from a `habits` row plus its `checkins` rows,
    replaying every stored check-in through `record_checkin` so the domain object's hash-set
    (topic 07 co-09) reflects the full, real history -- the DB is the source of truth; the
    domain object is a transient in-memory VIEW of it, rebuilt on every load."""
    habit = Habit(
        id=int(habit_row["id"]),
        name=str(habit_row["name"]),
        archived=bool(habit_row["archived"]),
    )
    for checkin_row in conn.execute(
        "SELECT checkin_date FROM checkins WHERE habit_id = ?",
        (habit_row["id"],),  # => co-20
    ):
        habit.record_checkin(date.fromisoformat(str(checkin_row["checkin_date"])))
    return habit


def create_habit(conn: sqlite3.Connection, user_id: int, data: HabitCreate) -> Habit:
    cursor = conn.execute(
        "INSERT INTO habits (user_id, name) VALUES (?, ?)",
        (user_id, data.name),  # => co-20
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM habits WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    assert row is not None
    return _load_habit(conn, row)


def get_habit(conn: sqlite3.Connection, habit_id: int, user_id: int) -> Habit | None:
    row = conn.execute(
        "SELECT * FROM habits WHERE id = ? AND user_id = ?",
        (habit_id, user_id),  # => co-20; ownership-scoped
    ).fetchone()
    return _load_habit(conn, row) if row is not None else None


def list_habits(
    conn: sqlite3.Connection, user_id: int, include_archived: bool = False
) -> list[Habit]:
    if include_archived:
        rows = conn.execute(
            "SELECT * FROM habits WHERE user_id = ? ORDER BY id",
            (user_id,),  # => co-20
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM habits WHERE user_id = ? AND archived = 0 ORDER BY id",
            (user_id,),  # => co-20
        ).fetchall()
    return [_load_habit(conn, row) for row in rows]


def archive_habit(
    conn: sqlite3.Connection, habit_id: int, user_id: int
) -> Habit | None:
    """Load the habit, archive it through the DOMAIN OBJECT's own guarded method (topic 08 --
    `habits.archived` is never set with a bare `UPDATE ... SET archived = 1` written by hand
    at the call site), then persist the domain object's decision back to the row."""
    row = conn.execute(
        "SELECT * FROM habits WHERE id = ? AND user_id = ?",
        (habit_id, user_id),  # => co-20
    ).fetchone()
    if row is None:
        return None
    habit = _load_habit(conn, row)
    habit.archive()  # => topic 08: the ONE guarded mutator, not a hand-written flag flip
    conn.execute(
        "UPDATE habits SET archived = ? WHERE id = ? AND user_id = ?",  # => co-20
        (int(habit.archived), habit_id, user_id),
    )
    conn.commit()
    return habit


def delete_habit(conn: sqlite3.Connection, habit_id: int, user_id: int) -> bool:
    cursor = conn.execute(
        "DELETE FROM habits WHERE id = ? AND user_id = ?",
        (habit_id, user_id),  # => co-20; ownership-scoped
    )
    conn.commit()
    return cursor.rowcount > 0


def record_checkin(
    conn: sqlite3.Connection, habit_id: int, checkin_date_iso: str
) -> None:
    conn.execute(
        "INSERT INTO checkins (habit_id, checkin_date) VALUES (?, ?) "  # => co-20
        "ON CONFLICT (habit_id, checkin_date) DO NOTHING",  # => co-10 upsert: a repeat check-in is a no-op
        (habit_id, checkin_date_iso),
    )
    conn.commit()


def search_habits(conn: sqlite3.Connection, user_id: int, q: str) -> list[Habit]:
    """Search this user's habits by a substring of their name -- co-03 (topic 17), the FIXED,
    parameterized version. The naive first draft built this WHERE clause with an f-string
    (`f"...WHERE name LIKE '%{q}%'"`) and a live SQL-injection attack against it is documented
    on this capstone's page; this shipped version binds `q` as a parameter, so it can never be
    interpreted as SQL text."""
    rows = conn.execute(
        "SELECT * FROM habits WHERE user_id = ? AND name LIKE '%' || ? || '%' ORDER BY id",  # => `?`: q is DATA
        (user_id, q),
    ).fetchall()
    return [_load_habit(conn, row) for row in rows]
