"""Example 60: APIRouter Prefix and Tags.

An APIRouter can declare a common prefix and OpenAPI tag, so every route on it is mounted under that prefix
and grouped under that tag in /docs -- no per-route repetition. Run: uvicorn app:app --port 8000. (co-10, co-20)
"""

from fastapi import APIRouter, FastAPI  # => APIRouter + FastAPI (co-10)

app = FastAPI()  # => the top-level ASGI application

# => prefix="/users" mounts every route below at /users/...; tags group them in /docs (co-20)
users_router = APIRouter(prefix="/users", tags=["users"])  # => one prefix + one tag for the whole group (co-10)


@users_router.get("/")  # => with the prefix, this becomes GET /users/ (co-10)
def list_users() -> dict[str, list[str]]:  # => a handler
    return {"users": ["ada", "bob"]}  # => a list (co-14)


@users_router.get("/{user_id}")  # => becomes GET /users/{user_id} (co-10, co-11)
def read_user(user_id: int) -> dict[str, int]:  # => a typed path param (co-11)
    return {"user_id": user_id}  # => echoed (co-14)


app.include_router(users_router)  # => mount -- the prefix applies to every route on the router (co-10)
