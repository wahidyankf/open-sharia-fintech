"""Example 66: Pagination Default -- a default limit applies when the param is absent."""
# => co-12, co-19: builds on the SAME limit/offset mechanism as Example 65, this time proving
# => what happens on the OTHER side -- a caller who sends no limit at all still gets a bounded page

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


def _seed(conn: sqlite3.Connection) -> None:  # => co-14: builds the SAME deterministic 25-row
    # => dataset used by every pagination/filter/sort example in this topic, so worked-out ids
    # => like "done={2,5,8,...}" stay correct however many of these example directories exist
    statuses = ["todo", "in_progress", "done"]  # => rotates every 3 rows -- index is i % 3
    priorities = ["low", "normal", "high"]  # => rotates every 2 rows via (i // 2) % 3 --
    # => DECORRELATED from status ON PURPOSE, so a combined status+priority filter genuinely
    # => narrows further than either field alone, instead of the two columns moving in lockstep
    rows = [
        (f"task {i}", statuses[i % 3], priorities[(i // 2) % 3], f"2026-07-{i:02d}T00:00:00")
        for i in range(1, 26)  # => the SAME 25-row seed used across the pagination/filter examples --
        # => 25 is more than DEFAULT_LIMIT, so the default page is PROVABLY shorter than the full set
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


DEFAULT_LIMIT = 10  # => co-19: a NAMED constant -- the exact bound applied when the caller sends
# => nothing at all for `?limit=` -- naming it (rather than a bare 10 inline) means the value is
# => documented once, reused everywhere below, and trivial to find without reading every route


def list_tasks(limit: int, offset: int) -> list[TaskRow]:  # => co-14, co-19: identical query shape
    # => to every other example in this cluster -- what's NEW here is what CALLS it, further down
    conn = get_connection()
    cursor = conn.execute(  # => co-14: LIMIT/OFFSET are parameterized, never string-interpolated
        "SELECT id, title, status, priority, created_at FROM tasks ORDER BY id LIMIT ? OFFSET ?",
        (limit, offset),  # => co-19: whatever the caller sent (or the default below) lands here
    )
    result = [dict(row) for row in cursor.fetchall()]  # type: ignore[misc]  # => sqlite3.Row -> dict
    conn.close()  # => co-14: closed immediately after this one query
    return result  # type: ignore[return-value]  # => shape matches TaskRow at runtime


def count_tasks() -> int:  # => co-19: total row count, used here only to PROVE the default is bounded --
    # => this example's curl calls THIS endpoint to show 25 rows exist, then /tasks to show only 10 return
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]  # => co-14: a single scalar query
    conn.close()
    return int(total)  # => SQLite returns a plain int already -- the cast documents the intent, not a fix


init_db()  # => co-15: runs once at import time, before the app starts serving

app = FastAPI()  # => a fresh app -- this example needs no auth, only the default-limit mechanism


@app.get("/tasks")  # => co-19: this example's focus -- what happens when limit is OMITTED entirely
def get_tasks(
    limit: int = Query(default=DEFAULT_LIMIT, ge=1),  # => co-12: the default only kicks in when
    # => `?limit=` is absent from the URL altogether -- sending `?limit=0` would instead hit ge=1's
    # => validation error, which is a DIFFERENT scenario than "the caller said nothing" (this example's)
    offset: int = Query(default=0, ge=0),  # => co-12: same default-when-absent behavior, for offset
) -> list[TaskRow]:
    return list_tasks(limit, offset)  # => co-19: the handler holds NO SQL -- co-24 layering


@app.get("/tasks/count")  # => a small helper endpoint proving 25 rows genuinely exist behind the default
def get_count() -> dict[str, int]:
    return {"total": count_tasks()}  # => co-19: contrast THIS number against /tasks's page length
