"""Example 47: FastAPI Depends() Supplies the DB Connection."""

# => co-23: the handler below never calls sqlite3.connect() or connection.close()
#    itself -- FastAPI's dependency injection owns the connection's entire lifecycle
import sqlite3  # => only needed for the type hint below, never for opening a connection

from fastapi import Depends, FastAPI  # => Depends() wires a dependency into a handler's signature

import repository  # => co-14/co-23: the module that owns both the SQL and the connection lifecycle

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, seeded tasks.db for every run


@app.get("/tasks")  # => co-08: a handler for listing tasks
def list_tasks_endpoint(
    connection: sqlite3.Connection = Depends(repository.get_connection),  # => co-23: injected per request
) -> list[dict[str, object]]:  # => a JSON array of plain dicts
    # => co-23: FastAPI calls get_connection() FOR THIS REQUEST and injects the
    #    value it yields here -- the handler never calls sqlite3.connect() itself
    rows = repository.list_tasks(connection)  # => co-14: SQL still lives only in the repository
    return [dict(row) for row in rows]  # => sqlite3.Row -> plain dict, JSON-serializable
