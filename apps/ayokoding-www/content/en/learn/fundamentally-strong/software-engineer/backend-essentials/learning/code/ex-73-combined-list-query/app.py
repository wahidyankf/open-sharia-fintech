"""Example 73: Combined List Query -- pagination + filter + sort together."""
# => co-19, co-20: Examples 65-72 built pagination, filtering, and sorting SEPARATELY -- this
# => example is the capstone-style proof that all three compose correctly in a single endpoint,
# => without one feature silently breaking another (e.g. total must reflect the FILTER, not ignore it)

import os  # => co-14: used for the DB_PATH lookup and the "start fresh" file check below
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


class Page(TypedDict):  # => co-09, co-19: the SAME envelope shape as Example 67, reused here
    items: list[TaskRow]  # => this page's rows, after filtering AND sorting AND slicing
    total: int  # => co-19, co-20: the FILTERED count -- not the whole 25-row table
    next: int | None  # => co-19: computed against the filtered total, not the unfiltered one


def _seed(conn: sqlite3.Connection) -> None:  # => co-14: builds the SAME deterministic 25-row
    # => dataset used by every pagination/filter/sort example in this topic, so worked-out ids
    # => like "done={2,5,8,...}" stay correct however many of these example directories exist
    statuses = ["todo", "in_progress", "done"]  # => rotates every 3 rows -- index is i % 3
    priorities = ["low", "normal", "high"]  # => rotates every 2 rows via (i // 2) % 3 --
    # => DECORRELATED from status ON PURPOSE, so a combined status+priority filter genuinely
    # => narrows further than either field alone, instead of the two columns moving in lockstep
    rows = [
        (f"task {i}", statuses[i % 3], priorities[(i // 2) % 3], f"2026-07-{i:02d}T00:00:00")
        for i in range(1, 26)  # => the SAME 25-row seed as every other pagination/filter/sort example
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


SortValue = Literal["created_at", "-created_at"]  # => co-20: same closed set as Example 72
_COLUMN_BY_SORT: dict[SortValue, str] = {  # => co-14: the SAME lookup-not-interpolate pattern
    "created_at": "created_at ASC",
    "-created_at": "created_at DESC",
}


def list_page(  # => co-19, co-20: ALL THREE features compose in one repository function --
    # => the order below matters: filter narrows the ROWS, sort orders them, THEN limit/offset slices
    status: str | None,  # => co-20: optional -- None means every status qualifies
    limit: int,  # => co-19: how many rows this page holds, at most
    offset: int,  # => co-19: how many filtered-and-sorted rows to skip before this page starts
    sort: SortValue,  # => co-20: which column/direction orders the result, before slicing happens
) -> Page:
    conn = get_connection()  # => co-14: one connection, reused for both queries this function issues
    clauses: list[str] = []  # => co-14, co-20: the filter half -- still fully parameterized,
    # => identical technique to Example 69, just reused inside a function that also sorts and paginates
    params: list[str] = []  # => co-14: kept in lockstep with `clauses`, exactly like Example 70
    if status is not None:  # => co-20: opt-in, exactly like the standalone filter example
        clauses.append("status = ?")  # => the one filterable column this composed example supports
        params.append(status)  # => co-14: the bound value, positionally matched to the ? above
    where = f" WHERE {' AND '.join(clauses)}" if clauses else ""  # => empty string when unfiltered

    total = int(conn.execute(f"SELECT COUNT(*) FROM tasks{where}", params).fetchone()[0])  # => co-19: total reflects the FILTERED count, not the whole table -- computed with the
    # => SAME where clause and params as the main query below, so the two numbers stay consistent
    order_clause = _COLUMN_BY_SORT[sort]  # => co-20: the sort half -- looked up, never interpolated raw
    cursor = conn.execute(  # => co-14, co-19, co-20: filter, sort, AND paginate in one statement
        f"SELECT id, title, status, priority, created_at FROM tasks{where} ORDER BY {order_clause} LIMIT ? OFFSET ?",  # => co-19: the pagination half, composed last --
        # => SQL applies WHERE, then ORDER BY, then LIMIT/OFFSET, in that fixed evaluation order
        [*params, limit, offset],  # => co-14: filter params FIRST, then limit/offset -- position
        # => must match the ? placeholders' left-to-right order in the SQL string exactly above
    )
    items = [dict(row) for row in cursor.fetchall()]  # type: ignore[misc]  # => sqlite3.Row -> dict
    conn.close()  # => co-14: closed immediately after both queries above finish
    next_offset = offset + limit  # => co-19: identical formula to Example 67, applied to the FILTERED total
    has_more = next_offset < total  # => whether another filtered-and-sorted page exists past this one
    return {  # => co-19, co-20: the SAME Page envelope shape as Example 67, now built from a
        # => query that filtered, sorted, AND paginated in a single round trip to SQLite
        "items": items,  # type: ignore[typeddict-item]  # => this page's slice, after all three steps
        "total": total,  # => co-19, co-20: the FILTERED total -- proves filter+pagination interact correctly
        "next": next_offset if has_more else None,  # => None once the filtered result set is exhausted
    }


init_db()  # => co-15: runs once at import time, before the app starts serving

app = FastAPI()  # => a fresh app -- this example needs no auth, only the composed list mechanism


@app.get("/tasks")  # => co-19, co-20: this example's focus -- all three composed in one call --
# => every query param below is INDEPENDENTLY optional, exactly matching its own standalone example
def get_tasks(
    status: str | None = Query(default=None),  # => co-20: same as Example 69
    limit: int = Query(default=10, ge=1, le=50),  # => co-19: same bounds as Example 68
    offset: int = Query(default=0, ge=0),  # => co-19: same as Example 65
    sort: SortValue = Query(default="created_at"),  # => co-20: same as Example 72
) -> Page:
    # => co-24: four independently-optional parameters, one delegated call -- zero SQL in this handler
    return list_page(status, limit, offset, sort)  # => co-24: the handler holds no SQL at all
