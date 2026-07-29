"""Capstone async FastAPI service -- routing, DI, errors, streaming, config, logging (co-01 to co-24).

Run with: uvicorn app.main:app --port 8000  (from learning/capstone/code/).
"""

import asyncio  # => asyncio drives the streaming generator (co-22)
import logging  # => structured logging (co-24)
import os
import time
from collections.abc import AsyncIterator, Awaitable, Callable

import aiosqlite  # => the async driver -- the DB session type (co-16)
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Request,
)  # => DI + routing + errors (co-10, co-15, co-17)
from fastapi.responses import (
    JSONResponse,
    Response,
    StreamingResponse,
)  # => streaming + error envelope (co-17, co-22)
from pydantic_settings import BaseSettings, SettingsConfigDict  # => env config (co-24)

from . import repository as repo
from .models import Task, TaskCreate, TaskPage, TaskUpdate

logging.basicConfig(
    level=logging.INFO, format="%(message)s"
)  # => one line per record (co-24)
logger = logging.getLogger("capstone")  # => a named logger


class Settings(BaseSettings):  # => typed config from env (co-24)
    model_config = SettingsConfigDict(env_prefix="CAPSTONE_")  # => CAPSTONE_ prefix
    db_path: str = os.path.join(
        os.path.dirname(__file__), "capstone.db"
    )  # => overridable so tests use a temp DB
    env: str = "dev"


settings = Settings()  # => resolved once at startup (co-24)


async def init_at_startup() -> (
    None
):  # => apply schema once before serving (co-18, co-16)
    await repo.init_db(settings.db_path)


app = FastAPI(
    title="Capstone Async FastAPI Service", on_startup=[init_at_startup]
)  # => co-18 startup hook


@app.exception_handler(
    HTTPException
)  # => one consistent {"error": {...}} envelope app-wide (co-17)
async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    _ = request  # => available for logging, unused in the mapping
    body = (
        exc.detail
        if isinstance(exc.detail, dict)
        else {"error": {"code": "error", "message": str(exc.detail)}}
    )
    return JSONResponse(status_code=exc.status_code, content=body)


@app.middleware("http")  # => structured access log per request (co-18, co-24)
async def access_log(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time.perf_counter()  # => baseline
    response: Response = await call_next(request)  # => run the handler
    logger.info(  # => structured: fixed keys, machine-parseable (co-24)
        "method=%s path=%s status=%d ms=%.3f",
        request.method,
        request.url.path,
        response.status_code,
        (time.perf_counter() - start) * 1000,
    )
    return response


async def get_db() -> AsyncIterator[
    aiosqlite.Connection
]:  # => one async session per request (co-15, co-16)
    conn = await repo.get_connection(settings.db_path)  # => async acquire (co-16)
    try:
        yield conn  # => hand the live session to the handler
    finally:
        await conn.close()  # => close on exit, even if the handler raised (co-15)


@app.get("/health")  # => LIVENESS -- always 200, no DB dependency (co-10)
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")  # => READINESS -- genuinely pings the async DB (co-16)
async def ready(conn: aiosqlite.Connection = Depends(get_db)) -> dict[str, str]:
    await repo.ping(conn)  # => async probe -- yields to the loop (co-16)
    return {"status": "ready"}


@app.post("/tasks", response_model=Task, status_code=201)  # => create (co-17)
async def create_task_route(
    body: TaskCreate, conn: aiosqlite.Connection = Depends(get_db)
) -> Task:
    return await repo.create_task(conn, body)  # => async repository call (co-16)


@app.get("/tasks/{task_id}", response_model=Task)  # => read one, 404 on missing (co-17)
async def read_task_route(
    task_id: int, conn: aiosqlite.Connection = Depends(get_db)
) -> Task:
    task = await repo.get_task(conn, task_id)  # => async SELECT
    if task is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )  # => co-17
    return task


@app.put("/tasks/{task_id}", response_model=Task)  # => replace (co-17)
async def update_task_route(
    task_id: int, body: TaskUpdate, conn: aiosqlite.Connection = Depends(get_db)
) -> Task:
    updated = await repo.update_task(conn, task_id, body)
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )
    return updated


@app.delete("/tasks/{task_id}", status_code=204)  # => delete (co-17)
async def delete_task_route(
    task_id: int, conn: aiosqlite.Connection = Depends(get_db)
) -> None:
    if not await repo.delete_task(conn, task_id):
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such task"}},
        )


@app.get("/tasks", response_model=TaskPage)  # => pagination + filtering (co-11, co-16)
async def list_tasks_route(
    limit: int = Query(default=10, ge=1, le=50),  # => bounded limit (co-11, co-13)
    offset: int = Query(default=0, ge=0),
    status: str | None = Query(default=None),
    conn: aiosqlite.Connection = Depends(get_db),
) -> TaskPage:
    return await repo.list_tasks(conn, limit, offset, status)


async def event_stream() -> AsyncIterator[bytes]:  # => a streaming generator (co-22)
    for i in range(3):  # => three events
        await asyncio.sleep(0.01)  # => pace the stream (co-02)
        yield f"data: event {i}\n\n".encode(
            "utf-8"
        )  # => one SSE-shaped chunk per yield (co-22)


@app.get("/events")  # => the streaming endpoint (co-22)
async def events() -> StreamingResponse:
    return StreamingResponse(
        event_stream(), media_type="text/event-stream"
    )  # => incremental SSE
