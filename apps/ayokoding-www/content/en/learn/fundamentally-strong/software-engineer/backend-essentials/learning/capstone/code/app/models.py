"""Capstone task API -- typed request/response models (co-09, co-10)."""

from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal["todo", "in_progress", "done"]  # => co-10: a closed set -- anything else is a 422


class TaskCreate(BaseModel):  # => co-10: the shape POST /tasks requires
    title: str = Field(min_length=1, max_length=200)  # => co-10: constrained -- empty titles are rejected
    description: str = Field(default="", max_length=2000)


class TaskUpdate(BaseModel):  # => co-02, co-10: PUT REPLACES the full resource with this exact shape
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    status: TaskStatus = "todo"


class Task(BaseModel):  # => co-09: the response shape for every task-returning endpoint
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: str


class TaskPage(BaseModel):  # => co-19: the paginated list envelope
    items: list[Task]
    total: int
    next: int | None
