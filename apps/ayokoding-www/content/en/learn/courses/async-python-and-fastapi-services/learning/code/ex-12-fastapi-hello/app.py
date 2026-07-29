"""Example 12: A First FastAPI Route.

Run: uvicorn app:app --port 8000, then: curl localhost:8000/  (co-10)
"""

from fastapi import FastAPI  # => the web framework whose routing this example exercises (co-10)

# => the module-level name "app" is exactly what "uvicorn app:app" imports (module app, attribute app)
app = FastAPI()  # => an ASGI application object the server serves


@app.get("/")  # => decorator-based ROUTING: GET "/" maps to read_root (co-10, co-11)
def read_root() -> dict[str, str]:  # => returning a dict is auto-serialized to a JSON response body (co-14)
    # => no manual json.dumps, no manual Content-Type, no manual status line -- the framework does all three
    return {"msg": "hello"}  # => FastAPI sets Content-Type: application/json and status 200 automatically
