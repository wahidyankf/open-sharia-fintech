"""Example 59: Splitting a Big App with APIRouter.

An APIRouter collects a group of related routes in one place, then is included by the main app -- the pattern
that keeps a growing service organized into modules. Run: uvicorn app:app --port 8000. (co-10)
"""

from fastapi import APIRouter, FastAPI  # => APIRouter groups routes; FastAPI includes them (co-10)

app = FastAPI()  # => the top-level ASGI application

items_router = APIRouter()  # => a router for the /items resource group (co-10)


@items_router.get("/items")  # => a route registered on the ROUTER, not the app yet
def list_items() -> dict[str, list[str]]:  # => a handler
    return {"items": ["a", "b"]}  # => a list response (co-14)


@items_router.post("/items")  # => another route on the same router
def create_item() -> dict[str, str]:  # => a handler
    return {"status": "created"}  # => an ack (co-14)


app.include_router(items_router)  # => mount the router's routes onto the app (co-10) -- now /items is live
