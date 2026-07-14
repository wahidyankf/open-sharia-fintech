"""Example 31: Validation -- Field Constraints."""

from fastapi import FastAPI  # => the web framework whose validation layer this example exercises
from pydantic import BaseModel, Field  # => Field() attaches constraints beyond a bare type

app = FastAPI()  # => the ASGI application uvicorn will serve


class TaskCreate(BaseModel):  # => the shape of a valid POST /tasks body
    title: str = Field(min_length=1)  # => co-10: rejects an empty string, not just a missing field
    priority: int = Field(gt=0)  # => co-10: rejects zero or negative priorities


@app.post("/tasks", status_code=201)  # => co-08: a handler for creating a task
def create_task(task: TaskCreate) -> dict[str, str | int]:  # => the union return type: str or int values
    # => both constraints are enforced BEFORE this line runs -- an out-of-range
    #    "priority" or an empty "title" never reaches the handler body
    return {"title": task.title, "priority": task.priority}  # => both fields, already constraint-checked
