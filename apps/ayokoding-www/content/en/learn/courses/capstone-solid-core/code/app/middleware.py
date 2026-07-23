"""Pass-1 capstone: Habit Tracker -- token-scoping middleware + security-header baseline
(topic 17). Reuses the same two-middleware shape topic 17's Security Essentials capstone
already verified, with one deliberate difference: Security Essentials' Task API was a single
shared resource, so it only guarded WRITE methods. Every habit here belongs to exactly one
user (topic 10's `habits.user_id` foreign key), so EVERY `/habits` request -- reads included --
must resolve a token: a read endpoint still needs to know WHICH user's habits to return.
"""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse


def make_token_check_middleware(
    resolve_token: Callable[[str], int | None],
) -> Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]:
    """Builds the token-scoping middleware around a `resolve_token` function so this module
    never imports `auth` (or an env-var secret) directly -- the secret stays in main.py,
    the ONE place that reads it from the environment."""

    async def token_check_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        needs_token = request.url.path.startswith(
            "/habits"
        )  # => ALL habit ops are user-scoped, reads included
        if needs_token:
            auth_header = request.headers.get("authorization", "")
            token = (
                auth_header.removeprefix("Bearer ")
                if auth_header.startswith("Bearer ")
                else ""
            )
            user_id = (
                resolve_token(token) if token else None
            )  # => real signature + expiry check
            if user_id is None:
                return JSONResponse(  # => the SAME structured envelope every other error uses
                    status_code=401,
                    content={
                        "error": {
                            "code": "unauthorized",
                            "message": "missing or invalid token",
                        }
                    },
                )
            request.state.user_id = (
                user_id  # => available to route handlers -- "who is this?"
            )
        return await call_next(request)

    return token_check_middleware


async def security_headers_middleware(  # => runs on EVERY response, success or error
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
