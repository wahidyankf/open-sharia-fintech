"""Capstone: the hardened task API -- routing, validation, errors, repository, auth, pagination.

Run with: uvicorn app.main:app --port 8000  (this doc's canonical prose port; the capstone's own
verification run in this topic used other ports to avoid colliding with other locally running
servers -- see the transcripts below for the exact port each one used).

This module takes the Backend-Essentials capstone app and hardens it end to end: a real
argon2id-backed /auth/register + /auth/login (co-09, co-10) issuing a signed, expiring bearer
token (co-11, co-12, co-17) that write routes now require instead of a hardcoded string; a
parameterized /tasks/search (co-03) replacing a naive f-string version; an autoescaped HTML
/tasks/{id}/view (co-06) replacing raw string interpolation; and a security-headers middleware
(co-19) stamping every response. Every other route (health, ready, CRUD, pagination) is
UNCHANGED from Backend-Essentials -- hardening this app never meant rewriting what already worked.
"""

import os
import sqlite3
from collections.abc import Iterator
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from . import auth
from . import repository as repo
from .middleware import make_token_check_middleware, security_headers_middleware
from .models import (
    Task,
    TaskCreate,
    TaskPage,
    TaskUpdate,
    TokenResponse,
    UserLogin,
    UserPublic,
    UserRegister,
)

DB_PATH = os.environ.get(  # => overridable so tests can point at a fresh, isolated file
    "CAPSTONE_DB_PATH", os.path.join(os.path.dirname(__file__), "tasks.db")
)
AUTH_SECRET = os.environ[
    "CAPSTONE_AUTH_SECRET"
]  # => co-17: REQUIRED, no hardcoded fallback --
# => this line raises KeyError and refuses to start if the secret is missing, by design

repo.init_db(DB_PATH)  # => applies schema.sql once, at import/startup time

app = FastAPI(title="Capstone Task API (Hardened)")
templates = Jinja2Templates(
    directory=str(Path(__file__).parent / "templates")
)  # => co-06: autoescaping loader


def get_db() -> Iterator[
    sqlite3.Connection
]:  # => one connection per request, dependency-injected
    conn = repo.get_connection(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def _resolve_token(
    token: str,
) -> int | None:  # => co-17: the ONE place AUTH_SECRET is actually used
    return auth.resolve_token(token, AUTH_SECRET)


app.middleware("http")(
    make_token_check_middleware(_resolve_token)
)  # => co-12: guards every write
app.middleware("http")(
    security_headers_middleware
)  # => co-19: stamps every response, success or error


@app.exception_handler(
    HTTPException
)  # => co-23: one consistent {"error": {...}} envelope, app-wide
async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    body = (
        exc.detail
        if isinstance(exc.detail, dict)
        else {"error": {"code": "error", "message": str(exc.detail)}}
    )
    return JSONResponse(status_code=exc.status_code, content=body)


@app.get("/health")  # => LIVENESS -- always 200, no DB dependency at all (unchanged)
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")  # => READINESS -- genuinely pings the database (unchanged)
def ready(
    response: Response, conn: sqlite3.Connection = Depends(get_db)
) -> dict[str, str]:
    try:
        repo.ping(conn)
        return {"status": "ready"}
    except sqlite3.OperationalError as exc:
        response.status_code = 503
        return {"status": "not_ready", "reason": str(exc)}


@app.post(
    "/auth/register", response_model=UserPublic, status_code=201
)  # => co-07, co-09: NEW
def register_route(
    body: UserRegister, conn: sqlite3.Connection = Depends(get_db)
) -> UserPublic:
    existing = repo.get_user_by_username(conn, body.username)
    if (
        existing is not None
    ):  # => co-23: a specific, honest conflict -- distinct from login's generic error
        raise HTTPException(
            status_code=409,
            detail={"error": {"code": "conflict", "message": "username already taken"}},
        )
    password_hash = auth.hash_password(
        body.password
    )  # => co-09: hash BEFORE it ever touches the DB
    return repo.create_user(conn, body.username, password_hash)


@app.post("/auth/login", response_model=TokenResponse)  # => co-09, co-11, co-12: NEW
def login_route(
    body: UserLogin, conn: sqlite3.Connection = Depends(get_db)
) -> TokenResponse:
    row = repo.get_user_by_username(conn, body.username)
    generic_error = HTTPException(  # => co-23: SAME message for "no such user" and "wrong password" --
        status_code=401,  # => an attacker probing usernames learns nothing from the response either way
        detail={
            "error": {"code": "unauthorized", "message": "invalid username or password"}
        },
    )
    if row is None:
        raise generic_error
    if not auth.verify_password(str(row["password_hash"]), body.password):
        raise generic_error
    token = auth.issue_token(int(row["id"]), AUTH_SECRET)  # => co-12, co-17
    return TokenResponse(access_token=token)


@app.post(
    "/tasks", response_model=Task, status_code=201
)  # => guarded (a WRITE) -- unchanged
def create_task_route(
    body: TaskCreate, conn: sqlite3.Connection = Depends(get_db)
) -> Task:
    return repo.create_task(conn, body)


@app.get(
    "/tasks/search", response_model=list[Task]
)  # => co-03: NEW, and registered BEFORE
def search_tasks_route(  # => /tasks/{task_id} below -- otherwise FastAPI would try to parse
    q: str = Query(default="", max_length=200),
    conn: sqlite3.Connection = Depends(get_db),
) -> list[
    Task
]:  # => "search" as an int task_id and 422 before ever reaching this route
    return repo.search_tasks(
        conn, q
    )  # => co-03: the FIXED, parameterized version -- see repository.py


@app.get("/tasks/{task_id}/view", response_class=HTMLResponse)  # => co-06: NEW
def view_task_route(
    task_id: int, request: Request, conn: sqlite3.Connection = Depends(get_db)
) -> HTMLResponse:
    task = repo.get_task(conn, task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )
    return templates.TemplateResponse(
        request, "task_view.html", {"task": task}
    )  # => co-06: autoescaped


@app.get(
    "/tasks/{task_id}", response_model=Task
)  # => read -- OPEN, no token required (unchanged)
def read_task_route(task_id: int, conn: sqlite3.Connection = Depends(get_db)) -> Task:
    task = repo.get_task(conn, task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )
    return task


@app.put(
    "/tasks/{task_id}", response_model=Task
)  # => replace -- guarded (a WRITE), unchanged
def update_task_route(
    task_id: int, body: TaskUpdate, conn: sqlite3.Connection = Depends(get_db)
) -> Task:
    updated = repo.update_task(conn, task_id, body)
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )
    return updated


@app.delete(
    "/tasks/{task_id}", status_code=204
)  # => delete -- guarded (a WRITE), unchanged
def delete_task_route(task_id: int, conn: sqlite3.Connection = Depends(get_db)) -> None:
    if not repo.delete_task(conn, task_id):
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )


@app.get(
    "/tasks", response_model=TaskPage
)  # => pagination + filtering -- OPEN, no token, unchanged
def list_tasks_route(
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    status: str | None = Query(default=None),
    conn: sqlite3.Connection = Depends(get_db),
) -> TaskPage:
    return repo.list_tasks(conn, limit, offset, status)
