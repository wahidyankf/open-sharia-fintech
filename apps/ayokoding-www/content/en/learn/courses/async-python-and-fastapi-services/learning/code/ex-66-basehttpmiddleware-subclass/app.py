"""Example 66: A Middleware Written as a Class.

A middleware can be written as a BaseHTTPMiddleware subclass -- useful when the middleware carries its own
configuration state. Run: uvicorn app:app --port 8000, then: curl -i localhost:8000/. (co-18)
"""

from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request  # => Request flows through the middleware (co-18)
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware  # => the class-based middleware base (co-18)


class HeaderMiddleware(BaseHTTPMiddleware):  # => a class-based middleware carrying config (co-18)
    def __init__(self, app, header_name: str, header_value: str) -> None:  # => config passed at construction
        super().__init__(app)  # => initialise the base
        self.header_name = header_name  # => the response header to add
        self.header_value = header_value  # => its value

    async def dispatch(  # => the per-request method (co-18)
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response: Response = await call_next(request)  # => run the downstream handler
        response.headers[self.header_name] = self.header_value  # => add the configured header (co-18)
        return response  # => the enriched response


app = FastAPI()  # => the ASGI application uvicorn serves
app.add_middleware(HeaderMiddleware, header_name="X-App", header_value="async-fastapi")  # => mount with config (co-18)


@app.get("/")  # => a route that knows nothing about the header
def read_root() -> dict[str, str]:  # => minimal handler
    return {"msg": "ok"}  # => the X-App header is added by the middleware outside this function
