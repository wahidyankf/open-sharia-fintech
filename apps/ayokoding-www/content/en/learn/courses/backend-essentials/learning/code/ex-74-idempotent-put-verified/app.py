"""Example 74: Idempotent PUT, Verified -- the same PUT applied twice leaves the same state."""
# => co-02: RFC 9110 CLASSIFIES PUT as idempotent, but a classification is only a promise --
# => this example actually PROVES it, by calling PUT twice and checking the row count stays 1

import os  # => co-14: used for the DB_PATH lookup and the "start fresh" file check below
import sqlite3  # => co-14: the stdlib DB driver -- no ORM, no extra dependency needed
from typing import TypedDict  # => co-09: a typed dict shape for what the repository returns

from fastapi import FastAPI, HTTPException  # => co-03: HTTPException raises the 404 branch below
from pydantic import BaseModel  # => co-10: validates the PUT request body's shape
# => (fully self-contained: nothing here is imported from any other example directory)

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")  # => co-14: one on-disk SQLite file,
# => PER EXAMPLE DIRECTORY -- never shared with any other example, keeping this one self-contained

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL
);
"""  # => co-15: a DELIBERATELY smaller schema than the pagination examples -- this one is about
# => idempotency, not filtering/sorting, so priority/created_at columns would only be noise here


class TaskRow(TypedDict):  # => co-14, co-24: the repository's typed return shape
    id: int  # => matches the schema's INTEGER PRIMARY KEY column
    title: str  # => matches the schema's title column
    status: str  # => matches the schema's status column


class TaskUpdate(BaseModel):  # => co-02, co-10: PUT REPLACES the full resource with this exact shape --
    # => unlike PATCH, there is no "only send the fields you're changing" option with PUT
    title: str  # => required -- omitting it entirely is a 422, not a partial update
    status: str  # => required -- same rule as title above


def init_db() -> None:  # => co-15: fresh schema + one seed row every time this module is imported
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)  # => start from a known, deterministic state every run
    conn = sqlite3.connect(DB_PATH)  # => co-14: a plain connection -- no row_factory needed for INSERT
    conn.execute(SCHEMA)  # => co-15: creates the table every query below depends on existing
    conn.execute(  # => co-14: a single-row INSERT, parameterized like every write in this topic
        "INSERT INTO tasks (title, status) VALUES (?, ?)", ("write the report", "todo")
    )  # => a single seed row -- id 1, the ONLY row this example's PUT calls will ever target
    conn.commit()  # => co-14: commits the seed insert
    conn.close()  # => co-14: connections are short-lived here -- opened, used, closed, never held


def get_connection() -> sqlite3.Connection:  # => co-14: the repository's ONLY entry point to the DB
    conn = sqlite3.connect(DB_PATH)  # => co-14: every read/write function below calls THIS helper
    conn.row_factory = sqlite3.Row  # => rows behave like dicts -- readable by column name
    return conn  # => a fresh connection per call -- co-14: no pooling, matches this example's scale


def replace_task(task_id: int, update: TaskUpdate) -> TaskRow:  # => co-02, co-14: PUT's repository
    # => function -- calling this TWICE with the SAME arguments must leave the SAME final state
    conn = get_connection()  # => co-14: one connection, used for the UPDATE and the confirming SELECT
    cursor = conn.execute(  # => co-14: cursor.rowcount tells us WHETHER a row actually matched below
        "UPDATE tasks SET title = ?, status = ? WHERE id = ?",  # => co-14: parameterized, idempotent
        # => by design -- an UPDATE that sets a column to the value it ALREADY holds changes nothing
        (update.title, update.status, task_id),  # => co-14: title, status, THEN the WHERE id last
    )
    # => co-02: nothing above distinguishes "first call" from "second identical call" -- the SQL
    # => itself has no memory of prior invocations, which is precisely what makes it idempotent
    if cursor.rowcount == 0:  # => co-02: RFC 9110 -- PUT may also CREATE; this example only replaces,
        # => so a missing id is treated as a 404 rather than silently inserting a NEW row at that id
        conn.close()  # => co-14: close before raising -- never leak a connection on the error path
        raise HTTPException(status_code=404, detail={"error": {"code": "not_found", "message": "no such task"}})
    conn.commit()  # => co-14: commits the UPDATE -- both the first AND second identical PUT commit here
    row = conn.execute(  # => co-14: re-reads the row to return its CURRENT state to the caller
        "SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    # => co-02: the SECOND PUT's response body is BYTE-IDENTICAL to the first one's -- proof enough
    conn.close()  # => co-14: closed after the confirming SELECT above returns the fresh row
    return dict(row)  # type: ignore[return-value]  # => sqlite3.Row -> TaskRow-shaped dict


def count_tasks() -> int:  # => proves PUT never INSERTS a duplicate row -- used only to verify
    # => idempotency, never called by any route a real client would hit
    conn = get_connection()  # => co-14: a fresh, short-lived connection just for this one scalar query
    total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]  # => co-14: a single scalar query
    conn.close()  # => co-14: closed immediately after reading the single count value
    return int(total)  # => stays 1 no matter how many times /tasks/1 is PUT to below
    # => a NON-idempotent bug here would look like: POST-style INSERT instead of UPDATE, growing this


init_db()  # => co-15: runs once at import time, before the app starts serving

app = FastAPI()  # => a fresh app -- this example needs no auth, only the idempotency proof
# => (co-24: routes, repository, and models all live in this ONE file, deliberately not split up)


@app.put("/tasks/{task_id}")  # => co-02: PUT -- RFC 9110 classifies this method as IDEMPOTENT --
# => this route's curl below calls it TWICE with an identical body to make that promise concrete
def put_task(  # => co-02: task_id comes from the URL PATH, the rest of the state from the BODY
    task_id: int, update: TaskUpdate
) -> TaskRow:
    return replace_task(task_id, update)  # => co-24: the handler holds no SQL -- co-24 layering


@app.get("/tasks/count")  # => a helper endpoint used ONLY to prove no duplicate row was ever created
def get_count() -> dict[str, int]:  # => co-02: called before AND after the two PUTs to compare
    return {"total": count_tasks()}  # => co-02: expected to read 1, both before AND after two PUTs
