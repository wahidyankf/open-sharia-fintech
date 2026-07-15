"""Capstone: hardened task API -- typed request/response models (co-07, co-09, co-10)."""

from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal[
    "todo", "in_progress", "done"
]  # => co-07: a closed set -- anything else is a 422


class TaskCreate(
    BaseModel
):  # => the shape POST /tasks requires -- unchanged from Backend-Essentials
    title: str = Field(min_length=1, max_length=200)
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


class TaskPage(BaseModel):  # => the paginated list envelope
    items: list[Task]
    total: int
    next: int | None


# --- co-07: allow-list validation for the NEW auth surface -------------------------------


class UserRegister(
    BaseModel
):  # => co-07: username is an ALLOW-LIST -- only letters/digits/underscore
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    # => co-07: an attacker cannot smuggle quotes, dashes, or SQL metacharacters through this field --
    # => this REJECTS `admin'--` outright, before any handler code runs
    password: str = Field(
        min_length=8, max_length=128
    )  # => co-09: bounds only -- the HASH is what protects it


class UserLogin(BaseModel):  # => same allow-list shape, reused for the login body
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)


class UserPublic(
    BaseModel
):  # => co-09: NEVER includes password_hash -- this is the only shape a client sees
    id: int
    username: str
    created_at: str


class TokenResponse(BaseModel):  # => co-12: the bearer token a successful login returns
    access_token: str
    token_type: Literal["bearer"] = "bearer"
