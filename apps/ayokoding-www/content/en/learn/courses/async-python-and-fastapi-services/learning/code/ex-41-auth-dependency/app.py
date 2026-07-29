"""Example 41: An Auth Dependency Gates Protected Routes.

A Depends that reads the Authorization header, validates a bearer token, and raises 401 otherwise -- gating
protected routes with one declared parameter. Run: uvicorn app:app --port 8000, then:
curl -i localhost:8000/me  and  curl -H 'Authorization: Bearer secret' localhost:8000/me  (co-15, co-17)
"""

from fastapi import Depends, FastAPI, Header, HTTPException  # => Header reads request headers (co-15, co-17)

app = FastAPI()  # => the ASGI application uvicorn serves

VALID_TOKEN = "secret"  # => a stand-in for a real signed/opaque token


def require_token(authorization: str | None = Header(default=None)) -> str:  # => a reusable auth dependency (co-15)
    # => Header(default=None) makes Authorization OPTIONAL so we can reject a missing one ourselves (co-17)
    if authorization != f"Bearer {VALID_TOKEN}":  # => exact match required (co-17)
        raise HTTPException(status_code=401, detail="invalid or missing token")  # => 401 before the handler runs
    return "caller"  # => a resolved caller identity handed to the handler


@app.get("/me")  # => a PROTECTED route -- declares the auth dependency
def me(caller: str = Depends(require_token)) -> dict[str, str]:  # => the dependency gates this route (co-15)
    return {"caller": caller}  # => only reachable with a valid token (co-14)


@app.get("/public")  # => an OPEN route -- declares no auth dependency
def public() -> dict[str, str]:  # => no token required
    return {"msg": "open"}  # => reachable by anyone (co-14)
