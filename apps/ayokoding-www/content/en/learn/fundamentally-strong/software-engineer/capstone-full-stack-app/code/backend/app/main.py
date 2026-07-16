"""Full-stack capstone -- the hardened HTTP JSON API (topic 11) a real browser frontend (topic
14) talks to over CORS-safe HTTP (topic 12), backed by SQLite (topic 10). The security-header
baseline is reused from topic 17 (Security Essentials / Pass-1 Capstone), file-for-file.

Run with: uvicorn app.main:app --port 8120  (this doc's canonical prose port; the actual
verification runs captured on this page may use other ports to avoid colliding with other
locally running servers -- see each transcript for the exact port it used).
"""

import os
import sqlite3
from collections.abc import Iterator

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from . import repository as repo
from .middleware import security_headers_middleware
from .models import Task, TaskCreate, TaskUpdate

# overridable so tests can point at a fresh, isolated file
DB_PATH = os.environ.get(
    "CAPSTONE2_DB_PATH", os.path.join(os.path.dirname(__file__), "tasks.db")
)
# => CORS-safe: an explicit ALLOW-LIST of exactly one origin -- the frontend's own static-file-
# => server origin -- never a wildcard "*"; overridable so tests/other setups can point elsewhere
FRONTEND_ORIGIN = os.environ.get("CAPSTONE2_FRONTEND_ORIGIN", "http://127.0.0.1:8121")

repo.init_db(DB_PATH)  # => applies schema.sql once, at startup

app = FastAPI(title="Full-Stack Capstone: Task API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],  # => allow-list of ONE, never "*"
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Content-Type"],
)
app.middleware("http")(security_headers_middleware)  # stamps every response


def get_db() -> Iterator[sqlite3.Connection]:  # => one connection per request
    conn = repo.get_connection(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


# => registered on Starlette's BASE HTTPException so this one handler also catches exceptions
# => Starlette raises internally (an unmatched route's 404, a wrong HTTP method's 405), not just
# => the ones this app's own routes raise
@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    body = (
        exc.detail
        if isinstance(exc.detail, dict)
        else {"error": {"code": "error", "message": str(exc.detail)}}
    )
    return JSONResponse(status_code=exc.status_code, content=body)


@app.get("/health")  # => LIVENESS -- always 200, no DB dependency at all
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")  # => READINESS -- genuinely pings the database
def ready(
    response: Response, conn: sqlite3.Connection = Depends(get_db)
) -> dict[str, str]:
    try:
        repo.ping(conn)
        return {"status": "ready"}
    except sqlite3.OperationalError as exc:
        response.status_code = 503
        return {"status": "not_ready", "reason": str(exc)}


# => Step 1 of the capstone spec: the CORS-safe read endpoint the frontend's first fetch calls
@app.get("/tasks", response_model=list[Task])
def list_tasks_route(conn: sqlite3.Connection = Depends(get_db)) -> list[Task]:
    return repo.list_tasks(conn)


# => Step 3 of the capstone spec: the create half of the create/update form
@app.post("/tasks", response_model=Task, status_code=201)
def create_task_route(
    body: TaskCreate, conn: sqlite3.Connection = Depends(get_db)
) -> Task:
    return repo.create_task(conn, body)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task_route(task_id: int, conn: sqlite3.Connection = Depends(get_db)) -> Task:
    task = repo.get_task(conn, task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )
    return task


# => Step 3 of the capstone spec: the update half of the create/update form
@app.put("/tasks/{task_id}", response_model=Task)
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
