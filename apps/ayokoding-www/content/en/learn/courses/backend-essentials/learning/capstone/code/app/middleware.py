"""Capstone task API -- the token-check middleware protecting writes (co-16, co-18)."""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse

VALID_TOKEN = "s3cr3t-token-abc123"  # => hardcoded stand-in for a real signed/opaque token
WRITE_METHODS = {"POST", "PUT", "DELETE"}  # => co-02: only WRITES need a token -- GET stays open


async def token_check_middleware(  # => co-16: wraps every request/response, deciding per method + path
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    needs_token = request.url.path.startswith("/tasks") and request.method in WRITE_METHODS  # => co-02, co-18: /health and /ready are NEVER guarded; GET /tasks* is NEVER guarded
    if needs_token:
        auth_header = request.headers.get("authorization")  # => co-04: reads the raw Authorization header
        if auth_header != f"Bearer {VALID_TOKEN}":  # => co-18: exact match required
            return JSONResponse(  # => co-11: the SAME structured envelope every other error in this app uses
                status_code=401,
                content={"error": {"code": "unauthorized", "message": "missing or invalid token"}},
            )
    return await call_next(request)  # => co-16: unmodified pass-through for every open route
