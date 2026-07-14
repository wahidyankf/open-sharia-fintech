"""Example 72: Sort Param -- ?sort=created_at (or -created_at) orders the list."""

import os
import sqlite3  # => co-14: the stdlib DB driver -- no ORM, no extra dependency needed
from typing import Literal, TypedDict  # => co-12: Literal constrains the sort param to two values

from fastapi import FastAPI, Query  # => co-12: query params are typed and validated here
# => (fully self-contained: nothing here is imported from any other example directory)

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")  # => co-14: one on-disk SQLite
# => file PER EXAMPLE DIRECTORY -- never shared with any other example, keeping each self-contained

# => co-15: the schema below backs every list query in this example. Column-by-column:
# =>   id          -- an auto-incrementing primary key, never chosen by the caller
# =>   title       -- the task's display text, no constraint on it beyond NOT NULL
# =>   status      -- co-20: a FILTERABLE field, exercised starting at Example 69
# =>   priority    -- co-20: a SECOND filterable field, exercised starting at Example 70
# =>   created_at  -- co-20: a SORTABLE field, exercised starting at Example 72
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class TaskRow(TypedDict):  # => co-14, co-24: the repository's typed return shape --
    # => every field below matches a SCHEMA column one-to-one, so `dict(row)` (further down)
    # => produces a value that satisfies this shape without any manual field-by-field mapping
    id: int  # => matches the schema's INTEGER PRIMARY KEY column
    title: str  # => matches the schema's title column
    status: str  # => matches the schema's status column
    priority: str  # => matches the schema's priority column
    created_at: str  # => matches the schema's created_at column


def _seed(conn: sqlite3.Connection) -> None:  # => co-14: builds the SAME deterministic 25-row
    # => dataset used by every pagination/filter/sort example in this topic, so worked-out ids
    # => like "done={2,5,8,...}" stay correct however many of these example directories exist
    statuses = ["todo", "in_progress", "done"]  # => rotates every 3 rows -- index is i % 3
    priorities = ["low", "normal", "high"]  # => rotates every 2 rows via (i // 2) % 3 --
    # => DECORRELATED from status ON PURPOSE, so a combined status+priority filter genuinely
    # => narrows further than either field alone, instead of the two columns moving in lockstep
    rows = [
        (f"task {i}", statuses[i % 3], priorities[(i // 2) % 3], f"2026-07-{i:02d}T00:00:00")
        for i in range(1, 26)  # => created_at already increases WITH id -- ascending sort looks
        # => like a no-op, so THIS example's curl deliberately checks descending order too, below
    ]
    conn.executemany(  # => co-14: a single batched INSERT for all 25 rows, one transaction
        "INSERT INTO tasks (title, status, priority, created_at) VALUES (?, ?, ?, ?)",  # => co-14:
        # => ? placeholders -- the SAME parameterization principle Example 71 stress-tests directly
        rows,
    )
    conn.commit()  # => co-14: commits the whole seed batch at once, not row-by-row


def init_db() -> None:  # => co-15: fresh schema + seed data every time this module is imported
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)  # => start from a known, deterministic state -- this example's expected
        # => row counts and ids only hold true starting from a CLEAN file, never an accumulated one
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)  # => co-15: creates the table every query below depends on existing
    _seed(conn)  # => populates it with the 25-row deterministic dataset described above
    conn.close()  # => co-14: connections are short-lived here -- opened, used, closed, never held


def get_connection() -> sqlite3.Connection:  # => co-14: the repository's ONLY entry point to
    # => the DB -- every query function below calls THIS instead of sqlite3.connect() directly
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # => rows behave like dicts -- readable by column name, which
    # => is what makes `dict(row)` below produce sensible {"id":..., "title":...} keys, not a tuple
    return conn  # => a fresh connection per call -- co-14: no pooling, matches this example's scale


SortValue = Literal["created_at", "-created_at"]  # => co-20: a closed set -- FastAPI 422s anything
# => else, unlike `status`/`priority` in the filter examples, which accept any string at all

_COLUMN_BY_SORT: dict[SortValue, str] = {  # => co-14: maps the PUBLIC sort value to a real column +
    # => direction -- this dict is the ONLY thing standing between user input and an ORDER BY clause
    "created_at": "created_at ASC",  # => oldest-first, matching the seed's natural insertion order
    "-created_at": "created_at DESC",  # => a leading "-" is a common REST convention for "descending"
}


def list_tasks(sort: SortValue) -> list[TaskRow]:  # => co-14, co-20: sort is a Literal, so `sort`
    # => can ONLY ever be one of the two dict keys above -- pyright itself enforces total coverage
    conn = get_connection()
    order_clause = _COLUMN_BY_SORT[sort]  # => co-14: looked up from a FIXED mapping -- never
    # => interpolates raw user input directly into ORDER BY, which parameterization cannot protect
    # => against (SQLite has no `?` placeholder syntax for column names or ASC/DESC keywords at all)
    cursor = conn.execute(f"SELECT id, title, status, priority, created_at FROM tasks ORDER BY {order_clause}")
    result = [dict(row) for row in cursor.fetchall()]  # type: ignore[misc]  # => sqlite3.Row -> dict
    conn.close()  # => co-14: closed immediately after this one query
    return result  # type: ignore[return-value]  # => shape matches TaskRow at runtime


init_db()  # => co-15: runs once at import time, before the app starts serving

app = FastAPI()  # => a fresh app -- this example needs no auth, only the sort mechanism


@app.get("/tasks")  # => co-20: this example's focus -- reordering the SAME underlying rows,
# => never changing WHICH rows come back, only the SEQUENCE they arrive in
def get_tasks(sort: SortValue = Query(default="created_at")) -> list[TaskRow]:
    return list_tasks(sort)  # => co-24: the handler holds no SQL -- it delegates to the repository
