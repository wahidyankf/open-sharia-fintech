"""Example 78: A Dockerfile for Multi-Worker ASGI Deploy -- the runnable app.

The sibling Dockerfile builds this app into a slim image and runs uvicorn with multiple workers -- one ASGI
process per core. Build: docker build -t async-fastapi . Run: docker run -p 8000:8000 async-fastapi. (co-24)
"""

from fastapi import FastAPI  # => the web framework the Dockerfile pins (co-24)

app = FastAPI(title="Deployable Service")  # => the ASGI application the image serves


@app.get("/")  # => a health-style route
def read_root() -> dict[str, str]:  # => a minimal handler
    return {"msg": "deployable"}  # => confirms the containerised service is up (co-14)


@app.get("/health")  # => a liveness probe the orchestrator polls (co-24)
def health() -> dict[str, str]:  # => no dependencies -> always 200
    return {"status": "ok"}  # => a container orchestrator reads this to decide routing (co-24)
