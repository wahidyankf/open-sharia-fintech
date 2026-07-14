"""Example 35: A Repository Module Connected to SQLite."""

# => this app.py is intentionally THIN -- every database detail lives in
#    repository.py, and this module only ever calls it, never imports sqlite3
from fastapi import FastAPI  # => the web framework whose handler wraps the repository below

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => co-24: schema setup happens ONCE, at import time, not per-request


@app.get("/tasks")  # => co-08: a handler for listing tasks
def list_tasks() -> list[dict[str, object]]:  # => a JSON array of plain dicts
    rows = repository.list_tasks()  # => co-14: the handler never writes SQL itself
    return [dict(row) for row in rows]  # => sqlite3.Row -> plain dict, JSON-serializable
