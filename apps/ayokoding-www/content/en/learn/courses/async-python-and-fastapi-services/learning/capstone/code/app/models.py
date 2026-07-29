"""Capstone async FastAPI service -- typed Pydantic v2 models (co-12, co-13, co-14)."""

from typing import Literal

from pydantic import BaseModel, Field

# => a closed status set -- anything else is a 422 (co-13)
TaskStatus = Literal["todo", "in_progress", "done"]


class TaskCreate(BaseModel):  # => the POST /tasks body shape (co-12)
    title: str = Field(
        min_length=1, max_length=200
    )  # => constrained -- empty titles rejected (co-13)
    description: str = Field(default="", max_length=2000)


class TaskUpdate(BaseModel):  # => the PUT /tasks/{id} body shape (co-12)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    status: TaskStatus = "todo"  # => a closed set -- an unknown status is a 422 (co-13)


class Task(
    BaseModel
):  # => the response shape for every task-returning endpoint (co-14)
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: str


class TaskPage(BaseModel):  # => the paginated list envelope (co-14, co-11)
    items: list[Task]
    total: int
    next: int | None  # => None once the last page is reached
