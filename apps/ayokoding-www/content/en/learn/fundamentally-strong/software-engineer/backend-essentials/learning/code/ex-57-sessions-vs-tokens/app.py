"""Example 57: Sessions vs Tokens -- two ways to identify the same caller."""
# => co-17: both mechanisms below answer the SAME question ("who is this caller?") with
# => two different tradeoffs -- session state lives on the server, token state lives on the wire

import uuid  # => generates unpredictable session ids -- a real server never uses a guessable id

from fastapi import Cookie, FastAPI, Header, HTTPException, Response  # => co-04: header/cookie params

app = FastAPI()  # => a fresh app; this example needs no persistence at all

# -- Session mechanism: server holds the state (co-17) -----------------------------------
SESSIONS: dict[str, str] = {}  # => session_id -> username; lives ONLY in this process's memory
# => a real deployment would put this in Redis/DB precisely because in-process memory
# => does not survive a restart or scale past one worker (co-05 tension, revisited ex-80)

# -- Token mechanism: the token itself IS the credential (co-17) -------------------------
VALID_TOKEN = "s3cr3t-token-abc123"  # => a hardcoded stand-in for a real signed/opaque token
# => (real tokens are cryptographically signed or opaque-and-looked-up -- never a literal, guessable
# => string -- this constant exists purely so curl can present a value the server will accept)
TOKEN_USER = "alice"  # => the token's fixed "owner" for this pedagogical example


@app.post("/login-session")  # => co-17: issues a SESSION -- server-side state plus a cookie
def login_session(response: Response) -> dict[str, str]:
    session_id = str(uuid.uuid4())  # => a fresh, unguessable identifier for this session
    SESSIONS[session_id] = "alice"  # => the SERVER remembers who this session belongs to
    response.set_cookie("session_id", session_id)  # => co-04: the CLIENT only gets an opaque id
    return {"mechanism": "session", "session_id": session_id}  # => confirms issuance to the caller


@app.get("/profile-session")  # => co-17: identifies the caller via the session cookie
def profile_session(session_id: str | None = Cookie(default=None)) -> dict[str, str]:
    if session_id is None or session_id not in SESSIONS:  # => no cookie, or server forgot it
        raise HTTPException(status_code=401, detail="no valid session")  # => co-03: 401 unauthenticated
    username = SESSIONS[session_id]  # => O(1) lookup -- but ONLY works on the process that has it
    return {"mechanism": "session", "username": username}  # => the caller's identity, resolved


@app.post("/login-token")  # => co-17, co-18: issues a TOKEN -- no server-side state created
def login_token() -> dict[str, str]:
    return {"mechanism": "token", "token": VALID_TOKEN}  # => the token itself carries everything needed


@app.get("/profile-token")  # => co-17, co-18: identifies the caller via the bearer token alone
def profile_token(authorization: str | None = Header(default=None)) -> dict[str, str]:
    if authorization != f"Bearer {VALID_TOKEN}":  # => co-04: reads the raw Authorization header
        raise HTTPException(status_code=401, detail="missing or invalid token")  # => 401, same as session
    return {"mechanism": "token", "username": TOKEN_USER}  # => resolved WITHOUT any server-side lookup
