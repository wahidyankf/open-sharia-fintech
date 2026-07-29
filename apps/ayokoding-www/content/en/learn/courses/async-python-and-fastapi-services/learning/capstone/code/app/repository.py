"""Capstone async FastAPI service -- the ONLY module that talks to the database (co-16, co-15)."""

from pathlib import Path

import aiosqlite  # => the async driver -- query waits yield to the loop (co-16)

from .models import Task, TaskCreate, TaskPage, TaskUpdate

SCHEMA_PATH = (
    Path(__file__).parent / "schema.sql"
)  # => the schema applied at startup (co-16)


async def get_connection(
    db_path: str,
) -> aiosqlite.Connection:  # => one async connection per request (co-15)
    conn = await aiosqlite.connect(db_path)  # => async acquire
    conn.row_factory = aiosqlite.Row  # => rows addressable by column name
    return conn


async def init_db(
    db_path: str,
) -> None:  # => apply schema.sql once at startup (co-16, co-18)
    conn = await get_connection(db_path)
    await conn.executescript(
        SCHEMA_PATH.read_text(encoding="utf-8")
    )  # => idempotent schema
    await conn.commit()
    await conn.close()


def _row_to_task(
    row: aiosqlite.Row,
) -> Task:  # => the ONE place a raw row becomes a typed Task (co-14)
    return Task(
        id=int(row["id"]),
        title=str(row["title"]),
        description=str(row["description"]),
        status=str(row["status"]),  # type: ignore[arg-type]  # => Pydantic validates against TaskStatus
        created_at=str(row["created_at"]),
    )


async def create_task(
    conn: aiosqlite.Connection, data: TaskCreate
) -> Task:  # => parameterized INSERT (co-16)
    cursor = await conn.execute(  # => ? placeholders, never f-strings (co-16)
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (data.title, data.description),
    )
    await conn.commit()
    row = await (
        await conn.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,))
    ).fetchone()
    assert (
        row is not None
    )  # => guaranteed by the INSERT above -- narrows Row | None for strict pyright
    return _row_to_task(row)  # => re-read to include DB-generated defaults


async def get_task(
    conn: aiosqlite.Connection, task_id: int
) -> Task | None:  # => parameterized SELECT (co-16)
    row = await (
        await conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    ).fetchone()
    return (
        _row_to_task(row) if row is not None else None
    )  # => None signals "not found" (co-17)


async def update_task(  # => parameterized UPDATE (co-16)
    conn: aiosqlite.Connection, task_id: int, data: TaskUpdate
) -> Task | None:
    cursor = await conn.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
        (data.title, data.description, data.status, task_id),
    )
    if cursor.rowcount == 0:  # => no row matched
        return None
    await conn.commit()
    row = await (
        await conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    ).fetchone()
    assert row is not None  # => rowcount > 0 above guarantees this
    return _row_to_task(row)


async def delete_task(
    conn: aiosqlite.Connection, task_id: int
) -> bool:  # => parameterized DELETE (co-16)
    cursor = await conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    await conn.commit()
    return cursor.rowcount > 0  # => True only if a row genuinely existed


async def list_tasks(  # => pagination + filtering in ONE parameterized query (co-11, co-16)
    conn: aiosqlite.Connection, limit: int, offset: int, status: str | None
) -> TaskPage:
    where = (
        " WHERE status = ?" if status is not None else ""
    )  # => an optional filter clause
    params: list[object] = [status] if status is not None else []
    total_row = await (
        await conn.execute(f"SELECT COUNT(*) AS n FROM tasks{where}", params)
    ).fetchone()
    assert total_row is not None  # => COUNT(*) always returns one row
    total = int(total_row["n"])  # => the FILTERED total (co-11)
    rows = await (
        await conn.execute(
            f"SELECT * FROM tasks{where} ORDER BY id LIMIT ? OFFSET ?",
            [*params, limit, offset],
        )
    ).fetchall()
    items = [_row_to_task(row) for row in rows]
    next_offset = offset + limit
    return TaskPage(
        items=items, total=total, next=next_offset if next_offset < total else None
    )  # => None at end


async def ping(
    conn: aiosqlite.Connection,
) -> bool:  # => cheapest real query -- used by /ready (co-16)
    await conn.execute("SELECT 1")
    return True
