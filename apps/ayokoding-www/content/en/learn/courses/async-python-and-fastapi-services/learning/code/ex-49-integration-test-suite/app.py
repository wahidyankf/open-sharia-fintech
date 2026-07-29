"""Example 49: A Full Async Integration Test Suite -- the app under test.

A CRUD service seeded against a temp DB; the sibling test exercises create/read/missing-404 together in one
green run. Run: pytest -v. (co-21, co-16, co-17)
"""

from collections.abc import AsyncIterator

import aiosqlite  # => the async driver (co-16)
from fastapi import Depends, FastAPI, HTTPException  # => DI + errors (co-15, co-17)
from pydantic import BaseModel  # => Pydantic models (co-12)

app = FastAPI()  # => the ASGI application the test imports

# => overridable so the test can point at a FRESH temp DB per run (co-21, co-16)
DB_PATH = "integration.db"


class NoteIn(BaseModel):  # => the body shape
    text: str


class Note(BaseModel):  # => the response shape (co-14)
    id: int
    text: str


async def get_session() -> AsyncIterator[aiosqlite.Connection]:  # => one session per request (co-15)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
        await db.commit()
        yield db


@app.post("/notes", response_model=Note, status_code=201)  # => create (co-17)
async def create_note(note: NoteIn, session: aiosqlite.Connection = Depends(get_session)) -> Note:
    cursor = await session.execute("INSERT INTO notes (text) VALUES (?)", (note.text,))
    await session.commit()
    return Note(id=int(cursor.lastrowid), text=note.text)


@app.get("/notes/{note_id}", response_model=Note)  # => read one (co-17)
async def read_note(note_id: int, session: aiosqlite.Connection = Depends(get_session)) -> Note:
    cursor = await session.execute("SELECT id, text FROM notes WHERE id = ?", (note_id,))
    row = await cursor.fetchone()
    if row is None:  # => missing -> 404 (co-17)
        raise HTTPException(status_code=404, detail="not found")
    return Note(id=int(row[0]), text=str(row[1]))
