"""Example 59: Token-Check Middleware -- validates a Bearer token on protected routes."""
# => co-16: a MIDDLEWARE runs on every request BEFORE routing decides which handler runs --
# => that makes it the right place for a cross-cutting concern like "is this caller allowed in?"
# => rather than repeating the same check inside every individual handler function

from collections.abc import Awaitable, Callable  # => precise typing for the middleware's signature

from fastapi import FastAPI, Request, Response  # => co-16: middleware operates on raw Request/Response
from fastapi.responses import JSONResponse  # => co-11: builds the structured 401 body by hand

app = FastAPI()  # => a fresh app -- this example needs no database, only routing + middleware

VALID_TOKEN = "s3cr3t-token-abc123"  # => hardcoded stand-in for a real signed/opaque token


@app.middleware("http")  # => co-16: registers a function that wraps EVERY request/response --
# => this decorator form is Starlette's original middleware API; FastAPI also accepts
# => `app.add_middleware(...)` for class-based middleware, but a function is simplest here
async def token_check_middleware(
    request: Request,  # => co-16: the INCOMING request -- path, method, and headers are readable here
    call_next: Callable[[Request], Awaitable[Response]],  # => co-16: calling this continues the chain
) -> Response:
    # => co-16: this `if` is the ENTIRE authorization policy for the whole app in one place --
    # => change what "needs a token" means by editing this one condition, not N handler functions
    if request.url.path.startswith("/protected"):  # => co-16: only THIS path prefix is guarded --
        # => Example 63 explores a read/write split instead of a path-prefix split like this one
        auth_header = request.headers.get("authorization")  # => co-04: reads the raw header --
        # => note the lowercase key: HTTP header names are case-insensitive, and Starlette's
        # => Headers mapping normalizes lookups accordingly regardless of the wire casing
        if auth_header != f"Bearer {VALID_TOKEN}":  # => co-18: exact string match, no partial credit --
            # => this branch fires for BOTH a missing header (None != "Bearer ...") and a garbage one
            return JSONResponse(  # => co-11: a structured envelope, never a stack trace or bare text
                status_code=401,  # => co-03: 401 Unauthorized -- "who you claim to be" was rejected
                content={"error": {"code": "unauthorized", "message": "missing or invalid token"}},
            )  # => co-16: returning HERE short-circuits the chain -- call_next() never runs,
            # => so the guarded handler function below never even starts executing
        request.state.user = "alice"  # => co-16: a valid token attaches identity for the handler to use --
        # => request.state is a plain per-request namespace; middleware writes to it, handlers read it
    return await call_next(request)  # => co-16: hands off to routing -- unmodified for open paths,
    # => and for /protected paths that passed the check above


@app.get("/public")  # => never touches the middleware's token branch at all -- doesn't start with /protected
def public() -> dict[str, str]:
    return {"access": "public"}  # => reachable with zero headers, zero token, always


@app.get("/protected/data")  # => co-18: only reachable with a valid token, per the middleware above --
# => this handler body itself contains NO auth logic whatsoever -- that separation is the whole point
def protected_data(request: Request) -> dict[str, str]:
    return {"access": "protected", "user": request.state.user}  # => identity set by the middleware,
    # => not re-derived here -- the handler simply trusts what already ran before it
