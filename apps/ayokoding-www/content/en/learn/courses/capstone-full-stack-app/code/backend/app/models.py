"""Full-stack capstone -- typed request/response models (topic 11 HTTP JSON API). The frontend's
`types.ts` `Task` interface mirrors this `Task` model's fields exactly: one shared shape,
expressed twice (Python here, TypeScript there), verified against each other on this page rather
than left to drift.
"""

from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal[
    "todo", "in_progress", "done"
]  # => a closed set -- anything else is a 422


class TaskCreate(BaseModel):  # => the shape POST /tasks requires
    title: str = Field(
        min_length=1, max_length=200
    )  # => empty titles are rejected before any handler runs
    description: str = Field(default="", max_length=2000)


class TaskUpdate(BaseModel):  # => PUT REPLACES the full resource with this exact shape
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    status: TaskStatus = "todo"


class Task(BaseModel):  # => the response shape for every task-returning endpoint
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: str
