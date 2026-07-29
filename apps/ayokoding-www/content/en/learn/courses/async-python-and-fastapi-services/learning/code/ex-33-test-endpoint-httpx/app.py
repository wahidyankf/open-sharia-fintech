"""Example 33: Testing an Endpoint with Async httpx -- the app under test.

A one-route app exercised in-process by an async httpx client in the sibling test_app.py. Run the app:
uvicorn app:app --port 8000; run the tests: pytest -v. (co-21)
"""

from fastapi import FastAPI  # => the web framework (co-10)

app = FastAPI()  # => the ASGI application both the server and the tests import


@app.get("/")  # => the route under test
def read_root() -> dict[str, str]:  # => a minimal handler
    return {"msg": "ok"}  # => the body the test asserts against (co-14)
