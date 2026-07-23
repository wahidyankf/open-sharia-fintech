"""Example 46: Layering -- No SQL in the Handler."""

# => co-24: this file is the PROOF -- its own test inspects this SOURCE FILE
#    and fails if any query keyword ever appears in it, not just at review time
from fastapi import FastAPI  # => the web framework whose handler wraps the repository below

import repository  # => co-24: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, seeded tasks.db for every run


@app.get("/tasks")  # => co-08: a handler for listing tasks
def list_tasks() -> list[dict[str, object]]:  # => a JSON array of plain dicts
    rows = repository.list_tasks()  # => co-24: the ENTIRE data-access line, one function call
    return [dict(row) for row in rows]  # => no query syntax, no "?", no sqlite3 import anywhere here
