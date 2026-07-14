"""Example 61: Invalid Token -- a protected route with a malformed/wrong token."""
# => co-18: a token can be WRONG in two different ways -- entirely absent (Example 60) or
# => present-but-incorrect (this example) -- and a caller sees the SAME 401 status either way,
# => which is deliberate: never leak which half of "no token" vs "bad token" a caller hit

from fastapi import Depends, FastAPI, HTTPException, Request  # => co-18: same dependency style as ex-60
from fastapi.responses import JSONResponse  # => co-11: builds the exception handler's structured body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # => co-18: parses "Bearer <token>"

app = FastAPI()  # => a fresh app -- this example needs no database, only auth plumbing
# => (fully self-contained: nothing here is imported from any other example directory)

VALID_TOKEN = "s3cr3t-token-abc123"  # => hardcoded stand-in for a real signed/opaque token
security = HTTPBearer(auto_error=False)  # => auto_error=False: WE own the 401 body's shape below,
# => not FastAPI's own built-in "Not authenticated" 403 default
# => (co-18: 401 means "I don't know who you are"; 403 means "I know, and you're not allowed")


@app.exception_handler(HTTPException)  # => co-11: one consistent {"error": {...}} envelope, unwrapped --
# => without this, every raise HTTPException(detail={"error": {...}}) below would ship doubly
# => nested as {"detail": {"error": {...}}} instead of the flat {"error": {...}} shape shown here
async def structured_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    body = (
        exc.detail
        if isinstance(exc.detail, dict)  # => every raise below already supplies a dict -- this
        # => isinstance check exists so the handler ALSO degrades gracefully for a plain string detail
        else {"error": {"code": "error", "message": str(exc.detail)}}
    )
    return JSONResponse(status_code=exc.status_code, content=body)  # => co-11: same shape, every error


def require_token(  # => co-23: identical dependency SHAPE to Example 60 -- the difference this
    # => example actually exercises lives entirely in what curl sends, not in this function's code
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    if credentials is None:  # => genuinely absent -- Example 60's case, still handled here for completeness
        # => so this dependency stays a fully correct, standalone, self-contained auth check on its own
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "unauthorized", "message": "Authorization header missing"}},
        )
    if credentials.credentials != VALID_TOKEN:  # => co-18: THIS example's focus -- present but WRONG --
        raise HTTPException(  # => a well-formed "Bearer <garbage>" header still fails the equality check;
            # => HTTPBearer already stripped the "Bearer " prefix, so `.credentials` is just the raw string
            status_code=401,
            detail={"error": {"code": "unauthorized", "message": "token is invalid"}},
        )
    return "alice"  # => the resolved identity -- unreachable from THIS example's own curl scenario,
    # => since the token sent below is deliberately wrong, but still needed for require_token to type-check
    # => (the type checker verifies EVERY code path returns str, reachable or not at runtime)


@app.get("/protected")  # => co-18: guarded entirely by the require_token dependency above --
# => the handler itself stays a single line, exactly like every open route -- FastAPI resolves
# => `require_token` BEFORE this function body runs, and never calls it at all if that dependency raises
def protected(user: str = Depends(require_token)) -> dict[str, str]:
    return {"user": user}  # => never actually reached when the curl below sends a garbage token
