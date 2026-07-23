"""Example 49: Middleware -- Request Logging."""  # => module docstring for this example

# => co-16: every request that reaches this app produces exactly ONE log
# => line, emitted here -- no individual handler ever calls logger.info() itself
import logging  # => Python's stdlib logging -- no third-party dependency needed

from fastapi import FastAPI, Request  # => Request is what every middleware receives first
from starlette.middleware.base import (  # => co-16: the two building blocks every middleware needs
    BaseHTTPMiddleware,  # => the base class FastAPI's own middleware system builds on
    RequestResponseEndpoint,  # => the precise type of "the rest of the pipeline", for typing call_next
)  # => closes the multi-line import from starlette.middleware.base
from starlette.responses import Response  # => the type dispatch() must always return

logging.basicConfig(level=logging.INFO)  # => ensures the "access" logger below is actually visible
logger = logging.getLogger("access")  # => co-16: a dedicated, named logger for this middleware

app = FastAPI()  # => the ASGI application uvicorn will serve


class LoggingMiddleware(BaseHTTPMiddleware):  # => co-16: wraps EVERY request/response pair
    async def dispatch(  # => co-16: dispatch()'s signature spans three lines
        self,  # => the middleware instance itself
        request: Request,  # => the incoming request, read but never mutated here
        call_next: RequestResponseEndpoint,  # => call_next runs the rest of the app
    ) -> Response:  # => must return the Response that eventually reaches the client
        response = await call_next(request)  # => the handler runs BEFORE the log line
        logger.info(  # => %s-style formatting -- logging module builds the string lazily
            "%s %s -> %s",  # => the format template: method, path, status
            request.method,  # => e.g. "GET"
            request.url.path,  # => e.g. "/tasks"
            response.status_code,  # => three fields, one line
        )  # => co-16: one structured line per request, method + path + outcome
        return response  # => the SAME response object, unmodified by logging


app.add_middleware(LoggingMiddleware)  # => applies to EVERY route, with zero per-route code

# => the "access" logger name is deliberate -- a real deployment could route it
# => to a separate log stream/file from application-level warnings and errors


@app.get("/tasks")  # => co-08: a handler that knows NOTHING about logging
def list_tasks() -> list[dict[str, str]]:  # => a plain handler, unaware any middleware even exists
    return [{"title": "Buy milk"}]  # => the middleware logs this request AFTER it returns
