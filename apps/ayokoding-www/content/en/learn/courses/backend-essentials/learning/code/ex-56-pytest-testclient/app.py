"""Example 56: pytest + FastAPI's TestClient."""

# => co-22: this app.py is unremarkable on purpose -- the interesting part of
#    this example lives entirely in test_app.py's fixture, not in this handler code
from fastapi import FastAPI  # => the web framework whose handlers this example's tests exercise
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn (and TestClient) will serve
repository.init_db()  # => a first, module-import-time reset -- the pytest fixture resets it AGAIN per test


class TaskCreate(BaseModel):  # => the shape of a valid POST /tasks body
    title: str  # => co-10: validated before either handler below sees it


@app.post("/tasks", status_code=201)  # => co-08: a handler for creating a task
def create_task(task: TaskCreate) -> dict[str, object]:  # => "task" only exists if validation passed
    new_id = repository.create_task(task.title)  # => co-14: the handler delegates the INSERT
    return {"id": new_id, "title": task.title}  # => echoes the id the DB actually assigned


@app.get("/tasks")  # => co-14: returns a JSON ARRAY, one element per row
def list_tasks() -> list[dict[str, object]]:  # => the array shape a client can iterate directly
    return [dict(row) for row in repository.list_tasks()]  # => sqlite3.Row -> plain dict, per row
