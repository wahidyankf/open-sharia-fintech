"""Capstone: hardened task API -- the ONLY module that talks to the database (co-03).

Every statement below is parameterized -- the entire injection surface Backend-Essentials
already closed for CRUD, PLUS the new search_tasks() this capstone adds and hardens.
"""

import sqlite3
from pathlib import Path

from .models import Task, TaskCreate, TaskPage, TaskUpdate, UserPublic

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = (
        sqlite3.Row
    )  # => rows are addressable by column name, not just position
    return conn


def init_db(
    db_path: str,
) -> None:  # => applies schema.sql once, safe to call repeatedly
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()


def _row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id=int(row["id"]),
        title=str(row["title"]),
        description=str(row["description"]),
        status=str(row["status"]),  # type: ignore[arg-type]  # => Pydantic validates this against TaskStatus
        created_at=str(row["created_at"]),
    )


def create_task(
    conn: sqlite3.Connection, data: TaskCreate
) -> Task:  # => co-03: parameterized INSERT
    cursor = conn.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",  # => co-03: ? placeholders, never f-strings
        (data.title, data.description),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    assert (
        row is not None
    )  # => guaranteed by the INSERT above -- narrows Row | None for strict-mode pyright
    return _row_to_task(row)


def get_task(
    conn: sqlite3.Connection, task_id: int
) -> Task | None:  # => co-03: parameterized SELECT
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return _row_to_task(row) if row is not None else None


def update_task(
    conn: sqlite3.Connection, task_id: int, data: TaskUpdate
) -> Task | None:  # => co-03
    cursor = conn.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",  # => parameterized
        (data.title, data.description, data.status, task_id),
    )
    if cursor.rowcount == 0:
        return None
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    assert row is not None
    return _row_to_task(row)


def delete_task(
    conn: sqlite3.Connection, task_id: int
) -> bool:  # => co-03: parameterized DELETE
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return cursor.rowcount > 0


def list_tasks(
    conn: sqlite3.Connection, limit: int, offset: int, status: str | None
) -> TaskPage:
    where = " WHERE status = ?" if status is not None else ""
    params: list[str] = [status] if status is not None else []
    total_row = conn.execute(
        f"SELECT COUNT(*) AS n FROM tasks{where}", params
    ).fetchone()
    assert total_row is not None
    total = int(total_row["n"])
    cursor = conn.execute(
        f"SELECT * FROM tasks{where} ORDER BY id LIMIT ? OFFSET ?",  # => still parameterized -- `where`
        [
            *params,
            limit,
            offset,
        ],  # => interpolates only a FIXED clause string, never attacker data
    )
    items = [_row_to_task(row) for row in cursor.fetchall()]
    next_offset = offset + limit
    return TaskPage(
        items=items, total=total, next=next_offset if next_offset < total else None
    )


def search_tasks(conn: sqlite3.Connection, q: str) -> list[Task]:
    """Search tasks by a substring of their title -- co-03, the FIXED version of this capstone's
    Step 1. The naive first draft built this WHERE clause with an f-string
    (`f"...LIKE '%{q}%'"`) and a live attack against it is documented on this capstone's page;
    this shipped version binds `q` as a parameter, so it can never be interpreted as SQL."""
    cursor = conn.execute(
        "SELECT * FROM tasks WHERE title LIKE '%' || ? || '%'",  # => co-03: `?` -- q is DATA, never SQL text
        (q,),
    )
    return [_row_to_task(row) for row in cursor.fetchall()]


def ping(
    conn: sqlite3.Connection,
) -> bool:  # => the cheapest possible real query -- used by /ready
    conn.execute("SELECT 1")
    return True


def create_user(
    conn: sqlite3.Connection, username: str, password_hash: str
) -> UserPublic:  # => co-03, co-09
    cursor = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",  # => parameterized; hash only, never raw
        (username, password_hash),
    )
    conn.commit()
    row = conn.execute(
        "SELECT id, username, created_at FROM users WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    assert row is not None
    return UserPublic(
        id=int(row["id"]),
        username=str(row["username"]),
        created_at=str(row["created_at"]),
    )


def get_user_by_username(
    conn: sqlite3.Connection, username: str
) -> sqlite3.Row | None:  # => co-03
    return conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
