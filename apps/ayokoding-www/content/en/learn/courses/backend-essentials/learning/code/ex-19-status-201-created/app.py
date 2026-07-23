"""Example 19: Status 201 Created."""

from fastapi import FastAPI, status  # => status carries named HTTP status constants
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

app = FastAPI()  # => the ASGI application uvicorn will serve


class Task(BaseModel):  # => a task the client wants created
    """A task the client wants created."""

    title: str  # => the one field this minimal task model carries


@app.post("/tasks", status_code=status.HTTP_201_CREATED)  # => override 200 default
def create_task(task: Task) -> Task:
    """RFC 9110: 201 means "a new resource was created" -- more precise than 200."""
    # => status.HTTP_201_CREATED is just the int 201 with a self-documenting
    # => name -- FastAPI would accept a bare `201` here too, but the constant
    # => reads clearly and matches every other status.HTTP_* used in this topic
    # => without status_code=..., this handler would default to 200 (co-03) --
    # => a technically-passing but IMPRECISE code for "a new resource now exists"
    return task  # => the response body still echoes the created resource
