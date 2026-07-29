"""Example 70: An OAuth2 Password Bearer Token Flow.

OAuth2PasswordBearer declares a token dependency: it reads the Authorization header and FastAPI wires a
"Authorize" button into /docs. This example validates a fixed token; real code verifies a signed JWT.
Run: uvicorn app:app --port 8000. (co-15, co-17)
"""

from fastapi import Depends, FastAPI, HTTPException  # => Depends + errors (co-15, co-17)
from fastapi.security import OAuth2PasswordBearer  # => the OAuth2 password-flow dependency (co-15)

app = FastAPI()  # => the ASGI application uvicorn serves

# => tokenUrl is the relative path clients hit to obtain a token (shown in /docs) (co-20)
oauth2 = OAuth2PasswordBearer(tokenUrl="token")  # => a dependency that reads "Authorization: Bearer ..." (co-15)
VALID_TOKEN = "secret"  # => a stand-in; real code verifies a signed JWT


def current_user(token: str = Depends(oauth2)) -> str:  # => resolves the caller from the token (co-15)
    if token != VALID_TOKEN:  # => invalid token
        raise HTTPException(status_code=401, detail="bad token", headers={"WWW-Authenticate": "Bearer"})  # => 401 (co-17)
    return "caller"  # => a resolved caller identity


@app.get("/me")  # => a protected route using the OAuth2 dependency
def me(user: str = Depends(current_user)) -> dict[str, str]:  # => the dependency gates this route (co-15)
    return {"user": user}  # => only reachable with a valid bearer token (co-14)
