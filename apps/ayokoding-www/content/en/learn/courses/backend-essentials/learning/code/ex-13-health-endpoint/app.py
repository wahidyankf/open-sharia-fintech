"""Example 13: Health Endpoint."""

from fastapi import FastAPI  # => the web framework this whole tier builds on

app = FastAPI()  # => the ASGI application uvicorn will serve


@app.get("/health")  # => a conventional liveness-check path (co-08)
def health() -> dict[str, str]:
    """Return 200 + a fixed body -- proves the process is up and answering."""
    # => this handler holds ZERO logic beyond returning a constant -- deliberately
    # => so: a liveness probe should never depend on anything that can itself fail
    # => (a database, a downstream service); see Advanced Example 76 for the
    # => contrast (a /ready endpoint that DOES check a dependency)
    return {"status": "ok"}  # => FastAPI defaults every 2xx return to status 200
