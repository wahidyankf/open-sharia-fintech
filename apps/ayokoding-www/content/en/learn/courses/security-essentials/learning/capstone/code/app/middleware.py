"""Capstone: hardened task API -- session-token auth middleware + security headers (co-12,
co-17, co-19). Backend-Essentials compared a single hardcoded string with `!=`; this version
resolves a REAL signed token issued by /auth/login, and adds a second middleware that stamps
every response (including error responses) with a security-header baseline.
"""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse

WRITE_METHODS = {
    "POST",
    "PUT",
    "DELETE",
}  # => only WRITES need a token -- GET stays open, unchanged


def make_token_check_middleware(
    resolve_token: Callable[[str], int | None],
) -> Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]:
    """Builds the write-guard middleware around a `resolve_token` function so this module
    never imports `auth` (or an env-var secret) directly -- co-17: the secret stays in main.py,
    the ONE place that reads it from the environment."""

    async def token_check_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        needs_token = (
            request.url.path.startswith("/tasks") and request.method in WRITE_METHODS
        )
        if needs_token:
            auth_header = request.headers.get("authorization", "")
            token = (
                auth_header.removeprefix("Bearer ")
                if auth_header.startswith("Bearer ")
                else ""
            )
            user_id = (
                resolve_token(token) if token else None
            )  # => co-12: real signature + expiry check
            if user_id is None:
                return JSONResponse(  # => co-23: the SAME structured envelope every other error uses
                    status_code=401,
                    content={
                        "error": {
                            "code": "unauthorized",
                            "message": "missing or invalid token",
                        }
                    },
                )
            request.state.user_id = (
                user_id  # => available to route handlers that need "who is this?"
            )
        return await call_next(request)

    return token_check_middleware


async def security_headers_middleware(  # => co-19: runs on EVERY response, success or error
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'"  # => restricts script/style sources
    )
    response.headers["X-Content-Type-Options"] = (
        "nosniff"  # => stops MIME-sniffing of response bodies
    )
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"  # => forces HTTPS
    )
    return response
