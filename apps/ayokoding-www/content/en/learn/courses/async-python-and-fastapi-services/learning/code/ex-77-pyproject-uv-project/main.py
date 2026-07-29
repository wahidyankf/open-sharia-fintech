"""Example 77: A uv Project from a Manifest -- the runnable app.

A uv project declares its dependencies in pyproject.toml (the sibling manifest); `uv sync` reproduces the exact
environment from that file, and `uv run uvicorn main:app --port 8000` boots the service. (co-07)
"""

from fastapi import FastAPI  # => the web framework pinned by the manifest (co-07)

app = FastAPI(title="uv Project Service")  # => the ASGI application uvicorn serves


@app.get("/")  # => a health-style route
def read_root() -> dict[str, str]:  # => a minimal handler
    return {"msg": "managed by uv"}  # => confirms the uv-managed service is up (co-14)
