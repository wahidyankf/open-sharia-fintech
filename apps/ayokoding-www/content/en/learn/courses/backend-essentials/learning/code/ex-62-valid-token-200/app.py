"""Example 62: Valid Token -- a protected route with a good token succeeds."""
# => co-18: this is the THIRD scenario in the 401 trio (Examples 60, 61, 62) -- same dependency,
# => same guarded route, only the curl's Authorization header changes across all three examples

from fastapi import Depends, FastAPI, HTTPException, Request  # => co-23: Depends wires the auth check in
from fastapi.responses import JSONResponse  # => co-11: builds the exception handler's structured body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # => co-18: parses "Bearer <token>"

app = FastAPI()  # => a fresh app -- this example needs no database, only auth plumbing

VALID_TOKEN = "s3cr3t-token-abc123"  # => hardcoded stand-in for a real signed/opaque token
security = HTTPBearer(auto_error=False)  # => auto_error=False: WE own the 401 body's shape below


@app.exception_handler(HTTPException)  # => co-11: unwraps FastAPI's default {"detail": ...} nesting
# => so a dict-shaped detail ships flat as {"error": {...}} -- same reusable pattern as ex-60/61
async def structured_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    body = (
        exc.detail
        if isinstance(exc.detail, dict)  # => the raise below always supplies a dict already
        else {"error": {"code": "error", "message": str(exc.detail)}}  # => fallback for a plain string
    )
    # => co-11: this handler is the ONLY place status codes get turned into response bodies --
    # => every route in this file stays completely free of response-formatting concerns
    return JSONResponse(status_code=exc.status_code, content=body)  # => co-11: same shape, every error


def require_token(  # => co-23: identical shape to ex-60/61 -- collapses the "missing" and "wrong"
    # => cases into ONE branch here, since this example's curl only ever needs to prove the OPPOSITE:
    # => that a genuinely correct token clears this check and reaches the handler body below
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    if credentials is None or credentials.credentials != VALID_TOKEN:  # => co-18: either failure mode
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "unauthorized", "message": "missing or invalid token"}},
        )  # => unreachable from THIS example's own curl -- kept only so the function is fully correct
        # => and equally usable if a reader copies this file and DOES send a bad token through it
    return "alice"  # => co-18: THIS example's focus -- the success path, reached only with a good token
    # => no session, no server-side lookup -- the token equality check above IS the entire proof


@app.get("/protected")  # => co-18: guarded entirely by the require_token dependency above
# => co-18: identical route SHAPE to ex-60/61 -- the only thing changing across the trio is the token
def protected(user: str = Depends(require_token)) -> dict[str, str | bool]:
    # => co-23: `user` is guaranteed to be "alice" here -- every failure path already returned 401
    return {"user": user, "granted": True}  # => a slightly richer body than ex-60/61 to mark success clearly
