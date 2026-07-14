"""Example 71: Filter Parameterized SQL -- an injection attempt is neutralized."""
# => co-14, co-20: every other pagination/filter example in this topic ALREADY parameterizes
# => its SQL -- this example is the one that proves WHY, by showing the vulnerable alternative

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
    rows = [(f"task {i}", statuses[i % 3], priorities[(i // 2) % 3], f"2026-07-{i:02d}T00:00:00") for i in range(1, 26)]
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


def list_tasks_safe(status: str) -> list[TaskRow]:  # => co-14, co-20: the SAFE, parameterized version --
    # => this is the ONLY function this example's route actually calls, further down
    conn = get_connection()
    cursor = conn.execute(  # => co-14: the value is bound as a PARAMETER, never concatenated into the SQL
        "SELECT id, title, status, priority, created_at FROM tasks WHERE status = ? ORDER BY id",
        (status,),  # => sqlite3 sends this as DATA, not as part of the SQL grammar at all -- an
        # => injection payload like `done' OR '1'='1` is just a literal STRING being compared here
    )
    result = [dict(row) for row in cursor.fetchall()]  # type: ignore[misc]  # => sqlite3.Row -> dict
    conn.close()  # => co-14: closed immediately after this one query
    return result  # type: ignore[return-value]  # => empty list when no row's status equals the payload


def list_tasks_unsafe_for_demo_only(  # => co-14: the VULNERABLE version -- exists ONLY as a
    status: str,  # => teaching contrast; never called by any route, only by this example's own tests
) -> list[TaskRow]:
    conn = get_connection()
    query = (  # => co-14: string-BUILDING the SQL text itself, not just its parameters
        f"SELECT id, title, status, priority, created_at FROM tasks WHERE status = '{status}' ORDER BY id"
    )
    # => DELIBERATELY f-string-interpolated -- shown ONLY to prove what parameterization prevents,
    # => never something a real handler should do; not wired to any route in this app
    cursor = conn.execute(query)  # => co-14: SQLite parses whatever ends up embedded in `query` as SQL
    result = [dict(row) for row in cursor.fetchall()]  # type: ignore[misc]  # => sqlite3.Row -> dict
    conn.close()  # => co-14: closed immediately after this one query
    return result  # type: ignore[return-value]  # => ALL 25 rows when the payload closes the quote early


init_db()  # => co-15: runs once at import time, before the app starts serving

app = FastAPI()  # => a fresh app -- this example needs no auth, only the safe/unsafe query contrast


@app.get("/tasks")  # => co-20: the ONLY route this app exposes uses the SAFE repository function --
# => `list_tasks_unsafe_for_demo_only` above is reachable only from Python code (like the tests
# => and curl-equivalent script below), never from any HTTP route a real caller could hit
def get_tasks(status: str = Query(...)) -> list[TaskRow]:  # => co-12: required, no default -- omitting
    # => `?status=` entirely is a 422, distinct from THIS example's own scenario of a crafted value
    return list_tasks_safe(status)  # => co-24: the handler always goes through the SAFE path
