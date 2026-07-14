"""Example 55: Create Then Read -- A Persisted Round Trip."""

# => co-02: POST writes, then a SEPARATE GET call reads the SAME id back --
#    proving the write genuinely reached durable storage, not just an in-memory echo
from fastapi import FastAPI, HTTPException  # => HTTPException raises FastAPI's default error shape
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, empty tasks.db for every run


class TaskCreate(BaseModel):  # => the shape of a valid POST /tasks body
    title: str  # => co-10: validated before either handler below sees it


@app.post("/tasks", status_code=201)  # => co-02: creates a new resource
def create_task(task: TaskCreate) -> dict[str, object]:  # => "task" only exists if validation passed
    new_id = repository.create_task(task.title)  # => step one of the round trip: the write
    return {"id": new_id, "title": task.title}  # => echoes the id the DB actually assigned


@app.get("/tasks/{task_id}")  # => co-02: reading the SAME resource back afterward
def get_task(task_id: int) -> dict[str, object]:  # => task_id arrives already parsed as an int
    row = repository.get_task(task_id)  # => step two of the round trip: the read
    if row is None:  # => the ONLY branch this handler makes -- everything else lives in the repo
        raise HTTPException(status_code=404)  # => FastAPI's plain default 404 shape
    return dict(row)  # => co-14: proves the POST actually reached durable storage
