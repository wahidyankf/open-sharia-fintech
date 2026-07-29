"""Example 40: Pagination and Filtering on a List Endpoint.

GET /tasks composes limit/offset pagination with an optional status filter in one parameterized query,
returning items plus total/next metadata. Run: uvicorn app:app --port 8000. (co-11, co-16)
"""

from collections.abc import AsyncIterator

import aiosqlite  # => the async driver (co-16)
from fastapi import Depends, FastAPI, Query  # => Query declares bounded params (co-11)
from pydantic import BaseModel  # => Pydantic models (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves
DB_PATH = "tasks.db"


class Task(BaseModel):  # => a row shape
    id: int
    title: str
    done: bool


class Page(BaseModel):  # => the paginated envelope (co-14)
    items: list[Task]  # => one page of rows
    total: int  # => the FILTERED count, not the whole table
    next: int | None  # => the next offset, or None at the end


async def get_session() -> AsyncIterator[aiosqlite.Connection]:  # => one session per request (co-15)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, done INTEGER)")
        await db.commit()
        yield db


@app.get("/tasks", response_model=Page)  # => the list endpoint
async def list_tasks(  # => pagination + filter composed in one query-shaping handler (co-11, co-16)
    done: bool | None = Query(default=None),  # => an OPTIONAL filter -- absent means "all"
    limit: int = Query(default=10, ge=1, le=50),  # => bounded limit (co-11): 1..50, default 10
    offset: int = Query(default=0, ge=0),  # => non-negative offset, default 0
    session: aiosqlite.Connection = Depends(get_session),
) -> Page:
    where = " WHERE done = ?" if done is not None else ""  # => an optional filter clause
    params: list[object] = [int(done)] if done is not None else []  # => filter value, parameterized (co-16)
    total_row = await (await session.execute(f"SELECT COUNT(*) FROM tasks{where}", params)).fetchone()  # => filtered count
    assert total_row is not None  # => COUNT(*) always returns one row
    total = int(total_row[0])  # => the filtered total (co-11)
    rows = await (await session.execute(f"SELECT id, title, done FROM tasks{where} ORDER BY id LIMIT ? OFFSET ?", [*params, limit, offset])).fetchall()  # => still parameterized (co-16)
    items = [Task(id=int(r[0]), title=str(r[1]), done=bool(r[2])) for r in rows]  # => typed rows (co-14)
    next_offset = offset + limit  # => the next page's offset
    return Page(items=items, total=total, next=next_offset if next_offset < total else None)  # => None at end
