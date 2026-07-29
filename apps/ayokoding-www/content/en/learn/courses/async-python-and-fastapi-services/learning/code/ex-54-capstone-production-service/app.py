"""Example 54: The Capstone Production Service (advanced-tier preview).

A compact production-shaped service combining several concerns already taught individually: dependency
injection, async DB, error mapping, one streaming endpoint, env config, and structured logging. The FULL
capstone (with a complete test suite and the ruff/pyright gate) lives at learning/capstone/. This example is
the advanced-tier preview of that shape. Run: uvicorn app:app --port 8000. (co-01 to co-24)
"""

import asyncio  # => asyncio drives the streaming generator (co-22)
import logging  # => structured logging (co-24)
import time
from collections.abc import AsyncIterator, Awaitable, Callable

import aiosqlite  # => async DB (co-16)
from fastapi import Depends, FastAPI, HTTPException, Request  # => DI + errors (co-15, co-17)
from fastapi.responses import Response, StreamingResponse  # => streaming (co-22)
from pydantic import BaseModel  # => Pydantic models (co-12)
from pydantic_settings import BaseSettings  # => env config (co-24)

logging.basicConfig(level=logging.INFO, format="%(message)s")  # => one line per record (co-24)
logger = logging.getLogger("capstone")  # => a named logger


class Settings(BaseSettings):  # => env config (co-24)
    db_path: str = "capstone.db"  # => overridable via env
    env: str = "dev"


settings = Settings()  # => resolved once at startup (co-24)
app = FastAPI()  # => the ASGI application uvicorn serves


class NoteIn(BaseModel):  # => body shape (co-12)
    text: str


class Note(BaseModel):  # => response shape (co-14)
    id: int
    text: str


async def get_session() -> AsyncIterator[aiosqlite.Connection]:  # => one session per request (co-15)
    async with aiosqlite.connect(settings.db_path) as db:  # => config-driven DB path (co-24)
        await db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
        await db.commit()
        yield db


@app.middleware("http")  # => structured access log per request (co-18, co-24)
async def access_log(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    start = time.perf_counter()  # => baseline
    response: Response = await call_next(request)  # => run the handler
    logger.info("method=%s path=%s status=%d ms=%.3f", request.method, request.url.path, response.status_code, (time.perf_counter() - start) * 1000)  # => structured (co-24)
    return response


@app.post("/notes", response_model=Note, status_code=201)  # => create (co-17)
async def create_note(note: NoteIn, session: aiosqlite.Connection = Depends(get_session)) -> Note:
    cursor = await session.execute("INSERT INTO notes (text) VALUES (?)", (note.text,))  # => parameterized (co-16)
    await session.commit()
    return Note(id=int(cursor.lastrowid), text=note.text)


@app.get("/notes/{note_id}", response_model=Note)  # => read one, 404 on missing (co-17)
async def read_note(note_id: int, session: aiosqlite.Connection = Depends(get_session)) -> Note:
    cursor = await session.execute("SELECT id, text FROM notes WHERE id = ?", (note_id,))
    row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="not found")  # => co-17
    return Note(id=int(row[0]), text=str(row[1]))


async def note_stream() -> AsyncIterator[bytes]:  # => a streaming generator (co-22)
    for i in range(3):  # => three chunks
        await asyncio.sleep(0.01)  # => pace the stream (co-02)
        yield f"note chunk {i}\n".encode("utf-8")  # => one chunk per yield (co-22)


@app.get("/stream")  # => the streaming endpoint (co-22)
async def stream() -> StreamingResponse:  # => incremental, not buffered
    return StreamingResponse(note_stream(), media_type="text/plain")  # => co-22
