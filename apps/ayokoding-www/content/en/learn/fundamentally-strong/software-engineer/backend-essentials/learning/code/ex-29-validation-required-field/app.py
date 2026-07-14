"""Example 29: Validation -- Required Field."""

from fastapi import FastAPI  # => the web framework whose validation layer this example exercises
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

app = FastAPI()  # => the ASGI application uvicorn will serve


class TaskCreate(BaseModel):  # => the shape of a valid POST /tasks body
    title: str  # => no default value -- Pydantic treats this as REQUIRED


@app.post("/tasks", status_code=201)  # => co-08: a handler for creating a task
def create_task(task: TaskCreate) -> dict[str, str]:  # => "task" only exists if validation passed
    # => FastAPI parses+validates the JSON body against TaskCreate BEFORE this
    #    line ever runs -- an invalid body never reaches this function body
    return {"title": task.title}  # => echoes back the validated field
