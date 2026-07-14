"""Example 67: Pagination Metadata -- the response includes total and next."""
# => co-19: Example 65 proved limit/offset SLICES the list; this example proves a client can also
# => discover how many pages exist and where the next one starts, without a separate count request

import os
import sqlite3  # => co-14: the stdlib DB driver -- no ORM, no extra dependency needed
from typing import TypedDict  # => co-09: a typed dict shape for what the repository returns

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


class Page(TypedDict):  # => co-09, co-19: the ENVELOPE shape -- not just a bare array anymore --
    # => every list endpoint from THIS example onward returns this shape instead of a raw list
    items: list[TaskRow]  # => this page's rows -- exactly what Example 65 returned on its own
    total: int  # => co-19: the FULL table's row count, independent of this page's size
    next: int | None  # => None means "no further page" -- a real, typed sentinel, not a magic number


def _seed(conn: sqlite3.Connection) -> None:  # => co-14: builds the SAME deterministic 25-row
    # => dataset used by every pagination/filter/sort example in this topic, so worked-out ids
    # => like "done={2,5,8,...}" stay correct however many of these example directories exist
    statuses = ["todo", "in_progress", "done"]  # => rotates every 3 rows -- index is i % 3
    priorities = ["low", "normal", "high"]  # => co-19: irrelevant to pagination itself, but kept
    # => identical to Example 65's schema/seed so this file stays a complete, self-contained app --
    # => rotates every 2 rows via (i // 2) % 3, DECORRELATED from status ON PURPOSE (a combined
    # => status+priority filter, exercised starting at Example 70, needs the two fields independent)
    rows = [
        (f"task {i}", statuses[i % 3], priorities[(i // 2) % 3], f"2026-07-{i:02d}T00:00:00")
        for i in range(1, 26)  # => 25 total rows -- big enough that a 10-row page genuinely has a next
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


def list_page(limit: int, offset: int) -> Page:  # => co-14, co-19: repository returns the FULL
    # => envelope this time -- not just the rows, but ENOUGH metadata for a client to keep paging
    conn = get_connection()
    total = int(conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0])  # => co-19: the WHOLE
    # => table's size, computed with a SEPARATE query -- the LIMIT below never touches this number
    cursor = conn.execute(  # => co-14: the exact same paginated SELECT as Example 65
        "SELECT id, title, status, priority, created_at FROM tasks ORDER BY id LIMIT ? OFFSET ?",
        (limit, offset),
    )
    items = [dict(row) for row in cursor.fetchall()]  # type: ignore[misc]  # => sqlite3.Row -> dict
    conn.close()  # => co-14: closed immediately after both queries above finish
    next_offset = offset + limit  # => co-19: the offset a client would use to fetch the FOLLOWING page
    has_more = next_offset < total  # => whether that following page would return anything at all --
    # => an offset landing exactly ON or past `total` means there is nothing left to return
    return {
        "items": items,  # type: ignore[typeddict-item]  # => this page's slice of rows
        "total": total,  # => co-19: the FULL count, letting a client compute "page 3 of N" itself
        "next": next_offset if has_more else None,  # => None signals "you have reached the end" --
        # => a typed sentinel a client can check with `if page["next"] is not None`, no magic number
    }


init_db()  # => co-15: runs once at import time, before the app starts serving

app = FastAPI()  # => a fresh app -- this example needs no auth, only the pagination envelope


@app.get("/tasks")  # => co-19, co-09: returns the metadata envelope, not a bare list -- Example 65's
# => `list[TaskRow]` return type becomes `Page` here, wrapping the same rows with total/next alongside
def get_tasks(
    limit: int = Query(default=10, ge=1),  # => co-12: identical constraint to Example 65
    offset: int = Query(default=0, ge=0),  # => co-12: identical constraint to Example 65
) -> Page:
    return list_page(limit, offset)  # => co-19: the handler holds NO SQL -- co-24 layering
