"""Example 60: Missing Token -- a protected route with no Authorization header at all."""
# => co-18: this is the FIRST of three 401 scenarios (60, 61, 62) that all reuse the SAME
# => dependency below -- only the request curl sends differs, which is the whole teaching point

from fastapi import Depends, FastAPI, HTTPException, Request  # => co-23: Depends injects the auth check
from fastapi.responses import JSONResponse  # => co-11: builds the exception handler's structured body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # => co-18: standard bearer scheme

app = FastAPI()  # => a fresh app -- this example needs no database, only auth plumbing


@app.exception_handler(HTTPException)  # => co-11: UNWRAPS FastAPI's default {"detail": ...} nesting --
# => without this handler, raising HTTPException(detail={"error": {...}}) would ship as
# => {"detail": {"error": {...}}}, doubly-nested and inconsistent with every OTHER error path
async def structured_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    body = (
        exc.detail
        if isinstance(exc.detail, dict)  # => the handlers below always raise dict-shaped detail
        else {"error": {"code": "error", "message": str(exc.detail)}}  # => fallback for plain-string detail
    )  # => reuses the raised dict AS-IS -- one consistent {"error": {...}} shape, no extra nesting
    return JSONResponse(status_code=exc.status_code, content=body)  # => co-11: same envelope, every error


VALID_TOKEN = "s3cr3t-token-abc123"  # => hardcoded stand-in for a real signed/opaque token
security = HTTPBearer(auto_error=False)  # => auto_error=False: WE decide the error shape, not
# => FastAPI's own default (which would raise a bare 403 with a generic "Not authenticated" body)


def require_token(  # => co-23: a reusable DEPENDENCY -- any route can opt in via Depends(require_token)
    credentials: HTTPAuthorizationCredentials | None = Depends(security),  # => co-23: FastAPI calls
    # => `security` FIRST, parses any Authorization header it finds, and hands the RESULT here
) -> str:
    if credentials is None:  # => co-18: no Authorization header was sent AT ALL -- this is THIS
        # => example's scenario specifically: curl with no -H "Authorization: ..." flag whatsoever
        raise HTTPException(  # => co-11: structured envelope, not a bare string
            status_code=401,  # => co-03: 401 -- the caller never even attempted to identify itself
            detail={"error": {"code": "unauthorized", "message": "Authorization header missing"}},
        )
    if credentials.credentials != VALID_TOKEN:  # => header present, but the token itself is wrong --
        # => Example 61 is the one that actually exercises THIS branch; unreachable from THIS example's curl
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "unauthorized", "message": "invalid token"}},
        )
    return "alice"  # => the resolved identity, available to any handler that depends on this --
    # => Example 62 is the one that actually reaches this successful return


@app.get("/protected")  # => co-18: guarded entirely by the require_token dependency above --
# => this handler's body contains ZERO auth logic; FastAPI runs the dependency before this even starts
def protected(user: str = Depends(require_token)) -> dict[str, str]:
    # => co-23: by the time execution reaches THIS line, `user` is guaranteed to be "alice" --
    # => every path that could have failed already returned a 401 response one call frame up
    return {"user": user}  # => only reached once require_token returns without raising
