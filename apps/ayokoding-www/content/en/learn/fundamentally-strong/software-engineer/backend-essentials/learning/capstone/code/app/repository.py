"""Capstone task API -- the ONLY module that talks to the database (co-14, co-24)."""

import sqlite3
from pathlib import Path

from .models import Task, TaskCreate, TaskPage, TaskUpdate

SCHEMA_PATH = Path(__file__).parent / "schema.sql"  # => co-15: the schema this repository applies at startup


def get_connection(db_path: str) -> sqlite3.Connection:  # => co-14, co-23: one connection per call/request
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # => rows are addressable by column name, not just position
    return conn


def init_db(db_path: str) -> None:  # => co-15: migrations -- applies schema.sql, safe to call repeatedly
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()


def _row_to_task(row: sqlite3.Row) -> Task:  # => co-14: the ONE place a raw sqlite3.Row becomes a typed Task
    return Task(
        id=int(row["id"]),
        title=str(row["title"]),
        description=str(row["description"]),
        status=str(row["status"]),  # type: ignore[arg-type]  # => Pydantic validates this against TaskStatus
        created_at=str(row["created_at"]),
    )


def create_task(conn: sqlite3.Connection, data: TaskCreate) -> Task:  # => co-14: parameterized INSERT
    cursor = conn.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",  # => co-14: ? placeholders, never f-strings
        (data.title, data.description),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
    assert row is not None  # => co-14: guaranteed by the INSERT above -- narrows Row | None for strict-mode pyright
    return _row_to_task(row)  # => the freshly-inserted row, re-read to include the DB-generated defaults


def get_task(conn: sqlite3.Connection, task_id: int) -> Task | None:  # => co-14: parameterized SELECT
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return _row_to_task(row) if row is not None else None  # => None signals "not found" -- co-24: the
    # => HANDLER decides how to turn that into a 404, this function only reports facts


def update_task(  # => co-02, co-14: PUT semantics -- REPLACES the whole resource
    conn: sqlite3.Connection, task_id: int, data: TaskUpdate
) -> Task | None:
    cursor = conn.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",  # => co-14: parameterized
        (data.title, data.description, data.status, task_id),
    )
    if cursor.rowcount == 0:  # => no row matched -- nothing to update
        return None
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    assert row is not None  # => co-14: rowcount > 0 above guarantees this -- narrows Row | None
    return _row_to_task(row)


def delete_task(conn: sqlite3.Connection, task_id: int) -> bool:  # => co-14: parameterized DELETE
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return cursor.rowcount > 0  # => True only if a row genuinely existed and was removed


def list_tasks(  # => co-19, co-20: pagination + filtering, composed in ONE parameterized query
    conn: sqlite3.Connection, limit: int, offset: int, status: str | None
) -> TaskPage:
    where = " WHERE status = ?" if status is not None else ""  # => co-20: an OPTIONAL filter clause
    params: list[str] = [status] if status is not None else []
    total_row = conn.execute(f"SELECT COUNT(*) AS n FROM tasks{where}", params).fetchone()
    assert total_row is not None  # => COUNT(*) always returns exactly one row -- narrows Row | None
    total = int(total_row["n"])  # => co-19: the FILTERED total, not the whole table
    cursor = conn.execute(
        f"SELECT * FROM tasks{where} ORDER BY id LIMIT ? OFFSET ?",  # => co-14, co-19: still parameterized
        [*params, limit, offset],
    )
    items = [_row_to_task(row) for row in cursor.fetchall()]
    next_offset = offset + limit
    return TaskPage(items=items, total=total, next=next_offset if next_offset < total else None)  # => co-19: None is the explicit "no further page" sentinel


def ping(conn: sqlite3.Connection) -> bool:  # => co-14: the cheapest possible real query -- used by /ready
    conn.execute("SELECT 1")
    return True
