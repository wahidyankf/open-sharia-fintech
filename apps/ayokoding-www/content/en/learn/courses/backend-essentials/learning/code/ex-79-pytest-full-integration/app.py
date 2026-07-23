"""Example 79: pytest Full Integration -- CRUD + token auth + pagination, one target app."""
# => co-14, co-18, co-19: this file combines EVERY major mechanism from this topic's advanced
# => tier into a single app -- the companion test_app.py is the fullest pytest suite in this
# => topic precisely because it verifies all three areas (CRUD, auth, pagination) genuinely coexist

import os  # => co-14: used for the DB_PATH lookup and the "start fresh" file check below

# => co-02: every route maps to exactly one HTTP verb -- POST create, GET read, PUT replace,
# => DELETE remove, plus a second GET for the paginated list -- the full set this topic covers
import sqlite3  # => co-14: the stdlib DB driver -- no ORM, no extra dependency needed
from typing import TypedDict  # => co-09: typed dict shapes for what the repository returns

from fastapi import Depends, FastAPI, HTTPException, Query, Request  # => co-23: Depends wires auth in
from fastapi.responses import JSONResponse  # => co-11: builds the exception handler's structured body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # => co-18: parses "Bearer <token>"
from pydantic import BaseModel  # => co-10: validates both the create and update request bodies
# => co-24: routes, repository, and models all live in this ONE file, deliberately not split up

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")  # => co-14: one on-disk SQLite file,
# => PER EXAMPLE DIRECTORY -- never shared with any other example, keeping this one self-contained

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'todo'
);
"""  # => co-15: DEFAULT 'todo' means a bare INSERT (title only) still produces a valid row


class TaskRow(TypedDict):  # => co-14, co-24: the repository's typed return shape
    id: int  # => matches the schema's INTEGER PRIMARY KEY column
    title: str  # => matches the schema's title column
    status: str  # => matches the schema's status column, defaulted server-side on create


class Page(TypedDict):  # => co-09, co-19: the SAME envelope shape used by the pagination examples
    items: list[TaskRow]  # => this page's rows, after any status filter and the limit/offset slice
    total: int  # => co-19, co-20: the FILTERED count -- not necessarily the whole table
    next: int | None  # => None means "no further page" -- a real, typed sentinel


class CreateTask(BaseModel):  # => co-10: POST's expected body shape -- deliberately narrow --
    # => a client cannot set a task's status at creation time; the schema's DEFAULT handles that
    title: str  # => co-10: required -- status is never client-settable at creation time


class UpdateTask(BaseModel):  # => co-02, co-10: PUT REPLACES the full resource with this exact shape
    title: str  # => required, same rule as CreateTask above
    status: str  # => required -- PUT (unlike POST) DOES let the caller set status explicitly
    # => (an invalid status value like "not_a_real_status" is still a plain str at this layer --
    # => nothing in this simplified example restricts it to a closed set of allowed values)


def init_db() -> None:  # => co-15: fresh schema every time this module is imported
    if os.path.exists(DB_PATH):  # => co-15: true on every run after the first, since nothing else
        # => in this example removes tasks.db besides this check itself
        os.remove(DB_PATH)  # => start from a known, deterministic state -- an empty table every run
    conn = sqlite3.connect(DB_PATH)  # => co-14: a plain connection -- no row_factory needed for DDL
    conn.execute(SCHEMA)  # => co-15: creates the table every repository function below depends on
    conn.commit()  # => co-14: commits the CREATE TABLE
    conn.close()  # => co-14: connections are short-lived here -- opened, used, closed, never held


def get_connection() -> sqlite3.Connection:  # => co-14: the repository's ONLY entry point to the DB
    conn = sqlite3.connect(DB_PATH)  # => co-14: every repository function below calls THIS helper
    conn.row_factory = sqlite3.Row  # => rows behave like dicts -- readable by column name
    return conn  # => a fresh connection per call -- co-14: no pooling, matches this example's scale


def create_task(title: str) -> TaskRow:  # => co-14: repository create -- the "C" of CRUD
    conn = get_connection()  # => co-14: one connection for both the INSERT and the confirming SELECT
    cursor = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))  # => co-14: parameterized
    conn.commit()  # => co-14: commits the new row before reading it back below
    row = conn.execute(  # => co-14: re-reads the row to return its server-assigned id + default status
        "SELECT id, title, status FROM tasks WHERE id = ?",
        (cursor.lastrowid,),  # => cursor.lastrowid
    ).fetchone()  # => co-14: the just-inserted row, guaranteed to exist immediately after commit
    conn.close()  # => co-14: closed after both the INSERT and the confirming SELECT finish
    return dict(row)  # type: ignore[return-value]  # => sqlite3.Row -> TaskRow-shaped dict


def get_task(task_id: int) -> TaskRow | None:  # => co-14: repository read -- the "R" of CRUD
    conn = get_connection()  # => co-14: opened just for this one read
    row = conn.execute(  # => co-14: a single parameterized lookup by primary key
        "SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()  # => co-14: None if the id doesn't exist, a Row if it does
    conn.close()  # => co-14: closed immediately after this one query
    return dict(row) if row else None  # type: ignore[return-value]  # => None signals "no such id"


def update_task(task_id: int, title: str, status: str) -> TaskRow | None:  # => co-14: repository
    # => update -- the "U" of CRUD, backing this example's PUT route
    conn = get_connection()  # => co-14: one connection for the UPDATE and the confirming SELECT
    cursor = conn.execute(  # => co-14: parameterized UPDATE, matching this topic's convention throughout
        "UPDATE tasks SET title = ?, status = ? WHERE id = ?",
        (title, status, task_id),  # => co-14
    )  # => co-14: cursor.rowcount below reveals whether this actually matched a row
    if cursor.rowcount == 0:  # => co-02: no row matched this id -- the route maps this to a 404
        conn.close()  # => co-14: close before returning -- never leak a connection on this path
        return None  # => co-02: signals "not found" up to the route, which raises the actual 404
    conn.commit()  # => co-14: commits the UPDATE now that we know a row genuinely matched
    row = conn.execute(  # => co-14: re-reads the row to return its post-update state to the caller
        "SELECT id, title, status FROM tasks WHERE id = ?",
        (task_id,),  # => co-14: same id as the UPDATE
    ).fetchone()  # => co-14: guaranteed non-None -- we just confirmed rowcount > 0 above
    conn.close()  # => co-14: closed after the confirming SELECT returns the fresh row
    return dict(row)  # type: ignore[return-value]  # => sqlite3.Row -> TaskRow-shaped dict


def delete_task(task_id: int) -> bool:  # => co-14: repository delete -- the "D" of CRUD
    conn = get_connection()  # => co-14: opened just for this one DELETE
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))  # => co-14: parameterized DELETE
    conn.commit()  # => co-14: commits regardless of whether a row actually matched
    conn.close()  # => co-14: closed immediately after the DELETE commits
    return cursor.rowcount > 0  # => co-02: True only if a row genuinely existed and was removed


def list_page(  # => co-19, co-20: full pagination+filter -- the SAME repository shape as the
    limit: int,  # => co-19: how many rows this page holds, at most
    offset: int,  # => co-19: how many filtered rows to skip before this page starts
    status: str | None,  # => co-20: optional -- None means every status qualifies
) -> Page:
    conn = get_connection()  # => co-14: one connection for both queries this function issues
    where = " WHERE status = ?" if status is not None else ""  # => co-20: opt-in, exactly like the
    # => standalone filter example -- an empty string here reproduces the fully unfiltered query
    params: list[str] = [status] if status is not None else []  # => co-14: kept in lockstep with `where`
    total = int(  # => co-19: the FILTERED count, computed with the SAME where clause and params
        conn.execute(f"SELECT COUNT(*) FROM tasks{where}", params).fetchone()[0]
    )  # => co-19: so the two numbers -- total and items -- stay consistent with each other
    cursor = conn.execute(  # => co-14, co-19, co-20: filter AND paginate in a single statement
        f"SELECT id, title, status FROM tasks{where} ORDER BY id LIMIT ? OFFSET ?",  # => co-15:
        # => ORDER BY id keeps page boundaries STABLE across repeated calls with the same params
        [*params, limit, offset],  # => co-14: filter params FIRST, then limit/offset, in that order
    )
    items = [dict(row) for row in cursor.fetchall()]  # type: ignore[misc]  # => sqlite3.Row -> dict
    conn.close()  # => co-14: closed immediately after both queries above finish
    next_offset = offset + limit  # => co-19: the offset a client would use to fetch the FOLLOWING page
    return {  # => co-19, co-20: the SAME Page envelope shape as the standalone pagination example
        "items": items,  # type: ignore[typeddict-item]  # => this page's slice, after filter+paginate
        "total": total,  # => co-19, co-20: the FILTERED total -- proves filter+pagination interact correctly
        "next": next_offset if next_offset < total else None,  # => None once the filtered set is exhausted
    }


init_db()  # => co-15: runs once at import time, before the app starts serving

app = FastAPI()  # => a fresh app -- routes below wire every repository function above to HTTP
# => (fully self-contained: nothing here is imported from any other example directory)

VALID_TOKEN = "s3cr3t-token-abc123"  # => hardcoded stand-in for a real signed/opaque token
# => (the SAME literal constant test_app.py's TestTokenAuth class asserts against below)
security = HTTPBearer(auto_error=False)  # => auto_error=False: WE own the 401 body's shape below


@app.exception_handler(HTTPException)  # => co-11: consistent envelope across every error this app
# => returns -- unwraps FastAPI's default {"detail": ...} nesting into the flat {"error": {...}} shape
async def handle_http_exception(  # => co-11: registered ONCE, catches every HTTPException app-wide
    request: Request, exc: HTTPException
) -> JSONResponse:
    body = (  # => co-11: normalizes whatever a route raised into ONE consistent envelope shape
        exc.detail  # => co-11: already a dict -- every raise in this file supplies one directly
        if isinstance(exc.detail, dict)  # => every raise below already supplies a dict
        else {"error": {"code": "error", "message": str(exc.detail)}}  # => fallback for a plain string
    )
    return JSONResponse(status_code=exc.status_code, content=body)  # => co-11: same shape, every error


def require_token(  # => co-18, co-23: guards every WRITE below -- reused via Depends() per route
    credentials: HTTPAuthorizationCredentials | None = Depends(security),  # => co-23: resolved BEFORE
    # => the guarded route's own handler body ever runs
) -> None:  # => co-23: returns nothing -- FastAPI only cares whether this raises or not
    if credentials is None or credentials.credentials != VALID_TOKEN:  # => co-18: either failure mode
        raise HTTPException(  # => co-11: structured envelope, matching every other error in this app
            status_code=401,  # => co-03: 401 Unauthorized -- "who you claim to be" was rejected
            detail={"error": {"code": "unauthorized", "message": "missing or invalid token"}},
        )
    # => co-18: reaching the end of this function without raising IS the "allowed" outcome --
    # => FastAPI just runs it for its side effect, and discards the None it returns


@app.post("/tasks", status_code=201, dependencies=[Depends(require_token)])  # => co-02, co-03, co-18:
# => CREATE -- a WRITE, so it's guarded; 201 signals a new resource now exists at the returned id
def post_task(body: CreateTask) -> TaskRow:  # => co-10: body already validated against CreateTask
    return create_task(body.title)  # => co-24: the handler holds no SQL -- co-24 layering


@app.get("/tasks/{task_id}")  # => co-02: reads stay OPEN, no token required
def read_task(task_id: int) -> TaskRow:  # => co-02: no dependencies=[...] list at all -- unguarded
    task = get_task(task_id)  # => co-24: delegates straight to the repository, no logic in between
    if task is None:  # => co-02: no row exists at this id
        raise HTTPException(  # => co-11: structured envelope, matching every other error in this app
            status_code=404,  # => co-03: Not Found -- the id is well-formed, just nonexistent
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )
    return task  # => co-24: the same TaskRow shape create_task returned on the way in
    # => this route is called between the CREATE and UPDATE steps in test_app.py's CRUD test


@app.put("/tasks/{task_id}", dependencies=[Depends(require_token)])  # => co-02, co-18: REPLACE --
# => a WRITE, so it's guarded; RFC 9110 classifies PUT as idempotent, unlike POST above
def put_task(task_id: int, body: UpdateTask) -> TaskRow:  # => co-02: id from the PATH, state from the BODY
    updated = update_task(task_id, body.title, body.status)  # => co-24: no SQL in this handler either
    if updated is None:  # => co-02: no row matched -- this example's PUT only replaces, never creates
        raise HTTPException(  # => co-11: structured envelope, matching every other error in this app
            status_code=404,  # => co-03: Not Found -- consistent with read_task's 404 above
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )
    return updated  # => co-24: the fresh, post-update row state
    # => co-18: reaching here at all already proves the caller passed the require_token dependency


@app.delete("/tasks/{task_id}", status_code=204, dependencies=[Depends(require_token)])  # => co-02,
# => co-03, co-18: DELETE -- a WRITE, so it's guarded; 204 carries no response body on success
def remove_task(task_id: int) -> None:  # => co-02: None return type -- 204 forbids a response body
    if not delete_task(task_id):  # => co-02: nothing matched this id -- report 404, not a silent no-op
        raise HTTPException(  # => co-11: structured envelope, matching every other error in this app
            status_code=404,  # => co-03: Not Found -- the SAME code every other missing-id error uses
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )
    # => co-02: a successful DELETE falls through here with nothing to return -- FastAPI sends 204


@app.get("/tasks")  # => co-19, co-20: pagination + filtering, open to everyone -- reads NEVER
# => require a token in this app, exactly matching the earlier standalone pagination/filter examples
def list_tasks(
    limit: int = Query(default=10, ge=1, le=50),  # => co-19: same bounds as the standalone example
    offset: int = Query(default=0, ge=0),  # => co-19: same default-when-absent behavior
    status: str | None = Query(default=None),  # => co-20: independently optional, same as elsewhere
) -> Page:
    return list_page(limit, offset, status)  # => co-24: the handler holds no SQL at all
