"""Example 40: CRUD -- Update."""

# => the "U" in CRUD -- one PUT endpoint, backed by repository.update_task(),
#    which reports back whether a row actually changed
from fastapi import FastAPI, HTTPException  # => HTTPException raises FastAPI's default error shape
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, seeded tasks.db for every run


class TaskUpdate(BaseModel):  # => the shape of a valid PUT /tasks/{id} body
    title: str  # => co-10: the replacement value, validated like any other body


@app.put("/tasks/{task_id}")  # => co-02: PUT replaces the addressed resource
def update_task(task_id: int, task: TaskUpdate) -> dict[str, object]:  # => path param + validated body
    changed = repository.update_task(task_id, task.title)  # => co-14: delegates the UPDATE
    if not changed:  # => the ONLY branch this handler makes -- everything else lives in the repo
        raise HTTPException(status_code=404)  # => FastAPI's plain default 404 shape
    return {"id": task_id, "title": task.title}  # => echoes the id + the value that was just written
