"""Example 35: Overriding a Dependency in Tests -- the app under test.

A handler depends on a DB session; the test OVERRIDES that dependency with a fake, so the test never touches
a real database. Run: pytest -v. (co-15, co-21)
"""

from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI  # => Depends declares the dependency (co-15)

app = FastAPI()  # => the ASGI application uvicorn serves


class UserStore:  # => a dependency the handler relies on
    async def current_user(self) -> str:  # => the real implementation hits a database
        return "real-db-user"  # => what production would return


async def get_user_store() -> AsyncIterator[UserStore]:  # => the dependency PROVIDER (co-15)
    store = UserStore()  # => production wiring
    yield store  # => hand it to the handler


@app.get("/me")  # => a route that needs the current user
async def me(store: UserStore = Depends(get_user_store)) -> dict[str, str]:  # => injected dependency (co-15)
    user = await store.current_user()  # => the handler depends on the store, not on how it was built
    return {"user": user}  # => reflects whatever the store returns -- real OR faked (co-14)
