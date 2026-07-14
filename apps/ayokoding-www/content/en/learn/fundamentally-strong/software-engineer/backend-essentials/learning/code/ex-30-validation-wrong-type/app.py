"""Example 30: Validation -- Wrong Type."""

from fastapi import FastAPI  # => the web framework whose validation layer this example exercises
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

app = FastAPI()  # => the ASGI application uvicorn will serve


class TaskCreate(BaseModel):  # => the shape of a valid POST /tasks body
    title: str  # => any string is acceptable here
    priority: int  # => MUST be an int -- a non-numeric string fails validation


@app.post("/tasks", status_code=201)  # => co-08: a handler for creating a task
def create_task(task: TaskCreate) -> dict[str, str | int]:  # => the union return type: str or int values
    # => co-10: FastAPI parses+validates the body against TaskCreate first --
    #    a non-numeric "priority" never reaches this line at all
    return {"title": task.title, "priority": task.priority}  # => both fields, already the right types
