"""Example 36: Parameterized Queries Neutralize Injection."""

# => this app.py is intentionally THIN -- the "?" placeholder safety property
#    lives entirely in repository.py, and this module only ever calls it
from fastapi import FastAPI  # => the web framework whose handler wraps the repository below

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, deterministic tasks.db for every run


@app.get("/tasks/search")  # => co-12: a typed query parameter
def search_tasks(title: str) -> list[dict[str, object]]:  # => "title" is really a SEARCH FRAGMENT
    rows = repository.search_by_title(title)  # => co-14: the "?" placeholder does the escaping
    return [dict(row) for row in rows]  # => sqlite3.Row -> plain dict, JSON-serializable
