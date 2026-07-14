"""Example 45: A Repository That Returns Typed Rows."""

# => co-24: this handler's own signature names TaskRow, so pyright checks the
#    SAME contract on both sides of the repository boundary, not just one
from fastapi import FastAPI  # => the web framework whose handler wraps the repository below

import repository  # => co-14: the module that owns EVERY database detail for this example
from repository import TaskRow  # => co-24: the typed shape this handler's own signature names

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, seeded tasks.db for every run


@app.get("/tasks")  # => co-08: a handler for listing tasks
def list_tasks() -> list[TaskRow]:  # => co-24: the handler's own signature names the typed shape
    tasks: list[TaskRow] = repository.list_tasks()  # => pyright checks this assignment for real
    total_title_chars = sum(  # => a trivial computation that only WORKS if "title" really exists
        len(task["title"])
        for task in tasks  # => typed access -- pyright knows "title" is a str
    )  # => typed access: pyright would flag task["missing_key"] as an error at edit time
    print(f"total title characters: {total_title_chars}")  # => proves the typed data is genuinely usable
    return tasks  # => TypedDict serializes to JSON exactly like a plain dict
