"""Example 22: A CRUD Create and Read Round Trip.

POST /notes creates a row; GET /notes/{id} reads it back -- persistence against an async SQLite file.
Run: uvicorn app:app --port 8000, then:
curl -X POST -H 'Content-Type: application/json' -d '{"text":"hello"}' localhost:8000/notes
curl localhost:8000/notes/1  (co-16, co-12)
"""

from collections.abc import AsyncIterator

import aiosqlite  # => the async driver (co-16)
from fastapi import Depends, FastAPI  # => Depends injects the session (co-15)
from pydantic import BaseModel  # => Pydantic models (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves
DB_PATH = "notes.db"  # => a file DB so created rows SURVIVE across requests (unlike ":memory:")


class NoteIn(BaseModel):  # => the request-body shape for a create (co-12)
    text: str  # => required


class Note(BaseModel):  # => the response shape (co-14)
    id: int  # => the DB-assigned primary key
    text: str  # => the stored text


async def get_session() -> AsyncIterator[aiosqlite.Connection]:  # => one session per request (co-15)
    async with aiosqlite.connect(DB_PATH) as db:  # => async acquire
        await db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")  # => idempotent schema (co-16)
        await db.commit()  # => persist the schema creation
        yield db  # => hand the session to the handler


@app.post("/notes", response_model=Note, status_code=201)  # => create -- 201 on success (co-17)
async def create_note(note: NoteIn, session: aiosqlite.Connection = Depends(get_session)) -> Note:
    cursor = await session.execute("INSERT INTO notes (text) VALUES (?)", (note.text,))  # => parameterized INSERT (co-16)
    await session.commit()  # => persist the row
    return Note(id=int(cursor.lastrowid), text=note.text)  # => the DB-assigned id + stored text


@app.get("/notes/{note_id}", response_model=Note)  # => read by id
async def read_note(note_id: int, session: aiosqlite.Connection = Depends(get_session)) -> Note:
    cursor = await session.execute("SELECT id, text FROM notes WHERE id = ?", (note_id,))  # => parameterized SELECT
    row = await cursor.fetchone()  # => one row or None
    if row is None:  # => missing -- the handler signals absence (ex-23 turns this into a clean 404)
        return Note(id=note_id, text="")  # => placeholder; ex-23 replaces this with HTTPException
    return Note(id=int(row[0]), text=str(row[1]))  # => the persisted row, as JSON (co-14)
