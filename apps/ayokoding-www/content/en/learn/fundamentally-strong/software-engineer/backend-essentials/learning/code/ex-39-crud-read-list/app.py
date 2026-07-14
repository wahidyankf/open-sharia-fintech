"""Example 39: CRUD -- Read List."""

# => the "R" (plural) in CRUD -- POST grows the list, GET returns the
#    whole array, so a single curl session can prove the two compose
from fastapi import FastAPI  # => the web framework whose handlers wrap the repository below
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, empty tasks.db for every run


class TaskCreate(BaseModel):  # => the shape of a valid POST /tasks body
    title: str  # => co-10: validated before either handler below sees it


@app.post("/tasks", status_code=201)  # => reused so curl can grow the list before listing it
def create_task(task: TaskCreate) -> dict[str, object]:  # => "task" only exists if validation passed
    new_id = repository.create_task(task.title)  # => co-14: the handler delegates the INSERT
    return {"id": new_id, "title": task.title}  # => echoes the id the DB actually assigned


@app.get("/tasks")  # => co-14: returns a JSON ARRAY, one element per row
def list_tasks() -> list[dict[str, object]]:  # => the array shape a client can iterate directly
    rows = repository.list_tasks()  # => co-14: the handler never writes SQL itself
    return [dict(row) for row in rows]  # => sqlite3.Row -> plain dict, JSON-serializable
