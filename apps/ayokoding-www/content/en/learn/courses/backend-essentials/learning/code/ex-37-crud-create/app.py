"""Example 37: CRUD -- Create."""

# => the "C" in CRUD -- one POST endpoint, backed by repository.create_task(),
#    the start of the growing task-management service this topic builds
from fastapi import FastAPI  # => the web framework whose handler wraps the repository below
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, empty tasks.db for every run


class TaskCreate(BaseModel):  # => the shape of a valid POST /tasks body
    title: str  # => co-10: validated before the handler ever sees it


@app.post("/tasks", status_code=201)  # => co-03: 201 signals a new resource was created
def create_task(task: TaskCreate) -> dict[str, object]:  # => "task" only exists if validation passed
    new_id = repository.create_task(task.title)  # => co-14: the handler delegates the INSERT
    return {"id": new_id, "title": task.title}  # => echoes the id the DB actually assigned
