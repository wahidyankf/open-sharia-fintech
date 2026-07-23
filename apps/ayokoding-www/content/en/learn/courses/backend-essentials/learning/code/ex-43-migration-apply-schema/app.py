"""Example 43: Apply a schema.sql Migration at Startup."""  # => module docstring for this example

# => the schema lives in a SEPARATE schema.sql file, not a Python string --
# => this app.py only ever asks repository.py "did the migration succeed?"
from fastapi import FastAPI  # => the web framework whose health check wraps the repository below

import repository  # => co-15: the module that owns the schema.sql migration for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.apply_schema()  # => co-15: runs BEFORE the app accepts a single request
assert repository.table_exists(  # => fails FAST, at import time, not on the first real request
    "tasks"  # => the single table name this migration creates
), "migration failed: tasks table missing"  # => verified before uvicorn finishes booting --
# => a crash here is far cheaper to diagnose than a 500 on the very first real request


@app.get("/health")  # => co-08: a readiness-style check a load balancer could poll
def health() -> dict[str, bool]:  # => a tiny, machine-checkable readiness signal
    return {"tasks_table_ready": repository.table_exists("tasks")}  # => re-verified per request
