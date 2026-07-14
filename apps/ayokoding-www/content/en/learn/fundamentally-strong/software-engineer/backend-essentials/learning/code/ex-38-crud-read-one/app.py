"""Example 38: CRUD -- Read One."""

# => the "R" (singular) in CRUD -- one GET endpoint, backed by
#    repository.get_task(), returning a 404 when the id does not exist
from fastapi import FastAPI, HTTPException  # => HTTPException raises FastAPI's default error shape

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, seeded tasks.db for every run


@app.get("/tasks/{task_id}")  # => co-12: a typed integer path parameter
def get_task(task_id: int) -> dict[str, object]:  # => task_id arrives already parsed as an int
    row = repository.get_task(task_id)  # => co-14: the handler delegates the SELECT
    if row is None:  # => the ONLY branch this handler makes -- everything else lives in the repo
        raise HTTPException(status_code=404)  # => FastAPI's plain default 404 shape
    return dict(row)  # => sqlite3.Row -> plain dict, JSON-serializable
