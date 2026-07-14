"""Example 80: Stateless, Two Workers -- two independent processes sharing only the DB file."""
# => co-05: the culmination of every earlier "co-05 caveat" note scattered across this topic's
# => in-memory examples -- here, TWO SEPARATE OS processes serve requests, and a caller genuinely
# => cannot tell them apart, because neither process holds any state the OTHER doesn't also see

import os  # => co-14: reads the WORKER_PORT env var and resolves DB_PATH relative to this file
import sqlite3  # => co-14: the stdlib DB driver -- the ONLY thing shared between the two processes
from typing import TypedDict  # => co-09: a typed dict shape for what the repository returns

from fastapi import FastAPI, HTTPException  # => co-03: HTTPException raises the 404 branch below
from pydantic import BaseModel  # => co-10: validates the POST request body's shape
# => (the two_workers.sh script below starts TWO of these processes, on ports 8003 and 8004)

# => co-05, co-24: DB_PATH resolves relative to THIS file, so both a process started on port 8003 and
# => a SEPARATE process started on port 8004 -- run from the same directory -- point at the EXACT SAME
# => on-disk file. Nothing in this module is shared between the two processes except that file.
DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

# => co-15: the schema below adds ONE column beyond a plain task table -- handled_by exists purely
# => so this demo can PROVE which process wrote each row, by reading it back from the OTHER process
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    handled_by TEXT NOT NULL
);
"""


class TaskRow(TypedDict):  # => co-14, co-24: the repository's typed return shape --
    # => identical regardless of which of the two processes assembled this particular dict
    id: int  # => matches the schema's INTEGER PRIMARY KEY column
    title: str  # => matches the schema's title column
    handled_by: str  # => matches the schema's handled_by column -- this example's whole proof point


class CreateTask(BaseModel):  # => co-10: POST's expected body shape -- identical regardless of
    # => which of the two processes happens to receive this specific request
    title: str  # => co-10: required -- handled_by is NEVER client-settable, only server-assigned


def init_db_if_absent() -> None:  # => co-05: only the FIRST process to start creates the schema; the
    # => name itself documents the race: whichever process imports this module FIRST wins, harmlessly
    conn = sqlite3.connect(DB_PATH)  # => second process reuses the SAME file, never re-initializing it
    conn.execute(SCHEMA)  # => CREATE TABLE IF NOT EXISTS -- safe to call from either process, any order
    conn.commit()  # => co-14: commits the CREATE TABLE, if this is genuinely the first process to run it
    conn.close()  # => co-14: connections are short-lived here -- opened, used, closed, never held


def get_connection() -> sqlite3.Connection:  # => co-14: the repository's ONLY entry point to the DB
    conn = sqlite3.connect(DB_PATH, timeout=5)  # => a real timeout -- two processes DO contend for the file
    conn.row_factory = sqlite3.Row  # => rows behave like dicts -- readable by column name
    return conn  # => a fresh connection per call -- NEITHER process holds a long-lived connection open


PORT = os.environ.get("WORKER_PORT", "unknown")  # => co-05: identifies WHICH process served a given request
# => purely for this demo's own proof -- a real client never needs to know or care which worker answered


def create_task(title: str) -> TaskRow:  # => co-14: the ONLY state this write produces lives in the DB file
    conn = get_connection()  # => co-14: one connection for both the INSERT and the confirming SELECT
    cursor = conn.execute(  # => co-14: PORT (this PROCESS's own identity) is stamped onto the row itself
        "INSERT INTO tasks (title, handled_by) VALUES (?, ?)", (title, PORT)
    )
    conn.commit()  # => co-14: commits the new row -- durably written to the shared file on disk
    row = conn.execute(  # => co-14: re-reads the row to return its server-assigned id + handled_by
        "SELECT id, title, handled_by FROM tasks WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.close()  # => co-14: closed after both the INSERT and the confirming SELECT finish
    return dict(row)  # type: ignore[return-value]  # => sqlite3.Row -> TaskRow-shaped dict


def get_task(task_id: int) -> TaskRow | None:  # => co-05, co-14: reads the SAME file, regardless of
    conn = get_connection()  # => which process is running THIS particular request
    row = conn.execute(  # => co-14: a single parameterized lookup by primary key
        "SELECT id, title, handled_by FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()  # => co-05: returns the ORIGINAL handled_by, even if a DIFFERENT process reads it now
    conn.close()  # => co-14: closed immediately after this one query
    return dict(row) if row else None  # type: ignore[return-value]  # => None signals "no such id"


init_db_if_absent()  # => co-15: runs at import time in EVERY process -- safe, since CREATE TABLE
# => IF NOT EXISTS is a no-op for whichever process starts second

app = FastAPI()  # => a fresh app -- one instance PER process, sharing nothing but the DB file below
# => (fully self-contained: nothing here is imported from any other example directory)


@app.post("/tasks", status_code=201)  # => co-05: whichever worker RECEIVES this request stamps its
# => OWN port into handled_by, but the resulting row is immediately visible to the OTHER worker too
# => co-05: this handler holds NO in-process cache or dict at all --
# => everything it produces is written to the shared file, never kept in this process's own memory
def post_task(body: CreateTask) -> TaskRow:
    return create_task(body.title)  # => co-24: the handler holds no SQL -- co-24 layering


@app.get("/tasks/{task_id}")  # => co-05, co-24: statelessness means THIS process needs no memory of
def read_task(task_id: int) -> TaskRow:  # => the request that created the row -- the DB file is the
    task = get_task(task_id)  # => only source of truth, shared identically across every worker
    if task is None:  # => co-02: no row exists at this id, in EITHER process's view of the shared file
        raise HTTPException(  # => co-11: structured envelope, matching every other example's shape
            status_code=404,  # => co-03: Not Found -- identical regardless of which process answers
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )
    return task  # => co-05: identical response whether THIS process or the OTHER created the row


@app.get("/whoami")  # => reports which worker port answered -- used only to PROVE two processes are involved
def whoami() -> dict[str, str]:
    return {"port": PORT}  # => co-05: this differs by PROCESS, unlike everything else in a response body
    # => a request to worker A and the SAME request replayed to worker B differ ONLY in this one field
