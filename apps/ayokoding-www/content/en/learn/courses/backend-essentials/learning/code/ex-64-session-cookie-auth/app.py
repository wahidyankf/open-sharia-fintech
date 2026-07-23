"""Example 64: Session-Cookie Auth -- set a session cookie on login, read it next request."""
# => co-17: this is Example 57's session mechanism made into its OWN complete, runnable app --
# => login mints server-side state, the browser only ever holds an opaque cookie pointing at it

import uuid  # => generates the unguessable session id -- never a sequential/predictable value

from fastapi import Cookie, FastAPI, HTTPException, Request, Response  # => co-17: cookie-based session
from fastapi.responses import JSONResponse  # => co-11: builds the exception handler's structured body

app = FastAPI()  # => a fresh app -- this example needs no database, only the in-memory dict below
# => (fully self-contained: nothing here is imported from any other example directory)

SESSIONS: dict[str, str] = {}  # => session_id -> username; server-side state (co-17) -- this dict
# => IS the session store; a real deployment would put this in Redis/a DB, precisely because
# => in-process memory vanishes on restart and isn't shared across multiple worker processes
USERNAME = "alice"  # => the ONE registered user this pedagogical example recognizes
PASSWORD = "wonderland"  # => a hardcoded password -- never do this in real code (co-17 caveat)
# => (a real login endpoint hashes and salts stored passwords -- this constant exists purely
# => so curl has something deterministic to submit; nothing here is meant as production auth advice)


@app.exception_handler(HTTPException)  # => co-11: consistent envelope, same pattern as ex-60..63
async def structured_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    body = (
        exc.detail
        if isinstance(exc.detail, dict)  # => every raise below supplies a dict already
        else {"error": {"code": "error", "message": str(exc.detail)}}  # => fallback for a plain string
    )
    return JSONResponse(status_code=exc.status_code, content=body)  # => co-11: same shape, every error


@app.post("/login")  # => co-17: authenticates, then ESTABLISHES a session -- unlike Example 58's
# => token endpoint, this one has a SIDE EFFECT: it writes a new entry into SESSIONS below
def login(username: str, password: str, response: Response) -> dict[str, str]:
    if username != USERNAME or password != PASSWORD:  # => co-17: reject any mismatch immediately --
        # => deliberately the SAME message for both a wrong username and a wrong password --
        # => never let a caller distinguish "no such user" from "wrong password" via the response
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "unauthorized", "message": "invalid credentials"}},
        )
    session_id = str(uuid.uuid4())  # => a fresh, unguessable session identifier -- a real deployment
    # => also rotates this on every login, so an old leaked cookie can't be replayed indefinitely
    SESSIONS[session_id] = username  # => co-17: the SERVER remembers this session belongs to username
    response.set_cookie(  # => co-04: writes a Set-Cookie response header -- curl's -c flag captures it
        "session_id", session_id, httponly=True
    )  # => co-04: httponly prevents client-side JS from reading it -- mitigates cookie-theft via XSS
    return {"logged_in_as": username}  # => co-17: confirms WHO logged in -- never the session id itself
    # => (leaking the session id in the JSON body too would defeat httponly's whole protection above)


@app.get("/me")  # => co-17: identifies the caller purely from the session cookie on THIS request --
# => curl's -b flag is what actually SENDS the cookie captured by -c above back to this endpoint
def me(session_id: str | None = Cookie(default=None)) -> dict[str, str]:
    if session_id is None or session_id not in SESSIONS:  # => no cookie, or the server never issued it
        # => (also covers a server restart, since SESSIONS is in-memory and empties on every reload)
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "unauthorized", "message": "no active session"}},
        )
    return {"username": SESSIONS[session_id]}  # => the SAME identity established at login, now confirmed
    # => co-17: notice this handler never re-checks a password -- the cookie's PRESENCE in
    # => SESSIONS is the entire proof of identity for every request after the original login
