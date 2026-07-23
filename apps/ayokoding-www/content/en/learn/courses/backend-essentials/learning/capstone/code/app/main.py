"""Capstone: a small HTTP JSON task API -- routing, validation, errors, repository, auth, pagination.

Run with: uvicorn app.main:app --port 8000  (this doc's canonical prose port; the capstone's own
verification run in this topic used --port 8003 to avoid colliding with other locally running examples).
"""

import os
import sqlite3
from collections.abc import Iterator

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse

from . import repository as repo
from .middleware import token_check_middleware
from .models import Task, TaskCreate, TaskPage, TaskUpdate

DB_PATH = os.environ.get(  # => co-14: overridable so tests/readiness-down demos can point elsewhere
    "CAPSTONE_DB_PATH", os.path.join(os.path.dirname(__file__), "tasks.db")
)

repo.init_db(DB_PATH)  # => co-15: applies schema.sql once, at import/startup time

app = FastAPI(title="Capstone Task API")
app.middleware("http")(token_check_middleware)  # => co-16, co-18: guards every write, as documented above


def get_db() -> Iterator[sqlite3.Connection]:  # => co-23: dependency injection -- one connection/request
    conn = repo.get_connection(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


@app.exception_handler(HTTPException)  # => co-11: one consistent {"error": {...}} envelope, app-wide
async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    body = exc.detail if isinstance(exc.detail, dict) else {"error": {"code": "error", "message": str(exc.detail)}}
    return JSONResponse(status_code=exc.status_code, content=body)


@app.get("/health")  # => co-08: LIVENESS -- always 200, no DB dependency at all
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")  # => co-08, co-14: READINESS -- genuinely pings the database
def ready(response: Response, conn: sqlite3.Connection = Depends(get_db)) -> dict[str, str]:
    try:
        repo.ping(conn)
        return {"status": "ready"}
    except sqlite3.OperationalError as exc:
        response.status_code = 503
        return {"status": "not_ready", "reason": str(exc)}


@app.post("/tasks", response_model=Task, status_code=201)  # => co-02, co-03, co-10: create -- guarded
def create_task_route(  # => by the middleware above, since this is a WRITE
    body: TaskCreate, conn: sqlite3.Connection = Depends(get_db)
) -> Task:
    return repo.create_task(conn, body)


@app.get("/tasks/{task_id}", response_model=Task)  # => co-02, co-12: read -- OPEN, no token required
def read_task_route(task_id: int, conn: sqlite3.Connection = Depends(get_db)) -> Task:
    task = repo.get_task(conn, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"error": {"code": "not_found", "message": "no such task"}})
    return task


@app.put("/tasks/{task_id}", response_model=Task)  # => co-02: replace -- guarded (a WRITE)
def update_task_route(task_id: int, body: TaskUpdate, conn: sqlite3.Connection = Depends(get_db)) -> Task:
    updated = repo.update_task(conn, task_id, body)
    if updated is None:
        raise HTTPException(status_code=404, detail={"error": {"code": "not_found", "message": "no such task"}})
    return updated


@app.delete("/tasks/{task_id}", status_code=204)  # => co-02, co-03: delete -- guarded (a WRITE)
def delete_task_route(task_id: int, conn: sqlite3.Connection = Depends(get_db)) -> None:
    if not repo.delete_task(conn, task_id):
        raise HTTPException(status_code=404, detail={"error": {"code": "not_found", "message": "no such task"}})


@app.get("/tasks", response_model=TaskPage)  # => co-19, co-20: pagination + filtering -- OPEN, no token
def list_tasks_route(
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    status: str | None = Query(default=None),
    conn: sqlite3.Connection = Depends(get_db),
) -> TaskPage:
    return repo.list_tasks(conn, limit, offset, status)
