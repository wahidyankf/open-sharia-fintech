"""Example 58: Issue a Token -- POST /login returns a token string."""
# => co-17: this is the OTHER half of Example 57's token mechanism -- where does the token
# => a client presents on every later call actually come FROM? This is that issuing endpoint.

from fastapi import FastAPI, HTTPException  # => co-17, co-18: raises 401 on bad credentials
from pydantic import BaseModel  # => co-10: a typed model validates the login body

app = FastAPI()  # => a fresh app -- no persistence, no session store, nothing survives a restart

VALID_TOKEN = "s3cr3t-token-abc123"  # => hardcoded stand-in for a real signed/opaque token
# => (a real login endpoint would look up the user, verify a hashed password, then mint a
# => fresh signed JWT or opaque token -- this example fixes ALL of that to one literal string
# => so the FOCUS stays on the request/response SHAPE, not on cryptography or password hashing)
USERNAME = "alice"  # => the ONE registered user this pedagogical example recognizes
PASSWORD = "wonderland"  # => a hardcoded password -- never do this in real code (co-17 caveat)


class Credentials(BaseModel):  # => co-10: the shape POST /login expects
    username: str  # => a plain required string field
    password: str  # => a plain required string field, never returned in any response
    # => (a real API would also never LOG this field -- pydantic gives no free redaction,
    # => so that discipline has to be a deliberate choice in whatever logs the request)


class TokenResponse(BaseModel):  # => co-09: declares the exact shape of a successful login
    token: str  # => the ONLY thing the client needs to authenticate future requests


@app.post("/login", response_model=TokenResponse)  # => co-17, co-18: issues a token, no session created
def login(credentials: Credentials) -> TokenResponse:
    # => co-10: FastAPI already validated `credentials` matches the Credentials shape above --
    # => by the time this line runs, both fields are guaranteed to be present strings
    if credentials.username != USERNAME or credentials.password != PASSWORD:  # => co-10: reject any mismatch immediately -- deliberately the SAME message for both
        # => a wrong username and a wrong password, so a caller can't enumerate valid usernames
        raise HTTPException(status_code=401, detail="invalid credentials")  # => co-03: 401, not 404
    return TokenResponse(token=VALID_TOKEN)  # => co-09: the response body IS just the token --
    # => no session id, no server-side record created -- co-17's defining difference from ex-57
