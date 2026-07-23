"""Example 53: The 422 Detail Array Lists Every Offending Field."""

# => the SAME TaskCreate shape as ex-31, but this example's test specifically
#    breaks BOTH fields at once to show the detail array grows, not just the first
from fastapi import FastAPI  # => the web framework whose validation layer this example exercises
from pydantic import BaseModel, Field  # => Field() attaches constraints beyond a bare type

app = FastAPI()  # => the ASGI application uvicorn will serve


class TaskCreate(BaseModel):  # => the shape of a valid POST /tasks body
    title: str = Field(min_length=1)  # => two INDEPENDENT constraints...
    priority: int = Field(gt=0)  # => ...that can both fail on the SAME request


@app.post("/tasks", status_code=201)  # => co-08: a handler for creating a task
def create_task(task: TaskCreate) -> dict[str, object]:  # => "task" only exists if BOTH fields passed
    return {"title": task.title, "priority": task.priority}  # => both fields, already constraint-checked
