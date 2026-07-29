"""Example 39: A Full Typed Async CRUD Service.

A complete typed async CRUD over aiosqlite: dependency-injected sessions, Pydantic validation, a 404 on a
missing id, and parameterized queries throughout -- no SQL in any handler beyond the repository layer.
Run: uvicorn app:app --port 8000, then exercise POST/GET/PUT/DELETE on /tasks. (co-10 to co-17)
"""

from collections.abc import AsyncIterator

import aiosqlite  # => the async driver (co-16)
from fastapi import Depends, FastAPI, HTTPException  # => DI + error mapping (co-15, co-17)
from pydantic import BaseModel  # => Pydantic models (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves
DB_PATH = "tasks.db"  # => a file DB so rows survive across requests


class TaskIn(BaseModel):  # => the create/replace body shape (co-12)
    title: str  # => required
    done: bool = False  # => optional with a default


class Task(BaseModel):  # => the response shape (co-14)
    id: int
    title: str
    done: bool


async def get_session() -> AsyncIterator[aiosqlite.Connection]:  # => one async session per request (co-15)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, done INTEGER)")  # => idempotent schema (co-16)
        await db.commit()
        yield db


def _row_to_task(row: aiosqlite.Row | tuple) -> Task:  # => the ONE place a raw row becomes a typed Task (co-14)
    return Task(id=int(row[0]), title=str(row[1]), done=bool(row[2]))  # => narrowed, typed fields


@app.post("/tasks", response_model=Task, status_code=201)  # => create (co-17)
async def create_task(task: TaskIn, session: aiosqlite.Connection = Depends(get_session)) -> Task:
    cursor = await session.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, int(task.done)))  # => parameterized (co-16)
    await session.commit()
    return Task(id=int(cursor.lastrowid), title=task.title, done=task.done)  # => the new row


@app.get("/tasks/{task_id}", response_model=Task)  # => read one (co-17)
async def read_task(task_id: int, session: aiosqlite.Connection = Depends(get_session)) -> Task:
    cursor = await session.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))  # => parameterized
    row = await cursor.fetchone()
    if row is None:  # => missing -> precise 404 (co-17)
        raise HTTPException(status_code=404, detail="task not found")
    return _row_to_task(row)  # => the persisted row


@app.put("/tasks/{task_id}", response_model=Task)  # => replace (co-17)
async def update_task(task_id: int, task: TaskIn, session: aiosqlite.Connection = Depends(get_session)) -> Task:
    cursor = await session.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (task.title, int(task.done), task_id))  # => parameterized
    await session.commit()
    if cursor.rowcount == 0:  # => no row matched -> 404
        raise HTTPException(status_code=404, detail="task not found")
    row = await (await session.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))).fetchone()
    assert row is not None  # => rowcount > 0 guarantees this -- narrows for the type checker
    return _row_to_task(row)


@app.delete("/tasks/{task_id}", status_code=204)  # => delete (co-17)
async def delete_task(task_id: int, session: aiosqlite.Connection = Depends(get_session)) -> None:
    cursor = await session.execute("DELETE FROM tasks WHERE id = ?", (task_id,))  # => parameterized
    await session.commit()
    if cursor.rowcount == 0:  # => nothing deleted -> 404
        raise HTTPException(status_code=404, detail="task not found")
