"""Example 65: Pagination limit/offset -- GET /tasks?limit=&offset= slices the list."""

import os
import sqlite3
from typing import TypedDict

from fastapi import FastAPI, Query  # => co-12: limit/offset are typed QUERY parameters

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")  # => co-14: a real on-disk SQLite file,
# => one PER EXAMPLE directory -- never shared with any other example, keeping each self-contained

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


class TaskRow(TypedDict):  # => co-14, co-24: the repository's typed return shape
    id: int  # => matches the schema's INTEGER PRIMARY KEY column
    title: str  # => matches the schema's title column
    status: str  # => matches the schema's status column
    priority: str  # => matches the schema's priority column
    created_at: str  # => matches the schema's created_at column


def _seed(conn: sqlite3.Connection) -> None:
    statuses = ["todo", "in_progress", "done"]  # => rotates every 3 rows -- index is i % 3
    priorities = ["low", "normal", "high"]  # => rotates every 2 rows via (i // 2) % 3 -- DECORRELATED
    # => from status ON PURPOSE, so that filtering by BOTH fields together (Example 70) genuinely
    # => narrows the result further than either single filter alone, instead of the two columns
    # => always moving in lockstep (which would make a combined filter demonstrate nothing new)
    rows = [
        (f"task {i}", statuses[i % 3], priorities[(i // 2) % 3], f"2026-07-{i:02d}T00:00:00")
        for i in range(1, 26)  # => 25 rows -- enough to make a small page window visibly DIFFERENT
        # => from the full list, unlike a 1-2 row toy dataset where pagination wouldn't be provable
    ]
    conn.executemany(  # => co-14: a single batched INSERT for all 25 rows, one transaction
        "INSERT INTO tasks (title, status, priority, created_at) VALUES (?, ?, ?, ?)",  # => co-14: ?
        # => placeholders -- the SAME parameterization principle Example 71 stress-tests directly
        rows,
    )
    conn.commit()  # => co-14: commits the whole seed batch at once


def init_db() -> None:  # => co-15: fresh schema + seed data every time this module is imported
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)  # => start from a known, deterministic state -- this example's expected
        # => row counts and ids only hold true starting from a CLEAN file, never an accumulated one
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)  # => co-15: creates the table every query below depends on existing
    _seed(conn)  # => populates it with the 25-row deterministic dataset described above
    conn.close()  # => co-14: connections are short-lived here -- opened, used, closed, never held


def get_connection() -> sqlite3.Connection:  # => co-14: the repository's ONLY entry point to the DB --
    # => every query function below calls THIS instead of sqlite3.connect() directly
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # => rows behave like dicts -- readable by column name, which is
    # => what makes `dict(row)` below produce sensible {"id":..., "title":...} keys, not just a tuple
    return conn  # => a fresh connection per call -- co-14: no pooling, matches this example's scale


def list_tasks(limit: int, offset: int) -> list[TaskRow]:  # => co-14, co-19: the repository function itself
    # => owns 100% of the SQL for this example -- co-24: the ONLY place LIMIT/OFFSET semantics live
    conn = get_connection()
    cursor = conn.execute(  # => co-14: LIMIT/OFFSET are parameterized, never string-interpolated --
        # => an f-string here would reopen the exact SQL-injection risk Example 71 stress-tests
        "SELECT id, title, status, priority, created_at FROM tasks ORDER BY id LIMIT ? OFFSET ?",
        (limit, offset),  # => co-19: THIS example's core mechanism -- limit caps the page size,
        # => offset skips ahead -- the exact two numbers a caller controls via query params below
    )  # => co-15: ORDER BY id keeps page boundaries STABLE across calls -- without an explicit
    # => order, SQLite offers no guarantee that repeated queries return rows in the same sequence
    result = [dict(row) for row in cursor.fetchall()]  # type: ignore[misc]  # => sqlite3.Row -> plain dict
    conn.close()  # => co-14: closed immediately after this one query -- no connection pooling needed here
    return result  # type: ignore[return-value]  # => shape matches TaskRow at runtime


init_db()  # => co-15: runs once at import time, before the app starts serving -- every curl call
# => below sees the SAME 25-row dataset, since nothing in this example ever re-seeds mid-run

app = FastAPI()  # => a fresh app -- this example needs no auth, only the pagination mechanism


@app.get("/tasks")  # => co-19: the paginated list endpoint this whole example is about --
# => FastAPI parses `?limit=&offset=` from the URL and hands them to this function as plain ints
def get_tasks(
    limit: int = Query(default=10, ge=1),  # => co-12: a typed, constrained query parameter --
    # => ge=1 rejects zero/negative limits before the handler body ever runs (co-10) --
    # => a caller who omits `?limit=` entirely gets the default of 10, proven by Example 66
    offset: int = Query(default=0, ge=0),  # => co-12: how many rows to skip before the page starts --
    # => ge=0 rejects a negative offset the same way limit rejects a non-positive value above
) -> list[TaskRow]:
    return list_tasks(limit, offset)  # => co-19: the handler holds NO SQL -- co-24 layering --
    # => every subsequent pagination/filter/sort example in this topic reuses this exact split:
    # => a thin route function delegating to a repository function that owns the actual query
