"""Example 23: Mapping a Failure to a Status with HTTPException.

Raising HTTPException(404) maps a missing resource to a precise status + body, instead of a 200 placeholder.
Run: uvicorn app:app --port 8000, then: curl -i localhost:8000/notes/999  (co-17)
"""

from collections.abc import AsyncIterator

import aiosqlite  # => the async driver (co-16)
from fastapi import Depends, FastAPI, HTTPException  # => HTTPException maps a failure to a status (co-17)
from pydantic import BaseModel  # => Pydantic models (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves
DB_PATH = "notes.db"  # => the same file DB as ex-22


class Note(BaseModel):  # => the response shape
    id: int
    text: str


async def get_session() -> AsyncIterator[aiosqlite.Connection]:  # => one session per request (co-15)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
        await db.commit()
        yield db


@app.get("/notes/{note_id}", response_model=Note)  # => read by id
async def read_note(note_id: int, session: aiosqlite.Connection = Depends(get_session)) -> Note:
    cursor = await session.execute("SELECT id, text FROM notes WHERE id = ?", (note_id,))  # => parameterized
    row = await cursor.fetchone()  # => one row or None
    if row is None:  # => missing resource
        # => raising HTTPException maps this to a precise status + body, never a 200 with empty data (co-17)
        raise HTTPException(status_code=404, detail="note not found")  # => 404 + a JSON detail body
    return Note(id=int(row[0]), text=str(row[1]))  # => the persisted row, as JSON (co-14)
