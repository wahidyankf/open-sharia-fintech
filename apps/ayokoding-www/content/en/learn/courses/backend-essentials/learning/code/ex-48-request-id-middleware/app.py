"""Example 48: Middleware -- X-Request-Id."""  # => module docstring for this example

# => co-16: a middleware runs around EVERY route, once registered -- no
# => individual handler in this file ever mentions X-Request-Id itself
import uuid  # => stdlib UUID generation -- no third-party dependency needed for this

from fastapi import FastAPI, Request  # => Request is what every middleware receives first
from starlette.middleware.base import (  # => co-16: the two building blocks every middleware needs
    BaseHTTPMiddleware,  # => the base class FastAPI's own middleware system builds on
    RequestResponseEndpoint,  # => the precise type of "the rest of the pipeline", for typing call_next
)  # => closes the multi-line import from starlette.middleware.base
from starlette.responses import Response  # => the type dispatch() must always return

app = FastAPI()  # => the ASGI application uvicorn will serve


class RequestIdMiddleware(BaseHTTPMiddleware):  # => co-16: wraps EVERY request/response pair
    async def dispatch(  # => co-16: dispatch()'s signature spans three lines
        self,
        request: Request,
        call_next: RequestResponseEndpoint,  # => call_next runs the rest of the app
    ) -> Response:  # => must return the Response that eventually reaches the client
        response = await call_next(request)  # => runs routing + the matched handler first
        response.headers["X-Request-Id"] = str(  # => co-04: mutates the OUTGOING response headers
            uuid.uuid4()  # => a fresh, unpredictable id -- different on every single request
        )  # => co-04: a fresh id, stamped on the way back out
        return response  # => the SAME response object, now carrying the header


app.add_middleware(RequestIdMiddleware)  # => applies to EVERY route, with zero per-route code

# => registration order matters when multiple middlewares are stacked, but this
# => example registers only one, so ordering has no observable effect here


@app.get("/tasks")  # => co-08: a handler that knows NOTHING about request ids
def list_tasks() -> list[dict[str, str]]:  # => a plain handler, unaware any middleware even exists
    return [{"title": "Buy milk"}]  # => the middleware adds the header AFTER this returns
