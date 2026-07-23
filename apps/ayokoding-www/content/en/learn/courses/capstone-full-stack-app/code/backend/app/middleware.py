"""Full-stack capstone -- the security-header baseline (topic 17 hardening), reused from
Security Essentials' / the Pass-1 Capstone's `security_headers_middleware`, file-for-file. CORS
itself is wired in `main.py` via Starlette's own `CORSMiddleware` -- a framework-provided,
battle-tested implementation, not hand-rolled here -- configured with an explicit ALLOW-LIST of
exactly one origin (never a wildcard `"*"`), which is what makes the read endpoint genuinely
"CORS-safe": only that one configured origin's browser-issued requests are allowed to read the
response.
"""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response


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
