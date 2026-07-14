"""Example 44: An Additive ALTER TABLE + Backfill Migration."""

# => two calls at import time: FIRST seed the OLD schema and a row, THEN
#    migrate -- proving the migration works against data that predates it
from fastapi import FastAPI  # => the web framework whose handler wraps the repository below

import repository  # => co-15: the module that owns the migration for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.create_v1_schema()  # => v1: (id, title) only, seeded with one pre-migration row
repository.migrate_add_priority_column()  # => co-15: additive ALTER TABLE + backfill UPDATE


@app.get("/tasks/{task_id}")  # => co-12: a typed integer path parameter
def get_task(task_id: int) -> dict[str, object]:  # => task_id arrives already parsed as an int
    row = repository.get_task(task_id)  # => co-14: delegates the SELECT
    assert row is not None  # => id 1 always exists in this example's fixed seed data
    return dict(row)  # => includes the BACKFILLED "priority" column
