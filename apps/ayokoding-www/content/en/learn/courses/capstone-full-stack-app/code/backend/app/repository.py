"""Full-stack capstone -- the ONLY module that talks to the database (topic 10 SQL Essentials).
Every statement below binds its inputs as `?` placeholders (parameterized queries) -- never an
f-string -- so client-supplied data is always treated as DATA, never as SQL text.
"""

import sqlite3
from pathlib import Path

from .models import Task, TaskCreate, TaskUpdate

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = (
        sqlite3.Row
    )  # => rows are addressable by column name, not just position
    return conn


def init_db(db_path: str) -> None:  # => applies schema.sql; safe to call repeatedly
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()


def _row_to_task(
    row: sqlite3.Row,
) -> Task:  # => the ONE place a raw sqlite3.Row becomes a typed Task
    return Task(
        id=int(row["id"]),
        title=str(row["title"]),
        description=str(row["description"]),
        status=str(row["status"]),  # type: ignore[arg-type]  # => Pydantic validates this against TaskStatus
        created_at=str(row["created_at"]),
    )


def create_task(conn: sqlite3.Connection, data: TaskCreate) -> Task:
    cursor = conn.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",  # => ? placeholders, never f-strings
        (data.title, data.description),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    assert (
        row is not None
    )  # => guaranteed by the INSERT above -- narrows Row | None for strict-mode pyright
    return _row_to_task(
        row
    )  # => the freshly-inserted row, re-read to include DB-generated defaults


def get_task(conn: sqlite3.Connection, task_id: int) -> Task | None:
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return (
        _row_to_task(row) if row is not None else None
    )  # => None signals "not found" -- the
    # => HANDLER decides how to turn that into a 404, this function only reports facts


def update_task(  # => PUT semantics -- REPLACES the whole resource
    conn: sqlite3.Connection, task_id: int, data: TaskUpdate
) -> Task | None:
    cursor = conn.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",  # => parameterized
        (data.title, data.description, data.status, task_id),
    )
    if cursor.rowcount == 0:  # => no row matched -- nothing to update
        return None
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    assert (
        row is not None
    )  # => rowcount > 0 above guarantees this -- narrows Row | None
    return _row_to_task(row)


def list_tasks(
    conn: sqlite3.Connection,
) -> list[Task]:  # => the CORS-safe read endpoint's data source
    rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    return [_row_to_task(row) for row in rows]


def ping(
    conn: sqlite3.Connection,
) -> bool:  # => the cheapest possible real query -- used by /ready
    conn.execute("SELECT 1")
    return True
